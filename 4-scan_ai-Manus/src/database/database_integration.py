#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database Integration Module

This module integrates all database components with the main system,
ensuring proper connections between the four database types and the
various system modules.

Author: Agricultural AI System Team
Date: April 27, 2025
"""

import os
import sys
import logging
from datetime import datetime
import json
import yaml
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import database components
from database.database_manager import DatabaseManager
from database.database_synchronizer import DatabaseSynchronizer
from database.migration_manager import MigrationManager
from database.database_monitor import DatabaseMonitor
from database.database_reporting import DatabaseReportingSystem

# Import other system components that need database integration
from auth.auth_manager import AuthManager
from auth.permission_manager import PermissionManager
from disease_detection.detector import DiseaseDetector
from nutrient_analysis.analyzer import NutrientAnalyzer
from plant_breeding.predictor import BreedingPredictor
from treatment_recommendation.recommender import TreatmentRecommender
from treatment_recommendation.enhanced_recommender import EnhancedTreatmentRecommender
from data_collection.web_scraper import WebScraper
from data_collection.image_search import ImageSearch
from data_collection.advanced_scraper import AdvancedScraper
from data_collection.source_verifier import SourceVerifier
from data_collection.comprehensive_search import ComprehensiveSearch
from continuous_learning.learning_manager import LearningManager
from variety_comparison.variety_manager import VarietyManager
from nursery_management.nursery_manager import NurseryManager
from farm_management.farm_manager import FarmManager
from cost_management.cost_calculator import CostCalculator
from inventory_management.inventory_manager import InventoryManager
from financial_reporting.financial_reporting_system import FinancialReportingSystem
from ai_assistant.assistant_agent import AIAssistant
from organization.organization_manager import OrganizationManager
from crop_organization.crop_organization_manager import CropOrganizationManager
from trusted_sources.trusted_sources_manager import TrustedSourcesManager

# Import utility modules
from utils.config_loader import ConfigLoader
from utils.logger_setup import setup_logger

class DatabaseIntegration:
    """
    Integrates all database components with the main system.
    """
    
    def __init__(self, config_path=None):
        """
        Initialize the database integration module.
        
        Args:
            config_path (str): Path to the configuration file.
        """
        # Load environment variables
        load_dotenv()
        
        # Setup logging
        self.logger = setup_logger('database_integration')
        self.logger.info("Initializing database integration module")
        
        # Load configuration
        self.config = ConfigLoader(config_path).load_config()
        
        # Initialize database managers for each database type
        self.operational_db = DatabaseManager(
            db_type='operational',
            connection_string=os.getenv('OPERATIONAL_DB_CONNECTION'),
            config=self.config.get('databases', {}).get('operational', {})
        )
        
        self.employee_training_db = DatabaseManager(
            db_type='employee_training',
            connection_string=os.getenv('EMPLOYEE_TRAINING_DB_CONNECTION'),
            config=self.config.get('databases', {}).get('employee_training', {})
        )
        
        self.system_training_db = DatabaseManager(
            db_type='system_training',
            connection_string=os.getenv('SYSTEM_TRAINING_DB_CONNECTION'),
            config=self.config.get('databases', {}).get('system_training', {})
        )
        
        self.backup_db = DatabaseManager(
            db_type='backup',
            connection_string=os.getenv('BACKUP_DB_CONNECTION'),
            config=self.config.get('databases', {}).get('backup', {})
        )
        
        # Initialize database synchronizer
        self.synchronizer = DatabaseSynchronizer(
            source_dbs=[self.operational_db, self.employee_training_db, self.system_training_db],
            target_db=self.backup_db,
            config=self.config.get('synchronization', {})
        )
        
        # Initialize migration manager
        self.migration_manager = MigrationManager(
            databases=[self.operational_db, self.employee_training_db, 
                      self.system_training_db, self.backup_db],
            config=self.config.get('migration', {})
        )
        
        # Initialize database monitor
        self.monitor = DatabaseMonitor(
            databases=[self.operational_db, self.employee_training_db, 
                      self.system_training_db, self.backup_db],
            config=self.config.get('monitoring', {})
        )
        
        # Initialize reporting system
        self.reporting = DatabaseReportingSystem(
            databases=[self.operational_db, self.employee_training_db, 
                      self.system_training_db, self.backup_db],
            config=self.config.get('reporting', {})
        )
        
        self.logger.info("Database components initialized successfully")
    
    def integrate_with_auth_system(self):
        """
        Integrate database components with the authentication system.
        """
        self.logger.info("Integrating databases with authentication system")
        
        # Connect auth manager with operational database
        auth_manager = AuthManager()
        auth_manager.set_database(self.operational_db)
        
        # Connect permission manager with operational database
        permission_manager = PermissionManager()
        permission_manager.set_database(self.operational_db)
        
        # Connect organization manager with operational database
        org_manager = OrganizationManager()
        org_manager.set_database(self.operational_db)
        
        self.logger.info("Authentication system integration complete")
        return True
    
    def integrate_with_core_modules(self):
        """
        Integrate database components with core system modules.
        """
        self.logger.info("Integrating databases with core system modules")
        
        # Disease detection module
        disease_detector = DiseaseDetector()
        disease_detector.set_operational_db(self.operational_db)
        disease_detector.set_training_db(self.system_training_db)
        
        # Nutrient analysis module
        nutrient_analyzer = NutrientAnalyzer()
        nutrient_analyzer.set_operational_db(self.operational_db)
        nutrient_analyzer.set_training_db(self.system_training_db)
        
        # Breeding prediction module
        breeding_predictor = BreedingPredictor()
        breeding_predictor.set_operational_db(self.operational_db)
        breeding_predictor.set_training_db(self.system_training_db)
        
        # Treatment recommendation modules
        treatment_recommender = TreatmentRecommender()
        treatment_recommender.set_operational_db(self.operational_db)
        treatment_recommender.set_training_db(self.system_training_db)
        
        enhanced_recommender = EnhancedTreatmentRecommender()
        enhanced_recommender.set_operational_db(self.operational_db)
        enhanced_recommender.set_training_db(self.system_training_db)
        
        self.logger.info("Core modules integration complete")
        return True
    
    def integrate_with_data_collection(self):
        """
        Integrate database components with data collection modules.
        """
        self.logger.info("Integrating databases with data collection modules")
        
        # Web scraper
        web_scraper = WebScraper()
        web_scraper.set_database(self.operational_db)
        
        # Image search
        image_search = ImageSearch()
        image_search.set_database(self.operational_db)
        
        # Advanced scraper
        advanced_scraper = AdvancedScraper()
        advanced_scraper.set_database(self.operational_db)
        
        # Source verifier
        source_verifier = SourceVerifier()
        source_verifier.set_database(self.operational_db)
        
        # Comprehensive search
        comprehensive_search = ComprehensiveSearch()
        comprehensive_search.set_database(self.operational_db)
        
        # Trusted sources manager
        trusted_sources = TrustedSourcesManager()
        trusted_sources.set_database(self.operational_db)
        
        self.logger.info("Data collection modules integration complete")
        return True
    
    def integrate_with_learning_system(self):
        """
        Integrate database components with learning system.
        """
        self.logger.info("Integrating databases with learning system")
        
        # Learning manager
        learning_manager = LearningManager()
        learning_manager.set_operational_db(self.operational_db)
        learning_manager.set_training_db(self.system_training_db)
        learning_manager.set_employee_training_db(self.employee_training_db)
        learning_manager.set_backup_db(self.backup_db)
        
        self.logger.info("Learning system integration complete")
        return True
    
    def integrate_with_management_modules(self):
        """
        Integrate database components with management modules.
        """
        self.logger.info("Integrating databases with management modules")
        
        # Variety comparison
        variety_manager = VarietyManager()
        variety_manager.set_database(self.operational_db)
        
        # Nursery management
        nursery_manager = NurseryManager()
        nursery_manager.set_database(self.operational_db)
        
        # Farm management
        farm_manager = FarmManager()
        farm_manager.set_database(self.operational_db)
        
        # Cost management
        cost_calculator = CostCalculator()
        cost_calculator.set_database(self.operational_db)
        
        # Inventory management
        inventory_manager = InventoryManager()
        inventory_manager.set_database(self.operational_db)
        
        # Financial reporting
        financial_reporting = FinancialReportingSystem()
        financial_reporting.set_database(self.operational_db)
        
        # Crop organization
        crop_organization = CropOrganizationManager()
        crop_organization.set_database(self.operational_db)
        
        self.logger.info("Management modules integration complete")
        return True
    
    def integrate_with_ai_assistant(self):
        """
        Integrate database components with AI assistant.
        """
        self.logger.info("Integrating databases with AI assistant")
        
        # AI assistant
        ai_assistant = AIAssistant()
        ai_assistant.set_operational_db(self.operational_db)
        ai_assistant.set_training_db(self.system_training_db)
        
        self.logger.info("AI assistant integration complete")
        return True
    
    def setup_daily_backup(self):
        """
        Set up daily backup procedures.
        """
        self.logger.info("Setting up daily backup procedures")
        
        # Configure backup schedule
        backup_config = {
            'schedule': {
                'frequency': 'daily',
                'time': '00:00',
                'retention_days': 30
            },
            'backup_types': ['full', 'incremental'],
            'compression': True,
            'encryption': True
        }
        
        # Update synchronizer configuration
        self.synchronizer.update_config(backup_config)
        
        # Schedule initial backup
        self.synchronizer.schedule_backup()
        
        self.logger.info("Daily backup procedures configured")
        return True
    
    def verify_integration(self):
        """
        Verify that all integrations are working correctly.
        """
        self.logger.info("Verifying database integrations")
        
        # Check database connections
        operational_status = self.operational_db.test_connection()
        employee_training_status = self.employee_training_db.test_connection()
        system_training_status = self.system_training_db.test_connection()
        backup_status = self.backup_db.test_connection()
        
        # Check synchronization
        sync_status = self.synchronizer.test_synchronization()
        
        # Check migration
        migration_status = self.migration_manager.verify_schema_versions()
        
        # Check monitoring
        monitoring_status = self.monitor.check_monitoring_status()
        
        # Compile results
        integration_status = {
            'database_connections': {
                'operational': operational_status,
                'employee_training': employee_training_status,
                'system_training': system_training_status,
                'backup': backup_status
            },
            'synchronization': sync_status,
            'migration': migration_status,
            'monitoring': monitoring_status,
            'timestamp': datetime.now().isoformat()
        }
        
        # Log results
        self.logger.info(f"Integration verification results: {json.dumps(integration_status)}")
        
        # Return overall status
        all_statuses = [
            operational_status, employee_training_status, 
            system_training_status, backup_status,
            sync_status, migration_status, monitoring_status
        ]
        
        return all(all_statuses)
    
    def initialize_all_integrations(self):
        """
        Initialize all database integrations.
        """
        self.logger.info("Initializing all database integrations")
        
        try:
            # Integrate with all system components
            auth_integration = self.integrate_with_auth_system()
            core_integration = self.integrate_with_core_modules()
            data_integration = self.integrate_with_data_collection()
            learning_integration = self.integrate_with_learning_system()
            management_integration = self.integrate_with_management_modules()
            assistant_integration = self.integrate_with_ai_assistant()
            
            # Set up backup procedures
            backup_setup = self.setup_daily_backup()
            
            # Verify all integrations
            verification = self.verify_integration()
            
            integration_results = {
                'auth_integration': auth_integration,
                'core_integration': core_integration,
                'data_integration': data_integration,
                'learning_integration': learning_integration,
                'management_integration': management_integration,
                'assistant_integration': assistant_integration,
                'backup_setup': backup_setup,
                'verification': verification,
                'timestamp': datetime.now().isoformat()
            }
            
            self.logger.info(f"Integration results: {json.dumps(integration_results)}")
            
            if all(integration_results.values()):
                self.logger.info("All database integrations completed successfully")
                return True
            else:
                self.logger.error("Some database integrations failed")
                return False
                
        except Exception as e:
            self.logger.error(f"Error during database integration: {str(e)}")
            return False


if __name__ == "__main__":
    # Initialize database integration
    integrator = DatabaseIntegration()
    
    # Run all integrations
    success = integrator.initialize_all_integrations()
    
    if success:
        print("Database integration completed successfully")
        sys.exit(0)
    else:
        print("Database integration failed")
        sys.exit(1)
