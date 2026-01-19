#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Variety Comparison System for Agricultural AI System.
Handles crop variety data management, comparison, and analysis.
"""

import os
import sys
import json
import logging
import datetime
import uuid
from typing import Dict, List, Any, Optional, Tuple, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('variety_comparison')


class VarietyComparisonSystem:
    """
    System for managing and comparing crop varieties.
    Allows tracking of variety characteristics, trial locations, and performance metrics.
    """
    
    def __init__(self, config_path: str, database_manager=None, image_processor=None, audit_manager=None):
        """
        Initialize the variety comparison system.
        
        Args:
            config_path: Path to configuration file
            database_manager: Database manager instance
            image_processor: Image processor instance
            audit_manager: Audit manager instance
        """
        self.config_path = config_path
        self.database_manager = database_manager
        self.image_processor = image_processor
        self.audit_manager = audit_manager
        
        # Load configuration
        self.config = self._load_config()
        
        # Initialize data directories
        self._init_directories()
        
        logger.info("Variety Comparison System initialized")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Get variety comparison specific config
            if 'variety_comparison' not in config:
                config['variety_comparison'] = {
                    'data_dir': os.path.join(os.path.dirname(self.config_path), '../data/varieties'),
                    'images_dir': os.path.join(os.path.dirname(self.config_path), '../data/varieties/images'),
                    'trials_dir': os.path.join(os.path.dirname(self.config_path), '../data/varieties/trials'),
                    'default_comparison_metrics': [
                        'fruit_color', 'fruit_size', 'fruit_shape', 'tolerance', 
                        'resistance', 'productivity', 'quality'
                    ]
                }
                
                # Save updated config
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=2)
            
            return config
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            # Return default configuration
            return {
                'variety_comparison': {
                    'data_dir': os.path.join(os.path.dirname(self.config_path), '../data/varieties'),
                    'images_dir': os.path.join(os.path.dirname(self.config_path), '../data/varieties/images'),
                    'trials_dir': os.path.join(os.path.dirname(self.config_path), '../data/varieties/trials'),
                    'default_comparison_metrics': [
                        'fruit_color', 'fruit_size', 'fruit_shape', 'tolerance', 
                        'resistance', 'productivity', 'quality'
                    ]
                }
            }
    
    def _init_directories(self):
        """Initialize required directories."""
        os.makedirs(self.config['variety_comparison']['data_dir'], exist_ok=True)
        os.makedirs(self.config['variety_comparison']['images_dir'], exist_ok=True)
        os.makedirs(self.config['variety_comparison']['trials_dir'], exist_ok=True)
    
    def add_variety(self, variety_data: Dict[str, Any], user_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a new crop variety to the system.
        
        Args:
            variety_data: Dictionary containing variety information
            user_info: Information about the user performing the action
            
        Returns:
            Dictionary with operation result
        """
        try:
            # Validate required fields
            required_fields = ['name', 'scientific_name', 'crop_type', 'description']
            for field in required_fields:
                if field not in variety_data:
                    return {
                        'success': False,
                        'error': f"Missing required field: {field}"
                    }
            
            # Generate unique ID if not provided
            if 'id' not in variety_data:
                variety_data['id'] = str(uuid.uuid4())
            
            # Add metadata
            variety_data['created_at'] = datetime.datetime.now().isoformat()
            variety_data['created_by'] = user_info.get('id')
            variety_data['updated_at'] = variety_data['created_at']
            variety_data['updated_by'] = user_info.get('id')
            
            # Save to database
            if self.database_manager:
                result = self.database_manager.insert_data(
                    table='varieties',
                    data=variety_data
                )
                
                if not result.get('success', False):
                    return result
            
            # Save to file system as backup
            variety_file = os.path.join(
                self.config['variety_comparison']['data_dir'],
                f"{variety_data['id']}.json"
            )
            
            with open(variety_file, 'w', encoding='utf-8') as f:
                json.dump(variety_data, f, indent=2)
            
            # Log the action
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="VARIETY",
                    action="add_variety",
                    component="variety_comparison",
                    user_info=user_info,
                    details={"variety_id": variety_data['id'], "name": variety_data['name']},
                    status="success"
                )
            
            return {
                'success': True,
                'variety_id': variety_data['id'],
                'message': f"Variety '{variety_data['name']}' added successfully"
            }
            
        except Exception as e:
            logger.error(f"Error adding variety: {e}")
            
            # Log the error
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="VARIETY",
                    action="add_variety",
                    component="variety_comparison",
                    user_info=user_info,
                    details={"error": str(e)},
                    status="error"
                )
            
            return {
                'success': False,
                'error': f"Error adding variety: {str(e)}"
            }
    
    def update_variety(self, variety_id: str, variety_data: Dict[str, Any], user_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing crop variety.
        
        Args:
            variety_id: ID of the variety to update
            variety_data: Dictionary containing updated variety information
            user_info: Information about the user performing the action
            
        Returns:
            Dictionary with operation result
        """
        try:
            # Get existing variety
            existing_variety = self.get_variety(variety_id)
            
            if not existing_variety.get('success', False):
                return existing_variety
            
            existing_data = existing_variety['variety']
            
            # Update fields
            for key, value in variety_data.items():
                if key not in ['id', 'created_at', 'created_by']:
                    existing_data[key] = value
            
            # Update metadata
            existing_data['updated_at'] = datetime.datetime.now().isoformat()
            existing_data['updated_by'] = user_info.get('id')
            
            # Save to database
            if self.database_manager:
                result = self.database_manager.update_data(
                    table='varieties',
                    data=existing_data,
                    condition=f"id = '{variety_id}'"
                )
                
                if not result.get('success', False):
                    return result
            
            # Save to file system as backup
            variety_file = os.path.join(
                self.config['variety_comparison']['data_dir'],
                f"{variety_id}.json"
            )
            
            with open(variety_file, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, indent=2)
            
            # Log the action
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="VARIETY",
                    action="update_variety",
                    component="variety_comparison",
                    user_info=user_info,
                    details={"variety_id": variety_id, "name": existing_data['name']},
                    status="success"
                )
            
            return {
                'success': True,
                'variety_id': variety_id,
                'message': f"Variety '{existing_data['name']}' updated successfully"
            }
            
        except Exception as e:
            logger.error(f"Error updating variety: {e}")
            
            # Log the error
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="VARIETY",
                    action="update_variety",
                    component="variety_comparison",
                    user_info=user_info,
                    details={"variety_id": variety_id, "error": str(e)},
                    status="error"
                )
            
            return {
                'success': False,
                'error': f"Error updating variety: {str(e)}"
            }
    
    def get_variety(self, variety_id: str) -> Dict[str, Any]:
        """
        Get information about a specific variety.
        
        Args:
            variety_id: ID of the variety to retrieve
            
        Returns:
            Dictionary with variety information
        """
        try:
            # Try to get from database
            if self.database_manager:
                result = self.database_manager.query_data(
                    table='varieties',
                    condition=f"id = '{variety_id}'"
                )
                
                if result.get('success', False) and result.get('data'):
                    return {
                        'success': True,
                        'variety': result['data'][0]
                    }
            
            # Try to get from file system
            variety_file = os.path.join(
                self.config['variety_comparison']['data_dir'],
                f"{variety_id}.json"
            )
            
            if os.path.exists(variety_file):
                with open(variety_file, 'r', encoding='utf-8') as f:
                    variety_data = json.load(f)
                
                return {
                    'success': True,
                    'variety': variety_data
                }
            
            return {
                'success': False,
                'error': f"Variety with ID '{variety_id}' not found"
            }
            
        except Exception as e:
            logger.error(f"Error getting variety: {e}")
            return {
                'success': False,
                'error': f"Error getting variety: {str(e)}"
            }
    
    def list_varieties(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        List varieties based on optional filters.
        
        Args:
            filters: Optional dictionary of filter criteria
            
        Returns:
            Dictionary with list of varieties
        """
        try:
            varieties = []
            
            # Try to get from database
            if self.database_manager:
                condition = ""
                if filters:
                    conditions = []
                    for key, value in filters.items():
                        if isinstance(value, str):
                            conditions.append(f"{key} LIKE '%{value}%'")
                        else:
                            conditions.append(f"{key} = {value}")
                    
                    if conditions:
                        condition = " AND ".join(conditions)
                
                result = self.database_manager.query_data(
                    table='varieties',
                    condition=condition
                )
                
                if result.get('success', False):
                    return {
                        'success': True,
                        'varieties': result['data']
                    }
            
            # Try to get from file system
            variety_files = [f for f in os.listdir(self.config['variety_comparison']['data_dir']) 
                            if f.endswith('.json')]
            
            for file in variety_files:
                file_path = os.path.join(self.config['variety_comparison']['data_dir'], file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    variety_data = json.load(f)
                
                # Apply filters if provided
                if filters:
                    include = True
                    for key, value in filters.items():
                        if key in variety_data:
                            if isinstance(value, str) and isinstance(variety_data[key], str):
                                if value.lower() not in variety_data[key].lower():
                                    include = False
                                    break
                            elif variety_data[key] != value:
                                include = False
                                break
                    
                    if include:
                        varieties.append(variety_data)
                else:
                    varieties.append(variety_data)
            
            return {
                'success': True,
                'varieties': varieties
            }
            
        except Exception as e:
            logger.error(f"Error listing varieties: {e}")
            return {
                'success': False,
                'error': f"Error listing varieties: {str(e)}"
            }
    
    def add_variety_image(self, variety_id: str, image_path: str, 
                         image_type: str, description: str, 
                         user_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add an image for a variety.
        
        Args:
            variety_id: ID of the variety
            image_path: Path to the image file
            image_type: Type of image (e.g., 'fruit', 'plant', 'leaf')
            description: Description of the image
            user_info: Information about the user performing the action
            
        Returns:
            Dictionary with operation result
        """
        try:
            # Check if variety exists
            variety_result = self.get_variety(variety_id)
            if not variety_result.get('success', False):
                return variety_result
            
            # Generate image ID
            image_id = str(uuid.uuid4())
            
            # Create destination directory
            dest_dir = os.path.join(
                self.config['variety_comparison']['images_dir'],
                variety_id
            )
            os.makedirs(dest_dir, exist_ok=True)
            
            # Get file extension
            _, ext = os.path.splitext(image_path)
            
            # Copy image to destination
            dest_path = os.path.join(dest_dir, f"{image_id}{ext}")
            
            import shutil
            shutil.copy2(image_path, dest_path)
            
            # Process image if image processor is available
            if self.image_processor:
                process_result = self.image_processor.process_image(
                    image_path=dest_path,
                    output_path=dest_path,
                    operations=['resize', 'optimize']
                )
                
                if not process_result.get('success', False):
                    logger.warning(f"Image processing warning: {process_result.get('error')}")
            
            # Create image metadata
            image_data = {
                'id': image_id,
                'variety_id': variety_id,
                'path': dest_path,
                'type': image_type,
                'description': description,
                'uploaded_at': datetime.datetime.now().isoformat(),
                'uploaded_by': user_info.get('id')
            }
            
            # Save to database
            if self.database_manager:
                result = self.database_manager.insert_data(
                    table='variety_images',
                    data=image_data
                )
                
                if not result.get('success', False):
                    return result
            
            # Save metadata to file
            metadata_file = os.path.join(dest_dir, f"{image_id}.json")
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(image_data, f, indent=2)
            
            # Update variety with image reference
            variety_data = variety_result['variety']
            if 'images' not in variety_data:
                variety_data['images'] = []
            
            variety_data['images'].append({
                'id': image_id,
                'type': image_type,
                'path': dest_path
            })
            
            self.update_variety(variety_id, variety_data, user_info)
            
            # Log the action
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="VARIETY",
                    action="add_variety_image",
                    component="variety_comparison",
                    user_info=user_info,
                    details={"variety_id": variety_id, "image_id": image_id},
                    status="success"
                )
            
            return {
                'success': True,
                'image_id': image_id,
                'message': f"Image added to variety successfully"
            }
            
        except Exception as e:
            logger.error(f"Error adding variety image: {e}")
            
            # Log the error
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="VARIETY",
                    action="add_variety_image",
                    component="variety_comparison",
                    user_info=user_info,
                    details={"variety_id": variety_id, "error": str(e)},
                    status="error"
                )
            
            return {
                'success': False,
                'error': f"Error adding variety image: {str(e)}"
            }
    
    def add_trial_location(self, location_data: Dict[str, Any], user_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a new trial location.
        
        Args:
            location_data: Dictionary containing location information
            user_info: Information about the user performing the action
            
        Returns:
            Dictionary with operation result
        """
        try:
            # Validate required fields
            required_fields = ['name', 'coordinates', 'area', 'soil_type', 'climate']
            for field in required_fields:
                if field not in location_data:
                    return {
                        'success': False,
                        'error': f"Missing required field: {field}"
                    }
            
            # Generate unique ID if not provided
            if 'id' not in location_data:
                location_data['id'] = str(uuid.uuid4())
            
            # Add metadata
            location_data['created_at'] = datetime.datetime.now().isoformat()
            location_data['created_by'] = user_info.get('id')
            location_data['updated_at'] = location_data['created_at']
            location_data['updated_by'] = user_info.get('id')
            
            # Save to database
            if self.database_manager:
                result = self.database_manager.insert_data(
                    table='trial_locations',
                    data=location_data
                )
                
                if not result.get('success', False):
                    return result
            
            # Save to file system as backup
            locations_dir = os.path.join(
                self.config['variety_comparison']['trials_dir'],
                'locations'
            )
            os.makedirs(locations_dir, exist_ok=True)
            
            location_file = os.path.join(
                locations_dir,
                f"{location_data['id']}.json"
            )
            
            with open(location_file, 'w', encoding='utf-8') as f:
                json.dump(location_data, f, indent=2)
            
            # Log the action
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="TRIAL",
                    action="add_trial_location",
                    component="variety_comparison",
                    user_info=user_info,
                    details={"location_id": location_data['id'], "name": location_data['name']},
                    status="success"
                )
            
            return {
                'success': True,
                'location_id': location_data['id'],
                'message': f"Trial location '{location_data['name']}' added successfully"
            }
            
        except Exception as e:
            logger.error(f"Error adding trial location: {e}")
            
            # Log the error
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="TRIAL",
                    action="add_trial_location",
                    component="variety_comparison",
                    user_info=user_info,
                    details={"error": str(e)},
                    status="error"
                )
            
            return {
                'success': False,
                'error': f"Error adding trial location: {str(e)}"
            }
    
    def add_variety_trial(self, trial_data: Dict[str, Any], user_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a new variety trial.
        
        Args:
            trial_data: Dictionary containing trial information
            user_info: Information about the user performing the action
            
        Returns:
            Dictionary with operation result
        """
        try:
            # Validate required fields
            required_fields = ['variety_id', 'location_id', 'planting_date', 'area', 'reference_varieties']
            for field in required_fields:
                if field not in trial_data:
                    return {
                        'success': False,
                        'error': f"Missing required field: {field}"
                    }
            
            # Check if variety exists
            variety_result = self.get_variety(trial_data['variety_id'])
            if not variety_result.get('success', False):
                return variety_result
            
            # Generate unique ID if not provided
            if 'id' not in trial_data:
                trial_data['id'] = str(uuid.uuid4())
            
            # Add metadata
            trial_data['created_at'] = datetime.datetime.now().isoformat()
            trial_data['created_by'] = user_info.get('id')
            trial_data['updated_at'] = trial_data['created_at']
            trial_data['updated_by'] = user_info.get('id')
            trial_data['status'] = trial_data.get('status', 'active')
            
            # Save to database
            if self.database_manager:
                result = self.database_manager.insert_data(
                    table='variety_trials',
                    data=trial_data
                )
                
                if not result.get('success', False):
                    return result
            
            # Save to file system as backup
            trials_dir = os.path.join(
                self.config['variety_comparison']['trials_dir'],
                'data'
            )
            os.makedirs(trials_dir, exist_ok=True)
            
            trial_file = os.path.join(
                trials_dir,
                f"{trial_data['id']}.json"
            )
            
            with open(trial_file, 'w', encoding='utf-8') as f:
                json.dump(trial_data, f, indent=2)
            
            # Log the action
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="TRIAL",
                    action="add_variety_trial",
                    component="variety_comparison",
                    user_info=user_info,
                    details={
                        "trial_id": trial_data['id'], 
                        "variety_id": trial_data['variety_id'],
                        "location_id": trial_data['location_id']
                    },
                    status="success"
                )
            
            return {
                'success': True,
                'trial_id': trial_data['id'],
                'message': f"Variety trial added successfully"
            }
            
        except Exception as e:
            logger.error(f"Error adding variety trial: {e}")
            
            # Log the error
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="TRIAL",
                    action="add_variety_trial",
                    component="variety_comparison",
                    user_info=user_info,
                    details={"error": str(e)},
                    status="error"
                )
            
            return {
                'success': False,
                'error': f"Error adding variety trial: {str(e)}"
            }
    
    def update_trial_results(self, trial_id: str, results_data: Dict[str, Any], 
                            user_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update results for a variety trial.
        
        Args:
            trial_id: ID of the trial
            results_data: Dictionary containing trial results
            user_info: Information about the user performing the action
            
        Returns:
            Dictionary with operation result
        """
        try:
            # Get existing trial
            trial_file = os.path.join(
                self.config['variety_comparison']['trials_dir'],
                'data',
                f"{trial_id}.json"
            )
            
            if not os.path.exists(trial_file):
                return {
                    'success': False,
                    'error': f"Trial with ID '{trial_id}' not found"
                }
            
            with open(trial_file, 'r', encoding='utf-8') as f:
                trial_data = json.load(f)
            
            # Update results
            if 'results' not in trial_data:
                trial_data['results'] = {}
            
            for key, value in results_data.items():
                trial_data['results'][key] = value
            
            # Update metadata
            trial_data['updated_at'] = datetime.datetime.now().isoformat()
            trial_data['updated_by'] = user_info.get('id')
            
            # Save to database
            if self.database_manager:
                result = self.database_manager.update_data(
                    table='variety_trials',
                    data=trial_data,
                    condition=f"id = '{trial_id}'"
                )
                
                if not result.get('success', False):
                    return result
            
            # Save to file system
            with open(trial_file, 'w', encoding='utf-8') as f:
                json.dump(trial_data, f, indent=2)
            
            # Log the action
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="TRIAL",
                    action="update_trial_results",
                    component="variety_comparison",
                    user_info=user_info,
                    details={"trial_id": trial_id},
                    status="success"
                )
            
            return {
                'success': True,
                'trial_id': trial_id,
                'message': f"Trial results updated successfully"
            }
            
        except Exception as e:
            logger.error(f"Error updating trial results: {e}")
            
            # Log the error
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="TRIAL",
                    action="update_trial_results",
                    component="variety_comparison",
                    user_info=user_info,
                    details={"trial_id": trial_id, "error": str(e)},
                    status="error"
                )
            
            return {
                'success': False,
                'error': f"Error updating trial results: {str(e)}"
            }
    
    def add_comparison_metric(self, metric_data: Dict[str, Any], user_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a new comparison metric for varieties.
        
        Args:
            metric_data: Dictionary containing metric information
            user_info: Information about the user performing the action
            
        Returns:
            Dictionary with operation result
        """
        try:
            # Validate required fields
            required_fields = ['name', 'description', 'unit', 'crop_types']
            for field in required_fields:
                if field not in metric_data:
                    return {
                        'success': False,
                        'error': f"Missing required field: {field}"
                    }
            
            # Generate unique ID if not provided
            if 'id' not in metric_data:
                metric_data['id'] = str(uuid.uuid4())
            
            # Add metadata
            metric_data['created_at'] = datetime.datetime.now().isoformat()
            metric_data['created_by'] = user_info.get('id')
            metric_data['updated_at'] = metric_data['created_at']
            metric_data['updated_by'] = user_info.get('id')
            
            # Save to database
            if self.database_manager:
                result = self.database_manager.insert_data(
                    table='comparison_metrics',
                    data=metric_data
                )
                
                if not result.get('success', False):
                    return result
            
            # Save to file system as backup
            metrics_dir = os.path.join(
                self.config['variety_comparison']['data_dir'],
                'metrics'
            )
            os.makedirs(metrics_dir, exist_ok=True)
            
            metric_file = os.path.join(
                metrics_dir,
                f"{metric_data['id']}.json"
            )
            
            with open(metric_file, 'w', encoding='utf-8') as f:
                json.dump(metric_data, f, indent=2)
            
            # Log the action
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="METRIC",
                    action="add_comparison_metric",
                    component="variety_comparison",
                    user_info=user_info,
                    details={"metric_id": metric_data['id'], "name": metric_data['name']},
                    status="success"
                )
            
            return {
                'success': True,
                'metric_id': metric_data['id'],
                'message': f"Comparison metric '{metric_data['name']}' added successfully"
            }
            
        except Exception as e:
            logger.error(f"Error adding comparison metric: {e}")
            
            # Log the error
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="METRIC",
                    action="add_comparison_metric",
                    component="variety_comparison",
                    user_info=user_info,
                    details={"error": str(e)},
                    status="error"
                )
            
            return {
                'success': False,
                'error': f"Error adding comparison metric: {str(e)}"
            }
    
    def get_comparison_metrics(self, crop_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Get comparison metrics, optionally filtered by crop type.
        
        Args:
            crop_type: Optional crop type to filter metrics
            
        Returns:
            Dictionary with list of metrics
        """
        try:
            metrics = []
            
            # Try to get from database
            if self.database_manager:
                condition = ""
                if crop_type:
                    condition = f"crop_types LIKE '%{crop_type}%'"
                
                result = self.database_manager.query_data(
                    table='comparison_metrics',
                    condition=condition
                )
                
                if result.get('success', False):
                    return {
                        'success': True,
                        'metrics': result['data']
                    }
            
            # Try to get from file system
            metrics_dir = os.path.join(
                self.config['variety_comparison']['data_dir'],
                'metrics'
            )
            
            if os.path.exists(metrics_dir):
                metric_files = [f for f in os.listdir(metrics_dir) if f.endswith('.json')]
                
                for file in metric_files:
                    file_path = os.path.join(metrics_dir, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        metric_data = json.load(f)
                    
                    # Filter by crop type if provided
                    if crop_type:
                        if 'crop_types' in metric_data and crop_type in metric_data['crop_types']:
                            metrics.append(metric_data)
                    else:
                        metrics.append(metric_data)
            
            # If no metrics found, return default metrics
            if not metrics:
                default_metrics = []
                for metric in self.config['variety_comparison']['default_comparison_metrics']:
                    default_metrics.append({
                        'id': metric,
                        'name': metric.replace('_', ' ').title(),
                        'description': f"Default metric for {metric.replace('_', ' ')}",
                        'unit': '',
                        'crop_types': ['all']
                    })
                
                return {
                    'success': True,
                    'metrics': default_metrics,
                    'note': 'Using default metrics'
                }
            
            return {
                'success': True,
                'metrics': metrics
            }
            
        except Exception as e:
            logger.error(f"Error getting comparison metrics: {e}")
            return {
                'success': False,
                'error': f"Error getting comparison metrics: {str(e)}"
            }
    
    def compare_varieties(self, variety_ids: List[str], metrics: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Compare multiple varieties based on specified metrics.
        
        Args:
            variety_ids: List of variety IDs to compare
            metrics: Optional list of metric IDs to use for comparison
            
        Returns:
            Dictionary with comparison results
        """
        try:
            if not variety_ids:
                return {
                    'success': False,
                    'error': "No varieties specified for comparison"
                }
            
            # Get varieties
            varieties = []
            for variety_id in variety_ids:
                result = self.get_variety(variety_id)
                if result.get('success', False):
                    varieties.append(result['variety'])
                else:
                    return {
                        'success': False,
                        'error': f"Variety with ID '{variety_id}' not found"
                    }
            
            # Get metrics if not provided
            if not metrics:
                # Try to determine crop type from first variety
                crop_type = varieties[0].get('crop_type') if varieties else None
                
                metrics_result = self.get_comparison_metrics(crop_type)
                if metrics_result.get('success', False):
                    metrics = [m['id'] for m in metrics_result['metrics']]
            
            # Get trial results for each variety
            comparison_data = {}
            for variety in varieties:
                variety_id = variety['id']
                variety_name = variety['name']
                
                # Initialize variety data in comparison
                comparison_data[variety_id] = {
                    'id': variety_id,
                    'name': variety_name,
                    'metrics': {}
                }
                
                # Get trials for this variety
                trials_dir = os.path.join(
                    self.config['variety_comparison']['trials_dir'],
                    'data'
                )
                
                if os.path.exists(trials_dir):
                    trial_files = [f for f in os.listdir(trials_dir) if f.endswith('.json')]
                    
                    for file in trial_files:
                        file_path = os.path.join(trials_dir, file)
                        with open(file_path, 'r', encoding='utf-8') as f:
                            trial_data = json.load(f)
                        
                        if trial_data.get('variety_id') == variety_id and 'results' in trial_data:
                            # Process trial results
                            for metric in metrics:
                                if metric in trial_data['results']:
                                    if metric not in comparison_data[variety_id]['metrics']:
                                        comparison_data[variety_id]['metrics'][metric] = []
                                    
                                    comparison_data[variety_id]['metrics'][metric].append(
                                        trial_data['results'][metric]
                                    )
            
            # Calculate averages for metrics
            for variety_id, variety_data in comparison_data.items():
                for metric, values in variety_data['metrics'].items():
                    if values:
                        # Calculate average if numeric values
                        try:
                            numeric_values = [float(v) for v in values if isinstance(v, (int, float)) or (isinstance(v, str) and v.replace('.', '', 1).isdigit())]
                            if numeric_values:
                                variety_data['metrics'][metric] = {
                                    'values': values,
                                    'average': sum(numeric_values) / len(numeric_values)
                                }
                            else:
                                # For non-numeric values, just keep the list
                                variety_data['metrics'][metric] = {
                                    'values': values
                                }
                        except:
                            # For non-numeric values, just keep the list
                            variety_data['metrics'][metric] = {
                                'values': values
                            }
            
            return {
                'success': True,
                'comparison': comparison_data,
                'metrics': metrics
            }
            
        except Exception as e:
            logger.error(f"Error comparing varieties: {e}")
            return {
                'success': False,
                'error': f"Error comparing varieties: {str(e)}"
            }
    
    def add_user_rating(self, variety_id: str, rating_data: Dict[str, Any], 
                       user_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a user rating for a variety.
        
        Args:
            variety_id: ID of the variety
            rating_data: Dictionary containing rating information
            user_info: Information about the user performing the action
            
        Returns:
            Dictionary with operation result
        """
        try:
            # Validate required fields
            required_fields = ['rating', 'comments']
            for field in required_fields:
                if field not in rating_data:
                    return {
                        'success': False,
                        'error': f"Missing required field: {field}"
                    }
            
            # Check if variety exists
            variety_result = self.get_variety(variety_id)
            if not variety_result.get('success', False):
                return variety_result
            
            # Generate unique ID if not provided
            if 'id' not in rating_data:
                rating_data['id'] = str(uuid.uuid4())
            
            # Add metadata
            rating_data['variety_id'] = variety_id
            rating_data['user_id'] = user_info.get('id')
            rating_data['username'] = user_info.get('username')
            rating_data['created_at'] = datetime.datetime.now().isoformat()
            
            # Save to database
            if self.database_manager:
                result = self.database_manager.insert_data(
                    table='variety_ratings',
                    data=rating_data
                )
                
                if not result.get('success', False):
                    return result
            
            # Save to file system as backup
            ratings_dir = os.path.join(
                self.config['variety_comparison']['data_dir'],
                'ratings',
                variety_id
            )
            os.makedirs(ratings_dir, exist_ok=True)
            
            rating_file = os.path.join(
                ratings_dir,
                f"{rating_data['id']}.json"
            )
            
            with open(rating_file, 'w', encoding='utf-8') as f:
                json.dump(rating_data, f, indent=2)
            
            # Update variety with rating reference
            variety_data = variety_result['variety']
            if 'ratings' not in variety_data:
                variety_data['ratings'] = []
            
            variety_data['ratings'].append({
                'id': rating_data['id'],
                'rating': rating_data['rating'],
                'user_id': user_info.get('id')
            })
            
            # Calculate average rating
            ratings = [r['rating'] for r in variety_data['ratings'] if 'rating' in r]
            if ratings:
                variety_data['average_rating'] = sum(ratings) / len(ratings)
            
            self.update_variety(variety_id, variety_data, user_info)
            
            # Log the action
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="RATING",
                    action="add_user_rating",
                    component="variety_comparison",
                    user_info=user_info,
                    details={"variety_id": variety_id, "rating_id": rating_data['id']},
                    status="success"
                )
            
            return {
                'success': True,
                'rating_id': rating_data['id'],
                'message': f"Rating added to variety successfully"
            }
            
        except Exception as e:
            logger.error(f"Error adding user rating: {e}")
            
            # Log the error
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="RATING",
                    action="add_user_rating",
                    component="variety_comparison",
                    user_info=user_info,
                    details={"variety_id": variety_id, "error": str(e)},
                    status="error"
                )
            
            return {
                'success': False,
                'error': f"Error adding user rating: {str(e)}"
            }
    
    def get_variety_ratings(self, variety_id: str) -> Dict[str, Any]:
        """
        Get ratings for a specific variety.
        
        Args:
            variety_id: ID of the variety
            
        Returns:
            Dictionary with ratings information
        """
        try:
            # Check if variety exists
            variety_result = self.get_variety(variety_id)
            if not variety_result.get('success', False):
                return variety_result
            
            ratings = []
            
            # Try to get from database
            if self.database_manager:
                result = self.database_manager.query_data(
                    table='variety_ratings',
                    condition=f"variety_id = '{variety_id}'"
                )
                
                if result.get('success', False):
                    return {
                        'success': True,
                        'ratings': result['data']
                    }
            
            # Try to get from file system
            ratings_dir = os.path.join(
                self.config['variety_comparison']['data_dir'],
                'ratings',
                variety_id
            )
            
            if os.path.exists(ratings_dir):
                rating_files = [f for f in os.listdir(ratings_dir) if f.endswith('.json')]
                
                for file in rating_files:
                    file_path = os.path.join(ratings_dir, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        rating_data = json.load(f)
                    
                    ratings.append(rating_data)
            
            # Calculate average rating
            if ratings:
                rating_values = [r['rating'] for r in ratings if 'rating' in r]
                average_rating = sum(rating_values) / len(rating_values) if rating_values else 0
            else:
                average_rating = 0
            
            return {
                'success': True,
                'ratings': ratings,
                'average_rating': average_rating,
                'count': len(ratings)
            }
            
        except Exception as e:
            logger.error(f"Error getting variety ratings: {e}")
            return {
                'success': False,
                'error': f"Error getting variety ratings: {str(e)}"
            }
