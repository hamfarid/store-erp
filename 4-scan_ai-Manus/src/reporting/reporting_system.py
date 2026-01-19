#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Advanced Reporting System for Agricultural AI System.
Provides comprehensive reporting at system, user, learning, and database levels.
"""

import os
import sys
import json
import logging
import datetime
import uuid
import csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Union
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('reporting')


class ReportingSystem:
    """
    Advanced Reporting System for the Agricultural AI System.
    Provides comprehensive reporting at system, user, learning, and database levels.
    """
    
    def __init__(self, config_path: str, database_manager=None, audit_manager=None, 
                 auth_manager=None):
        """
        Initialize the Reporting System.
        
        Args:
            config_path: Path to configuration file
            database_manager: Database manager instance
            audit_manager: Audit manager instance
            auth_manager: Authentication manager instance
        """
        self.config_path = config_path
        self.database_manager = database_manager
        self.audit_manager = audit_manager
        self.auth_manager = auth_manager
        
        # Load configuration
        self.config = self._load_config()
        
        # Initialize data directories
        self._init_directories()
        
        logger.info("Reporting System initialized")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Get reporting specific config
            if 'reporting' not in config:
                config['reporting'] = {
                    'reports_dir': os.path.join(os.path.dirname(self.config_path), '../data/reports'),
                    'templates_dir': os.path.join(os.path.dirname(self.config_path), '../data/reports/templates'),
                    'charts_dir': os.path.join(os.path.dirname(self.config_path), '../data/reports/charts'),
                    'export_formats': ['pdf', 'csv', 'json', 'html'],
                    'default_date_range': 30,  # days
                    'report_types': {
                        'system_performance': {
                            'enabled': True,
                            'default_metrics': [
                                'api_response_time',
                                'model_accuracy',
                                'system_uptime',
                                'error_rate',
                                'resource_usage'
                            ]
                        },
                        'user_activity': {
                            'enabled': True,
                            'default_metrics': [
                                'active_users',
                                'queries_per_user',
                                'uploads_per_user',
                                'disease_detections',
                                'nutrient_analyses'
                            ]
                        },
                        'learning_progress': {
                            'enabled': True,
                            'default_metrics': [
                                'model_accuracy_trend',
                                'training_iterations',
                                'data_quality_score',
                                'knowledge_base_growth',
                                'error_reduction_rate'
                            ]
                        },
                        'database_updates': {
                            'enabled': True,
                            'default_metrics': [
                                'records_added',
                                'records_modified',
                                'database_size',
                                'query_performance',
                                'backup_status'
                            ]
                        },
                        'variety_comparison': {
                            'enabled': True,
                            'default_metrics': [
                                'varieties_compared',
                                'comparison_criteria',
                                'top_performing_varieties',
                                'trial_locations',
                                'yield_metrics'
                            ]
                        },
                        'nursery_management': {
                            'enabled': True,
                            'default_metrics': [
                                'seedling_success_rate',
                                'nursery_capacity_utilization',
                                'order_fulfillment_rate',
                                'growth_cycle_adherence',
                                'customer_satisfaction'
                            ]
                        }
                    },
                    'scheduled_reports': [
                        {
                            'name': 'Daily System Summary',
                            'type': 'system_performance',
                            'frequency': 'daily',
                            'time': '23:00',
                            'recipients': ['admin'],
                            'format': 'pdf'
                        },
                        {
                            'name': 'Weekly Learning Progress',
                            'type': 'learning_progress',
                            'frequency': 'weekly',
                            'day': 'Monday',
                            'time': '08:00',
                            'recipients': ['admin', 'development_manager'],
                            'format': 'pdf'
                        },
                        {
                            'name': 'Monthly Database Status',
                            'type': 'database_updates',
                            'frequency': 'monthly',
                            'day': 1,
                            'time': '06:00',
                            'recipients': ['admin', 'database_manager'],
                            'format': 'pdf'
                        }
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
                'reporting': {
                    'reports_dir': os.path.join(os.path.dirname(self.config_path), '../data/reports'),
                    'templates_dir': os.path.join(os.path.dirname(self.config_path), '../data/reports/templates'),
                    'charts_dir': os.path.join(os.path.dirname(self.config_path), '../data/reports/charts'),
                    'export_formats': ['pdf', 'csv', 'json', 'html'],
                    'default_date_range': 30,  # days
                    'report_types': {
                        'system_performance': {
                            'enabled': True,
                            'default_metrics': [
                                'api_response_time',
                                'model_accuracy',
                                'system_uptime',
                                'error_rate',
                                'resource_usage'
                            ]
                        },
                        'user_activity': {
                            'enabled': True,
                            'default_metrics': [
                                'active_users',
                                'queries_per_user',
                                'uploads_per_user',
                                'disease_detections',
                                'nutrient_analyses'
                            ]
                        },
                        'learning_progress': {
                            'enabled': True,
                            'default_metrics': [
                                'model_accuracy_trend',
                                'training_iterations',
                                'data_quality_score',
                                'knowledge_base_growth',
                                'error_reduction_rate'
                            ]
                        },
                        'database_updates': {
                            'enabled': True,
                            'default_metrics': [
                                'records_added',
                                'records_modified',
                                'database_size',
                                'query_performance',
                                'backup_status'
                            ]
                        },
                        'variety_comparison': {
                            'enabled': True,
                            'default_metrics': [
                                'varieties_compared',
                                'comparison_criteria',
                                'top_performing_varieties',
                                'trial_locations',
                                'yield_metrics'
                            ]
                        },
                        'nursery_management': {
                            'enabled': True,
                            'default_metrics': [
                                'seedling_success_rate',
                                'nursery_capacity_utilization',
                                'order_fulfillment_rate',
                                'growth_cycle_adherence',
                                'customer_satisfaction'
                            ]
                        }
                    },
                    'scheduled_reports': [
                        {
                            'name': 'Daily System Summary',
                            'type': 'system_performance',
                            'frequency': 'daily',
                            'time': '23:00',
                            'recipients': ['admin'],
                            'format': 'pdf'
                        },
                        {
                            'name': 'Weekly Learning Progress',
                            'type': 'learning_progress',
                            'frequency': 'weekly',
                            'day': 'Monday',
                            'time': '08:00',
                            'recipients': ['admin', 'development_manager'],
                            'format': 'pdf'
                        },
                        {
                            'name': 'Monthly Database Status',
                            'type': 'database_updates',
                            'frequency': 'monthly',
                            'day': 1,
                            'time': '06:00',
                            'recipients': ['admin', 'database_manager'],
                            'format': 'pdf'
                        }
                    ]
                }
            }
    
    def _init_directories(self):
        """Initialize required directories."""
        os.makedirs(self.config['reporting']['reports_dir'], exist_ok=True)
        os.makedirs(self.config['reporting']['templates_dir'], exist_ok=True)
        os.makedirs(self.config['reporting']['charts_dir'], exist_ok=True)
        
        # Create directories for each report type
        for report_type in self.config['reporting']['report_types']:
            os.makedirs(os.path.join(self.config['reporting']['reports_dir'], report_type), exist_ok=True)
            os.makedirs(os.path.join(self.config['reporting']['charts_dir'], report_type), exist_ok=True)
    
    def generate_report(self, user_info: Dict[str, Any], report_type: str, 
                       start_date: Optional[str] = None, end_date: Optional[str] = None,
                       metrics: Optional[List[str]] = None, 
                       export_format: str = 'pdf') -> Dict[str, Any]:
        """
        Generate a report of the specified type.
        
        Args:
            user_info: Information about the user
            report_type: Type of report to generate
            start_date: Optional start date for report data (ISO format)
            end_date: Optional end date for report data (ISO format)
            metrics: Optional list of metrics to include
            export_format: Format to export the report in
            
        Returns:
            Dictionary with report generation result
        """
        try:
            # Check if report type is valid
            if report_type not in self.config['reporting']['report_types']:
                return {
                    'success': False,
                    'error': f"Invalid report type: {report_type}"
                }
            
            # Check if report type is enabled
            if not self.config['reporting']['report_types'][report_type]['enabled']:
                return {
                    'success': False,
                    'error': f"Report type '{report_type}' is disabled"
                }
            
            # Check if export format is valid
            if export_format not in self.config['reporting']['export_formats']:
                return {
                    'success': False,
                    'error': f"Invalid export format: {export_format}"
                }
            
            # Set default dates if not provided
            if not end_date:
                end_date = datetime.datetime.now().isoformat()
            
            if not start_date:
                # Calculate start date based on default date range
                default_range = self.config['reporting']['default_date_range']
                start_date = (datetime.datetime.fromisoformat(end_date) - 
                             datetime.timedelta(days=default_range)).isoformat()
            
            # Set default metrics if not provided
            if not metrics:
                metrics = self.config['reporting']['report_types'][report_type]['default_metrics']
            
            # Generate report ID
            report_id = str(uuid.uuid4())
            
            # Get report data
            report_data = self._get_report_data(report_type, start_date, end_date, metrics)
            
            # Generate charts
            chart_files = self._generate_charts(report_type, report_id, report_data)
            
            # Create report content
            report_content = self._create_report_content(
                report_type, report_id, start_date, end_date, metrics, report_data, chart_files
            )
            
            # Export report
            report_file = self._export_report(
                report_type, report_id, report_content, export_format
            )
            
            # Log the action
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="REPORTING",
                    action="generate_report",
                    component="reporting",
                    user_info=user_info,
                    details={
                        "report_id": report_id,
                        "report_type": report_type,
                        "start_date": start_date,
                        "end_date": end_date
                    },
                    status="success"
                )
            
            return {
                'success': True,
                'report_id': report_id,
                'report_file': report_file,
                'message': f"Report generated successfully"
            }
            
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            
            # Log the error
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="REPORTING",
                    action="generate_report",
                    component="reporting",
                    user_info=user_info,
                    details={"error": str(e)},
                    status="error"
                )
            
            return {
                'success': False,
                'error': f"Error generating report: {str(e)}"
            }
    
    def _get_report_data(self, report_type: str, start_date: str, end_date: str, 
                        metrics: List[str]) -> Dict[str, Any]:
        """
        Get data for a report.
        
        Args:
            report_type: Type of report
            start_date: Start date for report data (ISO format)
            end_date: End date for report data (ISO format)
            metrics: List of metrics to include
            
        Returns:
            Dictionary with report data
        """
        # Convert dates to datetime objects
        start_datetime = datetime.datetime.fromisoformat(start_date)
        end_datetime = datetime.datetime.fromisoformat(end_date)
        
        # Initialize data dictionary
        data = {
            'report_type': report_type,
            'start_date': start_date,
            'end_date': end_date,
            'metrics': {},
            'summary': {}
        }
        
        # Get data for each metric
        for metric in metrics:
            metric_data = self._get_metric_data(report_type, metric, start_datetime, end_datetime)
            data['metrics'][metric] = metric_data
        
        # Generate summary statistics
        data['summary'] = self._generate_summary(report_type, data['metrics'])
        
        return data
    
    def _get_metric_data(self, report_type: str, metric: str, 
                        start_datetime: datetime.datetime, 
                        end_datetime: datetime.datetime) -> Dict[str, Any]:
        """
        Get data for a specific metric.
        
        Args:
            report_type: Type of report
            metric: Metric to get data for
            start_datetime: Start date for metric data
            end_datetime: End date for metric data
            
        Returns:
            Dictionary with metric data
        """
        # This method would normally query the database or other data sources
        # For this example, we'll generate simulated data
        
        # Generate date range
        date_range = []
        current_date = start_datetime
        while current_date <= end_datetime:
            date_range.append(current_date.date().isoformat())
            current_date += datetime.timedelta(days=1)
        
        # Generate simulated data based on report type and metric
        if report_type == 'system_performance':
            if metric == 'api_response_time':
                # Simulate API response time (milliseconds)
                values = [round(np.random.normal(200, 50), 2) for _ in range(len(date_range))]
                return {
                    'label': 'API Response Time (ms)',
                    'dates': date_range,
                    'values': values,
                    'unit': 'ms',
                    'trend': 'decreasing' if values[-1] < values[0] else 'increasing'
                }
            elif metric == 'model_accuracy':
                # Simulate model accuracy (percentage)
                base_accuracy = 85
                values = [min(99, max(70, base_accuracy + np.random.normal(0, 3))) for _ in range(len(date_range))]
                values = [round(v, 2) for v in values]
                return {
                    'label': 'Model Accuracy (%)',
                    'dates': date_range,
                    'values': values,
                    'unit': '%',
                    'trend': 'increasing' if values[-1] > values[0] else 'decreasing'
                }
            elif metric == 'system_uptime':
                # Simulate system uptime (percentage)
                values = [round(min(100, max(90, 99 + np.random.normal(0, 1))), 2) for _ in range(len(date_range))]
                return {
                    'label': 'System Uptime (%)',
                    'dates': date_range,
                    'values': values,
                    'unit': '%',
                    'trend': 'stable'
                }
            elif metric == 'error_rate':
                # Simulate error rate (percentage)
                values = [round(max(0, min(10, 2 + np.random.normal(0, 1))), 2) for _ in range(len(date_range))]
                return {
                    'label': 'Error Rate (%)',
                    'dates': date_range,
                    'values': values,
                    'unit': '%',
                    'trend': 'decreasing' if values[-1] < values[0] else 'increasing'
                }
            elif metric == 'resource_usage':
                # Simulate resource usage (percentage)
                values = [round(min(95, max(30, 60 + np.random.normal(0, 10))), 2) for _ in range(len(date_range))]
                return {
                    'label': 'Resource Usage (%)',
                    'dates': date_range,
                    'values': values,
                    'unit': '%',
                    'trend': 'fluctuating'
                }
        
        elif report_type == 'user_activity':
            if metric == 'active_users':
                # Simulate active users (count)
                base_users = 100
                values = [max(1, int(base_users + np.random.normal(0, 20))) for _ in range(len(date_range))]
                return {
                    'label': 'Active Users',
                    'dates': date_range,
                    'values': values,
                    'unit': 'users',
                    'trend': 'increasing' if values[-1] > values[0] else 'decreasing'
                }
            elif metric == 'queries_per_user':
                # Simulate queries per user (count)
                values = [round(max(0.1, min(20, 5 + np.random.normal(0, 2))), 2) for _ in range(len(date_range))]
                return {
                    'label': 'Queries per User',
                    'dates': date_range,
                    'values': values,
                    'unit': 'queries',
                    'trend': 'stable'
                }
            elif metric == 'uploads_per_user':
                # Simulate uploads per user (count)
                values = [round(max(0, min(10, 2 + np.random.normal(0, 1))), 2) for _ in range(len(date_range))]
                return {
                    'label': 'Uploads per User',
                    'dates': date_range,
                    'values': values,
                    'unit': 'uploads',
                    'trend': 'increasing' if values[-1] > values[0] else 'stable'
                }
            elif metric == 'disease_detections':
                # Simulate disease detections (count)
                values = [max(0, int(50 + np.random.normal(0, 15))) for _ in range(len(date_range))]
                return {
                    'label': 'Disease Detections',
                    'dates': date_range,
                    'values': values,
                    'unit': 'detections',
                    'trend': 'fluctuating'
                }
            elif metric == 'nutrient_analyses':
                # Simulate nutrient analyses (count)
                values = [max(0, int(30 + np.random.normal(0, 10))) for _ in range(len(date_range))]
                return {
                    'label': 'Nutrient Analyses',
                    'dates': date_range,
                    'values': values,
                    'unit': 'analyses',
                    'trend': 'increasing' if values[-1] > values[0] else 'stable'
                }
        
        elif report_type == 'learning_progress':
            if metric == 'model_accuracy_trend':
                # Simulate model accuracy trend (percentage)
                base_accuracy = 80
                increment = 0.05
                values = [round(min(99, base_accuracy + increment * i + np.random.normal(0, 1)), 2) for i in range(len(date_range))]
                return {
                    'label': 'Model Accuracy Trend (%)',
                    'dates': date_range,
                    'values': values,
                    'unit': '%',
                    'trend': 'increasing'
                }
            elif metric == 'training_iterations':
                # Simulate training iterations (count)
                values = [max(1, int(5 + np.random.normal(0, 2))) for _ in range(len(date_range))]
                return {
                    'label': 'Training Iterations',
                    'dates': date_range,
                    'values': values,
                    'unit': 'iterations',
                    'trend': 'stable'
                }
            elif metric == 'data_quality_score':
                # Simulate data quality score (percentage)
                values = [round(min(100, max(70, 85 + np.random.normal(0, 5))), 2) for _ in range(len(date_range))]
                return {
                    'label': 'Data Quality Score (%)',
                    'dates': date_range,
                    'values': values,
                    'unit': '%',
                    'trend': 'increasing' if values[-1] > values[0] else 'stable'
                }
            elif metric == 'knowledge_base_growth':
                # Simulate knowledge base growth (count)
                base_count = 1000
                daily_increment = 20
                values = [base_count + i * daily_increment + int(np.random.normal(0, 10)) for i in range(len(date_range))]
                return {
                    'label': 'Knowledge Base Entries',
                    'dates': date_range,
                    'values': values,
                    'unit': 'entries',
                    'trend': 'increasing'
                }
            elif metric == 'error_reduction_rate':
                # Simulate error reduction rate (percentage)
                base_error = 15
                reduction_factor = 0.98
                values = [round(max(1, base_error * (reduction_factor ** i) + np.random.normal(0, 0.5)), 2) for i in range(len(date_range))]
                return {
                    'label': 'Error Rate (%)',
                    'dates': date_range,
                    'values': values,
                    'unit': '%',
                    'trend': 'decreasing'
                }
        
        elif report_type == 'database_updates':
            if metric == 'records_added':
                # Simulate records added (count)
                values = [max(0, int(100 + np.random.normal(0, 30))) for _ in range(len(date_range))]
                return {
                    'label': 'Records Added',
                    'dates': date_range,
                    'values': values,
                    'unit': 'records',
                    'trend': 'fluctuating'
                }
            elif metric == 'records_modified':
                # Simulate records modified (count)
                values = [max(0, int(50 + np.random.normal(0, 20))) for _ in range(len(date_range))]
                return {
                    'label': 'Records Modified',
                    'dates': date_range,
                    'values': values,
                    'unit': 'records',
                    'trend': 'fluctuating'
                }
            elif metric == 'database_size':
                # Simulate database size (MB)
                base_size = 500
                daily_increment = 5
                values = [round(base_size + i * daily_increment + np.random.normal(0, 2), 2) for i in range(len(date_range))]
                return {
                    'label': 'Database Size (MB)',
                    'dates': date_range,
                    'values': values,
                    'unit': 'MB',
                    'trend': 'increasing'
                }
            elif metric == 'query_performance':
                # Simulate query performance (milliseconds)
                values = [round(max(10, min(500, 100 + np.random.normal(0, 30))), 2) for _ in range(len(date_range))]
                return {
                    'label': 'Query Performance (ms)',
                    'dates': date_range,
                    'values': values,
                    'unit': 'ms',
                    'trend': 'stable'
                }
            elif metric == 'backup_status':
                # Simulate backup status (boolean)
                # 1 = success, 0 = failure
                values = [1 if np.random.random() > 0.05 else 0 for _ in range(len(date_range))]
                return {
                    'label': 'Backup Status',
                    'dates': date_range,
                    'values': values,
                    'unit': 'status',
                    'trend': 'stable'
                }
        
        elif report_type == 'variety_comparison':
            if metric == 'varieties_compared':
                # Simulate varieties compared (count)
                values = [max(1, int(10 + np.random.normal(0, 3))) for _ in range(len(date_range))]
                return {
                    'label': 'Varieties Compared',
                    'dates': date_range,
                    'values': values,
                    'unit': 'varieties',
                    'trend': 'increasing' if values[-1] > values[0] else 'stable'
                }
            elif metric == 'comparison_criteria':
                # Simulate comparison criteria (count)
                values = [max(1, int(5 + np.random.normal(0, 1))) for _ in range(len(date_range))]
                return {
                    'label': 'Comparison Criteria',
                    'dates': date_range,
                    'values': values,
                    'unit': 'criteria',
                    'trend': 'increasing' if values[-1] > values[0] else 'stable'
                }
            elif metric == 'top_performing_varieties':
                # Simulate top performing varieties data
                # This would be more complex in a real system
                varieties = ['Variety A', 'Variety B', 'Variety C', 'Variety D', 'Variety E']
                scores = [round(np.random.uniform(70, 95), 1) for _ in varieties]
                sorted_data = sorted(zip(varieties, scores), key=lambda x: x[1], reverse=True)
                return {
                    'label': 'Top Performing Varieties',
                    'varieties': [v[0] for v in sorted_data],
                    'scores': [v[1] for v in sorted_data],
                    'unit': 'score',
                    'trend': 'not_applicable'
                }
            elif metric == 'trial_locations':
                # Simulate trial locations (count)
                values = [max(1, int(3 + np.random.normal(0, 1))) for _ in range(len(date_range))]
                return {
                    'label': 'Trial Locations',
                    'dates': date_range,
                    'values': values,
                    'unit': 'locations',
                    'trend': 'stable'
                }
            elif metric == 'yield_metrics':
                # Simulate yield metrics (tons/hectare)
                values = [round(max(1, min(15, 8 + np.random.normal(0, 2))), 2) for _ in range(len(date_range))]
                return {
                    'label': 'Average Yield (tons/ha)',
                    'dates': date_range,
                    'values': values,
                    'unit': 'tons/ha',
                    'trend': 'increasing' if values[-1] > values[0] else 'stable'
                }
        
        elif report_type == 'nursery_management':
            if metric == 'seedling_success_rate':
                # Simulate seedling success rate (percentage)
                values = [round(min(100, max(70, 85 + np.random.normal(0, 5))), 2) for _ in range(len(date_range))]
                return {
                    'label': 'Seedling Success Rate (%)',
                    'dates': date_range,
                    'values': values,
                    'unit': '%',
                    'trend': 'increasing' if values[-1] > values[0] else 'stable'
                }
            elif metric == 'nursery_capacity_utilization':
                # Simulate nursery capacity utilization (percentage)
                values = [round(min(100, max(50, 75 + np.random.normal(0, 10))), 2) for _ in range(len(date_range))]
                return {
                    'label': 'Nursery Capacity Utilization (%)',
                    'dates': date_range,
                    'values': values,
                    'unit': '%',
                    'trend': 'fluctuating'
                }
            elif metric == 'order_fulfillment_rate':
                # Simulate order fulfillment rate (percentage)
                values = [round(min(100, max(80, 90 + np.random.normal(0, 3))), 2) for _ in range(len(date_range))]
                return {
                    'label': 'Order Fulfillment Rate (%)',
                    'dates': date_range,
                    'values': values,
                    'unit': '%',
                    'trend': 'stable'
                }
            elif metric == 'growth_cycle_adherence':
                # Simulate growth cycle adherence (percentage)
                values = [round(min(100, max(70, 85 + np.random.normal(0, 5))), 2) for _ in range(len(date_range))]
                return {
                    'label': 'Growth Cycle Adherence (%)',
                    'dates': date_range,
                    'values': values,
                    'unit': '%',
                    'trend': 'increasing' if values[-1] > values[0] else 'stable'
                }
            elif metric == 'customer_satisfaction':
                # Simulate customer satisfaction (score out of 5)
                values = [round(min(5, max(3, 4.2 + np.random.normal(0, 0.3))), 2) for _ in range(len(date_range))]
                return {
                    'label': 'Customer Satisfaction (out of 5)',
                    'dates': date_range,
                    'values': values,
                    'unit': 'score',
                    'trend': 'stable'
                }
        
        # Default case for unknown metrics
        return {
            'label': metric,
            'dates': date_range,
            'values': [0] * len(date_range),
            'unit': 'unknown',
            'trend': 'unknown'
        }
    
    def _generate_summary(self, report_type: str, metrics_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate summary statistics for a report.
        
        Args:
            report_type: Type of report
            metrics_data: Dictionary with metrics data
            
        Returns:
            Dictionary with summary statistics
        """
        summary = {
            'key_findings': [],
            'trends': [],
            'recommendations': []
        }
        
        # Generate key findings based on report type
        if report_type == 'system_performance':
            # Check model accuracy
            if 'model_accuracy' in metrics_data:
                accuracy_values = metrics_data['model_accuracy']['values']
                avg_accuracy = sum(accuracy_values) / len(accuracy_values)
                if avg_accuracy > 90:
                    summary['key_findings'].append(f"Model accuracy is excellent at {avg_accuracy:.2f}%")
                elif avg_accuracy > 80:
                    summary['key_findings'].append(f"Model accuracy is good at {avg_accuracy:.2f}%")
                else:
                    summary['key_findings'].append(f"Model accuracy needs improvement at {avg_accuracy:.2f}%")
            
            # Check error rate
            if 'error_rate' in metrics_data:
                error_values = metrics_data['error_rate']['values']
                avg_error = sum(error_values) / len(error_values)
                if avg_error < 2:
                    summary['key_findings'].append(f"Error rate is very low at {avg_error:.2f}%")
                elif avg_error < 5:
                    summary['key_findings'].append(f"Error rate is acceptable at {avg_error:.2f}%")
                else:
                    summary['key_findings'].append(f"Error rate is high at {avg_error:.2f}% and needs attention")
            
            # Generate trends
            for metric, data in metrics_data.items():
                if 'trend' in data:
                    trend = data['trend']
                    if trend == 'increasing':
                        if metric in ['model_accuracy', 'system_uptime']:
                            summary['trends'].append(f"{data['label']} is improving")
                        elif metric in ['api_response_time', 'error_rate', 'resource_usage']:
                            summary['trends'].append(f"{data['label']} is increasing, which may be concerning")
                    elif trend == 'decreasing':
                        if metric in ['model_accuracy', 'system_uptime']:
                            summary['trends'].append(f"{data['label']} is declining, which may be concerning")
                        elif metric in ['api_response_time', 'error_rate']:
                            summary['trends'].append(f"{data['label']} is decreasing, which is positive")
            
            # Generate recommendations
            if 'model_accuracy' in metrics_data and metrics_data['model_accuracy']['trend'] == 'decreasing':
                summary['recommendations'].append("Consider retraining models to improve accuracy")
            
            if 'error_rate' in metrics_data and metrics_data['error_rate']['trend'] == 'increasing':
                summary['recommendations'].append("Investigate causes of increasing error rate")
            
            if 'resource_usage' in metrics_data:
                resource_values = metrics_data['resource_usage']['values']
                max_resource = max(resource_values)
                if max_resource > 80:
                    summary['recommendations'].append("Monitor resource usage closely as it's approaching capacity")
        
        elif report_type == 'user_activity':
            # Check active users
            if 'active_users' in metrics_data:
                user_values = metrics_data['active_users']['values']
                avg_users = sum(user_values) / len(user_values)
                trend = metrics_data['active_users']['trend']
                
                if trend == 'increasing':
                    summary['key_findings'].append(f"User base is growing with an average of {avg_users:.0f} active users")
                elif trend == 'decreasing':
                    summary['key_findings'].append(f"User base is shrinking with an average of {avg_users:.0f} active users")
                else:
                    summary['key_findings'].append(f"User base is stable with an average of {avg_users:.0f} active users")
            
            # Check queries per user
            if 'queries_per_user' in metrics_data:
                query_values = metrics_data['queries_per_user']['values']
                avg_queries = sum(query_values) / len(query_values)
                summary['key_findings'].append(f"Users perform an average of {avg_queries:.2f} queries")
            
            # Generate trends
            for metric, data in metrics_data.items():
                if 'trend' in data:
                    trend = data['trend']
                    if trend == 'increasing':
                        summary['trends'].append(f"{data['label']} is increasing")
                    elif trend == 'decreasing':
                        summary['trends'].append(f"{data['label']} is decreasing")
            
            # Generate recommendations
            if 'active_users' in metrics_data and metrics_data['active_users']['trend'] == 'decreasing':
                summary['recommendations'].append("Investigate reasons for declining user engagement")
            
            if 'disease_detections' in metrics_data and 'nutrient_analyses' in metrics_data:
                disease_values = metrics_data['disease_detections']['values']
                nutrient_values = metrics_data['nutrient_analyses']['values']
                
                if sum(disease_values) > sum(nutrient_values) * 2:
                    summary['recommendations'].append("Users are focusing more on disease detection. Consider enhancing nutrient analysis features")
                elif sum(nutrient_values) > sum(disease_values) * 2:
                    summary['recommendations'].append("Users are focusing more on nutrient analysis. Consider enhancing disease detection features")
        
        elif report_type == 'learning_progress':
            # Check model accuracy trend
            if 'model_accuracy_trend' in metrics_data:
                accuracy_values = metrics_data['model_accuracy_trend']['values']
                start_accuracy = accuracy_values[0]
                end_accuracy = accuracy_values[-1]
                
                if end_accuracy > start_accuracy:
                    improvement = end_accuracy - start_accuracy
                    summary['key_findings'].append(f"Model accuracy has improved by {improvement:.2f}% during the period")
                else:
                    decline = start_accuracy - end_accuracy
                    summary['key_findings'].append(f"Model accuracy has declined by {decline:.2f}% during the period")
            
            # Check knowledge base growth
            if 'knowledge_base_growth' in metrics_data:
                kb_values = metrics_data['knowledge_base_growth']['values']
                start_kb = kb_values[0]
                end_kb = kb_values[-1]
                growth = end_kb - start_kb
                
                summary['key_findings'].append(f"Knowledge base has grown by {growth} entries during the period")
            
            # Generate trends
            for metric, data in metrics_data.items():
                if 'trend' in data:
                    trend = data['trend']
                    if trend == 'increasing' and metric in ['model_accuracy_trend', 'data_quality_score', 'knowledge_base_growth']:
                        summary['trends'].append(f"{data['label']} is improving")
                    elif trend == 'decreasing' and metric == 'error_reduction_rate':
                        summary['trends'].append(f"Error rate is decreasing, which is positive")
            
            # Generate recommendations
            if 'data_quality_score' in metrics_data:
                quality_values = metrics_data['data_quality_score']['values']
                avg_quality = sum(quality_values) / len(quality_values)
                
                if avg_quality < 80:
                    summary['recommendations'].append("Improve data quality to enhance learning outcomes")
            
            if 'training_iterations' in metrics_data:
                iteration_values = metrics_data['training_iterations']['values']
                avg_iterations = sum(iteration_values) / len(iteration_values)
                
                if avg_iterations < 3:
                    summary['recommendations'].append("Consider increasing training frequency to improve model performance")
        
        elif report_type == 'database_updates':
            # Check database size
            if 'database_size' in metrics_data:
                size_values = metrics_data['database_size']['values']
                start_size = size_values[0]
                end_size = size_values[-1]
                growth = end_size - start_size
                
                summary['key_findings'].append(f"Database size has increased by {growth:.2f} MB during the period")
            
            # Check records added
            if 'records_added' in metrics_data:
                records_values = metrics_data['records_added']['values']
                total_records = sum(records_values)
                
                summary['key_findings'].append(f"A total of {total_records} records were added during the period")
            
            # Check backup status
            if 'backup_status' in metrics_data:
                backup_values = metrics_data['backup_status']['values']
                success_rate = sum(backup_values) / len(backup_values) * 100
                
                if success_rate < 100:
                    summary['key_findings'].append(f"Backup success rate is {success_rate:.2f}%, with some failures detected")
                else:
                    summary['key_findings'].append(f"All database backups were successful during the period")
            
            # Generate trends
            for metric, data in metrics_data.items():
                if 'trend' in data:
                    trend = data['trend']
                    summary['trends'].append(f"{data['label']} is {trend}")
            
            # Generate recommendations
            if 'query_performance' in metrics_data:
                performance_values = metrics_data['query_performance']['values']
                avg_performance = sum(performance_values) / len(performance_values)
                
                if avg_performance > 200:
                    summary['recommendations'].append("Consider optimizing database queries to improve performance")
            
            if 'backup_status' in metrics_data:
                backup_values = metrics_data['backup_status']['values']
                success_rate = sum(backup_values) / len(backup_values) * 100
                
                if success_rate < 95:
                    summary['recommendations'].append("Investigate and resolve backup failures to ensure data safety")
        
        elif report_type == 'variety_comparison':
            # Check varieties compared
            if 'varieties_compared' in metrics_data:
                variety_values = metrics_data['varieties_compared']['values']
                avg_varieties = sum(variety_values) / len(variety_values)
                
                summary['key_findings'].append(f"An average of {avg_varieties:.1f} varieties were compared per day")
            
            # Check top performing varieties
            if 'top_performing_varieties' in metrics_data:
                varieties = metrics_data['top_performing_varieties']['varieties']
                scores = metrics_data['top_performing_varieties']['scores']
                
                if len(varieties) > 0:
                    summary['key_findings'].append(f"The top performing variety is {varieties[0]} with a score of {scores[0]}")
            
            # Check yield metrics
            if 'yield_metrics' in metrics_data:
                yield_values = metrics_data['yield_metrics']['values']
                avg_yield = sum(yield_values) / len(yield_values)
                
                summary['key_findings'].append(f"Average yield across varieties is {avg_yield:.2f} tons/ha")
            
            # Generate trends
            for metric, data in metrics_data.items():
                if 'trend' in data and data['trend'] != 'not_applicable':
                    trend = data['trend']
                    summary['trends'].append(f"{data['label']} is {trend}")
            
            # Generate recommendations
            if 'top_performing_varieties' in metrics_data:
                varieties = metrics_data['top_performing_varieties']['varieties']
                scores = metrics_data['top_performing_varieties']['scores']
                
                if len(varieties) > 1:
                    summary['recommendations'].append(f"Focus on {varieties[0]} and {varieties[1]} for best results")
            
            if 'comparison_criteria' in metrics_data:
                criteria_values = metrics_data['comparison_criteria']['values']
                avg_criteria = sum(criteria_values) / len(criteria_values)
                
                if avg_criteria < 5:
                    summary['recommendations'].append("Consider adding more comparison criteria for more comprehensive analysis")
        
        elif report_type == 'nursery_management':
            # Check seedling success rate
            if 'seedling_success_rate' in metrics_data:
                success_values = metrics_data['seedling_success_rate']['values']
                avg_success = sum(success_values) / len(success_values)
                
                if avg_success > 90:
                    summary['key_findings'].append(f"Seedling success rate is excellent at {avg_success:.2f}%")
                elif avg_success > 80:
                    summary['key_findings'].append(f"Seedling success rate is good at {avg_success:.2f}%")
                else:
                    summary['key_findings'].append(f"Seedling success rate needs improvement at {avg_success:.2f}%")
            
            # Check nursery capacity utilization
            if 'nursery_capacity_utilization' in metrics_data:
                capacity_values = metrics_data['nursery_capacity_utilization']['values']
                avg_capacity = sum(capacity_values) / len(capacity_values)
                
                if avg_capacity > 90:
                    summary['key_findings'].append(f"Nursery is operating near full capacity at {avg_capacity:.2f}%")
                elif avg_capacity < 60:
                    summary['key_findings'].append(f"Nursery has significant unused capacity at {avg_capacity:.2f}%")
                else:
                    summary['key_findings'].append(f"Nursery capacity utilization is optimal at {avg_capacity:.2f}%")
            
            # Check customer satisfaction
            if 'customer_satisfaction' in metrics_data:
                satisfaction_values = metrics_data['customer_satisfaction']['values']
                avg_satisfaction = sum(satisfaction_values) / len(satisfaction_values)
                
                summary['key_findings'].append(f"Customer satisfaction rating is {avg_satisfaction:.2f} out of 5")
            
            # Generate trends
            for metric, data in metrics_data.items():
                if 'trend' in data:
                    trend = data['trend']
                    summary['trends'].append(f"{data['label']} is {trend}")
            
            # Generate recommendations
            if 'seedling_success_rate' in metrics_data:
                success_values = metrics_data['seedling_success_rate']['values']
                avg_success = sum(success_values) / len(success_values)
                
                if avg_success < 80:
                    summary['recommendations'].append("Review seedling care protocols to improve success rate")
            
            if 'nursery_capacity_utilization' in metrics_data:
                capacity_values = metrics_data['nursery_capacity_utilization']['values']
                avg_capacity = sum(capacity_values) / len(capacity_values)
                
                if avg_capacity > 90:
                    summary['recommendations'].append("Consider expanding nursery capacity to meet demand")
                elif avg_capacity < 60:
                    summary['recommendations'].append("Develop strategies to increase nursery utilization")
            
            if 'order_fulfillment_rate' in metrics_data:
                fulfillment_values = metrics_data['order_fulfillment_rate']['values']
                avg_fulfillment = sum(fulfillment_values) / len(fulfillment_values)
                
                if avg_fulfillment < 90:
                    summary['recommendations'].append("Improve order fulfillment processes to meet customer expectations")
        
        return summary
    
    def _generate_charts(self, report_type: str, report_id: str, 
                        report_data: Dict[str, Any]) -> List[str]:
        """
        Generate charts for a report.
        
        Args:
            report_type: Type of report
            report_id: ID of the report
            report_data: Dictionary with report data
            
        Returns:
            List of chart file paths
        """
        chart_files = []
        
        # Create charts directory for this report
        charts_dir = os.path.join(
            self.config['reporting']['charts_dir'],
            report_type,
            report_id
        )
        os.makedirs(charts_dir, exist_ok=True)
        
        # Generate charts for each metric
        for metric, data in report_data['metrics'].items():
            if 'dates' in data and 'values' in data:
                # Time series chart
                chart_file = os.path.join(charts_dir, f"{metric}_time_series.png")
                
                plt.figure(figsize=(10, 6))
                plt.plot(data['dates'], data['values'])
                plt.title(data['label'])
                plt.xlabel('Date')
                plt.ylabel(data['unit'])
                plt.grid(True)
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.savefig(chart_file)
                plt.close()
                
                chart_files.append(chart_file)
            
            # Special case for top performing varieties
            if metric == 'top_performing_varieties' and 'varieties' in data and 'scores' in data:
                chart_file = os.path.join(charts_dir, f"{metric}_bar_chart.png")
                
                plt.figure(figsize=(10, 6))
                plt.bar(data['varieties'], data['scores'])
                plt.title(data['label'])
                plt.xlabel('Variety')
                plt.ylabel('Score')
                plt.grid(True, axis='y')
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.savefig(chart_file)
                plt.close()
                
                chart_files.append(chart_file)
        
        # Generate summary charts
        if report_type == 'system_performance':
            if 'model_accuracy' in report_data['metrics'] and 'error_rate' in report_data['metrics']:
                chart_file = os.path.join(charts_dir, "accuracy_vs_error.png")
                
                accuracy_data = report_data['metrics']['model_accuracy']
                error_data = report_data['metrics']['error_rate']
                
                plt.figure(figsize=(10, 6))
                plt.plot(accuracy_data['dates'], accuracy_data['values'], label='Accuracy (%)')
                plt.plot(error_data['dates'], error_data['values'], label='Error Rate (%)')
                plt.title('Model Accuracy vs Error Rate')
                plt.xlabel('Date')
                plt.ylabel('Percentage')
                plt.grid(True)
                plt.legend()
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.savefig(chart_file)
                plt.close()
                
                chart_files.append(chart_file)
        
        elif report_type == 'user_activity':
            if 'disease_detections' in report_data['metrics'] and 'nutrient_analyses' in report_data['metrics']:
                chart_file = os.path.join(charts_dir, "detection_vs_analysis.png")
                
                detection_data = report_data['metrics']['disease_detections']
                analysis_data = report_data['metrics']['nutrient_analyses']
                
                plt.figure(figsize=(10, 6))
                plt.plot(detection_data['dates'], detection_data['values'], label='Disease Detections')
                plt.plot(analysis_data['dates'], analysis_data['values'], label='Nutrient Analyses')
                plt.title('Disease Detections vs Nutrient Analyses')
                plt.xlabel('Date')
                plt.ylabel('Count')
                plt.grid(True)
                plt.legend()
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.savefig(chart_file)
                plt.close()
                
                chart_files.append(chart_file)
        
        return chart_files
    
    def _create_report_content(self, report_type: str, report_id: str, 
                              start_date: str, end_date: str, metrics: List[str],
                              report_data: Dict[str, Any], 
                              chart_files: List[str]) -> Dict[str, Any]:
        """
        Create content for a report.
        
        Args:
            report_type: Type of report
            report_id: ID of the report
            start_date: Start date for report data
            end_date: End date for report data
            metrics: List of metrics included
            report_data: Dictionary with report data
            chart_files: List of chart file paths
            
        Returns:
            Dictionary with report content
        """
        # Format dates for display
        start_date_display = datetime.datetime.fromisoformat(start_date).strftime('%Y-%m-%d')
        end_date_display = datetime.datetime.fromisoformat(end_date).strftime('%Y-%m-%d')
        
        # Create report title based on report type
        title_map = {
            'system_performance': 'System Performance Report',
            'user_activity': 'User Activity Report',
            'learning_progress': 'Learning Progress Report',
            'database_updates': 'Database Updates Report',
            'variety_comparison': 'Variety Comparison Report',
            'nursery_management': 'Nursery Management Report'
        }
        
        title = title_map.get(report_type, f"{report_type.replace('_', ' ').title()} Report")
        
        # Create report content
        content = {
            'report_id': report_id,
            'title': title,
            'subtitle': f"Period: {start_date_display} to {end_date_display}",
            'generated_at': datetime.datetime.now().isoformat(),
            'report_type': report_type,
            'start_date': start_date,
            'end_date': end_date,
            'metrics': metrics,
            'summary': report_data['summary'],
            'chart_files': chart_files,
            'data': report_data
        }
        
        return content
    
    def _export_report(self, report_type: str, report_id: str, 
                      report_content: Dict[str, Any], 
                      export_format: str) -> str:
        """
        Export a report to the specified format.
        
        Args:
            report_type: Type of report
            report_id: ID of the report
            report_content: Dictionary with report content
            export_format: Format to export the report in
            
        Returns:
            Path to the exported report file
        """
        # Create reports directory for this report
        reports_dir = os.path.join(
            self.config['reporting']['reports_dir'],
            report_type,
            report_id
        )
        os.makedirs(reports_dir, exist_ok=True)
        
        # Export report based on format
        if export_format == 'json':
            # Export as JSON
            report_file = os.path.join(reports_dir, f"report.json")
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report_content, f, indent=2)
            
            return report_file
        
        elif export_format == 'csv':
            # Export as CSV
            report_file = os.path.join(reports_dir, f"report.csv")
            
            # Flatten data for CSV export
            csv_data = []
            
            # Add header row
            header = ['Date']
            for metric in report_content['metrics']:
                if metric in report_content['data']['metrics']:
                    header.append(report_content['data']['metrics'][metric]['label'])
            
            csv_data.append(header)
            
            # Add data rows
            if len(report_content['data']['metrics']) > 0:
                first_metric = list(report_content['data']['metrics'].keys())[0]
                if 'dates' in report_content['data']['metrics'][first_metric]:
                    dates = report_content['data']['metrics'][first_metric]['dates']
                    
                    for i, date in enumerate(dates):
                        row = [date]
                        
                        for metric in report_content['metrics']:
                            if metric in report_content['data']['metrics'] and 'values' in report_content['data']['metrics'][metric]:
                                values = report_content['data']['metrics'][metric]['values']
                                if i < len(values):
                                    row.append(values[i])
                                else:
                                    row.append('')
                            else:
                                row.append('')
                        
                        csv_data.append(row)
            
            # Write CSV file
            with open(report_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(csv_data)
            
            return report_file
        
        elif export_format == 'html':
            # Export as HTML
            report_file = os.path.join(reports_dir, f"report.html")
            
            # Create HTML content
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{report_content['title']}</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        line-height: 1.6;
                        margin: 0;
                        padding: 20px;
                        color: #333;
                    }}
                    .container {{
                        max-width: 1200px;
                        margin: 0 auto;
                    }}
                    h1, h2, h3 {{
                        color: #2c3e50;
                    }}
                    .subtitle {{
                        color: #7f8c8d;
                        font-size: 1.2em;
                        margin-bottom: 30px;
                    }}
                    .section {{
                        margin-bottom: 30px;
                        border-bottom: 1px solid #eee;
                        padding-bottom: 20px;
                    }}
                    .chart-container {{
                        margin: 20px 0;
                        text-align: center;
                    }}
                    .chart {{
                        max-width: 100%;
                        height: auto;
                    }}
                    table {{
                        width: 100%;
                        border-collapse: collapse;
                        margin: 20px 0;
                    }}
                    th, td {{
                        padding: 12px 15px;
                        border-bottom: 1px solid #ddd;
                        text-align: left;
                    }}
                    th {{
                        background-color: #f8f9fa;
                    }}
                    tr:hover {{
                        background-color: #f5f5f5;
                    }}
                    .summary-item {{
                        margin-bottom: 10px;
                    }}
                    .footer {{
                        margin-top: 50px;
                        text-align: center;
                        color: #7f8c8d;
                        font-size: 0.9em;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>{report_content['title']}</h1>
                    <div class="subtitle">{report_content['subtitle']}</div>
                    
                    <div class="section">
                        <h2>Summary</h2>
                        
                        <h3>Key Findings</h3>
                        <ul>
            """
            
            # Add key findings
            for finding in report_content['summary']['key_findings']:
                html_content += f"            <li class=\"summary-item\">{finding}</li>\n"
            
            html_content += """
                        </ul>
                        
                        <h3>Trends</h3>
                        <ul>
            """
            
            # Add trends
            for trend in report_content['summary']['trends']:
                html_content += f"            <li class=\"summary-item\">{trend}</li>\n"
            
            html_content += """
                        </ul>
                        
                        <h3>Recommendations</h3>
                        <ul>
            """
            
            # Add recommendations
            for recommendation in report_content['summary']['recommendations']:
                html_content += f"            <li class=\"summary-item\">{recommendation}</li>\n"
            
            html_content += """
                        </ul>
                    </div>
                    
                    <div class="section">
                        <h2>Charts</h2>
            """
            
            # Add charts
            for chart_file in report_content['chart_files']:
                chart_name = os.path.basename(chart_file).replace('_', ' ').replace('.png', '')
                chart_name = chart_name.title()
                
                # Get relative path to chart file
                rel_path = os.path.relpath(chart_file, os.path.dirname(report_file))
                
                html_content += f"""
                        <div class="chart-container">
                            <h3>{chart_name}</h3>
                            <img class="chart" src="{rel_path}" alt="{chart_name}">
                        </div>
                """
            
            html_content += """
                    </div>
                    
                    <div class="section">
                        <h2>Metrics</h2>
            """
            
            # Add metrics tables
            for metric, data in report_content['data']['metrics'].items():
                if 'dates' in data and 'values' in data:
                    html_content += f"""
                        <h3>{data['label']}</h3>
                        <table>
                            <thead>
                                <tr>
                                    <th>Date</th>
                                    <th>Value ({data['unit']})</th>
                                </tr>
                            </thead>
                            <tbody>
                    """
                    
                    for i, date in enumerate(data['dates']):
                        if i < len(data['values']):
                            html_content += f"""
                                <tr>
                                    <td>{date}</td>
                                    <td>{data['values'][i]}</td>
                                </tr>
                            """
                    
                    html_content += """
                            </tbody>
                        </table>
                    """
                
                # Special case for top performing varieties
                elif metric == 'top_performing_varieties' and 'varieties' in data and 'scores' in data:
                    html_content += f"""
                        <h3>{data['label']}</h3>
                        <table>
                            <thead>
                                <tr>
                                    <th>Variety</th>
                                    <th>Score</th>
                                </tr>
                            </thead>
                            <tbody>
                    """
                    
                    for i, variety in enumerate(data['varieties']):
                        if i < len(data['scores']):
                            html_content += f"""
                                <tr>
                                    <td>{variety}</td>
                                    <td>{data['scores'][i]}</td>
                                </tr>
                            """
                    
                    html_content += """
                            </tbody>
                        </table>
                    """
            
            html_content += f"""
                    </div>
                    
                    <div class="footer">
                        <p>Report generated at: {datetime.datetime.fromisoformat(report_content['generated_at']).strftime('%Y-%m-%d %H:%M:%S')}</p>
                        <p>Report ID: {report_content['report_id']}</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Write HTML file
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return report_file
        
        elif export_format == 'pdf':
            # For PDF export, we'll first create an HTML file and then convert it to PDF
            # In a real implementation, you would use a library like WeasyPrint or ReportLab
            # For this example, we'll just create an HTML file with a note
            
            html_file = self._export_report(report_type, report_id, report_content, 'html')
            
            # In a real implementation, convert HTML to PDF here
            # For this example, we'll just create a PDF file with a note
            report_file = os.path.join(reports_dir, f"report.pdf")
            
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(f"This is a placeholder for a PDF report. In a real implementation, the HTML report would be converted to PDF.\n\n")
                f.write(f"Please refer to the HTML report at: {html_file}\n")
            
            return report_file
        
        else:
            # Default to JSON
            return self._export_report(report_type, report_id, report_content, 'json')
    
    def list_reports(self, user_info: Dict[str, Any], report_type: Optional[str] = None,
                    limit: Optional[int] = 10) -> Dict[str, Any]:
        """
        List available reports.
        
        Args:
            user_info: Information about the user
            report_type: Optional type of reports to list
            limit: Optional maximum number of reports to return
            
        Returns:
            Dictionary with list of reports
        """
        try:
            reports = []
            
            # Get reports directory
            reports_dir = self.config['reporting']['reports_dir']
            
            # If report type is specified, only list reports of that type
            if report_type:
                if report_type not in self.config['reporting']['report_types']:
                    return {
                        'success': False,
                        'error': f"Invalid report type: {report_type}"
                    }
                
                report_types = [report_type]
            else:
                # List all report types
                report_types = list(self.config['reporting']['report_types'].keys())
            
            # Get reports for each type
            for rt in report_types:
                rt_dir = os.path.join(reports_dir, rt)
                
                if os.path.exists(rt_dir):
                    # Get report IDs (directory names)
                    report_ids = [d for d in os.listdir(rt_dir) if os.path.isdir(os.path.join(rt_dir, d))]
                    
                    for report_id in report_ids:
                        # Check if report has a JSON file
                        json_file = os.path.join(rt_dir, report_id, 'report.json')
                        
                        if os.path.exists(json_file):
                            # Get report metadata
                            with open(json_file, 'r', encoding='utf-8') as f:
                                report_data = json.load(f)
                            
                            # Add report to list
                            reports.append({
                                'id': report_id,
                                'type': rt,
                                'title': report_data.get('title', ''),
                                'subtitle': report_data.get('subtitle', ''),
                                'generated_at': report_data.get('generated_at', ''),
                                'formats': self._get_available_formats(rt, report_id)
                            })
            
            # Sort reports by generation time (newest first)
            reports.sort(key=lambda x: x['generated_at'], reverse=True)
            
            # Apply limit
            if limit:
                reports = reports[:limit]
            
            return {
                'success': True,
                'reports': reports
            }
            
        except Exception as e:
            logger.error(f"Error listing reports: {e}")
            return {
                'success': False,
                'error': f"Error listing reports: {str(e)}"
            }
    
    def _get_available_formats(self, report_type: str, report_id: str) -> List[str]:
        """
        Get available formats for a report.
        
        Args:
            report_type: Type of report
            report_id: ID of the report
            
        Returns:
            List of available formats
        """
        formats = []
        
        # Check each format
        for fmt in self.config['reporting']['export_formats']:
            report_file = os.path.join(
                self.config['reporting']['reports_dir'],
                report_type,
                report_id,
                f"report.{fmt}"
            )
            
            if os.path.exists(report_file):
                formats.append(fmt)
        
        return formats
    
    def get_report(self, user_info: Dict[str, Any], report_type: str, report_id: str,
                 export_format: str = 'pdf') -> Dict[str, Any]:
        """
        Get a specific report.
        
        Args:
            user_info: Information about the user
            report_type: Type of report
            report_id: ID of the report
            export_format: Format to get the report in
            
        Returns:
            Dictionary with report information
        """
        try:
            # Check if report type is valid
            if report_type not in self.config['reporting']['report_types']:
                return {
                    'success': False,
                    'error': f"Invalid report type: {report_type}"
                }
            
            # Check if export format is valid
            if export_format not in self.config['reporting']['export_formats']:
                return {
                    'success': False,
                    'error': f"Invalid export format: {export_format}"
                }
            
            # Check if report exists
            report_dir = os.path.join(
                self.config['reporting']['reports_dir'],
                report_type,
                report_id
            )
            
            if not os.path.exists(report_dir):
                return {
                    'success': False,
                    'error': f"Report not found: {report_id}"
                }
            
            # Check if report is available in requested format
            report_file = os.path.join(report_dir, f"report.{export_format}")
            
            if not os.path.exists(report_file):
                # Try to export to requested format
                json_file = os.path.join(report_dir, 'report.json')
                
                if os.path.exists(json_file):
                    # Load report content
                    with open(json_file, 'r', encoding='utf-8') as f:
                        report_content = json.load(f)
                    
                    # Export to requested format
                    report_file = self._export_report(
                        report_type, report_id, report_content, export_format
                    )
                else:
                    return {
                        'success': False,
                        'error': f"Report not available in format: {export_format}"
                    }
            
            # Get report metadata
            json_file = os.path.join(report_dir, 'report.json')
            
            if os.path.exists(json_file):
                with open(json_file, 'r', encoding='utf-8') as f:
                    report_data = json.load(f)
                
                # Log the action
                if self.audit_manager:
                    self.audit_manager.log_action(
                        action_type="REPORTING",
                        action="get_report",
                        component="reporting",
                        user_info=user_info,
                        details={
                            "report_id": report_id,
                            "report_type": report_type,
                            "export_format": export_format
                        },
                        status="success"
                    )
                
                return {
                    'success': True,
                    'report_file': report_file,
                    'report_id': report_id,
                    'report_type': report_type,
                    'title': report_data.get('title', ''),
                    'subtitle': report_data.get('subtitle', ''),
                    'generated_at': report_data.get('generated_at', ''),
                    'export_format': export_format
                }
            else:
                return {
                    'success': False,
                    'error': f"Report metadata not found"
                }
            
        except Exception as e:
            logger.error(f"Error getting report: {e}")
            
            # Log the error
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="REPORTING",
                    action="get_report",
                    component="reporting",
                    user_info=user_info,
                    details={
                        "report_id": report_id,
                        "report_type": report_type,
                        "error": str(e)
                    },
                    status="error"
                )
            
            return {
                'success': False,
                'error': f"Error getting report: {str(e)}"
            }
    
    def schedule_report(self, user_info: Dict[str, Any], report_type: str, 
                       name: str, frequency: str, recipients: List[str],
                       day: Optional[Union[str, int]] = None, 
                       time: str = '00:00',
                       export_format: str = 'pdf',
                       metrics: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Schedule a report for automatic generation.
        
        Args:
            user_info: Information about the user
            report_type: Type of report to generate
            name: Name of the scheduled report
            frequency: Frequency of report generation (daily, weekly, monthly)
            recipients: List of recipient user IDs or roles
            day: Day for weekly (Monday, Tuesday, etc.) or monthly (1-31) reports
            time: Time of day to generate report (HH:MM)
            export_format: Format to export the report in
            metrics: Optional list of metrics to include
            
        Returns:
            Dictionary with scheduling result
        """
        try:
            # Check if user is admin
            if user_info.get('role') != 'admin':
                return {
                    'success': False,
                    'error': "Only admin users can schedule reports"
                }
            
            # Check if report type is valid
            if report_type not in self.config['reporting']['report_types']:
                return {
                    'success': False,
                    'error': f"Invalid report type: {report_type}"
                }
            
            # Check if report type is enabled
            if not self.config['reporting']['report_types'][report_type]['enabled']:
                return {
                    'success': False,
                    'error': f"Report type '{report_type}' is disabled"
                }
            
            # Check if frequency is valid
            valid_frequencies = ['daily', 'weekly', 'monthly']
            if frequency not in valid_frequencies:
                return {
                    'success': False,
                    'error': f"Invalid frequency: {frequency}. Must be one of {valid_frequencies}"
                }
            
            # Check day parameter
            if frequency == 'weekly':
                valid_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                if not day or day not in valid_days:
                    return {
                        'success': False,
                        'error': f"Invalid day for weekly report: {day}. Must be one of {valid_days}"
                    }
            elif frequency == 'monthly':
                if not day or not isinstance(day, int) or day < 1 or day > 31:
                    return {
                        'success': False,
                        'error': f"Invalid day for monthly report: {day}. Must be between 1 and 31"
                    }
            
            # Check time format
            try:
                hour, minute = time.split(':')
                hour = int(hour)
                minute = int(minute)
                
                if hour < 0 or hour > 23 or minute < 0 or minute > 59:
                    raise ValueError()
            except:
                return {
                    'success': False,
                    'error': f"Invalid time format: {time}. Must be in format HH:MM"
                }
            
            # Check if export format is valid
            if export_format not in self.config['reporting']['export_formats']:
                return {
                    'success': False,
                    'error': f"Invalid export format: {export_format}"
                }
            
            # Check if metrics are valid
            if metrics:
                valid_metrics = self.config['reporting']['report_types'][report_type]['default_metrics']
                for metric in metrics:
                    if metric not in valid_metrics:
                        return {
                            'success': False,
                            'error': f"Invalid metric: {metric}. Valid metrics for {report_type} are {valid_metrics}"
                        }
            
            # Create scheduled report
            scheduled_report = {
                'name': name,
                'type': report_type,
                'frequency': frequency,
                'time': time,
                'recipients': recipients,
                'format': export_format
            }
            
            if day:
                scheduled_report['day'] = day
            
            if metrics:
                scheduled_report['metrics'] = metrics
            
            # Add to scheduled reports
            self.config['reporting']['scheduled_reports'].append(scheduled_report)
            
            # Save configuration
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)
            
            # Log the action
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="REPORTING",
                    action="schedule_report",
                    component="reporting",
                    user_info=user_info,
                    details={
                        "name": name,
                        "report_type": report_type,
                        "frequency": frequency
                    },
                    status="success"
                )
            
            return {
                'success': True,
                'message': f"Report '{name}' scheduled successfully"
            }
            
        except Exception as e:
            logger.error(f"Error scheduling report: {e}")
            
            # Log the error
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="REPORTING",
                    action="schedule_report",
                    component="reporting",
                    user_info=user_info,
                    details={"error": str(e)},
                    status="error"
                )
            
            return {
                'success': False,
                'error': f"Error scheduling report: {str(e)}"
            }
    
    def list_scheduled_reports(self, user_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        List scheduled reports.
        
        Args:
            user_info: Information about the user
            
        Returns:
            Dictionary with list of scheduled reports
        """
        try:
            # Check if user is admin
            if user_info.get('role') != 'admin':
                return {
                    'success': False,
                    'error': "Only admin users can view scheduled reports"
                }
            
            return {
                'success': True,
                'scheduled_reports': self.config['reporting']['scheduled_reports']
            }
            
        except Exception as e:
            logger.error(f"Error listing scheduled reports: {e}")
            return {
                'success': False,
                'error': f"Error listing scheduled reports: {str(e)}"
            }
    
    def delete_scheduled_report(self, user_info: Dict[str, Any], report_name: str) -> Dict[str, Any]:
        """
        Delete a scheduled report.
        
        Args:
            user_info: Information about the user
            report_name: Name of the scheduled report to delete
            
        Returns:
            Dictionary with deletion result
        """
        try:
            # Check if user is admin
            if user_info.get('role') != 'admin':
                return {
                    'success': False,
                    'error': "Only admin users can delete scheduled reports"
                }
            
            # Find report by name
            for i, report in enumerate(self.config['reporting']['scheduled_reports']):
                if report['name'] == report_name:
                    # Remove report
                    del self.config['reporting']['scheduled_reports'][i]
                    
                    # Save configuration
                    with open(self.config_path, 'w', encoding='utf-8') as f:
                        json.dump(self.config, f, indent=2)
                    
                    # Log the action
                    if self.audit_manager:
                        self.audit_manager.log_action(
                            action_type="REPORTING",
                            action="delete_scheduled_report",
                            component="reporting",
                            user_info=user_info,
                            details={"name": report_name},
                            status="success"
                        )
                    
                    return {
                        'success': True,
                        'message': f"Scheduled report '{report_name}' deleted successfully"
                    }
            
            return {
                'success': False,
                'error': f"Scheduled report '{report_name}' not found"
            }
            
        except Exception as e:
            logger.error(f"Error deleting scheduled report: {e}")
            
            # Log the error
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="REPORTING",
                    action="delete_scheduled_report",
                    component="reporting",
                    user_info=user_info,
                    details={"name": report_name, "error": str(e)},
                    status="error"
                )
            
            return {
                'success': False,
                'error': f"Error deleting scheduled report: {str(e)}"
            }
    
    def run_scheduled_reports(self) -> Dict[str, Any]:
        """
        Run scheduled reports that are due.
        This method would typically be called by a scheduler.
        
        Returns:
            Dictionary with execution results
        """
        try:
            now = datetime.datetime.now()
            current_time = now.strftime('%H:%M')
            current_day_of_week = now.strftime('%A')
            current_day_of_month = now.day
            
            results = {
                'success': True,
                'reports_generated': [],
                'reports_failed': []
            }
            
            # Check each scheduled report
            for report in self.config['reporting']['scheduled_reports']:
                try:
                    # Check if report is due
                    if report['time'] == current_time:
                        if report['frequency'] == 'daily':
                            # Daily report is due
                            self._run_scheduled_report(report, results)
                        elif report['frequency'] == 'weekly' and report.get('day') == current_day_of_week:
                            # Weekly report is due
                            self._run_scheduled_report(report, results)
                        elif report['frequency'] == 'monthly' and report.get('day') == current_day_of_month:
                            # Monthly report is due
                            self._run_scheduled_report(report, results)
                except Exception as e:
                    logger.error(f"Error running scheduled report '{report.get('name')}': {e}")
                    results['reports_failed'].append({
                        'name': report.get('name'),
                        'error': str(e)
                    })
            
            return results
            
        except Exception as e:
            logger.error(f"Error running scheduled reports: {e}")
            return {
                'success': False,
                'error': f"Error running scheduled reports: {str(e)}"
            }
    
    def _run_scheduled_report(self, report: Dict[str, Any], results: Dict[str, Any]):
        """
        Run a specific scheduled report.
        
        Args:
            report: Scheduled report configuration
            results: Results dictionary to update
        """
        # Set date range
        end_date = datetime.datetime.now().isoformat()
        
        if report['frequency'] == 'daily':
            # Last 24 hours
            start_date = (datetime.datetime.now() - datetime.timedelta(days=1)).isoformat()
        elif report['frequency'] == 'weekly':
            # Last 7 days
            start_date = (datetime.datetime.now() - datetime.timedelta(days=7)).isoformat()
        elif report['frequency'] == 'monthly':
            # Last 30 days
            start_date = (datetime.datetime.now() - datetime.timedelta(days=30)).isoformat()
        else:
            # Default to last 30 days
            start_date = (datetime.datetime.now() - datetime.timedelta(days=30)).isoformat()
        
        # Generate report
        result = self.generate_report(
            user_info={'id': 'system', 'role': 'admin'},
            report_type=report['type'],
            start_date=start_date,
            end_date=end_date,
            metrics=report.get('metrics'),
            export_format=report['format']
        )
        
        if result.get('success', False):
            # Report generated successfully
            results['reports_generated'].append({
                'name': report['name'],
                'report_id': result['report_id'],
                'report_file': result['report_file']
            })
            
            # Distribute report to recipients
            # In a real implementation, this would send emails or notifications
            # For this example, we'll just log it
            logger.info(f"Report '{report['name']}' (ID: {result['report_id']}) would be distributed to: {report['recipients']}")
        else:
            # Report generation failed
            results['reports_failed'].append({
                'name': report['name'],
                'error': result.get('error', 'Unknown error')
            })
