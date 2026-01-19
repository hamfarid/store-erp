#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Keyword management system for the Agricultural AI System.

This module provides functionality for managing keywords related to plant diseases,
soil types, nutrient deficiencies, and plant varieties. It supports categorization,
searching, and updating of keywords.
"""

import os
import json
import logging
import shutil
from datetime import datetime
import re
import sqlite3
import yaml
import csv
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('keyword_manager')

class KeywordManager:
    """
    Manages keywords for the Agricultural AI System.
    
    This class provides methods to:
    1. Add, update, and delete keywords
    2. Categorize keywords by type (disease, soil, nutrient, variety)
    3. Search for keywords
    4. Import and export keywords
    5. Track keyword changes
    """
    
    # Keyword categories
    CATEGORIES = {
        'disease': {
            'subcategories': ['viral', 'bacterial', 'fungal', 'pest', 'physiological'],
            'attributes': ['symptoms', 'causes', 'treatments', 'prevention', 'severity_levels']
        },
        'soil': {
            'subcategories': ['clay', 'sandy', 'loamy', 'silty', 'peaty', 'chalky', 'saline'],
            'attributes': ['characteristics', 'ph_range', 'suitable_crops', 'improvement_methods']
        },
        'nutrient': {
            'subcategories': ['macronutrient', 'micronutrient', 'secondary_nutrient'],
            'attributes': ['deficiency_symptoms', 'excess_symptoms', 'sources', 'recommended_levels']
        },
        'variety': {
            'subcategories': ['grain', 'vegetable', 'fruit', 'ornamental', 'industrial', 'forage'],
            'attributes': ['characteristics', 'growing_conditions', 'yield_potential', 'resistance', 'parent_varieties']
        },
        'deformity': {
            'subcategories': ['growth', 'fruit', 'leaf', 'stem', 'root'],
            'attributes': ['appearance', 'causes', 'treatments', 'prevention']
        }
    }
    
    def __init__(self, config=None):
        """
        Initialize the keyword manager.
        
        Args:
            config (dict): Configuration dictionary with keyword management settings
        """
        self.config = config or {}
        
        # Default configuration
        self.default_config = {
            'keywords_dir': 'data/keywords',
            'db_path': 'data/database/keywords.db',
            'export_dir': 'data/exports/keywords',
            'backup_dir': 'data/backups/keywords',
        }
        
        # Merge with provided config
        for key, value in self.default_config.items():
            if key not in self.config:
                self.config[key] = value
        
        # Create necessary directories
        for dir_key in ['keywords_dir', 'export_dir', 'backup_dir']:
            os.makedirs(self.config[dir_key], exist_ok=True)
        
        # Create category subdirectories
        for category in self.CATEGORIES.keys():
            os.makedirs(os.path.join(self.config['keywords_dir'], category), exist_ok=True)
        
        # Ensure database directory exists
        os.makedirs(os.path.dirname(self.config['db_path']), exist_ok=True)
        
        # Initialize database
        self._init_database()
        
        logger.info("Keyword manager initialized")
    
    def _init_database(self):
        """Initialize the SQLite database for keyword management."""
        try:
            conn = sqlite3.connect(self.config['db_path'])
            cursor = conn.cursor()
            
            # Create keywords table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS keywords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT,
                description TEXT,
                attributes TEXT,
                related_terms TEXT,
                created_at TEXT NOT NULL,
                created_by TEXT,
                updated_at TEXT,
                updated_by TEXT,
                UNIQUE(keyword, category)
            )
            ''')
            
            # Create keyword_history table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS keyword_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword_id INTEGER NOT NULL,
                action TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                user_id INTEGER,
                username TEXT,
                old_value TEXT,
                new_value TEXT,
                FOREIGN KEY (keyword_id) REFERENCES keywords (id)
            )
            ''')
            
            # Create keyword_search_index table for faster searching
            cursor.execute('''
            CREATE VIRTUAL TABLE IF NOT EXISTS keyword_search_index
            USING fts5(keyword, category, subcategory, description, related_terms, content='keywords', content_rowid='id')
            ''')
            
            # Create trigger to update search index when keywords are inserted
            cursor.execute('''
            CREATE TRIGGER IF NOT EXISTS keywords_ai AFTER INSERT ON keywords BEGIN
                INSERT INTO keyword_search_index(rowid, keyword, category, subcategory, description, related_terms)
                VALUES (new.id, new.keyword, new.category, new.subcategory, new.description, new.related_terms);
            END;
            ''')
            
            # Create trigger to update search index when keywords are updated
            cursor.execute('''
            CREATE TRIGGER IF NOT EXISTS keywords_au AFTER UPDATE ON keywords BEGIN
                UPDATE keyword_search_index SET
                    keyword = new.keyword,
                    category = new.category,
                    subcategory = new.subcategory,
                    description = new.description,
                    related_terms = new.related_terms
                WHERE rowid = old.id;
            END;
            ''')
            
            # Create trigger to update search index when keywords are deleted
            cursor.execute('''
            CREATE TRIGGER IF NOT EXISTS keywords_ad AFTER DELETE ON keywords BEGIN
                DELETE FROM keyword_search_index WHERE rowid = old.id;
            END;
            ''')
            
            conn.commit()
            conn.close()
            
            logger.info("Keyword database initialized")
            
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            logger.error(traceback.format_exc())
            raise
    
    def add_keyword(self, keyword, category, subcategory=None, description=None, 
                   attributes=None, related_terms=None, user_info=None):
        """
        Add a new keyword.
        
        Args:
            keyword (str): The keyword to add
            category (str): Category of the keyword (disease, soil, nutrient, variety)
            subcategory (str): Subcategory of the keyword
            description (str): Description of the keyword
            attributes (dict): Additional attributes of the keyword
            related_terms (list): Related terms or synonyms
            user_info (dict): Information about the user adding the keyword
            
        Returns:
            tuple: (success, message, keyword_id)
        """
        # Validate category
        if category not in self.CATEGORIES:
            return False, f"Invalid category: {category}", None
        
        # Validate subcategory if provided
        if subcategory and subcategory not in self.CATEGORIES[category]['subcategories']:
            return False, f"Invalid subcategory for {category}: {subcategory}", None
        
        try:
            conn = sqlite3.connect(self.config['db_path'])
            cursor = conn.cursor()
            
            # Check if keyword already exists in this category
            cursor.execute('''
            SELECT id FROM keywords
            WHERE keyword = ? AND category = ?
            ''', (keyword, category))
            
            existing = cursor.fetchone()
            
            if existing:
                conn.close()
                return False, f"Keyword '{keyword}' already exists in category '{category}'", existing[0]
            
            # Prepare attributes and related terms for storage
            attributes_json = json.dumps(attributes) if attributes else None
            related_terms_json = json.dumps(related_terms) if related_terms else None
            
            # Get user information
            username = user_info.get('username') if user_info else None
            
            # Insert the keyword
            cursor.execute('''
            INSERT INTO keywords (
                keyword, category, subcategory, description, attributes, 
                related_terms, created_at, created_by, updated_at, updated_by
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                keyword, category, subcategory, description, attributes_json,
                related_terms_json, datetime.now().isoformat(), username,
                datetime.now().isoformat(), username
            ))
            
            keyword_id = cursor.lastrowid
            
            # Record the action in history
            cursor.execute('''
            INSERT INTO keyword_history (
                keyword_id, action, timestamp, username, new_value
            )
            VALUES (?, ?, ?, ?, ?)
            ''', (
                keyword_id, 'add', datetime.now().isoformat(), username,
                json.dumps({
                    'keyword': keyword,
                    'category': category,
                    'subcategory': subcategory,
                    'description': description,
                    'attributes': attributes,
                    'related_terms': related_terms
                })
            ))
            
            conn.commit()
            
            # Also save to file system for backup and easier access
            self._save_keyword_to_file(keyword_id, keyword, category, subcategory, 
                                      description, attributes, related_terms)
            
            conn.close()
            
            return True, f"Keyword '{keyword}' added successfully to category '{category}'", keyword_id
            
        except Exception as e:
            logger.error(f"Error adding keyword: {e}")
            logger.error(traceback.format_exc())
            if conn:
                conn.close()
            return False, f"Error adding keyword: {str(e)}", None
    
    def update_keyword(self, keyword_id, updates, user_info=None):
        """
        Update an existing keyword.
        
        Args:
            keyword_id (int): ID of the keyword to update
            updates (dict): Dictionary of fields to update
            user_info (dict): Information about the user updating the keyword
            
        Returns:
            tuple: (success, message)
        """
        try:
            conn = sqlite3.connect(self.config['db_path'])
            cursor = conn.cursor()
            
            # Get current keyword data
            cursor.execute('''
            SELECT id, keyword, category, subcategory, description, attributes, related_terms
            FROM keywords
            WHERE id = ?
            ''', (keyword_id,))
            
            result = cursor.fetchone()
            
            if not result:
                conn.close()
                return False, f"Keyword with ID {keyword_id} not found"
            
            keyword_id, keyword, category, subcategory, description, attributes_json, related_terms_json = result
            
            # Parse JSON fields
            attributes = json.loads(attributes_json) if attributes_json else {}
            related_terms = json.loads(related_terms_json) if related_terms_json else []
            
            # Store old values for history
            old_values = {
                'keyword': keyword,
                'category': category,
                'subcategory': subcategory,
                'description': description,
                'attributes': attributes,
                'related_terms': related_terms
            }
            
            # Update fields
            new_keyword = updates.get('keyword', keyword)
            new_category = updates.get('category', category)
            new_subcategory = updates.get('subcategory', subcategory)
            new_description = updates.get('description', description)
            
            # Handle attributes update (merge with existing)
            if 'attributes' in updates:
                if isinstance(updates['attributes'], dict):
                    attributes.update(updates['attributes'])
                else:
                    attributes = updates['attributes']
            
            # Handle related terms update
            if 'related_terms' in updates:
                if isinstance(updates['related_terms'], list):
                    # Merge and deduplicate
                    related_terms = list(set(related_terms + updates['related_terms']))
                else:
                    related_terms = updates['related_terms']
            
            # Validate category if changed
            if new_category != category and new_category not in self.CATEGORIES:
                conn.close()
                return False, f"Invalid category: {new_category}"
            
            # Validate subcategory if provided and category exists
            if new_subcategory and new_category in self.CATEGORIES:
                if new_subcategory not in self.CATEGORIES[new_category]['subcategories']:
                    conn.close()
                    return False, f"Invalid subcategory for {new_category}: {new_subcategory}"
            
            # Get user information
            username = user_info.get('username') if user_info else None
            
            # Prepare JSON fields
            attributes_json = json.dumps(attributes)
            related_terms_json = json.dumps(related_terms)
            
            # Update the keyword
            cursor.execute('''
            UPDATE keywords SET
                keyword = ?,
                category = ?,
                subcategory = ?,
                description = ?,
                attributes = ?,
                related_terms = ?,
                updated_at = ?,
                updated_by = ?
            WHERE id = ?
            ''', (
                new_keyword, new_category, new_subcategory, new_description,
                attributes_json, related_terms_json, datetime.now().isoformat(),
                username, keyword_id
            ))
            
            # Store new values for history
            new_values = {
                'keyword': new_keyword,
                'category': new_category,
                'subcategory': new_subcategory,
                'description': new_description,
                'attributes': attributes,
                'related_terms': related_terms
            }
            
            # Record the action in history
            cursor.execute('''
            INSERT INTO keyword_history (
                keyword_id, action, timestamp, username, old_value, new_value
            )
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                keyword_id, 'update', datetime.now().isoformat(), username,
                json.dumps(old_values), json.dumps(new_values)
            ))
            
            conn.commit()
            
            # Also update file system backup
            self._save_keyword_to_file(keyword_id, new_keyword, new_category, new_subcategory, 
                                      new_description, attributes, related_terms)
            
            conn.close()
            
            return True, f"Keyword '{new_keyword}' updated successfully"
            
        except Exception as e:
            logger.error(f"Error updating keyword: {e}")
            logger.error(traceback.format_exc())
            if conn:
                conn.close()
            return False, f"Error updating keyword: {str(e)}"
    
    def delete_keyword(self, keyword_id, user_info=None):
        """
        Delete a keyword.
        
        Args:
            keyword_id (int): ID of the keyword to delete
            user_info (dict): Information about the user deleting the keyword
            
        Returns:
            tuple: (success, message)
        """
        try:
            conn = sqlite3.connect(self.config['db_path'])
            cursor = conn.cursor()
            
            # Get current keyword data for history
            cursor.execute('''
            SELECT keyword, category, subcategory, description, attributes, related_terms
            FROM keywords
            WHERE id = ?
            ''', (keyword_id,))
            
            result = cursor.fetchone()
            
            if not result:
                conn.close()
                return False, f"Keyword with ID {keyword_id} not found"
            
            keyword, category, subcategory, description, attributes_json, related_terms_json = result
            
            # Parse JSON fields
            attributes = json.loads(attributes_json) if attributes_json else {}
            related_terms = json.loads(related_terms_json) if related_terms_json else []
            
            # Get user information
            username = user_info.get('username') if user_info else None
            
            # Record the action in history
            cursor.execute('''
            INSERT INTO keyword_history (
                keyword_id, action, timestamp, username, old_value
            )
            VALUES (?, ?, ?, ?, ?)
            ''', (
                keyword_id, 'delete', datetime.now().isoformat(), username,
                json.dumps({
                    'keyword': keyword,
                    'category': category,
                    'subcategory': subcategory,
                    'description': description,
                    'attributes': attributes,
                    'related_terms': related_terms
                })
            ))
            
            # Delete the keyword
            cursor.execute('DELETE FROM keywords WHERE id = ?', (keyword_id,))
            
            conn.commit()
            
            # Also delete from file system
            self._delete_keyword_file(keyword, category)
            
            conn.close()
            
            return True, f"Keyword '{keyword}' deleted successfully"
            
        except Exception as e:
            logger.error(f"Error deleting keyword: {e}")
            if conn:
                conn.close()
            return False, f"Error deleting keyword: {str(e)}"
    
    def get_keyword(self, keyword_id):
        """
        Get a keyword by ID.
        
        Args:
            keyword_id (int): ID of the keyword to get
            
        Returns:
            dict: Keyword data, or None if not found
        """
        try:
            conn = sqlite3.connect(self.config['db_path'])
            cursor = conn.cursor()
            
            cursor.execute('''
            SELECT id, keyword, category, subcategory, description, attributes, 
                   related_terms, created_at, created_by, updated_at, updated_by
            FROM keywords
            WHERE id = ?
            ''', (keyword_id,))
            
            result = cursor.fetchone()
            
            if not result:
                conn.close()
                return None
            
            id, keyword, category, subcategory, description, attributes_json, \
            related_terms_json, created_at, created_by, updated_at, updated_by = result
            
            # Parse JSON fields
            attributes = json.loads(attributes_json) if attributes_json else {}
            related_terms = json.loads(related_terms_json) if related_terms_json else []
            
            keyword_data = {
                'id': id,
                'keyword': keyword,
                'category': category,
                'subcategory': subcategory,
                'description': description,
                'attributes': attributes,
                'related_terms': related_terms,
                'created_at': created_at,
                'created_by': created_by,
                'updated_at': updated_at,
                'updated_by': updated_by
            }
            
            conn.close()
            
            return keyword_data
            
        except Exception as e:
            logger.error(f"Error getting keyword: {e}")
            if conn:
                conn.close()
            return None
    
    def search_keywords(self, query, category=None, subcategory=None, limit=100, offset=0):
        """
        Search for keywords.
        
        Args:
            query (str): Search query
            category (str): Filter by category
            subcategory (str): Filter by subcategory
            limit (int): Maximum number of results
            offset (int): Offset for pagination
            
        Returns:
            list: List of matching keywords
        """
        try:
            conn = sqlite3.connect(self.config['db_path'])
            cursor = conn.cursor()
            
            # Prepare search conditions
            search_conditions = []
            params = []
            
            if query:
                # Use FTS5 for full-text search
                search_conditions.append('''
                id IN (
                    SELECT rowid FROM keyword_search_index
                    WHERE keyword_search_index MATCH ?
                )
                ''')
                params.append(query)
            
            if category:
                search_conditions.append('category = ?')
                params.append(category)
            
            if subcategory:
                search_conditions.append('subcategory = ?')
                params.append(subcategory)
            
            # Build the query
            sql_query = '''
            SELECT id, keyword, category, subcategory, description, attributes, 
                   related_terms, created_at, created_by, updated_at, updated_by
            FROM keywords
            '''
            
            if search_conditions:
                sql_query += ' WHERE ' + ' AND '.join(search_conditions)
            
            sql_query += ' ORDER BY keyword LIMIT ? OFFSET ?'
            params.extend([limit, offset])
            
            cursor.execute(sql_query, params)
            
            results = []
            for row in cursor.fetchall():
                id, keyword, category, subcategory, description, attributes_json, \
                related_terms_json, created_at, created_by, updated_at, updated_by = row
                
                # Parse JSON fields
                attributes = json.loads(attributes_json) if attributes_json else {}
                related_terms = json.loads(related_terms_json) if related_terms_json else []
                
                results.append({
                    'id': id,
                    'keyword': keyword,
                    'category': category,
                    'subcategory': subcategory,
                    'description': description,
                    'attributes': attributes,
                    'related_terms': related_terms,
                    'created_at': created_at,
                    'created_by': created_by,
                    'updated_at': updated_at,
                    'updated_by': updated_by
                })
            
            conn.close()
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching keywords: {e}")
            if conn:
                conn.close()
            return []
    
    def get_keywords_by_category(self, category, subcategory=None, limit=1000, offset=0):
        """
        Get keywords by category.
        
        Args:
            category (str): Category to filter by
            subcategory (str): Subcategory to filter by
            limit (int): Maximum number of results
            offset (int): Offset for pagination
            
        Returns:
            list: List of keywords in the category
        """
        try:
            conn = sqlite3.connect(self.config['db_path'])
            cursor = conn.cursor()
            
            # Prepare query conditions
            conditions = ['category = ?']
            params = [category]
            
            if subcategory:
                conditions.append('subcategory = ?')
                params.append(subcategory)
            
            # Build the query
            query = f'''
            SELECT id, keyword, category, subcategory, description, attributes, 
                   related_terms, created_at, created_by, updated_at, updated_by
            FROM keywords
            WHERE {' AND '.join(conditions)}
            ORDER BY keyword
            LIMIT ? OFFSET ?
            '''
            
            params.extend([limit, offset])
            
            cursor.execute(query, params)
            
            results = []
            for row in cursor.fetchall():
                id, keyword, category, subcategory, description, attributes_json, \
                related_terms_json, created_at, created_by, updated_at, updated_by = row
                
                # Parse JSON fields
                attributes = json.loads(attributes_json) if attributes_json else {}
                related_terms = json.loads(related_terms_json) if related_terms_json else []
                
                results.append({
                    'id': id,
                    'keyword': keyword,
                    'category': category,
                    'subcategory': subcategory,
                    'description': description,
                    'attributes': attributes,
                    'related_terms': related_terms,
                    'created_at': created_at,
                    'created_by': created_by,
                    'updated_at': updated_at,
                    'updated_by': updated_by
                })
            
            conn.close()
            
            return results
            
        except Exception as e:
            logger.error(f"Error getting keywords by category: {e}")
            if conn:
                conn.close()
            return []
    
    def get_keyword_history(self, keyword_id):
        """
        Get history of changes for a keyword.
        
        Args:
            keyword_id (int): ID of the keyword
            
        Returns:
            list: List of history entries
        """
        try:
            conn = sqlite3.connect(self.config['db_path'])
            cursor = conn.cursor()
            
            cursor.execute('''
            SELECT id, action, timestamp, username, old_value, new_value
            FROM keyword_history
            WHERE keyword_id = ?
            ORDER BY timestamp DESC
            ''', (keyword_id,))
            
            history = []
            for row in cursor.fetchall():
                id, action, timestamp, username, old_value, new_value = row
                
                # Parse JSON fields
                old_value_dict = json.loads(old_value) if old_value else None
                new_value_dict = json.loads(new_value) if new_value else None
                
                history.append({
                    'id': id,
                    'action': action,
                    'timestamp': timestamp,
                    'username': username,
                    'old_value': old_value_dict,
                    'new_value': new_value_dict
                })
            
            conn.close()
            
            return history
            
        except Exception as e:
            logger.error(f"Error getting keyword history: {e}")
            if conn:
                conn.close()
            return []
    
    def export_keywords(self, category=None, format='json', file_path=None):
        """
        Export keywords to a file.
        
        Args:
            category (str): Category to export, or None for all
            format (str): Export format (json, csv, yaml)
            file_path (str): Path to save the file, or None for default
            
        Returns:
            tuple: (success, message, export_file_path)
        """
        try:
            # Get keywords to export
            if category:
                keywords = self.get_keywords_by_category(category)
            else:
                # Get all keywords
                conn = sqlite3.connect(self.config['db_path'])
                cursor = conn.cursor()
                
                cursor.execute('''
                SELECT id, keyword, category, subcategory, description, attributes, 
                       related_terms, created_at, created_by, updated_at, updated_by
                FROM keywords
                ORDER BY category, keyword
                ''')
                
                keywords = []
                for row in cursor.fetchall():
                    id, keyword, category, subcategory, description, attributes_json, \
                    related_terms_json, created_at, created_by, updated_at, updated_by = row
                    
                    # Parse JSON fields
                    attributes = json.loads(attributes_json) if attributes_json else {}
                    related_terms = json.loads(related_terms_json) if related_terms_json else []
                    
                    keywords.append({
                        'id': id,
                        'keyword': keyword,
                        'category': category,
                        'subcategory': subcategory,
                        'description': description,
                        'attributes': attributes,
                        'related_terms': related_terms,
                        'created_at': created_at,
                        'created_by': created_by,
                        'updated_at': updated_at,
                        'updated_by': updated_by
                    })
                
                conn.close()
            
            if not keywords:
                return False, "No keywords found to export", None
            
            # Determine export file path
            if not file_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"keywords_{category or 'all'}_{timestamp}.{format}"
                file_path = os.path.join(self.config['export_dir'], filename)
            
            # Ensure export directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Export in the requested format
            if format == 'json':
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(keywords, f, indent=2, ensure_ascii=False)
            
            elif format == 'csv':
                # Flatten the data for CSV export
                flattened_data = []
                for kw in keywords:
                    flat_kw = {
                        'id': kw['id'],
                        'keyword': kw['keyword'],
                        'category': kw['category'],
                        'subcategory': kw['subcategory'],
                        'description': kw['description'],
                        'related_terms': ', '.join(kw['related_terms']) if kw['related_terms'] else '',
                        'created_at': kw['created_at'],
                        'created_by': kw['created_by'],
                        'updated_at': kw['updated_at'],
                        'updated_by': kw['updated_by']
                    }
                    
                    # Add attributes as separate columns
                    for attr_key, attr_value in kw['attributes'].items():
                        flat_kw[f"attr_{attr_key}"] = str(attr_value)
                    
                    flattened_data.append(flat_kw)
                
                # Get all possible columns
                columns = set()
                for kw in flattened_data:
                    columns.update(kw.keys())
                
                columns = sorted(list(columns))
                
                with open(file_path, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=columns)
                    writer.writeheader()
                    writer.writerows(flattened_data)
            
            elif format == 'yaml':
                with open(file_path, 'w', encoding='utf-8') as f:
                    yaml.dump(keywords, f, default_flow_style=False, allow_unicode=True)
            
            else:
                return False, f"Unsupported export format: {format}", None
            
            return True, f"Exported {len(keywords)} keywords to {file_path}", file_path
            
        except Exception as e:
            logger.error(f"Error exporting keywords: {e}")
            logger.error(traceback.format_exc())
            return False, f"Error exporting keywords: {str(e)}", None
    
    def import_keywords(self, file_path, merge_strategy='update', user_info=None):
        """
        Import keywords from a file.
        
        Args:
            file_path (str): Path to the file to import
            merge_strategy (str): Strategy for handling duplicates ('update', 'skip', 'replace')
            user_info (dict): Information about the user importing the keywords
            
        Returns:
            tuple: (success, message, stats)
        """
        if not os.path.exists(file_path):
            return False, f"File not found: {file_path}", None
        
        try:
            # Determine file format from extension
            file_ext = os.path.splitext(file_path)[1].lower()
            
            # Load keywords from file
            if file_ext == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    keywords = json.load(f)
            
            elif file_ext == '.csv':
                keywords = []
                with open(file_path, 'r', encoding='utf-8', newline='') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        # Extract base fields
                        keyword = {
                            'keyword': row.get('keyword'),
                            'category': row.get('category'),
                            'subcategory': row.get('subcategory'),
                            'description': row.get('description'),
                            'attributes': {},
                            'related_terms': []
                        }
                        
                        # Extract related terms
                        if 'related_terms' in row and row['related_terms']:
                            keyword['related_terms'] = [term.strip() for term in row['related_terms'].split(',')]
                        
                        # Extract attributes
                        for key, value in row.items():
                            if key.startswith('attr_') and value:
                                attr_name = key[5:]  # Remove 'attr_' prefix
                                keyword['attributes'][attr_name] = value
                        
                        keywords.append(keyword)
            
            elif file_ext == '.yaml' or file_ext == '.yml':
                with open(file_path, 'r', encoding='utf-8') as f:
                    keywords = yaml.safe_load(f)
            
            else:
                return False, f"Unsupported file format: {file_ext}", None
            
            if not keywords:
                return False, "No keywords found in the file", None
            
            # Import keywords
            stats = {
                'total': len(keywords),
                'added': 0,
                'updated': 0,
                'skipped': 0,
                'failed': 0
            }
            
            for kw in keywords:
                # Validate required fields
                if not kw.get('keyword') or not kw.get('category'):
                    stats['failed'] += 1
                    continue
                
                # Check if keyword already exists
                conn = sqlite3.connect(self.config['db_path'])
                cursor = conn.cursor()
                
                cursor.execute('''
                SELECT id FROM keywords
                WHERE keyword = ? AND category = ?
                ''', (kw['keyword'], kw['category']))
                
                existing = cursor.fetchone()
                conn.close()
                
                if existing:
                    # Handle existing keyword based on merge strategy
                    if merge_strategy == 'skip':
                        stats['skipped'] += 1
                        continue
                    
                    elif merge_strategy == 'update':
                        # Update existing keyword
                        success, _ = self.update_keyword(
                            existing[0],
                            {
                                'subcategory': kw.get('subcategory'),
                                'description': kw.get('description'),
                                'attributes': kw.get('attributes', {}),
                                'related_terms': kw.get('related_terms', [])
                            },
                            user_info
                        )
                        
                        if success:
                            stats['updated'] += 1
                        else:
                            stats['failed'] += 1
                    
                    elif merge_strategy == 'replace':
                        # Delete and re-add
                        self.delete_keyword(existing[0], user_info)
                        
                        success, _, _ = self.add_keyword(
                            kw['keyword'],
                            kw['category'],
                            kw.get('subcategory'),
                            kw.get('description'),
                            kw.get('attributes', {}),
                            kw.get('related_terms', []),
                            user_info
                        )
                        
                        if success:
                            stats['updated'] += 1
                        else:
                            stats['failed'] += 1
                
                else:
                    # Add new keyword
                    success, _, _ = self.add_keyword(
                        kw['keyword'],
                        kw['category'],
                        kw.get('subcategory'),
                        kw.get('description'),
                        kw.get('attributes', {}),
                        kw.get('related_terms', []),
                        user_info
                    )
                    
                    if success:
                        stats['added'] += 1
                    else:
                        stats['failed'] += 1
            
            return True, f"Imported keywords: {stats['added']} added, {stats['updated']} updated, {stats['skipped']} skipped, {stats['failed']} failed", stats
            
        except Exception as e:
            logger.error(f"Error importing keywords: {e}")
            logger.error(traceback.format_exc())
            return False, f"Error importing keywords: {str(e)}", None
    
    def _save_keyword_to_file(self, keyword_id, keyword, category, subcategory, 
                             description, attributes, related_terms):
        """
        Save a keyword to a file for backup and easier access.
        
        Args:
            keyword_id (int): ID of the keyword
            keyword (str): The keyword
            category (str): Category of the keyword
            subcategory (str): Subcategory of the keyword
            description (str): Description of the keyword
            attributes (dict): Additional attributes of the keyword
            related_terms (list): Related terms or synonyms
        """
        try:
            # Create category directory if it doesn't exist
            category_dir = os.path.join(self.config['keywords_dir'], category)
            os.makedirs(category_dir, exist_ok=True)
            
            # Create a safe filename from the keyword
            safe_keyword = re.sub(r'[^\w\s-]', '', keyword).strip().lower()
            safe_keyword = re.sub(r'[-\s]+', '_', safe_keyword)
            
            # Prepare data for file
            data = {
                'id': keyword_id,
                'keyword': keyword,
                'category': category,
                'subcategory': subcategory,
                'description': description,
                'attributes': attributes,
                'related_terms': related_terms,
                'last_updated': datetime.now().isoformat()
            }
            
            # Save to JSON file
            file_path = os.path.join(category_dir, f"{safe_keyword}.json")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
        except Exception as e:
            logger.error(f"Error saving keyword to file: {e}")
    
    def _delete_keyword_file(self, keyword, category):
        """
        Delete a keyword file.
        
        Args:
            keyword (str): The keyword
            category (str): Category of the keyword
        """
        try:
            # Create a safe filename from the keyword
            safe_keyword = re.sub(r'[^\w\s-]', '', keyword).strip().lower()
            safe_keyword = re.sub(r'[-\s]+', '_', safe_keyword)
            
            # Delete the file if it exists
            file_path = os.path.join(self.config['keywords_dir'], category, f"{safe_keyword}.json")
            if os.path.exists(file_path):
                os.remove(file_path)
            
        except Exception as e:
            logger.error(f"Error deleting keyword file: {e}")
    
    def get_categories(self):
        """
        Get all available categories and their subcategories.
        
        Returns:
            dict: Dictionary of categories and their subcategories
        """
        return self.CATEGORIES
    
    def get_category_stats(self):
        """
        Get statistics about keywords in each category.
        
        Returns:
            dict: Dictionary of category statistics
        """
        try:
            conn = sqlite3.connect(self.config['db_path'])
            cursor = conn.cursor()
            
            # Get counts by category
            cursor.execute('''
            SELECT category, COUNT(*) as count
            FROM keywords
            GROUP BY category
            ''')
            
            category_counts = {row[0]: row[1] for row in cursor.fetchall()}
            
            # Get counts by subcategory
            cursor.execute('''
            SELECT category, subcategory, COUNT(*) as count
            FROM keywords
            WHERE subcategory IS NOT NULL
            GROUP BY category, subcategory
            ''')
            
            subcategory_counts = {}
            for row in cursor.fetchall():
                category, subcategory, count = row
                if category not in subcategory_counts:
                    subcategory_counts[category] = {}
                subcategory_counts[category][subcategory] = count
            
            conn.close()
            
            # Prepare stats
            stats = {}
            for category, subcategories in self.CATEGORIES.items():
                stats[category] = {
                    'count': category_counts.get(category, 0),
                    'subcategories': {}
                }
                
                for subcategory in subcategories['subcategories']:
                    count = 0
                    if category in subcategory_counts and subcategory in subcategory_counts[category]:
                        count = subcategory_counts[category][subcategory]
                    
                    stats[category]['subcategories'][subcategory] = count
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting category stats: {e}")
            if conn:
                conn.close()
            return {}


# Example usage
if __name__ == "__main__":
    # Example configuration
    config = {
        'keywords_dir': 'data/keywords',
        'db_path': 'data/database/keywords.db',
        'export_dir': 'data/exports/keywords',
    }
    
    # Create keyword manager
    keyword_manager = KeywordManager(config)
    
    # Example: Add some keywords
    user_info = {'id': 1, 'username': 'admin'}
    
    # Add a disease keyword
    keyword_manager.add_keyword(
        keyword="Bacterial Leaf Blight",
        category="disease",
        subcategory="bacterial",
        description="A serious bacterial disease affecting rice plants, caused by Xanthomonas oryzae pv. oryzae.",
        attributes={
            "symptoms": "Water-soaked lesions on leaf margins, which later turn yellow and then white.",
            "causes": "Xanthomonas oryzae pv. oryzae bacteria",
            "treatments": "Copper-based bactericides, resistant varieties",
            "prevention": "Crop rotation, field sanitation, resistant varieties",
            "severity_levels": ["mild", "moderate", "severe"]
        },
        related_terms=["Rice Bacterial Blight", "Kresek", "Xanthomonas oryzae"],
        user_info=user_info
    )
    
    # Add a soil keyword
    keyword_manager.add_keyword(
        keyword="Clay Soil",
        category="soil",
        subcategory="clay",
        description="Soil with high clay content, characterized by small particles and high water retention.",
        attributes={
            "characteristics": "Small particles, sticky when wet, hard when dry",
            "ph_range": "6.0-8.0",
            "suitable_crops": ["Rice", "Wheat", "Certain vegetables"],
            "improvement_methods": ["Adding organic matter", "Adding sand", "Avoiding compaction"]
        },
        related_terms=["Heavy soil", "Clayey soil"],
        user_info=user_info
    )
    
    # Add a nutrient keyword
    keyword_manager.add_keyword(
        keyword="Nitrogen Deficiency",
        category="nutrient",
        subcategory="macronutrient",
        description="A condition where plants lack sufficient nitrogen for optimal growth.",
        attributes={
            "deficiency_symptoms": "Yellowing of older leaves, stunted growth",
            "excess_symptoms": "Excessive vegetative growth, delayed flowering",
            "sources": ["Ammonium nitrate", "Urea", "Compost", "Manure"],
            "recommended_levels": "Varies by crop, typically 100-200 kg/ha"
        },
        related_terms=["N deficiency", "Nitrogen shortage"],
        user_info=user_info
    )
    
    # Example: Search for keywords
    results = keyword_manager.search_keywords("blight")
    print(f"Search results for 'blight': {len(results)} keywords found")
    
    # Example: Export keywords
    success, message, export_file = keyword_manager.export_keywords(format='json')
    print(f"Export result: {message}")
    
    # Example: Get category stats
    stats = keyword_manager.get_category_stats()
    print("Keyword statistics by category:")
    for category, data in stats.items():
        print(f"  {category}: {data['count']} keywords")
        for subcategory, count in data['subcategories'].items():
            print(f"    - {subcategory}: {count} keywords")
