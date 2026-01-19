#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data import/export framework for the Agricultural AI System.

This module provides functionality for importing and exporting data,
validating imported data against schema, and merging data with existing datasets.
"""

import os
import json
import logging
import shutil
import hashlib
import pandas as pd
import numpy as np
from datetime import datetime
import csv
import yaml
import sqlite3
import zipfile
import tempfile
import jsonschema
from PIL import Image
import io
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('data_management')

class DataManager:
    """
    Manages data import, export, validation, and merging for the Agricultural AI System.
    
    This class provides methods to:
    1. Import data from various formats (CSV, JSON, images)
    2. Export data to various formats
    3. Validate imported data against schema
    4. Merge imported data with existing datasets
    5. Track data lineage and changes
    """
    
    def __init__(self, config=None):
        """
        Initialize the data manager.
        
        Args:
            config (dict): Configuration dictionary with data management settings
        """
        self.config = config or {}
        
        # Default configuration
        self.default_config = {
            'data_dir': 'data',
            'import_dir': 'data/imports',
            'export_dir': 'data/exports',
            'schema_dir': 'data/schemas',
            'temp_dir': 'data/temp',
            'backup_dir': 'data/backups',
            'max_import_file_size': 100 * 1024 * 1024,  # 100 MB
            'max_image_dimensions': (4096, 4096),  # Max width, height
            'supported_image_formats': ['jpg', 'jpeg', 'png', 'tif', 'tiff', 'bmp'],
            'supported_data_formats': ['csv', 'json', 'yaml', 'xlsx'],
            'db_path': 'data/database/data_management.db',
        }
        
        # Merge with provided config
        for key, value in self.default_config.items():
            if key not in self.config:
                self.config[key] = value
        
        # Create necessary directories
        for dir_key in ['data_dir', 'import_dir', 'export_dir', 'schema_dir', 'temp_dir', 'backup_dir']:
            os.makedirs(self.config[dir_key], exist_ok=True)
        
        # Ensure database directory exists
        os.makedirs(os.path.dirname(self.config['db_path']), exist_ok=True)
        
        # Initialize database
        self._init_database()
        
        logger.info("Data manager initialized")
    
    def _init_database(self):
        """Initialize the SQLite database for data management."""
        try:
            conn = sqlite3.connect(self.config['db_path'])
            cursor = conn.cursor()
            
            # Create import_history table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS import_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                user_id INTEGER,
                username TEXT,
                file_name TEXT NOT NULL,
                file_type TEXT NOT NULL,
                file_size INTEGER NOT NULL,
                file_hash TEXT NOT NULL,
                target_dataset TEXT NOT NULL,
                records_imported INTEGER,
                records_rejected INTEGER,
                validation_errors TEXT,
                status TEXT NOT NULL,
                merge_strategy TEXT
            )
            ''')
            
            # Create export_history table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS export_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                user_id INTEGER,
                username TEXT,
                file_name TEXT NOT NULL,
                file_type TEXT NOT NULL,
                file_size INTEGER NOT NULL,
                source_dataset TEXT NOT NULL,
                records_exported INTEGER,
                filters TEXT,
                status TEXT NOT NULL
            )
            ''')
            
            # Create dataset_versions table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS dataset_versions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dataset_name TEXT NOT NULL,
                version TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                user_id INTEGER,
                username TEXT,
                file_path TEXT NOT NULL,
                file_hash TEXT NOT NULL,
                record_count INTEGER,
                description TEXT,
                parent_version TEXT,
                UNIQUE(dataset_name, version)
            )
            ''')
            
            conn.commit()
            conn.close()
            
            logger.info("Data management database initialized")
            
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise
    
    def _compute_file_hash(self, file_path):
        """
        Compute SHA-256 hash of a file.
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            str: Hex digest of the hash
        """
        sha256_hash = hashlib.sha256()
        
        with open(file_path, "rb") as f:
            # Read and update hash in chunks of 4K
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        
        return sha256_hash.hexdigest()
    
    def _validate_against_schema(self, data, schema_name):
        """
        Validate data against a JSON schema.
        
        Args:
            data (dict or list): Data to validate
            schema_name (str): Name of the schema file (without extension)
            
        Returns:
            tuple: (is_valid, errors)
        """
        schema_path = os.path.join(self.config['schema_dir'], f"{schema_name}.json")
        
        if not os.path.exists(schema_path):
            logger.error(f"Schema file not found: {schema_path}")
            return False, ["Schema file not found"]
        
        try:
            with open(schema_path, 'r') as f:
                schema = json.load(f)
            
            validator = jsonschema.Draft7Validator(schema)
            errors = list(validator.iter_errors(data))
            
            if errors:
                error_messages = []
                for error in errors:
                    path = '.'.join(str(p) for p in error.path) if error.path else '(root)'
                    error_messages.append(f"{path}: {error.message}")
                
                return False, error_messages
            
            return True, []
            
        except Exception as e:
            logger.error(f"Error validating against schema: {e}")
            return False, [str(e)]
    
    def _validate_image(self, image_path):
        """
        Validate an image file.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            tuple: (is_valid, error_message)
        """
        try:
            # Check file extension
            ext = os.path.splitext(image_path)[1].lower().lstrip('.')
            if ext not in self.config['supported_image_formats']:
                return False, f"Unsupported image format: {ext}"
            
            # Check file size
            file_size = os.path.getsize(image_path)
            if file_size > self.config['max_import_file_size']:
                return False, f"Image file too large: {file_size} bytes (max: {self.config['max_import_file_size']} bytes)"
            
            # Open and validate image
            with Image.open(image_path) as img:
                width, height = img.size
                
                # Check dimensions
                max_width, max_height = self.config['max_image_dimensions']
                if width > max_width or height > max_height:
                    return False, f"Image dimensions too large: {width}x{height} (max: {max_width}x{max_height})"
                
                # Verify image can be read
                img.verify()
            
            return True, None
            
        except Exception as e:
            logger.error(f"Error validating image: {e}")
            return False, str(e)
    
    def _restructure_data(self, data, target_structure):
        """
        Restructure imported data to match the target structure.
        
        Args:
            data (dict or list): Data to restructure
            target_structure (dict): Target structure description
            
        Returns:
            tuple: (restructured_data, errors)
        """
        try:
            # This is a simplified implementation
            # In a real system, this would be more sophisticated
            
            if isinstance(data, list) and isinstance(target_structure, dict) and 'type' in target_structure:
                if target_structure['type'] == 'array' and 'items' in target_structure:
                    item_structure = target_structure['items']
                    
                    restructured = []
                    errors = []
                    
                    for i, item in enumerate(data):
                        if isinstance(item, dict):
                            new_item = {}
                            
                            # Map fields according to structure
                            for field, field_def in item_structure.get('properties', {}).items():
                                source_field = field_def.get('source_field', field)
                                
                                if source_field in item:
                                    new_item[field] = item[source_field]
                                elif field_def.get('required', False):
                                    errors.append(f"Item {i}: Missing required field '{field}'")
                            
                            restructured.append(new_item)
                        else:
                            errors.append(f"Item {i}: Expected object, got {type(item).__name__}")
                    
                    return restructured, errors
            
            # If no restructuring needed or not supported, return as is
            return data, []
            
        except Exception as e:
            logger.error(f"Error restructuring data: {e}")
            return data, [str(e)]
    
    def import_data(self, file_path, target_dataset, schema_name=None, 
                   merge_strategy='append', user_info=None, restructure=None):
        """
        Import data from a file into the system.
        
        Args:
            file_path (str): Path to the file to import
            target_dataset (str): Name of the dataset to import into
            schema_name (str): Name of the schema to validate against
            merge_strategy (str): Strategy for merging with existing data ('append', 'replace', 'update')
            user_info (dict): Information about the user performing the import
            restructure (dict): Optional structure to restructure data to
            
        Returns:
            tuple: (success, message, import_id)
        """
        if not os.path.exists(file_path):
            return False, f"File not found: {file_path}", None
        
        # Check file size
        file_size = os.path.getsize(file_path)
        if file_size > self.config['max_import_file_size']:
            return False, f"File too large: {file_size} bytes (max: {self.config['max_import_file_size']} bytes)", None
        
        # Get file type
        file_ext = os.path.splitext(file_path)[1].lower().lstrip('.')
        
        # Compute file hash
        file_hash = self._compute_file_hash(file_path)
        
        # Create import record
        import_id = self._create_import_record(
            file_path=file_path,
            file_type=file_ext,
            file_size=file_size,
            file_hash=file_hash,
            target_dataset=target_dataset,
            merge_strategy=merge_strategy,
            user_info=user_info
        )
        
        if not import_id:
            return False, "Failed to create import record", None
        
        try:
            # Create a copy of the file in the import directory
            import_file_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.path.basename(file_path)}"
            import_file_path = os.path.join(self.config['import_dir'], import_file_name)
            shutil.copy2(file_path, import_file_path)
            
            # Process based on file type
            if file_ext in self.config['supported_image_formats']:
                return self._import_image(
                    import_id=import_id,
                    file_path=import_file_path,
                    target_dataset=target_dataset,
                    user_info=user_info
                )
            elif file_ext in self.config['supported_data_formats']:
                return self._import_data_file(
                    import_id=import_id,
                    file_path=import_file_path,
                    file_type=file_ext,
                    target_dataset=target_dataset,
                    schema_name=schema_name,
                    merge_strategy=merge_strategy,
                    user_info=user_info,
                    restructure=restructure
                )
            else:
                self._update_import_status(
                    import_id=import_id,
                    status="failed",
                    validation_errors=["Unsupported file format"]
                )
                return False, f"Unsupported file format: {file_ext}", import_id
            
        except Exception as e:
            logger.error(f"Error during import: {e}")
            self._update_import_status(
                import_id=import_id,
                status="failed",
                validation_errors=[str(e)]
            )
            return False, f"Error during import: {str(e)}", import_id
    
    def _import_image(self, import_id, file_path, target_dataset, user_info=None):
        """
        Import an image file.
        
        Args:
            import_id (int): ID of the import record
            file_path (str): Path to the image file
            target_dataset (str): Name of the dataset to import into
            user_info (dict): Information about the user performing the import
            
        Returns:
            tuple: (success, message, import_id)
        """
        try:
            # Validate image
            is_valid, error = self._validate_image(file_path)
            
            if not is_valid:
                self._update_import_status(
                    import_id=import_id,
                    status="failed",
                    validation_errors=[error]
                )
                return False, f"Image validation failed: {error}", import_id
            
            # Determine target directory
            target_dir = os.path.join(self.config['data_dir'], target_dataset)
            os.makedirs(target_dir, exist_ok=True)
            
            # Copy image to target directory
            target_file = os.path.join(target_dir, os.path.basename(file_path))
            shutil.copy2(file_path, target_file)
            
            # Update import status
            self._update_import_status(
                import_id=import_id,
                status="completed",
                records_imported=1,
                records_rejected=0
            )
            
            return True, f"Image imported successfully to {target_dataset}", import_id
            
        except Exception as e:
            logger.error(f"Error importing image: {e}")
            self._update_import_status(
                import_id=import_id,
                status="failed",
                validation_errors=[str(e)]
            )
            return False, f"Error importing image: {str(e)}", import_id
    
    def _import_data_file(self, import_id, file_path, file_type, target_dataset, 
                         schema_name=None, merge_strategy='append', user_info=None, restructure=None):
        """
        Import a data file (CSV, JSON, etc.).
        
        Args:
            import_id (int): ID of the import record
            file_path (str): Path to the data file
            file_type (str): Type of the file (csv, json, etc.)
            target_dataset (str): Name of the dataset to import into
            schema_name (str): Name of the schema to validate against
            merge_strategy (str): Strategy for merging with existing data
            user_info (dict): Information about the user performing the import
            restructure (dict): Optional structure to restructure data to
            
        Returns:
            tuple: (success, message, import_id)
        """
        try:
            # Load data from file
            data = self._load_data_from_file(file_path, file_type)
            
            if data is None:
                self._update_import_status(
                    import_id=import_id,
                    status="failed",
                    validation_errors=["Failed to load data from file"]
                )
                return False, "Failed to load data from file", import_id
            
            # Restructure data if needed
            if restructure:
                data, restructure_errors = self._restructure_data(data, restructure)
                
                if restructure_errors:
                    self._update_import_status(
                        import_id=import_id,
                        status="failed",
                        validation_errors=restructure_errors
                    )
                    return False, f"Data restructuring failed: {restructure_errors[0]}", import_id
            
            # Validate against schema if provided
            if schema_name:
                is_valid, errors = self._validate_against_schema(data, schema_name)
                
                if not is_valid:
                    self._update_import_status(
                        import_id=import_id,
                        status="failed",
                        validation_errors=errors
                    )
                    return False, f"Schema validation failed: {errors[0]}", import_id
            
            # Determine target file
            target_dir = os.path.join(self.config['data_dir'], target_dataset)
            os.makedirs(target_dir, exist_ok=True)
            
            # Default target file name
            target_file_name = f"{target_dataset}.json"
            target_file = os.path.join(target_dir, target_file_name)
            
            # Handle merging with existing data
            if os.path.exists(target_file) and merge_strategy != 'replace':
                existing_data = self._load_data_from_file(target_file, 'json')
                
                if existing_data is not None:
                    # Create backup of existing data
                    backup_dir = os.path.join(self.config['backup_dir'], target_dataset)
                    os.makedirs(backup_dir, exist_ok=True)
                    
                    backup_file = os.path.join(
                        backup_dir, 
                        f"{target_dataset}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                    )
                    
                    with open(backup_file, 'w') as f:
                        json.dump(existing_data, f, indent=2)
                    
                    # Merge data
                    if merge_strategy == 'append':
                        if isinstance(existing_data, list) and isinstance(data, list):
                            merged_data = existing_data + data
                        else:
                            self._update_import_status(
                                import_id=import_id,
                                status="failed",
                                validation_errors=["Cannot append: data structures are not compatible"]
                            )
                            return False, "Cannot append: data structures are not compatible", import_id
                    
                    elif merge_strategy == 'update':
                        if isinstance(existing_data, dict) and isinstance(data, dict):
                            merged_data = {**existing_data, **data}
                        elif isinstance(existing_data, list) and isinstance(data, list):
                            # For lists, we need a key to identify records
                            # This is a simplified implementation
                            merged_data = existing_data.copy()
                            
                            # Assume each item is a dict with an 'id' field
                            existing_ids = {item.get('id'): i for i, item in enumerate(existing_data) if 'id' in item}
                            
                            for new_item in data:
                                if 'id' in new_item and new_item['id'] in existing_ids:
                                    # Update existing item
                                    merged_data[existing_ids[new_item['id']]] = new_item
                                else:
                                    # Add new item
                                    merged_data.append(new_item)
                        else:
                            self._update_import_status(
                                import_id=import_id,
                                status="failed",
                                validation_errors=["Cannot update: data structures are not compatible"]
                            )
                            return False, "Cannot update: data structures are not compatible", import_id
                    
                    else:
                        self._update_import_status(
                            import_id=import_id,
                            status="failed",
                            validation_errors=[f"Unknown merge strategy: {merge_strategy}"]
                        )
                        return False, f"Unknown merge strategy: {merge_strategy}", import_id
                    
                    # Save merged data
                    with open(target_file, 'w') as f:
                        json.dump(merged_data, f, indent=2)
                    
                    # Create a new version record
                    self._create_dataset_version(
                        dataset_name=target_dataset,
                        file_path=target_file,
                        description=f"Merged data using strategy: {merge_strategy}",
                        user_info=user_info
                    )
                    
                    # Update import status
                    records_imported = len(data) if isinstance(data, list) else 1
                    self._update_import_status(
                        import_id=import_id,
                        status="completed",
                        records_imported=records_imported,
                        records_rejected=0
                    )
                    
                    return True, f"Data merged successfully into {target_dataset} using strategy: {merge_strategy}", import_id
                
                else:
                    # Failed to load existing data, treat as replace
                    logger.warning(f"Failed to load existing data from {target_file}, treating as replace")
                    merge_strategy = 'replace'
            
            # Handle replace or new dataset
            with open(target_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            # Create a new version record
            self._create_dataset_version(
                dataset_name=target_dataset,
                file_path=target_file,
                description=f"{'Replaced' if merge_strategy == 'replace' else 'Created'} dataset",
                user_info=user_info
            )
            
            # Update import status
            records_imported = len(data) if isinstance(data, list) else 1
            self._update_import_status(
                import_id=import_id,
                status="completed",
                records_imported=records_imported,
                records_rejected=0
            )
            
            return True, f"Data {'replaced' if merge_strategy == 'replace' else 'imported'} successfully to {target_dataset}", import_id
            
        except Exception as e:
            logger.error(f"Error importing data file: {e}")
            logger.error(traceback.format_exc())
            self._update_import_status(
                import_id=import_id,
                status="failed",
                validation_errors=[str(e)]
            )
            return False, f"Error importing data file: {str(e)}", import_id
    
    def _load_data_from_file(self, file_path, file_type):
        """
        Load data from a file based on its type.
        
        Args:
            file_path (str): Path to the file
            file_type (str): Type of the file (csv, json, etc.)
            
        Returns:
            object: Loaded data, or None if loading failed
        """
        try:
            if file_type == 'json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif file_type == 'csv':
                df = pd.read_csv(file_path)
                return df.to_dict('records')
            
            elif file_type == 'yaml':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f)
            
            elif file_type == 'xlsx':
                df = pd.read_excel(file_path)
                return df.to_dict('records')
            
            else:
                logger.error(f"Unsupported file type for data loading: {file_type}")
                return None
            
        except Exception as e:
            logger.error(f"Error loading data from file: {e}")
            return None
    
    def _create_import_record(self, file_path, file_type, file_size, file_hash, 
                             target_dataset, merge_strategy, user_info=None):
        """
        Create a record of an import operation.
        
        Args:
            file_path (str): Path to the imported file
            file_type (str): Type of the file
            file_size (int): Size of the file in bytes
            file_hash (str): Hash of the file
            target_dataset (str): Name of the dataset being imported into
            merge_strategy (str): Strategy for merging with existing data
            user_info (dict): Information about the user performing the import
            
        Returns:
            int: ID of the created import record, or None if creation failed
        """
        try:
            conn = sqlite3.connect(self.config['db_path'])
            cursor = conn.cursor()
            
            user_id = user_info.get('id') if user_info else None
            username = user_info.get('username') if user_info else None
            
            cursor.execute('''
            INSERT INTO import_history (
                timestamp, user_id, username, file_name, file_type, file_size, 
                file_hash, target_dataset, status, merge_strategy
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                user_id,
                username,
                os.path.basename(file_path),
                file_type,
                file_size,
                file_hash,
                target_dataset,
                "in_progress",
                merge_strategy
            ))
            
            import_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return import_id
            
        except Exception as e:
            logger.error(f"Error creating import record: {e}")
            return None
    
    def _update_import_status(self, import_id, status, records_imported=None, 
                             records_rejected=None, validation_errors=None):
        """
        Update the status of an import operation.
        
        Args:
            import_id (int): ID of the import record
            status (str): New status ('in_progress', 'completed', 'failed')
            records_imported (int): Number of records successfully imported
            records_rejected (int): Number of records rejected
            validation_errors (list): List of validation error messages
        """
        try:
            conn = sqlite3.connect(self.config['db_path'])
            cursor = conn.cursor()
            
            update_fields = ["status = ?"]
            params = [status]
            
            if records_imported is not None:
                update_fields.append("records_imported = ?")
                params.append(records_imported)
            
            if records_rejected is not None:
                update_fields.append("records_rejected = ?")
                params.append(records_rejected)
            
            if validation_errors is not None:
                update_fields.append("validation_errors = ?")
                params.append(json.dumps(validation_errors))
            
            # Add import_id to params
            params.append(import_id)
            
            query = f"UPDATE import_history SET {', '.join(update_fields)} WHERE id = ?"
            cursor.execute(query, params)
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error updating import status: {e}")
    
    def _create_dataset_version(self, dataset_name, file_path, description=None, user_info=None):
        """
        Create a new version record for a dataset.
        
        Args:
            dataset_name (str): Name of the dataset
            file_path (str): Path to the dataset file
            description (str): Description of the version
            user_info (dict): Information about the user creating the version
            
        Returns:
            str: Version identifier, or None if creation failed
        """
        try:
            conn = sqlite3.connect(self.config['db_path'])
            cursor = conn.cursor()
            
            # Get the latest version for this dataset
            cursor.execute('''
            SELECT version FROM dataset_versions
            WHERE dataset_name = ?
            ORDER BY id DESC LIMIT 1
            ''', (dataset_name,))
            
            result = cursor.fetchone()
            
            if result:
                # Increment version
                latest_version = result[0]
                try:
                    version_parts = latest_version.split('.')
                    version_parts[-1] = str(int(version_parts[-1]) + 1)
                    new_version = '.'.join(version_parts)
                except:
                    # If version parsing fails, use timestamp
                    new_version = datetime.now().strftime("v%Y%m%d.%H%M%S")
            else:
                # First version
                new_version = "1.0.0"
            
            # Compute file hash
            file_hash = self._compute_file_hash(file_path)
            
            # Count records
            data = self._load_data_from_file(file_path, 'json')
            record_count = len(data) if isinstance(data, list) else 1
            
            user_id = user_info.get('id') if user_info else None
            username = user_info.get('username') if user_info else None
            
            cursor.execute('''
            INSERT INTO dataset_versions (
                dataset_name, version, timestamp, user_id, username,
                file_path, file_hash, record_count, description, parent_version
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                dataset_name,
                new_version,
                datetime.now().isoformat(),
                user_id,
                username,
                file_path,
                file_hash,
                record_count,
                description,
                latest_version if result else None
            ))
            
            conn.commit()
            conn.close()
            
            return new_version
            
        except Exception as e:
            logger.error(f"Error creating dataset version: {e}")
            return None
    
    def export_data(self, dataset_name, file_format='json', filters=None, user_info=None):
        """
        Export data from a dataset to a file.
        
        Args:
            dataset_name (str): Name of the dataset to export
            file_format (str): Format of the export file (json, csv, etc.)
            filters (dict): Filters to apply to the data
            user_info (dict): Information about the user performing the export
            
        Returns:
            tuple: (success, message, export_file_path)
        """
        try:
            # Check if dataset exists
            dataset_dir = os.path.join(self.config['data_dir'], dataset_name)
            dataset_file = os.path.join(dataset_dir, f"{dataset_name}.json")
            
            if not os.path.exists(dataset_file):
                return False, f"Dataset not found: {dataset_name}", None
            
            # Load data
            data = self._load_data_from_file(dataset_file, 'json')
            
            if data is None:
                return False, f"Failed to load data from dataset: {dataset_name}", None
            
            # Apply filters if provided
            if filters:
                data = self._apply_filters(data, filters)
            
            # Create export directory
            export_dir = os.path.join(self.config['export_dir'], dataset_name)
            os.makedirs(export_dir, exist_ok=True)
            
            # Generate export file name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            export_file_name = f"{dataset_name}_{timestamp}.{file_format}"
            export_file_path = os.path.join(export_dir, export_file_name)
            
            # Export data in the requested format
            if file_format == 'json':
                with open(export_file_path, 'w') as f:
                    json.dump(data, f, indent=2)
            
            elif file_format == 'csv':
                if isinstance(data, list):
                    df = pd.DataFrame(data)
                    df.to_csv(export_file_path, index=False)
                else:
                    return False, "Cannot export non-list data to CSV", None
            
            elif file_format == 'xlsx':
                if isinstance(data, list):
                    df = pd.DataFrame(data)
                    df.to_excel(export_file_path, index=False)
                else:
                    return False, "Cannot export non-list data to Excel", None
            
            else:
                return False, f"Unsupported export format: {file_format}", None
            
            # Create export record
            self._create_export_record(
                file_name=export_file_name,
                file_type=file_format,
                file_size=os.path.getsize(export_file_path),
                source_dataset=dataset_name,
                records_exported=len(data) if isinstance(data, list) else 1,
                filters=filters,
                user_info=user_info
            )
            
            return True, f"Data exported successfully to {export_file_path}", export_file_path
            
        except Exception as e:
            logger.error(f"Error exporting data: {e}")
            return False, f"Error exporting data: {str(e)}", None
    
    def _apply_filters(self, data, filters):
        """
        Apply filters to data.
        
        Args:
            data (list or dict): Data to filter
            filters (dict): Filters to apply
            
        Returns:
            object: Filtered data
        """
        if not filters or not isinstance(filters, dict):
            return data
        
        if isinstance(data, list):
            filtered_data = []
            
            for item in data:
                if isinstance(item, dict):
                    # Check if item matches all filters
                    matches = True
                    
                    for field, value in filters.items():
                        if field in item:
                            if isinstance(value, dict) and '$' in value:
                                # Advanced filter with operators
                                for op, op_value in value.items():
                                    if op == '$eq':
                                        if item[field] != op_value:
                                            matches = False
                                            break
                                    elif op == '$ne':
                                        if item[field] == op_value:
                                            matches = False
                                            break
                                    elif op == '$gt':
                                        if not (item[field] > op_value):
                                            matches = False
                                            break
                                    elif op == '$lt':
                                        if not (item[field] < op_value):
                                            matches = False
                                            break
                                    elif op == '$in':
                                        if item[field] not in op_value:
                                            matches = False
                                            break
                            else:
                                # Simple equality filter
                                if item[field] != value:
                                    matches = False
                                    break
                        else:
                            matches = False
                            break
                    
                    if matches:
                        filtered_data.append(item)
            
            return filtered_data
        
        return data
    
    def _create_export_record(self, file_name, file_type, file_size, source_dataset, 
                             records_exported, filters=None, user_info=None):
        """
        Create a record of an export operation.
        
        Args:
            file_name (str): Name of the exported file
            file_type (str): Type of the file
            file_size (int): Size of the file in bytes
            source_dataset (str): Name of the dataset being exported
            records_exported (int): Number of records exported
            filters (dict): Filters applied to the data
            user_info (dict): Information about the user performing the export
            
        Returns:
            int: ID of the created export record, or None if creation failed
        """
        try:
            conn = sqlite3.connect(self.config['db_path'])
            cursor = conn.cursor()
            
            user_id = user_info.get('id') if user_info else None
            username = user_info.get('username') if user_info else None
            
            cursor.execute('''
            INSERT INTO export_history (
                timestamp, user_id, username, file_name, file_type, file_size, 
                source_dataset, records_exported, filters, status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                user_id,
                username,
                file_name,
                file_type,
                file_size,
                source_dataset,
                records_exported,
                json.dumps(filters) if filters else None,
                "completed"
            ))
            
            export_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return export_id
            
        except Exception as e:
            logger.error(f"Error creating export record: {e}")
            return None
    
    def get_import_history(self, filters=None, limit=100, offset=0):
        """
        Get history of import operations.
        
        Args:
            filters (dict): Filters to apply
            limit (int): Maximum number of records to return
            offset (int): Offset for pagination
            
        Returns:
            list: List of import history records
        """
        try:
            conn = sqlite3.connect(self.config['db_path'])
            cursor = conn.cursor()
            
            query = '''
            SELECT id, timestamp, user_id, username, file_name, file_type, file_size, 
                   file_hash, target_dataset, records_imported, records_rejected, 
                   validation_errors, status, merge_strategy
            FROM import_history
            '''
            
            params = []
            where_clauses = []
            
            if filters:
                for key, value in filters.items():
                    if key in ['user_id', 'username', 'file_type', 'target_dataset', 'status', 'merge_strategy']:
                        where_clauses.append(f"{key} = ?")
                        params.append(value)
            
            if where_clauses:
                query += " WHERE " + " AND ".join(where_clauses)
            
            query += " ORDER BY timestamp DESC LIMIT ? OFFSET ?"
            params.extend([limit, offset])
            
            cursor.execute(query, params)
            
            history = []
            for row in cursor.fetchall():
                history.append({
                    'id': row[0],
                    'timestamp': row[1],
                    'user_id': row[2],
                    'username': row[3],
                    'file_name': row[4],
                    'file_type': row[5],
                    'file_size': row[6],
                    'file_hash': row[7],
                    'target_dataset': row[8],
                    'records_imported': row[9],
                    'records_rejected': row[10],
                    'validation_errors': json.loads(row[11]) if row[11] else None,
                    'status': row[12],
                    'merge_strategy': row[13]
                })
            
            conn.close()
            return history
            
        except Exception as e:
            logger.error(f"Error getting import history: {e}")
            return []
    
    def get_export_history(self, filters=None, limit=100, offset=0):
        """
        Get history of export operations.
        
        Args:
            filters (dict): Filters to apply
            limit (int): Maximum number of records to return
            offset (int): Offset for pagination
            
        Returns:
            list: List of export history records
        """
        try:
            conn = sqlite3.connect(self.config['db_path'])
            cursor = conn.cursor()
            
            query = '''
            SELECT id, timestamp, user_id, username, file_name, file_type, file_size, 
                   source_dataset, records_exported, filters, status
            FROM export_history
            '''
            
            params = []
            where_clauses = []
            
            if filters:
                for key, value in filters.items():
                    if key in ['user_id', 'username', 'file_type', 'source_dataset', 'status']:
                        where_clauses.append(f"{key} = ?")
                        params.append(value)
            
            if where_clauses:
                query += " WHERE " + " AND ".join(where_clauses)
            
            query += " ORDER BY timestamp DESC LIMIT ? OFFSET ?"
            params.extend([limit, offset])
            
            cursor.execute(query, params)
            
            history = []
            for row in cursor.fetchall():
                history.append({
                    'id': row[0],
                    'timestamp': row[1],
                    'user_id': row[2],
                    'username': row[3],
                    'file_name': row[4],
                    'file_type': row[5],
                    'file_size': row[6],
                    'source_dataset': row[7],
                    'records_exported': row[8],
                    'filters': json.loads(row[9]) if row[9] else None,
                    'status': row[10]
                })
            
            conn.close()
            return history
            
        except Exception as e:
            logger.error(f"Error getting export history: {e}")
            return []
    
    def get_dataset_versions(self, dataset_name):
        """
        Get version history for a dataset.
        
        Args:
            dataset_name (str): Name of the dataset
            
        Returns:
            list: List of version records
        """
        try:
            conn = sqlite3.connect(self.config['db_path'])
            cursor = conn.cursor()
            
            cursor.execute('''
            SELECT id, version, timestamp, user_id, username, file_path, 
                   file_hash, record_count, description, parent_version
            FROM dataset_versions
            WHERE dataset_name = ?
            ORDER BY id DESC
            ''', (dataset_name,))
            
            versions = []
            for row in cursor.fetchall():
                versions.append({
                    'id': row[0],
                    'version': row[1],
                    'timestamp': row[2],
                    'user_id': row[3],
                    'username': row[4],
                    'file_path': row[5],
                    'file_hash': row[6],
                    'record_count': row[7],
                    'description': row[8],
                    'parent_version': row[9]
                })
            
            conn.close()
            return versions
            
        except Exception as e:
            logger.error(f"Error getting dataset versions: {e}")
            return []
    
    def restore_dataset_version(self, dataset_name, version, user_info=None):
        """
        Restore a dataset to a previous version.
        
        Args:
            dataset_name (str): Name of the dataset
            version (str): Version to restore
            user_info (dict): Information about the user performing the restoration
            
        Returns:
            tuple: (success, message)
        """
        try:
            conn = sqlite3.connect(self.config['db_path'])
            cursor = conn.cursor()
            
            # Find the version record
            cursor.execute('''
            SELECT file_path, file_hash
            FROM dataset_versions
            WHERE dataset_name = ? AND version = ?
            ''', (dataset_name, version))
            
            result = cursor.fetchone()
            
            if not result:
                conn.close()
                return False, f"Version {version} not found for dataset {dataset_name}"
            
            source_file_path, source_file_hash = result
            
            # Check if source file exists
            if not os.path.exists(source_file_path):
                conn.close()
                return False, f"Source file not found: {source_file_path}"
            
            # Verify file hash
            current_hash = self._compute_file_hash(source_file_path)
            if current_hash != source_file_hash:
                conn.close()
                return False, f"Source file has been modified: {source_file_path}"
            
            # Determine target file
            target_dir = os.path.join(self.config['data_dir'], dataset_name)
            target_file = os.path.join(target_dir, f"{dataset_name}.json")
            
            # Create backup of current version
            if os.path.exists(target_file):
                backup_dir = os.path.join(self.config['backup_dir'], dataset_name)
                os.makedirs(backup_dir, exist_ok=True)
                
                backup_file = os.path.join(
                    backup_dir, 
                    f"{dataset_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                )
                
                shutil.copy2(target_file, backup_file)
            
            # Copy version file to target
            shutil.copy2(source_file_path, target_file)
            
            # Create a new version record
            new_version = self._create_dataset_version(
                dataset_name=dataset_name,
                file_path=target_file,
                description=f"Restored from version {version}",
                user_info=user_info
            )
            
            conn.close()
            
            return True, f"Dataset {dataset_name} restored to version {version}"
            
        except Exception as e:
            logger.error(f"Error restoring dataset version: {e}")
            return False, f"Error restoring dataset version: {str(e)}"
    
    def list_datasets(self):
        """
        List all available datasets.
        
        Returns:
            list: List of dataset information
        """
        try:
            datasets = []
            
            # Get all subdirectories in data_dir
            for item in os.listdir(self.config['data_dir']):
                item_path = os.path.join(self.config['data_dir'], item)
                
                if os.path.isdir(item_path):
                    # Check if it contains a dataset file
                    dataset_file = os.path.join(item_path, f"{item}.json")
                    
                    if os.path.exists(dataset_file):
                        # Get dataset info
                        file_size = os.path.getsize(dataset_file)
                        file_hash = self._compute_file_hash(dataset_file)
                        
                        # Get latest version info
                        conn = sqlite3.connect(self.config['db_path'])
                        cursor = conn.cursor()
                        
                        cursor.execute('''
                        SELECT version, timestamp, username
                        FROM dataset_versions
                        WHERE dataset_name = ?
                        ORDER BY id DESC LIMIT 1
                        ''', (item,))
                        
                        version_info = cursor.fetchone()
                        
                        if version_info:
                            version, timestamp, username = version_info
                        else:
                            version, timestamp, username = None, None, None
                        
                        conn.close()
                        
                        # Load data to count records
                        data = self._load_data_from_file(dataset_file, 'json')
                        record_count = len(data) if isinstance(data, list) else 1
                        
                        datasets.append({
                            'name': item,
                            'file_path': dataset_file,
                            'file_size': file_size,
                            'file_hash': file_hash,
                            'record_count': record_count,
                            'version': version,
                            'last_updated': timestamp,
                            'last_updated_by': username
                        })
            
            return datasets
            
        except Exception as e:
            logger.error(f"Error listing datasets: {e}")
            return []
    
    def create_dataset_package(self, dataset_names, include_versions=False, user_info=None):
        """
        Create a package containing multiple datasets.
        
        Args:
            dataset_names (list): Names of datasets to include
            include_versions (bool): Whether to include version history
            user_info (dict): Information about the user creating the package
            
        Returns:
            tuple: (success, message, package_file_path)
        """
        try:
            # Create a temporary directory for the package
            with tempfile.TemporaryDirectory() as temp_dir:
                # Create a manifest file
                manifest = {
                    'created_at': datetime.now().isoformat(),
                    'created_by': user_info.get('username') if user_info else None,
                    'datasets': []
                }
                
                # Copy datasets to the package
                for dataset_name in dataset_names:
                    dataset_dir = os.path.join(self.config['data_dir'], dataset_name)
                    dataset_file = os.path.join(dataset_dir, f"{dataset_name}.json")
                    
                    if not os.path.exists(dataset_file):
                        logger.warning(f"Dataset not found: {dataset_name}")
                        continue
                    
                    # Create dataset directory in the package
                    package_dataset_dir = os.path.join(temp_dir, dataset_name)
                    os.makedirs(package_dataset_dir, exist_ok=True)
                    
                    # Copy dataset file
                    shutil.copy2(dataset_file, os.path.join(package_dataset_dir, f"{dataset_name}.json"))
                    
                    # Get dataset info
                    file_size = os.path.getsize(dataset_file)
                    file_hash = self._compute_file_hash(dataset_file)
                    
                    dataset_info = {
                        'name': dataset_name,
                        'file_size': file_size,
                        'file_hash': file_hash,
                        'versions': []
                    }
                    
                    # Include version history if requested
                    if include_versions:
                        versions = self.get_dataset_versions(dataset_name)
                        
                        for version in versions:
                            dataset_info['versions'].append({
                                'version': version['version'],
                                'timestamp': version['timestamp'],
                                'username': version['username'],
                                'description': version['description']
                            })
                    
                    manifest['datasets'].append(dataset_info)
                
                # Write manifest file
                with open(os.path.join(temp_dir, 'manifest.json'), 'w') as f:
                    json.dump(manifest, f, indent=2)
                
                # Create zip file
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                package_file_name = f"dataset_package_{timestamp}.zip"
                package_file_path = os.path.join(self.config['export_dir'], package_file_name)
                
                with zipfile.ZipFile(package_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, _, files in os.walk(temp_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, temp_dir)
                            zipf.write(file_path, arcname)
                
                return True, f"Dataset package created successfully: {package_file_path}", package_file_path
                
        except Exception as e:
            logger.error(f"Error creating dataset package: {e}")
            return False, f"Error creating dataset package: {str(e)}", None
    
    def import_dataset_package(self, package_file_path, merge_strategy='append', user_info=None):
        """
        Import datasets from a package.
        
        Args:
            package_file_path (str): Path to the package file
            merge_strategy (str): Strategy for merging with existing data
            user_info (dict): Information about the user importing the package
            
        Returns:
            tuple: (success, message, imported_datasets)
        """
        try:
            # Create a temporary directory for extraction
            with tempfile.TemporaryDirectory() as temp_dir:
                # Extract the package
                with zipfile.ZipFile(package_file_path, 'r') as zipf:
                    zipf.extractall(temp_dir)
                
                # Read manifest
                manifest_path = os.path.join(temp_dir, 'manifest.json')
                
                if not os.path.exists(manifest_path):
                    return False, "Invalid package: manifest.json not found", []
                
                with open(manifest_path, 'r') as f:
                    manifest = json.load(f)
                
                # Import datasets
                imported_datasets = []
                
                for dataset_info in manifest.get('datasets', []):
                    dataset_name = dataset_info.get('name')
                    
                    if not dataset_name:
                        continue
                    
                    dataset_file = os.path.join(temp_dir, dataset_name, f"{dataset_name}.json")
                    
                    if not os.path.exists(dataset_file):
                        logger.warning(f"Dataset file not found in package: {dataset_name}")
                        continue
                    
                    # Import the dataset
                    success, message, import_id = self.import_data(
                        file_path=dataset_file,
                        target_dataset=dataset_name,
                        merge_strategy=merge_strategy,
                        user_info=user_info
                    )
                    
                    imported_datasets.append({
                        'name': dataset_name,
                        'success': success,
                        'message': message,
                        'import_id': import_id
                    })
                
                return True, f"Imported {len(imported_datasets)} datasets from package", imported_datasets
                
        except Exception as e:
            logger.error(f"Error importing dataset package: {e}")
            return False, f"Error importing dataset package: {str(e)}", []


# Example usage
if __name__ == "__main__":
    # Example configuration
    config = {
        'data_dir': 'data',
        'import_dir': 'data/imports',
        'export_dir': 'data/exports',
        'schema_dir': 'data/schemas',
        'db_path': 'data/database/data_management.db',
    }
    
    # Create data manager
    data_manager = DataManager(config)
    
    # Example: Create a simple schema
    os.makedirs(config['schema_dir'], exist_ok=True)
    
    example_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "array",
        "items": {
            "type": "object",
            "required": ["name", "type"],
            "properties": {
                "name": {"type": "string"},
                "type": {"type": "string", "enum": ["disease", "nutrient_deficiency", "soil_type"]},
                "description": {"type": "string"},
                "confidence": {"type": "number", "minimum": 0, "maximum": 1}
            }
        }
    }
    
    with open(os.path.join(config['schema_dir'], 'example_schema.json'), 'w') as f:
        json.dump(example_schema, f, indent=2)
    
    # Example: Import data
    example_data = [
        {
            "name": "Bacterial Blight",
            "type": "disease",
            "description": "A bacterial disease affecting leaves",
            "confidence": 0.95
        },
        {
            "name": "Nitrogen Deficiency",
            "type": "nutrient_deficiency",
            "description": "Lack of nitrogen causing yellowing",
            "confidence": 0.85
        }
    ]
    
    example_data_file = os.path.join(config['import_dir'], 'example_data.json')
    os.makedirs(config['import_dir'], exist_ok=True)
    
    with open(example_data_file, 'w') as f:
        json.dump(example_data, f, indent=2)
    
    # Import the data
    success, message, import_id = data_manager.import_data(
        file_path=example_data_file,
        target_dataset='example_dataset',
        schema_name='example_schema',
        merge_strategy='replace',
        user_info={'id': 1, 'username': 'admin'}
    )
    
    print(f"Import result: {success}, {message}, ID: {import_id}")
    
    # Example: Export data
    success, message, export_file_path = data_manager.export_data(
        dataset_name='example_dataset',
        file_format='json',
        user_info={'id': 1, 'username': 'admin'}
    )
    
    print(f"Export result: {success}, {message}, File: {export_file_path}")
    
    # Example: List datasets
    datasets = data_manager.list_datasets()
    print(f"Available datasets: {len(datasets)}")
    for dataset in datasets:
        print(f"  - {dataset['name']} (records: {dataset['record_count']})")
