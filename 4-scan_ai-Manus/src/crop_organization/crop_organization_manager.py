#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Crop Type Organization Module for Agricultural AI System.
Manages the organization of data by crop types (vegetables, fruits, crops).
"""

import os
import sys
import json
import logging
import datetime
import shutil
from typing import Dict, List, Any, Optional, Tuple, Union
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('crop_organization')


class CropOrganizationManager:
    """
    Manages the organization of data by crop types (vegetables, fruits, crops).
    Provides functionality for categorizing, searching, and managing crop data.
    """
    
    def __init__(self, config_path: str, database_manager=None, audit_manager=None):
        """
        Initialize the Crop Organization Manager.
        
        Args:
            config_path: Path to configuration file
            database_manager: Database manager instance
            audit_manager: Audit manager instance
        """
        self.config_path = config_path
        self.database_manager = database_manager
        self.audit_manager = audit_manager
        
        # Load configuration
        self.config = self._load_config()
        
        # Initialize data directories
        self._init_directories()
        
        # Load crop categories
        self.crop_categories = self._load_crop_categories()
        
        logger.info("Crop Organization Manager initialized")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Get crop organization specific config
            if 'crop_organization' not in config:
                config['crop_organization'] = {
                    'data_dir': os.path.join(os.path.dirname(self.config_path), '../data'),
                    'vegetables_dir': os.path.join(os.path.dirname(self.config_path), '../data/vegetables'),
                    'fruits_dir': os.path.join(os.path.dirname(self.config_path), '../data/fruits'),
                    'crops_dir': os.path.join(os.path.dirname(self.config_path), '../data/crops'),
                    'categories_file': os.path.join(os.path.dirname(self.config_path), '../data/crop_categories.json'),
                    'keywords_dir': os.path.join(os.path.dirname(self.config_path), '../data/keywords'),
                    'reference_dir': os.path.join(os.path.dirname(self.config_path), '../data/reference_datasets'),
                    'subcategories': {
                        'vegetables': [
                            'leafy_vegetables',
                            'root_vegetables',
                            'fruit_vegetables',
                            'bulb_vegetables',
                            'stem_vegetables',
                            'flower_vegetables'
                        ],
                        'fruits': [
                            'tropical_fruits',
                            'citrus_fruits',
                            'stone_fruits',
                            'pome_fruits',
                            'berries',
                            'melons'
                        ],
                        'crops': [
                            'cereals',
                            'legumes',
                            'oilseeds',
                            'fiber_crops',
                            'sugar_crops',
                            'forage_crops'
                        ]
                    },
                    'data_types': [
                        'images',
                        'diseases',
                        'nutrients',
                        'varieties',
                        'treatments',
                        'research',
                        'keywords'
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
                'crop_organization': {
                    'data_dir': os.path.join(os.path.dirname(self.config_path), '../data'),
                    'vegetables_dir': os.path.join(os.path.dirname(self.config_path), '../data/vegetables'),
                    'fruits_dir': os.path.join(os.path.dirname(self.config_path), '../data/fruits'),
                    'crops_dir': os.path.join(os.path.dirname(self.config_path), '../data/crops'),
                    'categories_file': os.path.join(os.path.dirname(self.config_path), '../data/crop_categories.json'),
                    'keywords_dir': os.path.join(os.path.dirname(self.config_path), '../data/keywords'),
                    'reference_dir': os.path.join(os.path.dirname(self.config_path), '../data/reference_datasets'),
                    'subcategories': {
                        'vegetables': [
                            'leafy_vegetables',
                            'root_vegetables',
                            'fruit_vegetables',
                            'bulb_vegetables',
                            'stem_vegetables',
                            'flower_vegetables'
                        ],
                        'fruits': [
                            'tropical_fruits',
                            'citrus_fruits',
                            'stone_fruits',
                            'pome_fruits',
                            'berries',
                            'melons'
                        ],
                        'crops': [
                            'cereals',
                            'legumes',
                            'oilseeds',
                            'fiber_crops',
                            'sugar_crops',
                            'forage_crops'
                        ]
                    },
                    'data_types': [
                        'images',
                        'diseases',
                        'nutrients',
                        'varieties',
                        'treatments',
                        'research',
                        'keywords'
                    ]
                }
            }
    
    def _init_directories(self):
        """Initialize required directories."""
        # Create main data directories
        os.makedirs(self.config['crop_organization']['data_dir'], exist_ok=True)
        os.makedirs(self.config['crop_organization']['vegetables_dir'], exist_ok=True)
        os.makedirs(self.config['crop_organization']['fruits_dir'], exist_ok=True)
        os.makedirs(self.config['crop_organization']['crops_dir'], exist_ok=True)
        os.makedirs(self.config['crop_organization']['keywords_dir'], exist_ok=True)
        os.makedirs(self.config['crop_organization']['reference_dir'], exist_ok=True)
        
        # Create subcategory directories
        for category, subcategories in self.config['crop_organization']['subcategories'].items():
            category_dir = self.config['crop_organization'][f'{category}_dir']
            
            for subcategory in subcategories:
                subcategory_dir = os.path.join(category_dir, subcategory)
                os.makedirs(subcategory_dir, exist_ok=True)
                
                # Create data type directories within each subcategory
                for data_type in self.config['crop_organization']['data_types']:
                    data_type_dir = os.path.join(subcategory_dir, data_type)
                    os.makedirs(data_type_dir, exist_ok=True)
        
        # Create keyword directories for each category
        for category in self.config['crop_organization']['subcategories'].keys():
            keyword_dir = os.path.join(self.config['crop_organization']['keywords_dir'], category)
            os.makedirs(keyword_dir, exist_ok=True)
        
        # Create reference dataset directories
        for category in self.config['crop_organization']['subcategories'].keys():
            reference_dir = os.path.join(self.config['crop_organization']['reference_dir'], category)
            os.makedirs(reference_dir, exist_ok=True)
    
    def _load_crop_categories(self) -> Dict[str, Any]:
        """
        Load crop categories from file.
        If file doesn't exist, create it with default categories.
        
        Returns:
            Dictionary with crop categories
        """
        categories_file = self.config['crop_organization']['categories_file']
        
        if os.path.exists(categories_file):
            try:
                with open(categories_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading crop categories: {e}")
        
        # Create default categories
        default_categories = {
            'vegetables': {
                'leafy_vegetables': [
                    'Spinach', 'Lettuce', 'Kale', 'Cabbage', 'Swiss Chard', 'Collard Greens'
                ],
                'root_vegetables': [
                    'Carrot', 'Radish', 'Turnip', 'Beetroot', 'Sweet Potato', 'Potato'
                ],
                'fruit_vegetables': [
                    'Tomato', 'Eggplant', 'Pepper', 'Cucumber', 'Zucchini', 'Pumpkin'
                ],
                'bulb_vegetables': [
                    'Onion', 'Garlic', 'Leek', 'Shallot', 'Fennel'
                ],
                'stem_vegetables': [
                    'Celery', 'Asparagus', 'Rhubarb', 'Kohlrabi'
                ],
                'flower_vegetables': [
                    'Broccoli', 'Cauliflower', 'Artichoke', 'Brussels Sprouts'
                ]
            },
            'fruits': {
                'tropical_fruits': [
                    'Banana', 'Mango', 'Pineapple', 'Papaya', 'Avocado', 'Coconut'
                ],
                'citrus_fruits': [
                    'Orange', 'Lemon', 'Lime', 'Grapefruit', 'Mandarin', 'Tangerine'
                ],
                'stone_fruits': [
                    'Peach', 'Plum', 'Cherry', 'Apricot', 'Nectarine'
                ],
                'pome_fruits': [
                    'Apple', 'Pear', 'Quince'
                ],
                'berries': [
                    'Strawberry', 'Blueberry', 'Raspberry', 'Blackberry', 'Cranberry', 'Grape'
                ],
                'melons': [
                    'Watermelon', 'Cantaloupe', 'Honeydew', 'Casaba'
                ]
            },
            'crops': {
                'cereals': [
                    'Wheat', 'Rice', 'Corn', 'Barley', 'Oats', 'Rye', 'Sorghum', 'Millet'
                ],
                'legumes': [
                    'Soybean', 'Peanut', 'Chickpea', 'Lentil', 'Bean', 'Pea'
                ],
                'oilseeds': [
                    'Sunflower', 'Rapeseed', 'Flaxseed', 'Sesame', 'Mustard'
                ],
                'fiber_crops': [
                    'Cotton', 'Jute', 'Hemp', 'Flax', 'Sisal'
                ],
                'sugar_crops': [
                    'Sugarcane', 'Sugar Beet'
                ],
                'forage_crops': [
                    'Alfalfa', 'Clover', 'Timothy', 'Ryegrass'
                ]
            }
        }
        
        # Save default categories
        try:
            with open(categories_file, 'w', encoding='utf-8') as f:
                json.dump(default_categories, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving default crop categories: {e}")
        
        return default_categories
    
    def add_crop(self, user_info: Dict[str, Any], crop_name: str, category: str, 
                subcategory: str, properties: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Add a new crop to the system.
        
        Args:
            user_info: Information about the user
            crop_name: Name of the crop
            category: Main category (vegetables, fruits, crops)
            subcategory: Subcategory within the main category
            properties: Optional properties of the crop
            
        Returns:
            Dictionary with operation result
        """
        try:
            # Check if category is valid
            if category not in self.config['crop_organization']['subcategories']:
                return {
                    'success': False,
                    'error': f"Invalid category: {category}. Valid categories are: {list(self.config['crop_organization']['subcategories'].keys())}"
                }
            
            # Check if subcategory is valid
            if subcategory not in self.config['crop_organization']['subcategories'][category]:
                return {
                    'success': False,
                    'error': f"Invalid subcategory: {subcategory}. Valid subcategories for {category} are: {self.config['crop_organization']['subcategories'][category]}"
                }
            
            # Check if crop already exists
            if crop_name in self.crop_categories[category][subcategory]:
                return {
                    'success': False,
                    'error': f"Crop '{crop_name}' already exists in {category}/{subcategory}"
                }
            
            # Add crop to categories
            self.crop_categories[category][subcategory].append(crop_name)
            
            # Save updated categories
            with open(self.config['crop_organization']['categories_file'], 'w', encoding='utf-8') as f:
                json.dump(self.crop_categories, f, indent=2)
            
            # Create directories for the new crop
            crop_dir = os.path.join(
                self.config['crop_organization'][f'{category}_dir'],
                subcategory,
                'varieties',
                crop_name
            )
            os.makedirs(crop_dir, exist_ok=True)
            
            # Create data type directories for the crop
            for data_type in self.config['crop_organization']['data_types']:
                if data_type != 'varieties':  # Skip varieties as we're already in that directory
                    data_type_dir = os.path.join(crop_dir, data_type)
                    os.makedirs(data_type_dir, exist_ok=True)
            
            # Save crop properties if provided
            if properties:
                properties_file = os.path.join(crop_dir, 'properties.json')
                with open(properties_file, 'w', encoding='utf-8') as f:
                    json.dump(properties, f, indent=2)
            
            # Log the action
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="CROP_ORGANIZATION",
                    action="add_crop",
                    component="crop_organization",
                    user_info=user_info,
                    details={
                        "crop_name": crop_name,
                        "category": category,
                        "subcategory": subcategory
                    },
                    status="success"
                )
            
            return {
                'success': True,
                'message': f"Crop '{crop_name}' added successfully to {category}/{subcategory}",
                'crop_dir': crop_dir
            }
            
        except Exception as e:
            logger.error(f"Error adding crop: {e}")
            
            # Log the error
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="CROP_ORGANIZATION",
                    action="add_crop",
                    component="crop_organization",
                    user_info=user_info,
                    details={
                        "crop_name": crop_name,
                        "category": category,
                        "subcategory": subcategory,
                        "error": str(e)
                    },
                    status="error"
                )
            
            return {
                'success': False,
                'error': f"Error adding crop: {str(e)}"
            }
    
    def remove_crop(self, user_info: Dict[str, Any], crop_name: str, category: str, 
                   subcategory: str) -> Dict[str, Any]:
        """
        Remove a crop from the system.
        
        Args:
            user_info: Information about the user
            crop_name: Name of the crop
            category: Main category (vegetables, fruits, crops)
            subcategory: Subcategory within the main category
            
        Returns:
            Dictionary with operation result
        """
        try:
            # Check if category is valid
            if category not in self.config['crop_organization']['subcategories']:
                return {
                    'success': False,
                    'error': f"Invalid category: {category}. Valid categories are: {list(self.config['crop_organization']['subcategories'].keys())}"
                }
            
            # Check if subcategory is valid
            if subcategory not in self.config['crop_organization']['subcategories'][category]:
                return {
                    'success': False,
                    'error': f"Invalid subcategory: {subcategory}. Valid subcategories for {category} are: {self.config['crop_organization']['subcategories'][category]}"
                }
            
            # Check if crop exists
            if crop_name not in self.crop_categories[category][subcategory]:
                return {
                    'success': False,
                    'error': f"Crop '{crop_name}' not found in {category}/{subcategory}"
                }
            
            # Remove crop from categories
            self.crop_categories[category][subcategory].remove(crop_name)
            
            # Save updated categories
            with open(self.config['crop_organization']['categories_file'], 'w', encoding='utf-8') as f:
                json.dump(self.crop_categories, f, indent=2)
            
            # Get crop directory
            crop_dir = os.path.join(
                self.config['crop_organization'][f'{category}_dir'],
                subcategory,
                'varieties',
                crop_name
            )
            
            # Check if directory exists
            if os.path.exists(crop_dir):
                # Create backup before deletion
                backup_dir = os.path.join(
                    self.config['crop_organization']['data_dir'],
                    'backups',
                    'deleted_crops',
                    f"{category}_{subcategory}_{crop_name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
                )
                os.makedirs(os.path.dirname(backup_dir), exist_ok=True)
                
                # Copy files to backup
                shutil.copytree(crop_dir, backup_dir)
                
                # Remove crop directory
                shutil.rmtree(crop_dir)
            
            # Log the action
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="CROP_ORGANIZATION",
                    action="remove_crop",
                    component="crop_organization",
                    user_info=user_info,
                    details={
                        "crop_name": crop_name,
                        "category": category,
                        "subcategory": subcategory
                    },
                    status="success"
                )
            
            return {
                'success': True,
                'message': f"Crop '{crop_name}' removed successfully from {category}/{subcategory}"
            }
            
        except Exception as e:
            logger.error(f"Error removing crop: {e}")
            
            # Log the error
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="CROP_ORGANIZATION",
                    action="remove_crop",
                    component="crop_organization",
                    user_info=user_info,
                    details={
                        "crop_name": crop_name,
                        "category": category,
                        "subcategory": subcategory,
                        "error": str(e)
                    },
                    status="error"
                )
            
            return {
                'success': False,
                'error': f"Error removing crop: {str(e)}"
            }
    
    def get_crop_info(self, crop_name: str, category: Optional[str] = None, 
                     subcategory: Optional[str] = None) -> Dict[str, Any]:
        """
        Get information about a crop.
        
        Args:
            crop_name: Name of the crop
            category: Optional main category (vegetables, fruits, crops)
            subcategory: Optional subcategory within the main category
            
        Returns:
            Dictionary with crop information
        """
        try:
            # If category and subcategory are provided, look in specific location
            if category and subcategory:
                # Check if category is valid
                if category not in self.config['crop_organization']['subcategories']:
                    return {
                        'success': False,
                        'error': f"Invalid category: {category}. Valid categories are: {list(self.config['crop_organization']['subcategories'].keys())}"
                    }
                
                # Check if subcategory is valid
                if subcategory not in self.config['crop_organization']['subcategories'][category]:
                    return {
                        'success': False,
                        'error': f"Invalid subcategory: {subcategory}. Valid subcategories for {category} are: {self.config['crop_organization']['subcategories'][category]}"
                    }
                
                # Check if crop exists
                if crop_name not in self.crop_categories[category][subcategory]:
                    return {
                        'success': False,
                        'error': f"Crop '{crop_name}' not found in {category}/{subcategory}"
                    }
                
                # Get crop directory
                crop_dir = os.path.join(
                    self.config['crop_organization'][f'{category}_dir'],
                    subcategory,
                    'varieties',
                    crop_name
                )
                
                # Get crop properties
                properties_file = os.path.join(crop_dir, 'properties.json')
                properties = {}
                
                if os.path.exists(properties_file):
                    with open(properties_file, 'r', encoding='utf-8') as f:
                        properties = json.load(f)
                
                return {
                    'success': True,
                    'crop_name': crop_name,
                    'category': category,
                    'subcategory': subcategory,
                    'properties': properties,
                    'crop_dir': crop_dir
                }
            
            # If category and subcategory are not provided, search in all categories
            for cat in self.crop_categories:
                for subcat in self.crop_categories[cat]:
                    if crop_name in self.crop_categories[cat][subcat]:
                        # Found the crop
                        crop_dir = os.path.join(
                            self.config['crop_organization'][f'{cat}_dir'],
                            subcat,
                            'varieties',
                            crop_name
                        )
                        
                        # Get crop properties
                        properties_file = os.path.join(crop_dir, 'properties.json')
                        properties = {}
                        
                        if os.path.exists(properties_file):
                            with open(properties_file, 'r', encoding='utf-8') as f:
                                properties = json.load(f)
                        
                        return {
                            'success': True,
                            'crop_name': crop_name,
                            'category': cat,
                            'subcategory': subcat,
                            'properties': properties,
                            'crop_dir': crop_dir
                        }
            
            # Crop not found
            return {
                'success': False,
                'error': f"Crop '{crop_name}' not found in any category"
            }
            
        except Exception as e:
            logger.error(f"Error getting crop info: {e}")
            return {
                'success': False,
                'error': f"Error getting crop info: {str(e)}"
            }
    
    def update_crop_properties(self, user_info: Dict[str, Any], crop_name: str, 
                              properties: Dict[str, Any], category: Optional[str] = None, 
                              subcategory: Optional[str] = None) -> Dict[str, Any]:
        """
        Update properties of a crop.
        
        Args:
            user_info: Information about the user
            crop_name: Name of the crop
            properties: New properties to set
            category: Optional main category (vegetables, fruits, crops)
            subcategory: Optional subcategory within the main category
            
        Returns:
            Dictionary with operation result
        """
        try:
            # Get crop info
            crop_info = self.get_crop_info(crop_name, category, subcategory)
            
            if not crop_info.get('success', False):
                return crop_info
            
            # Get crop directory
            crop_dir = crop_info['crop_dir']
            
            # Get existing properties
            properties_file = os.path.join(crop_dir, 'properties.json')
            existing_properties = {}
            
            if os.path.exists(properties_file):
                with open(properties_file, 'r', encoding='utf-8') as f:
                    existing_properties = json.load(f)
            
            # Update properties
            existing_properties.update(properties)
            
            # Save updated properties
            with open(properties_file, 'w', encoding='utf-8') as f:
                json.dump(existing_properties, f, indent=2)
            
            # Log the action
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="CROP_ORGANIZATION",
                    action="update_crop_properties",
                    component="crop_organization",
                    user_info=user_info,
                    details={
                        "crop_name": crop_name,
                        "category": crop_info['category'],
                        "subcategory": crop_info['subcategory']
                    },
                    status="success"
                )
            
            return {
                'success': True,
                'message': f"Properties of crop '{crop_name}' updated successfully",
                'properties': existing_properties
            }
            
        except Exception as e:
            logger.error(f"Error updating crop properties: {e}")
            
            # Log the error
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="CROP_ORGANIZATION",
                    action="update_crop_properties",
                    component="crop_organization",
                    user_info=user_info,
                    details={
                        "crop_name": crop_name,
                        "error": str(e)
                    },
                    status="error"
                )
            
            return {
                'success': False,
                'error': f"Error updating crop properties: {str(e)}"
            }
    
    def list_crops(self, category: Optional[str] = None, 
                  subcategory: Optional[str] = None) -> Dict[str, Any]:
        """
        List crops in the system.
        
        Args:
            category: Optional main category (vegetables, fruits, crops)
            subcategory: Optional subcategory within the main category
            
        Returns:
            Dictionary with list of crops
        """
        try:
            result = {
                'success': True,
                'crops': {}
            }
            
            # If category is provided
            if category:
                # Check if category is valid
                if category not in self.config['crop_organization']['subcategories']:
                    return {
                        'success': False,
                        'error': f"Invalid category: {category}. Valid categories are: {list(self.config['crop_organization']['subcategories'].keys())}"
                    }
                
                # If subcategory is provided
                if subcategory:
                    # Check if subcategory is valid
                    if subcategory not in self.config['crop_organization']['subcategories'][category]:
                        return {
                            'success': False,
                            'error': f"Invalid subcategory: {subcategory}. Valid subcategories for {category} are: {self.config['crop_organization']['subcategories'][category]}"
                        }
                    
                    # List crops in specific subcategory
                    result['crops'] = {
                        category: {
                            subcategory: self.crop_categories[category][subcategory]
                        }
                    }
                else:
                    # List crops in all subcategories of the category
                    result['crops'] = {
                        category: self.crop_categories[category]
                    }
            else:
                # List all crops
                result['crops'] = self.crop_categories
            
            return result
            
        except Exception as e:
            logger.error(f"Error listing crops: {e}")
            return {
                'success': False,
                'error': f"Error listing crops: {str(e)}"
            }
    
    def add_crop_data(self, user_info: Dict[str, Any], crop_name: str, data_type: str, 
                     file_path: str, data_name: Optional[str] = None, 
                     metadata: Optional[Dict[str, Any]] = None,
                     category: Optional[str] = None, 
                     subcategory: Optional[str] = None) -> Dict[str, Any]:
        """
        Add data for a crop.
        
        Args:
            user_info: Information about the user
            crop_name: Name of the crop
            data_type: Type of data (images, diseases, nutrients, etc.)
            file_path: Path to the data file
            data_name: Optional name for the data
            metadata: Optional metadata for the data
            category: Optional main category (vegetables, fruits, crops)
            subcategory: Optional subcategory within the main category
            
        Returns:
            Dictionary with operation result
        """
        try:
            # Check if data type is valid
            if data_type not in self.config['crop_organization']['data_types']:
                return {
                    'success': False,
                    'error': f"Invalid data type: {data_type}. Valid data types are: {self.config['crop_organization']['data_types']}"
                }
            
            # Check if file exists
            if not os.path.exists(file_path):
                return {
                    'success': False,
                    'error': f"File not found: {file_path}"
                }
            
            # Get crop info
            crop_info = self.get_crop_info(crop_name, category, subcategory)
            
            if not crop_info.get('success', False):
                return crop_info
            
            # Get data directory
            if data_type == 'varieties':
                data_dir = crop_info['crop_dir']
            else:
                data_dir = os.path.join(crop_info['crop_dir'], data_type)
            
            # Create directory if it doesn't exist
            os.makedirs(data_dir, exist_ok=True)
            
            # Generate data name if not provided
            if not data_name:
                data_name = os.path.basename(file_path)
            
            # Generate unique filename
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{data_name.replace(' ', '_')}_{timestamp}{os.path.splitext(file_path)[1]}"
            
            # Destination path
            dest_path = os.path.join(data_dir, filename)
            
            # Copy file
            shutil.copy2(file_path, dest_path)
            
            # Save metadata if provided
            if metadata:
                metadata_file = os.path.join(data_dir, f"{os.path.splitext(filename)[0]}.json")
                
                # Add file information to metadata
                metadata['file_name'] = filename
                metadata['original_file'] = os.path.basename(file_path)
                metadata['added_by'] = user_info.get('username', 'unknown')
                metadata['added_at'] = datetime.datetime.now().isoformat()
                
                with open(metadata_file, 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, indent=2)
            
            # Log the action
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="CROP_ORGANIZATION",
                    action="add_crop_data",
                    component="crop_organization",
                    user_info=user_info,
                    details={
                        "crop_name": crop_name,
                        "category": crop_info['category'],
                        "subcategory": crop_info['subcategory'],
                        "data_type": data_type,
                        "data_name": data_name
                    },
                    status="success"
                )
            
            return {
                'success': True,
                'message': f"Data '{data_name}' added successfully to crop '{crop_name}'",
                'data_path': dest_path
            }
            
        except Exception as e:
            logger.error(f"Error adding crop data: {e}")
            
            # Log the error
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="CROP_ORGANIZATION",
                    action="add_crop_data",
                    component="crop_organization",
                    user_info=user_info,
                    details={
                        "crop_name": crop_name,
                        "data_type": data_type,
                        "error": str(e)
                    },
                    status="error"
                )
            
            return {
                'success': False,
                'error': f"Error adding crop data: {str(e)}"
            }
    
    def list_crop_data(self, crop_name: str, data_type: str, 
                      category: Optional[str] = None, 
                      subcategory: Optional[str] = None) -> Dict[str, Any]:
        """
        List data for a crop.
        
        Args:
            crop_name: Name of the crop
            data_type: Type of data (images, diseases, nutrients, etc.)
            category: Optional main category (vegetables, fruits, crops)
            subcategory: Optional subcategory within the main category
            
        Returns:
            Dictionary with list of data
        """
        try:
            # Check if data type is valid
            if data_type not in self.config['crop_organization']['data_types']:
                return {
                    'success': False,
                    'error': f"Invalid data type: {data_type}. Valid data types are: {self.config['crop_organization']['data_types']}"
                }
            
            # Get crop info
            crop_info = self.get_crop_info(crop_name, category, subcategory)
            
            if not crop_info.get('success', False):
                return crop_info
            
            # Get data directory
            if data_type == 'varieties':
                data_dir = crop_info['crop_dir']
            else:
                data_dir = os.path.join(crop_info['crop_dir'], data_type)
            
            # Check if directory exists
            if not os.path.exists(data_dir):
                return {
                    'success': True,
                    'data': []
                }
            
            # List files in directory
            files = []
            for filename in os.listdir(data_dir):
                file_path = os.path.join(data_dir, filename)
                
                # Skip directories and metadata files
                if os.path.isdir(file_path) or filename.endswith('.json'):
                    continue
                
                # Get file information
                file_info = {
                    'name': filename,
                    'path': file_path,
                    'size': os.path.getsize(file_path),
                    'modified': datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
                }
                
                # Check if metadata exists
                metadata_file = os.path.join(data_dir, f"{os.path.splitext(filename)[0]}.json")
                
                if os.path.exists(metadata_file):
                    with open(metadata_file, 'r', encoding='utf-8') as f:
                        file_info['metadata'] = json.load(f)
                
                files.append(file_info)
            
            return {
                'success': True,
                'data': files
            }
            
        except Exception as e:
            logger.error(f"Error listing crop data: {e}")
            return {
                'success': False,
                'error': f"Error listing crop data: {str(e)}"
            }
    
    def add_keyword(self, user_info: Dict[str, Any], keyword: str, category: str, 
                   description: Optional[str] = None, 
                   related_keywords: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Add a keyword for a category.
        
        Args:
            user_info: Information about the user
            keyword: Keyword to add
            category: Category for the keyword (vegetables, fruits, crops)
            description: Optional description of the keyword
            related_keywords: Optional list of related keywords
            
        Returns:
            Dictionary with operation result
        """
        try:
            # Check if category is valid
            if category not in self.config['crop_organization']['subcategories']:
                return {
                    'success': False,
                    'error': f"Invalid category: {category}. Valid categories are: {list(self.config['crop_organization']['subcategories'].keys())}"
                }
            
            # Get keywords directory
            keywords_dir = os.path.join(self.config['crop_organization']['keywords_dir'], category)
            
            # Create directory if it doesn't exist
            os.makedirs(keywords_dir, exist_ok=True)
            
            # Get keywords file
            keywords_file = os.path.join(keywords_dir, 'keywords.json')
            
            # Load existing keywords
            keywords = {}
            
            if os.path.exists(keywords_file):
                with open(keywords_file, 'r', encoding='utf-8') as f:
                    keywords = json.load(f)
            
            # Check if keyword already exists
            if keyword in keywords:
                return {
                    'success': False,
                    'error': f"Keyword '{keyword}' already exists for category '{category}'"
                }
            
            # Add keyword
            keywords[keyword] = {
                'description': description or '',
                'related_keywords': related_keywords or [],
                'added_by': user_info.get('username', 'unknown'),
                'added_at': datetime.datetime.now().isoformat()
            }
            
            # Save updated keywords
            with open(keywords_file, 'w', encoding='utf-8') as f:
                json.dump(keywords, f, indent=2)
            
            # Log the action
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="CROP_ORGANIZATION",
                    action="add_keyword",
                    component="crop_organization",
                    user_info=user_info,
                    details={
                        "keyword": keyword,
                        "category": category
                    },
                    status="success"
                )
            
            return {
                'success': True,
                'message': f"Keyword '{keyword}' added successfully to category '{category}'"
            }
            
        except Exception as e:
            logger.error(f"Error adding keyword: {e}")
            
            # Log the error
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="CROP_ORGANIZATION",
                    action="add_keyword",
                    component="crop_organization",
                    user_info=user_info,
                    details={
                        "keyword": keyword,
                        "category": category,
                        "error": str(e)
                    },
                    status="error"
                )
            
            return {
                'success': False,
                'error': f"Error adding keyword: {str(e)}"
            }
    
    def list_keywords(self, category: Optional[str] = None) -> Dict[str, Any]:
        """
        List keywords for a category or all categories.
        
        Args:
            category: Optional category (vegetables, fruits, crops)
            
        Returns:
            Dictionary with list of keywords
        """
        try:
            result = {
                'success': True,
                'keywords': {}
            }
            
            # If category is provided
            if category:
                # Check if category is valid
                if category not in self.config['crop_organization']['subcategories']:
                    return {
                        'success': False,
                        'error': f"Invalid category: {category}. Valid categories are: {list(self.config['crop_organization']['subcategories'].keys())}"
                    }
                
                # Get keywords file
                keywords_file = os.path.join(
                    self.config['crop_organization']['keywords_dir'],
                    category,
                    'keywords.json'
                )
                
                # Load keywords
                if os.path.exists(keywords_file):
                    with open(keywords_file, 'r', encoding='utf-8') as f:
                        result['keywords'][category] = json.load(f)
                else:
                    result['keywords'][category] = {}
            else:
                # List keywords for all categories
                for cat in self.config['crop_organization']['subcategories']:
                    # Get keywords file
                    keywords_file = os.path.join(
                        self.config['crop_organization']['keywords_dir'],
                        cat,
                        'keywords.json'
                    )
                    
                    # Load keywords
                    if os.path.exists(keywords_file):
                        with open(keywords_file, 'r', encoding='utf-8') as f:
                            result['keywords'][cat] = json.load(f)
                    else:
                        result['keywords'][cat] = {}
            
            return result
            
        except Exception as e:
            logger.error(f"Error listing keywords: {e}")
            return {
                'success': False,
                'error': f"Error listing keywords: {str(e)}"
            }
    
    def add_reference_dataset(self, user_info: Dict[str, Any], dataset_name: str, 
                             category: str, file_path: str, 
                             description: Optional[str] = None,
                             metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Add a reference dataset for a category.
        
        Args:
            user_info: Information about the user
            dataset_name: Name of the dataset
            category: Category for the dataset (vegetables, fruits, crops)
            file_path: Path to the dataset file
            description: Optional description of the dataset
            metadata: Optional metadata for the dataset
            
        Returns:
            Dictionary with operation result
        """
        try:
            # Check if category is valid
            if category not in self.config['crop_organization']['subcategories']:
                return {
                    'success': False,
                    'error': f"Invalid category: {category}. Valid categories are: {list(self.config['crop_organization']['subcategories'].keys())}"
                }
            
            # Check if file exists
            if not os.path.exists(file_path):
                return {
                    'success': False,
                    'error': f"File not found: {file_path}"
                }
            
            # Get reference directory
            reference_dir = os.path.join(self.config['crop_organization']['reference_dir'], category)
            
            # Create directory if it doesn't exist
            os.makedirs(reference_dir, exist_ok=True)
            
            # Generate unique filename
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{dataset_name.replace(' ', '_')}_{timestamp}{os.path.splitext(file_path)[1]}"
            
            # Destination path
            dest_path = os.path.join(reference_dir, filename)
            
            # Copy file
            shutil.copy2(file_path, dest_path)
            
            # Create metadata
            if not metadata:
                metadata = {}
            
            metadata.update({
                'dataset_name': dataset_name,
                'description': description or '',
                'original_file': os.path.basename(file_path),
                'added_by': user_info.get('username', 'unknown'),
                'added_at': datetime.datetime.now().isoformat()
            })
            
            # Save metadata
            metadata_file = os.path.join(reference_dir, f"{os.path.splitext(filename)[0]}.json")
            
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
            
            # Log the action
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="CROP_ORGANIZATION",
                    action="add_reference_dataset",
                    component="crop_organization",
                    user_info=user_info,
                    details={
                        "dataset_name": dataset_name,
                        "category": category
                    },
                    status="success"
                )
            
            return {
                'success': True,
                'message': f"Reference dataset '{dataset_name}' added successfully to category '{category}'",
                'dataset_path': dest_path
            }
            
        except Exception as e:
            logger.error(f"Error adding reference dataset: {e}")
            
            # Log the error
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="CROP_ORGANIZATION",
                    action="add_reference_dataset",
                    component="crop_organization",
                    user_info=user_info,
                    details={
                        "dataset_name": dataset_name,
                        "category": category,
                        "error": str(e)
                    },
                    status="error"
                )
            
            return {
                'success': False,
                'error': f"Error adding reference dataset: {str(e)}"
            }
    
    def list_reference_datasets(self, category: Optional[str] = None) -> Dict[str, Any]:
        """
        List reference datasets for a category or all categories.
        
        Args:
            category: Optional category (vegetables, fruits, crops)
            
        Returns:
            Dictionary with list of reference datasets
        """
        try:
            result = {
                'success': True,
                'datasets': {}
            }
            
            # If category is provided
            if category:
                # Check if category is valid
                if category not in self.config['crop_organization']['subcategories']:
                    return {
                        'success': False,
                        'error': f"Invalid category: {category}. Valid categories are: {list(self.config['crop_organization']['subcategories'].keys())}"
                    }
                
                # Get reference directory
                reference_dir = os.path.join(self.config['crop_organization']['reference_dir'], category)
                
                # Check if directory exists
                if not os.path.exists(reference_dir):
                    result['datasets'][category] = []
                else:
                    # List files in directory
                    datasets = []
                    for filename in os.listdir(reference_dir):
                        file_path = os.path.join(reference_dir, filename)
                        
                        # Skip directories and metadata files
                        if os.path.isdir(file_path) or filename.endswith('.json'):
                            continue
                        
                        # Get file information
                        file_info = {
                            'name': filename,
                            'path': file_path,
                            'size': os.path.getsize(file_path),
                            'modified': datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
                        }
                        
                        # Check if metadata exists
                        metadata_file = os.path.join(reference_dir, f"{os.path.splitext(filename)[0]}.json")
                        
                        if os.path.exists(metadata_file):
                            with open(metadata_file, 'r', encoding='utf-8') as f:
                                file_info['metadata'] = json.load(f)
                        
                        datasets.append(file_info)
                    
                    result['datasets'][category] = datasets
            else:
                # List datasets for all categories
                for cat in self.config['crop_organization']['subcategories']:
                    # Get reference directory
                    reference_dir = os.path.join(self.config['crop_organization']['reference_dir'], cat)
                    
                    # Check if directory exists
                    if not os.path.exists(reference_dir):
                        result['datasets'][cat] = []
                    else:
                        # List files in directory
                        datasets = []
                        for filename in os.listdir(reference_dir):
                            file_path = os.path.join(reference_dir, filename)
                            
                            # Skip directories and metadata files
                            if os.path.isdir(file_path) or filename.endswith('.json'):
                                continue
                            
                            # Get file information
                            file_info = {
                                'name': filename,
                                'path': file_path,
                                'size': os.path.getsize(file_path),
                                'modified': datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
                            }
                            
                            # Check if metadata exists
                            metadata_file = os.path.join(reference_dir, f"{os.path.splitext(filename)[0]}.json")
                            
                            if os.path.exists(metadata_file):
                                with open(metadata_file, 'r', encoding='utf-8') as f:
                                    file_info['metadata'] = json.load(f)
                            
                            datasets.append(file_info)
                        
                        result['datasets'][cat] = datasets
            
            return result
            
        except Exception as e:
            logger.error(f"Error listing reference datasets: {e}")
            return {
                'success': False,
                'error': f"Error listing reference datasets: {str(e)}"
            }
    
    def search_crops(self, query: str, category: Optional[str] = None, 
                    subcategory: Optional[str] = None) -> Dict[str, Any]:
        """
        Search for crops by name or properties.
        
        Args:
            query: Search query
            category: Optional main category (vegetables, fruits, crops)
            subcategory: Optional subcategory within the main category
            
        Returns:
            Dictionary with search results
        """
        try:
            query = query.lower()
            results = []
            
            # If category is provided
            if category:
                # Check if category is valid
                if category not in self.config['crop_organization']['subcategories']:
                    return {
                        'success': False,
                        'error': f"Invalid category: {category}. Valid categories are: {list(self.config['crop_organization']['subcategories'].keys())}"
                    }
                
                # If subcategory is provided
                if subcategory:
                    # Check if subcategory is valid
                    if subcategory not in self.config['crop_organization']['subcategories'][category]:
                        return {
                            'success': False,
                            'error': f"Invalid subcategory: {subcategory}. Valid subcategories for {category} are: {self.config['crop_organization']['subcategories'][category]}"
                        }
                    
                    # Search in specific subcategory
                    for crop in self.crop_categories[category][subcategory]:
                        if query in crop.lower():
                            # Get crop info
                            crop_info = self.get_crop_info(crop, category, subcategory)
                            
                            if crop_info.get('success', False):
                                results.append(crop_info)
                else:
                    # Search in all subcategories of the category
                    for subcat in self.crop_categories[category]:
                        for crop in self.crop_categories[category][subcat]:
                            if query in crop.lower():
                                # Get crop info
                                crop_info = self.get_crop_info(crop, category, subcat)
                                
                                if crop_info.get('success', False):
                                    results.append(crop_info)
            else:
                # Search in all categories
                for cat in self.crop_categories:
                    for subcat in self.crop_categories[cat]:
                        for crop in self.crop_categories[cat][subcat]:
                            if query in crop.lower():
                                # Get crop info
                                crop_info = self.get_crop_info(crop, cat, subcat)
                                
                                if crop_info.get('success', False):
                                    results.append(crop_info)
            
            return {
                'success': True,
                'query': query,
                'results': results
            }
            
        except Exception as e:
            logger.error(f"Error searching crops: {e}")
            return {
                'success': False,
                'error': f"Error searching crops: {str(e)}"
            }
    
    def search_keywords(self, query: str, category: Optional[str] = None) -> Dict[str, Any]:
        """
        Search for keywords.
        
        Args:
            query: Search query
            category: Optional category (vegetables, fruits, crops)
            
        Returns:
            Dictionary with search results
        """
        try:
            query = query.lower()
            results = {}
            
            # Get keywords
            keywords = self.list_keywords(category)
            
            if not keywords.get('success', False):
                return keywords
            
            # Search in keywords
            for cat, cat_keywords in keywords['keywords'].items():
                cat_results = []
                
                for keyword, info in cat_keywords.items():
                    if query in keyword.lower() or query in info.get('description', '').lower():
                        cat_results.append({
                            'keyword': keyword,
                            'info': info
                        })
                
                if cat_results:
                    results[cat] = cat_results
            
            return {
                'success': True,
                'query': query,
                'results': results
            }
            
        except Exception as e:
            logger.error(f"Error searching keywords: {e}")
            return {
                'success': False,
                'error': f"Error searching keywords: {str(e)}"
            }
