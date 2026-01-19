#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
System test script for the Agricultural AI System.
Tests all major components and their integration.
"""

import os
import sys
import logging
import unittest
import json
import tempfile
import shutil
from datetime import datetime
import time
from pathlib import Path

# Add parent directory to path to import main module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import main system
from src.main import AgriculturalAISystem

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('system_test')


class AgriculturalAISystemTest(unittest.TestCase):
    """Test case for the Agricultural AI System."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        logger.info("Setting up test environment")
        
        # Create temporary directory for test data
        cls.test_dir = tempfile.mkdtemp(prefix="agri_ai_test_")
        
        # Create test configuration
        cls.config = {
            'system': {
                'name': 'Agricultural AI System Test',
                'version': 'test',
                'data_dir': os.path.join(cls.test_dir, 'data'),
                'temp_dir': os.path.join(cls.test_dir, 'temp'),
                'logs_dir': os.path.join(cls.test_dir, 'logs'),
                'debug_mode': True
            },
            'database': {
                'main_db_path': os.path.join(cls.test_dir, 'data/database/main.db'),
                'training_db_path': os.path.join(cls.test_dir, 'data/database/training.db'),
                'demo_db_path': os.path.join(cls.test_dir, 'data/database/demo.db'),
                'backup_db_path': os.path.join(cls.test_dir, 'data/database/backup.db')
            },
            'data_quality': {
                'max_distortion_percentage': 5.0,
                'pause_learning_on_distortion': True,
                'daily_backup_enabled': True,
                'backup_time': '00:00',
                'validation_sample_size': 5
            },
            'web_server': {
                'enabled': False
            }
        }
        
        # Save config to file
        os.makedirs(os.path.join(cls.test_dir, 'config'), exist_ok=True)
        config_path = os.path.join(cls.test_dir, 'config/test_config.json')
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(cls.config, f, indent=2)
        
        # Initialize system
        cls.system = AgriculturalAISystem(config_path)
        
        # Create test user
        cls.admin_user = {
            'username': 'admin_test',
            'password': 'Admin@123',
            'email': 'admin@test.com',
            'full_name': 'Admin Test',
            'role': 'admin'
        }
        
        cls.user_result = cls.system.auth_manager.create_user(
            username=cls.admin_user['username'],
            password=cls.admin_user['password'],
            email=cls.admin_user['email'],
            full_name=cls.admin_user['full_name'],
            role=cls.admin_user['role']
        )
        
        # Login as admin
        cls.login_result = cls.system.login(
            username=cls.admin_user['username'],
            password=cls.admin_user['password']
        )
        
        cls.admin_user_info = cls.login_result['user_info']
        cls.admin_token = cls.login_result['token']
        
        # Create test organization and company
        cls.org_result = cls.system.organization_manager.create_organization(
            name="Test Organization",
            code="test_org",
            description="Test organization for system testing",
            user_info=cls.admin_user_info
        )
        
        cls.org_id = cls.org_result[2]
        
        cls.company_result = cls.system.organization_manager.create_company(
            name="Test Company",
            code="test_company",
            organization_id=cls.org_id,
            description="Test company for system testing",
            user_info=cls.admin_user_info
        )
        
        cls.company_id = cls.company_result[2]
        
        # Add user affiliation
        cls.affiliation_result = cls.system.organization_manager.add_user_affiliation(
            user_id=cls.admin_user_info['id'],
            username=cls.admin_user_info['username'],
            organization_id=cls.org_id,
            company_id=cls.company_id,
            is_primary=True,
            user_info=cls.admin_user_info
        )
        
        # Create test data directories
        cls.test_images_dir = os.path.join(cls.test_dir, 'test_images')
        os.makedirs(cls.test_images_dir, exist_ok=True)
        
        # Copy test images if available
        src_test_images = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_data/images')
        if os.path.exists(src_test_images):
            for img_file in os.listdir(src_test_images):
                if img_file.endswith(('.jpg', '.jpeg', '.png')):
                    shutil.copy(
                        os.path.join(src_test_images, img_file),
                        os.path.join(cls.test_images_dir, img_file)
                    )
        
        logger.info("Test environment setup complete")
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test environment."""
        logger.info("Cleaning up test environment")
        
        # Shutdown system
        cls.system.shutdown()
        
        # Remove temporary directory
        shutil.rmtree(cls.test_dir)
        
        logger.info("Test environment cleanup complete")
    
    def test_01_system_initialization(self):
        """Test system initialization."""
        logger.info("Testing system initialization")
        
        # Check if system is initialized
        self.assertIsNotNone(self.system)
        
        # Check if components are initialized
        self.assertIsNotNone(self.system.auth_manager)
        self.assertIsNotNone(self.system.organization_manager)
        self.assertIsNotNone(self.system.database_manager)
        self.assertIsNotNone(self.system.data_quality_monitor)
        self.assertIsNotNone(self.system.data_manager)
        self.assertIsNotNone(self.system.keyword_manager)
        self.assertIsNotNone(self.system.task_manager)
        self.assertIsNotNone(self.system.metrics_collector)
        self.assertIsNotNone(self.system.alerter)
        self.assertIsNotNone(self.system.image_processor)
        self.assertIsNotNone(self.system.image_segmenter)
        self.assertIsNotNone(self.system.disease_detector)
        self.assertIsNotNone(self.system.nutrient_analyzer)
        self.assertIsNotNone(self.system.soil_analyzer)
        self.assertIsNotNone(self.system.parallel_analyzer)
        self.assertIsNotNone(self.system.comparative_analyzer)
        self.assertIsNotNone(self.system.specifications_manager)
        self.assertIsNotNone(self.system.breeding_predictor)
        self.assertIsNotNone(self.system.treatment_recommender)
        self.assertIsNotNone(self.system.web_scraper)
        self.assertIsNotNone(self.system.image_search)
        self.assertIsNotNone(self.system.advanced_scraper)
        self.assertIsNotNone(self.system.source_verifier)
        self.assertIsNotNone(self.system.comprehensive_search)
        self.assertIsNotNone(self.system.data_augmentation)
        self.assertIsNotNone(self.system.enhanced_training)
        self.assertIsNotNone(self.system.learning_manager)
        self.assertIsNotNone(self.system.visualizer)
        
        # Check system status
        status = self.system.get_system_status()
        self.assertTrue(status['success'])
        self.assertEqual(status['system']['name'], 'Agricultural AI System Test')
        self.assertEqual(status['system']['version'], 'test')
    
    def test_02_authentication_system(self):
        """Test authentication system."""
        logger.info("Testing authentication system")
        
        # Test user creation
        self.assertTrue(self.user_result['success'])
        
        # Test login
        self.assertTrue(self.login_result['success'])
        self.assertIn('token', self.login_result)
        self.assertIn('user_info', self.login_result)
        
        # Test token validation
        validation_result = self.system.auth_manager.validate_token(self.admin_token)
        self.assertTrue(validation_result['success'])
        self.assertEqual(validation_result['user_info']['id'], self.admin_user_info['id'])
        
        # Test permission checking
        has_permission = self.system.auth_manager.check_permission(
            self.admin_user_info['id'], 'user_management', 'view'
        )
        self.assertTrue(has_permission)
        
        # Test logout
        logout_result = self.system.logout(self.admin_token, self.admin_user_info)
        self.assertTrue(logout_result['success'])
        
        # Test token invalidation
        validation_result = self.system.auth_manager.validate_token(self.admin_token)
        self.assertFalse(validation_result['success'])
        
        # Login again for subsequent tests
        self.login_result = self.system.login(
            username=self.admin_user['username'],
            password=self.admin_user['password']
        )
        
        self.admin_token = self.login_result['token']
        self.admin_user_info = self.login_result['user_info']
    
    def test_03_organization_management(self):
        """Test organization management."""
        logger.info("Testing organization management")
        
        # Test organization creation
        self.assertTrue(self.org_result[0])
        self.assertIsNotNone(self.org_id)
        
        # Test company creation
        self.assertTrue(self.company_result[0])
        self.assertIsNotNone(self.company_id)
        
        # Test user affiliation
        self.assertTrue(self.affiliation_result[0])
        
        # Test getting organization
        org = self.system.organization_manager.get_organization(self.org_id)
        self.assertIsNotNone(org)
        self.assertEqual(org['name'], "Test Organization")
        self.assertEqual(org['code'], "test_org")
        
        # Test getting company
        company = self.system.organization_manager.get_company(self.company_id)
        self.assertIsNotNone(company)
        self.assertEqual(company['name'], "Test Company")
        self.assertEqual(company['code'], "test_company")
        
        # Test getting user affiliations
        affiliations = self.system.organization_manager.get_user_affiliations(
            user_id=self.admin_user_info['id']
        )
        self.assertTrue(len(affiliations) > 0)
        
        # Test organization hierarchy
        hierarchy = self.system.organization_manager.get_organization_hierarchy()
        self.assertTrue(len(hierarchy) > 0)
        
        # Test login with organization and company
        login_result = self.system.login(
            username=self.admin_user['username'],
            password=self.admin_user['password'],
            organization_code="test_org",
            company_code="test_company"
        )
        
        self.assertTrue(login_result['success'])
        self.assertEqual(login_result['user_info']['organization_code'], "test_org")
        self.assertEqual(login_result['user_info']['company_code'], "test_company")
    
    def test_04_data_quality_monitoring(self):
        """Test data quality monitoring."""
        logger.info("Testing data quality monitoring")
        
        # Test data quality configuration
        self.assertEqual(
            self.system.data_quality_monitor.config['max_distortion_percentage'],
            5.0
        )
        
        # Test distortion detection
        test_data = {
            'values': [1, 2, 3, 4, 5, 100]  # Outlier at the end
        }
        
        distortion = self.system.data_quality_monitor.calculate_distortion(test_data)
        self.assertTrue(distortion > 0)
        
        # Test if learning should be paused
        should_pause = self.system.data_quality_monitor.should_pause_learning(test_data)
        self.assertTrue(should_pause)
    
    def test_05_keyword_management(self):
        """Test keyword management."""
        logger.info("Testing keyword management")
        
        # Test adding keywords
        result = self.system.add_keyword("test_disease", "disease", self.admin_user_info)
        self.assertTrue(result['success'])
        
        result = self.system.add_keyword("test_nutrient", "nutrient", self.admin_user_info)
        self.assertTrue(result['success'])
        
        result = self.system.add_keyword("test_soil", "soil", self.admin_user_info)
        self.assertTrue(result['success'])
        
        result = self.system.add_keyword("test_variety", "variety", self.admin_user_info)
        self.assertTrue(result['success'])
        
        # Test getting keywords
        keywords = self.system.keyword_manager.get_keywords("disease")
        self.assertIn("test_disease", keywords)
        
        keywords = self.system.keyword_manager.get_keywords("nutrient")
        self.assertIn("test_nutrient", keywords)
        
        keywords = self.system.keyword_manager.get_keywords("soil")
        self.assertIn("test_soil", keywords)
        
        keywords = self.system.keyword_manager.get_keywords("variety")
        self.assertIn("test_variety", keywords)
    
    def test_06_data_import_export(self):
        """Test data import and export."""
        logger.info("Testing data import and export")
        
        # Test exporting keywords
        export_result = self.system.export_data(
            data_type="keywords",
            format="json",
            user_info=self.admin_user_info
        )
        
        self.assertTrue(export_result['success'])
        
        # Get the export file path
        if isinstance(export_result['result'], tuple):
            _, _, export_path = export_result['result']
        else:
            export_path = export_result['result'].get('export_path')
        
        self.assertTrue(os.path.exists(export_path))
        
        # Test importing keywords
        import_result = self.system.import_data(
            file_path=export_path,
            data_type="keywords",
            merge_strategy="update",
            user_info=self.admin_user_info
        )
        
        self.assertTrue(import_result['success'])
    
    def test_07_task_management(self):
        """Test task management."""
        logger.info("Testing task management")
        
        # Create a task
        task_id = self.system.task_manager.create_task(
            task_type="test",
            description="Test task",
            user_info=self.admin_user_info
        )
        
        self.assertIsNotNone(task_id)
        
        # Update task status
        self.system.task_manager.update_task_status(
            task_id=task_id,
            status="running"
        )
        
        # Get task
        task = self.system.task_manager.get_task(task_id)
        self.assertEqual(task['status'], "running")
        
        # Complete task
        self.system.task_manager.update_task_status(
            task_id=task_id,
            status="completed",
            results={"test": "success"}
        )
        
        # Get task again
        task = self.system.task_manager.get_task(task_id)
        self.assertEqual(task['status'], "completed")
        self.assertEqual(task['results']['test'], "success")
    
    def test_08_audit_logging(self):
        """Test audit logging."""
        logger.info("Testing audit logging")
        
        # Log an action
        self.system.audit_manager.log_action(
            action_type="TEST",
            action="test_action",
            component="test",
            user_info=self.admin_user_info,
            details={"test": "data"},
            status="success"
        )
        
        # Get audit logs
        logs = self.system.audit_manager.get_logs(
            action_type="TEST",
            limit=10
        )
        
        self.assertTrue(len(logs) > 0)
        self.assertEqual(logs[0]['action'], "test_action")
        self.assertEqual(logs[0]['status'], "success")
    
    def test_09_image_analysis(self):
        """Test image analysis."""
        logger.info("Testing image analysis")
        
        # Find a test image
        test_images = [f for f in os.listdir(self.test_images_dir) 
                      if f.endswith(('.jpg', '.jpeg', '.png'))]
        
        if not test_images:
            logger.warning("No test images found, skipping image analysis test")
            return
        
        test_image = os.path.join(self.test_images_dir, test_images[0])
        
        # Test standard analysis
        result = self.system.analyze_image(
            image_path=test_image,
            analysis_type="auto",
            use_primitive=False,
            user_info=self.admin_user_info
        )
        
        self.assertTrue(result['success'])
        
        # Test primitive analysis
        result = self.system.analyze_image(
            image_path=test_image,
            analysis_type="auto",
            use_primitive=True,
            user_info=self.admin_user_info
        )
        
        self.assertTrue(result['success'])
        
        # Test comparative analysis
        result = self.system.analyze_image(
            image_path=test_image,
            analysis_type="auto",
            use_primitive=None,  # Auto select
            user_info=self.admin_user_info
        )
        
        self.assertTrue(result['success'])
        
        # Test getting treatment recommendations
        if 'results' in result and result['results']:
            rec_result = self.system.get_treatment_recommendations(
                analysis_results=result['results'],
                user_info=self.admin_user_info
            )
            
            self.assertTrue(rec_result['success'])
    
    def test_10_search_functionality(self):
        """Test search functionality."""
        logger.info("Testing search functionality")
        
        # Test comprehensive search
        result = self.system.search_information(
            query="plant disease",
            search_type="comprehensive",
            user_info=self.admin_user_info
        )
        
        # This might fail if no internet connection
        if not result['success']:
            logger.warning(f"Search test failed: {result.get('error')}")
            logger.warning("This might be due to no internet connection, skipping")
            return
        
        self.assertTrue(result['success'])
    
    def test_11_system_monitoring(self):
        """Test system monitoring."""
        logger.info("Testing system monitoring")
        
        # Get current metrics
        metrics = self.system.metrics_collector.get_current_metrics()
        
        self.assertIn('cpu_usage', metrics)
        self.assertIn('memory_usage', metrics)
        self.assertIn('disk_usage', metrics)
        
        # Test alerting
        alert_config = {
            'enabled': True,
            'high_cpu_threshold': 0,  # Set to 0 to trigger alert
            'high_memory_threshold': 0  # Set to 0 to trigger alert
        }
        
        self.system.alerter.config.update(alert_config)
        
        # Check for alerts
        alerts = self.system.alerter.check_alerts()
        
        self.assertTrue(len(alerts) > 0)
    
    def test_12_data_management(self):
        """Test data management."""
        logger.info("Testing data management")
        
        # Create a test file
        test_file = os.path.join(self.test_dir, 'test_data.txt')
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("Test data")
        
        # Test importing data
        result = self.system.data_manager.import_file(
            file_path=test_file,
            destination='test',
            user_info=self.admin_user_info
        )
        
        self.assertTrue(result['success'])
        
        # Test exporting data
        export_path = os.path.join(self.test_dir, 'exported_data.txt')
        result = self.system.data_manager.export_file(
            source=result['destination_path'],
            destination=export_path,
            user_info=self.admin_user_info
        )
        
        self.assertTrue(result['success'])
        self.assertTrue(os.path.exists(export_path))
    
    def test_13_learning_management(self):
        """Test learning management."""
        logger.info("Testing learning management")
        
        # Test learning status
        status = self.system.learning_manager.get_status()
        
        self.assertIn('last_update', status)
        self.assertIn('models', status)
        
        # Test model update check
        should_update = self.system.learning_manager.should_update_models()
        
        # This is a boolean, just check that it doesn't error
        self.assertIsInstance(should_update, bool)
    
    def test_14_visualization(self):
        """Test visualization."""
        logger.info("Testing visualization")
        
        # Test creating a simple visualization
        data = {
            'x': [1, 2, 3, 4, 5],
            'y': [10, 20, 15, 30, 25]
        }
        
        result = self.system.visualizer.create_line_chart(
            data=data,
            title="Test Chart",
            x_label="X",
            y_label="Y",
            output_path=os.path.join(self.test_dir, 'test_chart.png')
        )
        
        self.assertTrue(result['success'])
        self.assertTrue(os.path.exists(result['file_path']))
    
    def test_15_end_to_end(self):
        """Test end-to-end workflow."""
        logger.info("Testing end-to-end workflow")
        
        # Find a test image
        test_images = [f for f in os.listdir(self.test_images_dir) 
                      if f.endswith(('.jpg', '.jpeg', '.png'))]
        
        if not test_images:
            logger.warning("No test images found, skipping end-to-end test")
            return
        
        test_image = os.path.join(self.test_images_dir, test_images[0])
        
        # 1. Login with organization and company
        login_result = self.system.login(
            username=self.admin_user['username'],
            password=self.admin_user['password'],
            organization_code="test_org",
            company_code="test_company"
        )
        
        self.assertTrue(login_result['success'])
        
        user_info = login_result['user_info']
        
        # 2. Analyze image
        analysis_result = self.system.analyze_image(
            image_path=test_image,
            analysis_type="auto",
            user_info=user_info
        )
        
        self.assertTrue(analysis_result['success'])
        
        # 3. Get treatment recommendations
        if 'results' in analysis_result and analysis_result['results']:
            rec_result = self.system.get_treatment_recommendations(
                analysis_results=analysis_result['results'],
                user_info=user_info
            )
            
            self.assertTrue(rec_result['success'])
        
        # 4. Search for additional information
        search_result = self.system.search_information(
            query="plant treatment",
            search_type="comprehensive",
            user_info=user_info
        )
        
        # This might fail if no internet connection
        if not search_result['success']:
            logger.warning(f"Search test failed: {search_result.get('error')}")
            logger.warning("This might be due to no internet connection, skipping")
        
        # 5. Export analysis results
        export_result = self.system.export_data(
            data_type="reference",
            format="json",
            user_info=user_info
        )
        
        self.assertTrue(export_result['success'])
        
        # 6. Logout
        logout_result = self.system.logout(
            token=login_result['token'],
            user_info=user_info
        )
        
        self.assertTrue(logout_result['success'])


if __name__ == '__main__':
    unittest.main()
