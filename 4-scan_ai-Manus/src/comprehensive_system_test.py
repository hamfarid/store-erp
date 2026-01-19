#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive System Test Suite

This module provides comprehensive testing for all components of the
Agricultural AI System, including database integration, authentication,
core modules, and all specialized features.

Author: Agricultural AI System Team
Date: April 27, 2025
"""

import os
import sys
import unittest
import json
import logging
from datetime import datetime
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import database components
from database.database_manager import DatabaseManager
from database.database_synchronizer import DatabaseSynchronizer
from database.migration_manager import MigrationManager
from database.database_monitor import DatabaseMonitor
from database.database_reporting import DatabaseReportingSystem
from database.database_integration import DatabaseIntegration

# Import authentication components
from auth.auth_manager import AuthManager
from auth.permission_manager import PermissionManager

# Import core modules
from disease_detection.detector import DiseaseDetector
from nutrient_analysis.analyzer import NutrientAnalyzer
from plant_breeding.predictor import BreedingPredictor
from treatment_recommendation.recommender import TreatmentRecommender
from treatment_recommendation.enhanced_recommender import EnhancedTreatmentRecommender

# Import data collection modules
from data_collection.web_scraper import WebScraper
from data_collection.image_search import ImageSearch
from data_collection.advanced_scraper import AdvancedScraper
from data_collection.source_verifier import SourceVerifier
from data_collection.comprehensive_search import ComprehensiveSearch

# Import learning modules
from continuous_learning.learning_manager import LearningManager

# Import management modules
from variety_comparison.variety_manager import VarietyManager
from nursery_management.nursery_manager import NurseryManager
from farm_management.farm_manager import FarmManager
from cost_management.cost_calculator import CostCalculator
from inventory_management.inventory_manager import InventoryManager
from financial_reporting.financial_reporting_system import FinancialReportingSystem
from organization.organization_manager import OrganizationManager
from crop_organization.crop_organization_manager import CropOrganizationManager
from trusted_sources.trusted_sources_manager import TrustedSourcesManager

# Import AI assistant
from ai_assistant.assistant_agent import AIAssistant

# Import utility modules
from utils.config_loader import ConfigLoader
from utils.logger_setup import setup_logger

# Set up logging
logger = setup_logger('system_test')

class DatabaseTests(unittest.TestCase):
    """Test cases for database components."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment for database tests."""
        load_dotenv()
        cls.config = ConfigLoader().load_config()
        
        # Use test database connections
        cls.operational_db = DatabaseManager(
            db_type='operational',
            connection_string=os.getenv('TEST_OPERATIONAL_DB_CONNECTION'),
            config=cls.config.get('databases', {}).get('operational', {})
        )
        
        cls.employee_training_db = DatabaseManager(
            db_type='employee_training',
            connection_string=os.getenv('TEST_EMPLOYEE_TRAINING_DB_CONNECTION'),
            config=cls.config.get('databases', {}).get('employee_training', {})
        )
        
        cls.system_training_db = DatabaseManager(
            db_type='system_training',
            connection_string=os.getenv('TEST_SYSTEM_TRAINING_DB_CONNECTION'),
            config=cls.config.get('databases', {}).get('system_training', {})
        )
        
        cls.backup_db = DatabaseManager(
            db_type='backup',
            connection_string=os.getenv('TEST_BACKUP_DB_CONNECTION'),
            config=cls.config.get('databases', {}).get('backup', {})
        )
    
    def test_database_connections(self):
        """Test database connections."""
        self.assertTrue(self.operational_db.test_connection())
        self.assertTrue(self.employee_training_db.test_connection())
        self.assertTrue(self.system_training_db.test_connection())
        self.assertTrue(self.backup_db.test_connection())
    
    def test_database_synchronization(self):
        """Test database synchronization."""
        synchronizer = DatabaseSynchronizer(
            source_dbs=[self.operational_db, self.employee_training_db, self.system_training_db],
            target_db=self.backup_db,
            config=self.config.get('synchronization', {})
        )
        self.assertTrue(synchronizer.test_synchronization())
    
    def test_database_migration(self):
        """Test database migration."""
        migration_manager = MigrationManager(
            databases=[self.operational_db, self.employee_training_db, 
                      self.system_training_db, self.backup_db],
            config=self.config.get('migration', {})
        )
        self.assertTrue(migration_manager.verify_schema_versions())
    
    def test_database_monitoring(self):
        """Test database monitoring."""
        monitor = DatabaseMonitor(
            databases=[self.operational_db, self.employee_training_db, 
                      self.system_training_db, self.backup_db],
            config=self.config.get('monitoring', {})
        )
        self.assertTrue(monitor.check_monitoring_status())
    
    def test_database_reporting(self):
        """Test database reporting."""
        reporting = DatabaseReportingSystem(
            databases=[self.operational_db, self.employee_training_db, 
                      self.system_training_db, self.backup_db],
            config=self.config.get('reporting', {})
        )
        self.assertIsNotNone(reporting.generate_database_status_report())
    
    def test_database_integration(self):
        """Test database integration."""
        integrator = DatabaseIntegration()
        self.assertTrue(integrator.initialize_all_integrations())


class AuthenticationTests(unittest.TestCase):
    """Test cases for authentication components."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment for authentication tests."""
        load_dotenv()
        cls.config = ConfigLoader().load_config()
        
        # Use test database connection
        cls.db = DatabaseManager(
            db_type='operational',
            connection_string=os.getenv('TEST_OPERATIONAL_DB_CONNECTION'),
            config=cls.config.get('databases', {}).get('operational', {})
        )
        
        # Initialize auth manager
        cls.auth_manager = AuthManager()
        cls.auth_manager.set_database(cls.db)
        
        # Initialize permission manager
        cls.permission_manager = PermissionManager()
        cls.permission_manager.set_database(cls.db)
        
        # Initialize organization manager
        cls.org_manager = OrganizationManager()
        cls.org_manager.set_database(cls.db)
        
        # Test user credentials
        cls.test_username = "test_admin"
        cls.test_password = "Test@123"
        cls.test_country = "Test Country"
        cls.test_company = "Test Company"
    
    def test_user_creation(self):
        """Test user creation."""
        user_id = self.auth_manager.create_user(
            username=self.test_username,
            password=self.test_password,
            role="admin",
            email="test@example.com",
            full_name="Test Admin"
        )
        self.assertIsNotNone(user_id)
    
    def test_user_authentication(self):
        """Test user authentication."""
        auth_result = self.auth_manager.authenticate(
            username=self.test_username,
            password=self.test_password
        )
        self.assertTrue(auth_result['success'])
    
    def test_permission_assignment(self):
        """Test permission assignment."""
        permission_result = self.permission_manager.assign_permission(
            user_id=self.test_username,
            module="disease_detection",
            permission_level="read_write"
        )
        self.assertTrue(permission_result)
    
    def test_permission_verification(self):
        """Test permission verification."""
        has_permission = self.permission_manager.check_permission(
            user_id=self.test_username,
            module="disease_detection",
            required_level="read"
        )
        self.assertTrue(has_permission)
    
    def test_organization_management(self):
        """Test organization management."""
        # Add country
        country_id = self.org_manager.add_country(self.test_country)
        self.assertIsNotNone(country_id)
        
        # Add company
        company_id = self.org_manager.add_company(
            country_id=country_id,
            company_name=self.test_company
        )
        self.assertIsNotNone(company_id)
        
        # Assign user to company
        assignment = self.org_manager.assign_user_to_company(
            user_id=self.test_username,
            company_id=company_id
        )
        self.assertTrue(assignment)
        
        # Verify user's company
        user_company = self.org_manager.get_user_company(self.test_username)
        self.assertEqual(user_company['name'], self.test_company)


class CoreModulesTests(unittest.TestCase):
    """Test cases for core system modules."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment for core modules tests."""
        load_dotenv()
        cls.config = ConfigLoader().load_config()
        
        # Use test database connections
        cls.operational_db = DatabaseManager(
            db_type='operational',
            connection_string=os.getenv('TEST_OPERATIONAL_DB_CONNECTION'),
            config=cls.config.get('databases', {}).get('operational', {})
        )
        
        cls.system_training_db = DatabaseManager(
            db_type='system_training',
            connection_string=os.getenv('TEST_SYSTEM_TRAINING_DB_CONNECTION'),
            config=cls.config.get('databases', {}).get('system_training', {})
        )
        
        # Initialize core modules
        cls.disease_detector = DiseaseDetector()
        cls.disease_detector.set_operational_db(cls.operational_db)
        cls.disease_detector.set_training_db(cls.system_training_db)
        
        cls.nutrient_analyzer = NutrientAnalyzer()
        cls.nutrient_analyzer.set_operational_db(cls.operational_db)
        cls.nutrient_analyzer.set_training_db(cls.system_training_db)
        
        cls.breeding_predictor = BreedingPredictor()
        cls.breeding_predictor.set_operational_db(cls.operational_db)
        cls.breeding_predictor.set_training_db(cls.system_training_db)
        
        cls.treatment_recommender = TreatmentRecommender()
        cls.treatment_recommender.set_operational_db(cls.operational_db)
        cls.treatment_recommender.set_training_db(cls.system_training_db)
        
        cls.enhanced_recommender = EnhancedTreatmentRecommender()
        cls.enhanced_recommender.set_operational_db(cls.operational_db)
        cls.enhanced_recommender.set_training_db(cls.system_training_db)
    
    def test_disease_detection(self):
        """Test disease detection module."""
        # Mock image path for testing
        test_image_path = os.path.join(os.path.dirname(__file__), "test_data", "test_plant.jpg")
        
        # Create test directory if it doesn't exist
        os.makedirs(os.path.join(os.path.dirname(__file__), "test_data"), exist_ok=True)
        
        # Create a simple test image if it doesn't exist
        if not os.path.exists(test_image_path):
            try:
                import numpy as np
                from PIL import Image
                
                # Create a simple green image (representing a plant)
                img_array = np.zeros((100, 100, 3), dtype=np.uint8)
                img_array[:, :, 1] = 255  # Green channel
                
                # Add some brown spots (representing disease)
                for i in range(10):
                    x = np.random.randint(0, 100)
                    y = np.random.randint(0, 100)
                    img_array[max(0, x-5):min(100, x+5), max(0, y-5):min(100, y+5), 0] = 165  # Brown color
                    img_array[max(0, x-5):min(100, x+5), max(0, y-5):min(100, y+5), 1] = 42
                    img_array[max(0, x-5):min(100, x+5), max(0, y-5):min(100, y+5), 2] = 42
                
                img = Image.fromarray(img_array)
                img.save(test_image_path)
            except ImportError:
                # If PIL is not available, create an empty file
                with open(test_image_path, 'w') as f:
                    f.write("Test image placeholder")
        
        # Test disease detection
        detection_result = self.disease_detector.detect_disease(test_image_path)
        self.assertIsNotNone(detection_result)
        self.assertIn('diseases', detection_result)
    
    def test_nutrient_analysis(self):
        """Test nutrient analysis module."""
        # Mock image path for testing
        test_image_path = os.path.join(os.path.dirname(__file__), "test_data", "test_plant.jpg")
        
        # Test nutrient analysis
        analysis_result = self.nutrient_analyzer.analyze_nutrients(test_image_path)
        self.assertIsNotNone(analysis_result)
        self.assertIn('deficiencies', analysis_result)
    
    def test_breeding_prediction(self):
        """Test breeding prediction module."""
        # Test data
        parent1 = {
            "variety": "Test Variety 1",
            "traits": {
                "yield": 8.5,
                "disease_resistance": 7.0,
                "drought_tolerance": 6.5
            }
        }
        
        parent2 = {
            "variety": "Test Variety 2",
            "traits": {
                "yield": 7.0,
                "disease_resistance": 8.5,
                "drought_tolerance": 7.5
            }
        }
        
        # Test breeding prediction
        prediction_result = self.breeding_predictor.predict_offspring(parent1, parent2)
        self.assertIsNotNone(prediction_result)
        self.assertIn('offspring_traits', prediction_result)
    
    def test_treatment_recommendation(self):
        """Test treatment recommendation module."""
        # Test data
        disease_info = {
            "name": "Test Disease",
            "severity": 7.5,
            "affected_area": 0.65
        }
        
        # Test treatment recommendation
        recommendation = self.treatment_recommender.recommend_treatment(disease_info)
        self.assertIsNotNone(recommendation)
        self.assertIn('treatments', recommendation)
    
    def test_enhanced_treatment_recommendation(self):
        """Test enhanced treatment recommendation module."""
        # Test data
        disease_info = {
            "name": "Test Disease",
            "severity": 7.5,
            "affected_area": 0.65
        }
        
        # Test enhanced treatment recommendation
        enhanced_recommendation = self.enhanced_recommender.recommend_treatment(disease_info)
        self.assertIsNotNone(enhanced_recommendation)
        self.assertIn('treatments', enhanced_recommendation)
        self.assertIn('dosages', enhanced_recommendation)


class ManagementModulesTests(unittest.TestCase):
    """Test cases for management modules."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment for management modules tests."""
        load_dotenv()
        cls.config = ConfigLoader().load_config()
        
        # Use test database connection
        cls.db = DatabaseManager(
            db_type='operational',
            connection_string=os.getenv('TEST_OPERATIONAL_DB_CONNECTION'),
            config=cls.config.get('databases', {}).get('operational', {})
        )
        
        # Initialize management modules
        cls.variety_manager = VarietyManager()
        cls.variety_manager.set_database(cls.db)
        
        cls.nursery_manager = NurseryManager()
        cls.nursery_manager.set_database(cls.db)
        
        cls.farm_manager = FarmManager()
        cls.farm_manager.set_database(cls.db)
        
        cls.cost_calculator = CostCalculator()
        cls.cost_calculator.set_database(cls.db)
        
        cls.inventory_manager = InventoryManager()
        cls.inventory_manager.set_database(cls.db)
        
        cls.financial_reporting = FinancialReportingSystem()
        cls.financial_reporting.set_database(cls.db)
        
        cls.crop_organization = CropOrganizationManager()
        cls.crop_organization.set_database(cls.db)
    
    def test_variety_comparison(self):
        """Test variety comparison module."""
        # Test data
        variety1 = {
            "name": "Test Variety 1",
            "type": "Tomato",
            "attributes": {
                "fruit_color": "Red",
                "fruit_size": "Large",
                "fruit_shape": "Round",
                "disease_resistance": 8.0,
                "yield": 7.5
            }
        }
        
        variety2 = {
            "name": "Test Variety 2",
            "type": "Tomato",
            "attributes": {
                "fruit_color": "Red",
                "fruit_size": "Medium",
                "fruit_shape": "Oval",
                "disease_resistance": 7.0,
                "yield": 8.5
            }
        }
        
        # Add varieties
        variety1_id = self.variety_manager.add_variety(variety1)
        variety2_id = self.variety_manager.add_variety(variety2)
        
        self.assertIsNotNone(variety1_id)
        self.assertIsNotNone(variety2_id)
        
        # Compare varieties
        comparison = self.variety_manager.compare_varieties([variety1_id, variety2_id])
        self.assertIsNotNone(comparison)
        self.assertIn('comparison_results', comparison)
    
    def test_nursery_management(self):
        """Test nursery management module."""
        # Test data
        nursery = {
            "name": "Test Nursery",
            "location": "Test Location",
            "capacity": 1000
        }
        
        seedling_type = {
            "name": "Test Seedling",
            "crop_type": "Tomato",
            "growth_duration_days": 30,
            "season": "Summer"
        }
        
        # Add nursery
        nursery_id = self.nursery_manager.add_nursery(nursery)
        self.assertIsNotNone(nursery_id)
        
        # Add seedling type
        seedling_type_id = self.nursery_manager.add_seedling_type(seedling_type)
        self.assertIsNotNone(seedling_type_id)
        
        # Book seedlings
        booking = {
            "customer_name": "Test Customer",
            "seedling_type_id": seedling_type_id,
            "quantity": 100,
            "booking_date": datetime.now().isoformat(),
            "delivery_date": datetime.now().isoformat()
        }
        
        booking_id = self.nursery_manager.book_seedlings(nursery_id, booking)
        self.assertIsNotNone(booking_id)
        
        # Check nursery capacity
        capacity_info = self.nursery_manager.get_nursery_capacity(nursery_id)
        self.assertIsNotNone(capacity_info)
        self.assertEqual(capacity_info['available_capacity'], 900)
    
    def test_farm_management(self):
        """Test farm management module."""
        # Test data
        farm = {
            "name": "Test Farm",
            "location": "Test Location",
            "total_area": 100.0,  # hectares
            "owner": "Test Owner"
        }
        
        crop = {
            "name": "Test Crop",
            "variety": "Test Variety",
            "planting_date": datetime.now().isoformat(),
            "expected_harvest_dates": [
                (datetime.now().isoformat(), 0.7),  # 70% harvest
                (datetime.now().isoformat(), 0.3)   # 30% harvest
            ],
            "area": 10.0,  # hectares
            "plants_count": 1000
        }
        
        # Add farm
        farm_id = self.farm_manager.add_farm(farm)
        self.assertIsNotNone(farm_id)
        
        # Add crop to farm
        crop_id = self.farm_manager.add_crop(farm_id, crop)
        self.assertIsNotNone(crop_id)
        
        # Get farm details
        farm_details = self.farm_manager.get_farm_details(farm_id)
        self.assertIsNotNone(farm_details)
        self.assertEqual(farm_details['name'], farm['name'])
        self.assertEqual(len(farm_details['crops']), 1)
    
    def test_cost_calculation(self):
        """Test cost calculation module."""
        # Test data
        cost_items = [
            {
                "category": "Seeds",
                "name": "Test Seeds",
                "quantity": 10,
                "unit_price": 5.0,
                "unit": "kg"
            },
            {
                "category": "Fertilizer",
                "name": "Test Fertilizer",
                "quantity": 50,
                "unit_price": 2.0,
                "unit": "kg"
            },
            {
                "category": "Pesticide",
                "name": "Test Pesticide",
                "quantity": 5,
                "unit_price": 10.0,
                "unit": "liter"
            },
            {
                "category": "Labor",
                "name": "Planting",
                "quantity": 20,
                "unit_price": 15.0,
                "unit": "hour"
            }
        ]
        
        # Calculate costs
        cost_summary = self.cost_calculator.calculate_costs(cost_items, area=10.0)
        self.assertIsNotNone(cost_summary)
        self.assertIn('total_cost', cost_summary)
        self.assertIn('cost_per_hectare', cost_summary)
        self.assertIn('cost_breakdown', cost_summary)
    
    def test_inventory_management(self):
        """Test inventory management module."""
        # Test data
        items = [
            {
                "category": "Fertilizer",
                "name": "Test Fertilizer",
                "quantity": 100,
                "unit": "kg",
                "unit_price": 2.0,
                "location": "Warehouse A"
            },
            {
                "category": "Pesticide",
                "name": "Test Pesticide",
                "quantity": 50,
                "unit": "liter",
                "unit_price": 10.0,
                "location": "Warehouse B"
            }
        ]
        
        # Add items to inventory
        for item in items:
            item_id = self.inventory_manager.add_item(item)
            self.assertIsNotNone(item_id)
        
        # Check inventory
        inventory = self.inventory_manager.get_inventory()
        self.assertIsNotNone(inventory)
        self.assertEqual(len(inventory), 2)
        
        # Update item quantity
        update_result = self.inventory_manager.update_item_quantity(
            category="Fertilizer",
            name="Test Fertilizer",
            quantity_change=-20,
            reason="Used in Farm A"
        )
        self.assertTrue(update_result)
        
        # Check updated inventory
        updated_item = self.inventory_manager.get_item(
            category="Fertilizer",
            name="Test Fertilizer"
        )
        self.assertIsNotNone(updated_item)
        self.assertEqual(updated_item['quantity'], 80)
    
    def test_financial_reporting(self):
        """Test financial reporting module."""
        # Test data
        expenses = [
            {
                "category": "Seeds",
                "amount": 500.0,
                "date": datetime.now().isoformat(),
                "description": "Test Seeds"
            },
            {
                "category": "Fertilizer",
                "amount": 1000.0,
                "date": datetime.now().isoformat(),
                "description": "Test Fertilizer"
            },
            {
                "category": "Labor",
                "amount": 2000.0,
                "date": datetime.now().isoformat(),
                "description": "Planting and Maintenance"
            }
        ]
        
        income = [
            {
                "category": "Crop Sales",
                "amount": 5000.0,
                "date": datetime.now().isoformat(),
                "description": "Test Crop Sales"
            }
        ]
        
        # Add financial data
        for expense in expenses:
            expense_id = self.financial_reporting.add_expense(expense)
            self.assertIsNotNone(expense_id)
        
        for inc in income:
            income_id = self.financial_reporting.add_income(inc)
            self.assertIsNotNone(income_id)
        
        # Generate financial report
        report = self.financial_reporting.generate_financial_report()
        self.assertIsNotNone(report)
        self.assertIn('total_expenses', report)
        self.assertIn('total_income', report)
        self.assertIn('profit', report)
        self.assertEqual(report['total_expenses'], 3500.0)
        self.assertEqual(report['total_income'], 5000.0)
        self.assertEqual(report['profit'], 1500.0)
    
    def test_crop_organization(self):
        """Test crop organization module."""
        # Test data
        vegetable = {
            "name": "Test Vegetable",
            "scientific_name": "Testus vegetablus",
            "description": "A test vegetable"
        }
        
        fruit = {
            "name": "Test Fruit",
            "scientific_name": "Testus fruitus",
            "description": "A test fruit"
        }
        
        crop = {
            "name": "Test Crop",
            "scientific_name": "Testus cropus",
            "description": "A test crop"
        }
        
        # Add crops to respective categories
        vegetable_id = self.crop_organization.add_vegetable(vegetable)
        fruit_id = self.crop_organization.add_fruit(fruit)
        crop_id = self.crop_organization.add_crop(crop)
        
        self.assertIsNotNone(vegetable_id)
        self.assertIsNotNone(fruit_id)
        self.assertIsNotNone(crop_id)
        
        # Get crops by category
        vegetables = self.crop_organization.get_vegetables()
        fruits = self.crop_organization.get_fruits()
        crops = self.crop_organization.get_crops()
        
        self.assertEqual(len(vegetables), 1)
        self.assertEqual(len(fruits), 1)
        self.assertEqual(len(crops), 1)


class AIAssistantTests(unittest.TestCase):
    """Test cases for AI assistant."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment for AI assistant tests."""
        load_dotenv()
        cls.config = ConfigLoader().load_config()
        
        # Use test database connections
        cls.operational_db = DatabaseManager(
            db_type='operational',
            connection_string=os.getenv('TEST_OPERATIONAL_DB_CONNECTION'),
            config=cls.config.get('databases', {}).get('operational', {})
        )
        
        cls.system_training_db = DatabaseManager(
            db_type='system_training',
            connection_string=os.getenv('TEST_SYSTEM_TRAINING_DB_CONNECTION'),
            config=cls.config.get('databases', {}).get('system_training', {})
        )
        
        # Initialize AI assistant
        cls.ai_assistant = AIAssistant()
        cls.ai_assistant.set_operational_db(cls.operational_db)
        cls.ai_assistant.set_training_db(cls.system_training_db)
    
    def test_free_assistant(self):
        """Test free AI assistant."""
        # Test query
        query = "What are common tomato diseases?"
        
        # Get response from free assistant
        response = self.ai_assistant.get_free_assistant_response(query)
        self.assertIsNotNone(response)
        self.assertIn('answer', response)
    
    def test_premium_assistant(self):
        """Test premium AI assistant."""
        # Test query
        query = "How to treat tomato blight?"
        
        # Get response from premium assistant
        response = self.ai_assistant.get_premium_assistant_response(
            query=query,
            user_id="test_admin",
            api_key=os.getenv('TEST_PREMIUM_API_KEY')
        )
        self.assertIsNotNone(response)
        self.assertIn('answer', response)
        self.assertIn('references', response)
    
    def test_file_operations(self):
        """Test file operations with AI assistant."""
        # Test file path
        test_file_path = os.path.join(os.path.dirname(__file__), "test_data", "test_file.txt")
        
        # Create test directory if it doesn't exist
        os.makedirs(os.path.join(os.path.dirname(__file__), "test_data"), exist_ok=True)
        
        # Create a test file
        with open(test_file_path, 'w') as f:
            f.write("This is a test file for AI assistant file operations.")
        
        # Upload file
        upload_result = self.ai_assistant.upload_file(
            file_path=test_file_path,
            user_id="test_admin",
            api_key=os.getenv('TEST_PREMIUM_API_KEY')
        )
        self.assertTrue(upload_result['success'])
        self.assertIn('file_id', upload_result)
        
        file_id = upload_result['file_id']
        
        # Download file
        download_path = os.path.join(os.path.dirname(__file__), "test_data", "downloaded_file.txt")
        download_result = self.ai_assistant.download_file(
            file_id=file_id,
            download_path=download_path,
            user_id="test_admin",
            api_key=os.getenv('TEST_PREMIUM_API_KEY')
        )
        self.assertTrue(download_result['success'])
        
        # Verify downloaded file
        self.assertTrue(os.path.exists(download_path))
        with open(download_path, 'r') as f:
            content = f.read()
        self.assertEqual(content, "This is a test file for AI assistant file operations.")


class IntegrationTests(unittest.TestCase):
    """Test cases for system integration."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment for integration tests."""
        load_dotenv()
        cls.config = ConfigLoader().load_config()
        
        # Initialize database integration
        cls.db_integration = DatabaseIntegration()
        
        # Ensure all database integrations are initialized
        cls.db_integration.initialize_all_integrations()
    
    def test_end_to_end_disease_detection_workflow(self):
        """Test end-to-end disease detection workflow."""
        # Initialize components
        auth_manager = AuthManager()
        disease_detector = DiseaseDetector()
        treatment_recommender = EnhancedTreatmentRecommender()
        
        # Test user credentials
        test_username = "test_user"
        test_password = "Test@123"
        
        # Create test user
        user_id = auth_manager.create_user(
            username=test_username,
            password=test_password,
            role="user",
            email="testuser@example.com",
            full_name="Test User"
        )
        self.assertIsNotNone(user_id)
        
        # Authenticate user
        auth_result = auth_manager.authenticate(
            username=test_username,
            password=test_password
        )
        self.assertTrue(auth_result['success'])
        
        # Mock image path for testing
        test_image_path = os.path.join(os.path.dirname(__file__), "test_data", "test_plant.jpg")
        
        # Detect disease
        detection_result = disease_detector.detect_disease(test_image_path)
        self.assertIsNotNone(detection_result)
        self.assertIn('diseases', detection_result)
        
        # Get treatment recommendation
        if detection_result['diseases']:
            disease_info = detection_result['diseases'][0]
            recommendation = treatment_recommender.recommend_treatment(disease_info)
            self.assertIsNotNone(recommendation)
            self.assertIn('treatments', recommendation)
            self.assertIn('dosages', recommendation)
    
    def test_end_to_end_farm_management_workflow(self):
        """Test end-to-end farm management workflow."""
        # Initialize components
        auth_manager = AuthManager()
        farm_manager = FarmManager()
        cost_calculator = CostCalculator()
        inventory_manager = InventoryManager()
        financial_reporting = FinancialReportingSystem()
        
        # Test user credentials
        test_username = "test_farm_manager"
        test_password = "Test@123"
        
        # Create test user
        user_id = auth_manager.create_user(
            username=test_username,
            password=test_password,
            role="farm_manager",
            email="farmmanager@example.com",
            full_name="Test Farm Manager"
        )
        self.assertIsNotNone(user_id)
        
        # Authenticate user
        auth_result = auth_manager.authenticate(
            username=test_username,
            password=test_password
        )
        self.assertTrue(auth_result['success'])
        
        # Add farm
        farm = {
            "name": "Integration Test Farm",
            "location": "Test Location",
            "total_area": 50.0,  # hectares
            "owner": "Test Owner"
        }
        farm_id = farm_manager.add_farm(farm)
        self.assertIsNotNone(farm_id)
        
        # Add crop to farm
        crop = {
            "name": "Integration Test Crop",
            "variety": "Test Variety",
            "planting_date": datetime.now().isoformat(),
            "expected_harvest_dates": [
                (datetime.now().isoformat(), 1.0)
            ],
            "area": 10.0,  # hectares
            "plants_count": 5000
        }
        crop_id = farm_manager.add_crop(farm_id, crop)
        self.assertIsNotNone(crop_id)
        
        # Add items to inventory
        fertilizer = {
            "category": "Fertilizer",
            "name": "Integration Test Fertilizer",
            "quantity": 500,
            "unit": "kg",
            "unit_price": 2.0,
            "location": "Main Warehouse"
        }
        fertilizer_id = inventory_manager.add_item(fertilizer)
        self.assertIsNotNone(fertilizer_id)
        
        # Calculate costs
        cost_items = [
            {
                "category": "Seeds",
                "name": "Integration Test Seeds",
                "quantity": 50,
                "unit_price": 5.0,
                "unit": "kg"
            },
            {
                "category": "Fertilizer",
                "name": "Integration Test Fertilizer",
                "quantity": 200,
                "unit_price": 2.0,
                "unit": "kg"
            },
            {
                "category": "Labor",
                "name": "Planting",
                "quantity": 100,
                "unit_price": 15.0,
                "unit": "hour"
            }
        ]
        cost_summary = cost_calculator.calculate_costs(cost_items, area=10.0)
        self.assertIsNotNone(cost_summary)
        
        # Update inventory
        update_result = inventory_manager.update_item_quantity(
            category="Fertilizer",
            name="Integration Test Fertilizer",
            quantity_change=-200,
            reason=f"Used for crop {crop_id} in farm {farm_id}"
        )
        self.assertTrue(update_result)
        
        # Add expenses to financial system
        for item in cost_items:
            expense = {
                "category": item["category"],
                "amount": item["quantity"] * item["unit_price"],
                "date": datetime.now().isoformat(),
                "description": f"{item['name']} for crop {crop_id}"
            }
            expense_id = financial_reporting.add_expense(expense)
            self.assertIsNotNone(expense_id)
        
        # Generate financial report
        report = financial_reporting.generate_financial_report()
        self.assertIsNotNone(report)
        self.assertIn('total_expenses', report)
        
        # Get farm details
        farm_details = farm_manager.get_farm_details(farm_id)
        self.assertIsNotNone(farm_details)
        self.assertEqual(farm_details['name'], farm['name'])
        self.assertEqual(len(farm_details['crops']), 1)


def run_tests():
    """Run all tests."""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(DatabaseTests))
    test_suite.addTest(unittest.makeSuite(AuthenticationTests))
    test_suite.addTest(unittest.makeSuite(CoreModulesTests))
    test_suite.addTest(unittest.makeSuite(ManagementModulesTests))
    test_suite.addTest(unittest.makeSuite(AIAssistantTests))
    test_suite.addTest(unittest.makeSuite(IntegrationTests))
    
    # Run tests
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_result = test_runner.run(test_suite)
    
    # Return test result
    return test_result


if __name__ == "__main__":
    # Run tests
    result = run_tests()
    
    # Print summary
    print("\nTest Summary:")
    print(f"Ran {result.testsRun} tests")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    # Exit with appropriate code
    if result.wasSuccessful():
        print("\nAll tests passed successfully!")
        sys.exit(0)
    else:
        print("\nSome tests failed!")
        sys.exit(1)
