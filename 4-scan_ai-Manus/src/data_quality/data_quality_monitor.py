#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data quality control module for the Agricultural AI System.

This module monitors data quality, detects data drift, and manages learning processes
to ensure model integrity and prevent training on corrupted or low-quality data.
"""

import os
import json
import logging
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import shutil
import hashlib
import threading
import time
from sklearn.metrics import mean_squared_error
from scipy.stats import wasserstein_distance
import matplotlib.pyplot as plt
import seaborn as sns

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('data_quality')

class DataQualityMonitor:
    """
    Monitors data quality and detects drift in training and inference data.
    
    This class provides methods to:
    1. Monitor data quality metrics
    2. Detect data drift beyond acceptable thresholds
    3. Pause learning processes when drift exceeds limits
    4. Save daily snapshots of learning results
    5. Manage data versioning for rollback capabilities
    """
    
    def __init__(self, config=None):
        """
        Initialize the data quality monitor.
        
        Args:
            config (dict): Configuration dictionary with thresholds and settings
        """
        self.config = config or {}
        
        # Default configuration
        self.default_config = {
            'max_drift_percentage': 5.0,  # Maximum allowed drift (5%)
            'drift_check_interval': 3600,  # Check drift every hour (seconds)
            'daily_snapshot_time': "00:00",  # Time to take daily snapshots (HH:MM)
            'snapshot_base_dir': 'data/snapshots',  # Directory for snapshots
            'reference_data_dir': 'data/reference_datasets',  # Reference data directory
            'metrics_history_size': 100,  # Number of metrics history points to keep
            'pause_learning_on_drift': True,  # Whether to pause learning when drift exceeds threshold
            'notification_channels': ['log'],  # Channels for notifications (log, email, etc.)
        }
        
        # Merge with provided config
        for key, value in self.default_config.items():
            if key not in self.config:
                self.config[key] = value
        
        # Create necessary directories
        os.makedirs(self.config['snapshot_base_dir'], exist_ok=True)
        
        # Initialize state
        self.reference_distributions = {}  # Baseline distributions for drift detection
        self.current_distributions = {}  # Current distributions for comparison
        self.drift_metrics = {}  # Drift metrics history
        self.learning_paused = False  # Whether learning is currently paused
        self.pause_reason = None  # Reason for pausing learning
        
        # Thread control
        self.monitoring_active = False
        self.monitoring_thread = None
        
        logger.info("Data quality monitor initialized")
    
    def start_monitoring(self):
        """Start the data quality monitoring thread."""
        if self.monitoring_active:
            logger.warning("Data quality monitoring is already active")
            return
        
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        logger.info("Data quality monitoring started")
    
    def stop_monitoring(self):
        """Stop the data quality monitoring thread."""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5.0)
            logger.info("Data quality monitoring stopped")
    
    def _monitoring_loop(self):
        """Main monitoring loop that runs in a separate thread."""
        last_drift_check = 0
        last_snapshot_day = datetime.now().day
        
        while self.monitoring_active:
            current_time = time.time()
            now = datetime.now()
            
            # Check for data drift
            if current_time - last_drift_check >= self.config['drift_check_interval']:
                self._check_data_drift()
                last_drift_check = current_time
            
            # Take daily snapshot if it's time
            snapshot_time = self.config['daily_snapshot_time'].split(':')
            snapshot_hour = int(snapshot_time[0])
            snapshot_minute = int(snapshot_time[1])
            
            if (now.day != last_snapshot_day and 
                now.hour == snapshot_hour and 
                now.minute == snapshot_minute):
                self._take_daily_snapshot()
                last_snapshot_day = now.day
            
            # Sleep to avoid high CPU usage
            time.sleep(60)  # Check every minute
    
    def set_reference_distribution(self, feature_name, distribution_data, metadata=None):
        """
        Set a reference distribution for a feature to use as baseline for drift detection.
        
        Args:
            feature_name (str): Name of the feature
            distribution_data (array-like): Distribution data (values or histogram)
            metadata (dict): Additional metadata about the distribution
        """
        self.reference_distributions[feature_name] = {
            'data': np.array(distribution_data),
            'metadata': metadata or {},
            'timestamp': datetime.now().isoformat()
        }
        logger.info(f"Reference distribution set for feature: {feature_name}")
    
    def update_current_distribution(self, feature_name, distribution_data, metadata=None):
        """
        Update the current distribution for a feature for drift comparison.
        
        Args:
            feature_name (str): Name of the feature
            distribution_data (array-like): Distribution data (values or histogram)
            metadata (dict): Additional metadata about the distribution
        """
        self.current_distributions[feature_name] = {
            'data': np.array(distribution_data),
            'metadata': metadata or {},
            'timestamp': datetime.now().isoformat()
        }
    
    def _check_data_drift(self):
        """
        Check for data drift by comparing current distributions to reference distributions.
        
        This method calculates drift metrics for each feature and determines if
        any exceed the configured threshold.
        """
        drift_detected = False
        max_drift_percentage = 0.0
        drifted_features = []
        
        for feature_name, ref_dist in self.reference_distributions.items():
            if feature_name not in self.current_distributions:
                logger.warning(f"No current distribution available for feature: {feature_name}")
                continue
            
            curr_dist = self.current_distributions[feature_name]
            
            # Calculate drift metric (Wasserstein distance)
            try:
                # Normalize distributions if they have different scales
                ref_data = ref_dist['data']
                curr_data = curr_dist['data']
                
                # If histograms, ensure they have the same bins
                if 'bins' in ref_dist['metadata'] and 'bins' in curr_dist['metadata']:
                    if not np.array_equal(ref_dist['metadata']['bins'], curr_dist['metadata']['bins']):
                        logger.warning(f"Histogram bins don't match for feature: {feature_name}")
                        continue
                
                # Calculate Wasserstein distance (Earth Mover's Distance)
                drift = wasserstein_distance(ref_data, curr_data)
                
                # Normalize to percentage based on reference distribution range
                ref_range = np.max(ref_data) - np.min(ref_data)
                if ref_range > 0:
                    drift_percentage = (drift / ref_range) * 100.0
                else:
                    drift_percentage = 0.0
                
                # Store drift metric
                timestamp = datetime.now().isoformat()
                if feature_name not in self.drift_metrics:
                    self.drift_metrics[feature_name] = []
                
                self.drift_metrics[feature_name].append({
                    'timestamp': timestamp,
                    'drift': drift,
                    'drift_percentage': drift_percentage
                })
                
                # Trim history if needed
                if len(self.drift_metrics[feature_name]) > self.config['metrics_history_size']:
                    self.drift_metrics[feature_name] = self.drift_metrics[feature_name][-self.config['metrics_history_size']:]
                
                # Check if drift exceeds threshold
                if drift_percentage > self.config['max_drift_percentage']:
                    drift_detected = True
                    drifted_features.append(feature_name)
                    max_drift_percentage = max(max_drift_percentage, drift_percentage)
                
                logger.debug(f"Drift for {feature_name}: {drift_percentage:.2f}%")
                
            except Exception as e:
                logger.error(f"Error calculating drift for feature {feature_name}: {e}")
        
        # Handle drift if detected
        if drift_detected:
            self._handle_drift_detection(max_drift_percentage, drifted_features)
        elif self.learning_paused and self.pause_reason == "data_drift":
            # Auto-resume if drift is back within limits
            self._resume_learning("Data drift is now within acceptable limits")
    
    def _handle_drift_detection(self, max_drift_percentage, drifted_features):
        """
        Handle detected data drift by pausing learning and sending notifications.
        
        Args:
            max_drift_percentage (float): Maximum drift percentage detected
            drifted_features (list): List of features that exceeded the drift threshold
        """
        message = (f"Data drift detected! Maximum drift: {max_drift_percentage:.2f}% "
                  f"(threshold: {self.config['max_drift_percentage']}%). "
                  f"Affected features: {', '.join(drifted_features)}")
        
        logger.warning(message)
        
        # Pause learning if configured to do so
        if self.config['pause_learning_on_drift'] and not self.learning_paused:
            self._pause_learning("data_drift", message)
        
        # Send notifications through configured channels
        self._send_notifications("DATA_DRIFT_ALERT", message)
        
        # Generate and save drift visualization
        self._generate_drift_visualization(drifted_features)
    
    def _pause_learning(self, reason, message):
        """
        Pause the learning process.
        
        Args:
            reason (str): Reason for pausing (e.g., "data_drift")
            message (str): Detailed message explaining the pause
        """
        self.learning_paused = True
        self.pause_reason = reason
        
        pause_info = {
            'timestamp': datetime.now().isoformat(),
            'reason': reason,
            'message': message
        }
        
        # Save pause info to file for persistence
        pause_file = os.path.join(self.config['snapshot_base_dir'], 'learning_pause.json')
        with open(pause_file, 'w') as f:
            json.dump(pause_info, f, indent=2)
        
        logger.warning(f"Learning paused: {message}")
        
        # Send notifications
        self._send_notifications("LEARNING_PAUSED", message)
    
    def _resume_learning(self, message):
        """
        Resume the learning process.
        
        Args:
            message (str): Message explaining why learning is being resumed
        """
        self.learning_paused = False
        self.pause_reason = None
        
        # Remove pause file if it exists
        pause_file = os.path.join(self.config['snapshot_base_dir'], 'learning_pause.json')
        if os.path.exists(pause_file):
            os.remove(pause_file)
        
        logger.info(f"Learning resumed: {message}")
        
        # Send notifications
        self._send_notifications("LEARNING_RESUMED", message)
    
    def is_learning_paused(self):
        """
        Check if learning is currently paused.
        
        Returns:
            tuple: (is_paused, reason, message)
        """
        if not self.learning_paused:
            return False, None, None
        
        # Check pause file for details
        pause_file = os.path.join(self.config['snapshot_base_dir'], 'learning_pause.json')
        if os.path.exists(pause_file):
            try:
                with open(pause_file, 'r') as f:
                    pause_info = json.load(f)
                return True, pause_info.get('reason'), pause_info.get('message')
            except Exception as e:
                logger.error(f"Error reading pause file: {e}")
        
        return True, self.pause_reason, "Unknown reason"
    
    def manually_resume_learning(self, approver_id, comment):
        """
        Manually resume learning after approval.
        
        Args:
            approver_id (str): ID of the person approving the resume
            comment (str): Comment explaining the approval
            
        Returns:
            bool: Whether the resume was successful
        """
        if not self.learning_paused:
            logger.warning("Cannot resume learning: Learning is not paused")
            return False
        
        message = f"Learning manually resumed by {approver_id}. Comment: {comment}"
        self._resume_learning(message)
        
        # Log the manual resume
        resume_log = {
            'timestamp': datetime.now().isoformat(),
            'approver_id': approver_id,
            'comment': comment,
            'previous_pause_reason': self.pause_reason
        }
        
        # Append to resume log
        resume_log_file = os.path.join(self.config['snapshot_base_dir'], 'manual_resumes.json')
        
        try:
            if os.path.exists(resume_log_file):
                with open(resume_log_file, 'r') as f:
                    logs = json.load(f)
            else:
                logs = []
            
            logs.append(resume_log)
            
            with open(resume_log_file, 'w') as f:
                json.dump(logs, f, indent=2)
        except Exception as e:
            logger.error(f"Error updating resume log: {e}")
        
        return True
    
    def _take_daily_snapshot(self):
        """
        Take a daily snapshot of learning results and data.
        
        This creates a timestamped directory with:
        1. Current model state
        2. Sample of current data
        3. Drift metrics
        4. Performance metrics
        """
        timestamp = datetime.now().strftime("%Y%m%d")
        snapshot_dir = os.path.join(self.config['snapshot_base_dir'], f"snapshot_{timestamp}")
        
        try:
            os.makedirs(snapshot_dir, exist_ok=True)
            
            # Save drift metrics
            drift_file = os.path.join(snapshot_dir, "drift_metrics.json")
            with open(drift_file, 'w') as f:
                json.dump(self.drift_metrics, f, indent=2)
            
            # Save current distributions
            distributions_file = os.path.join(snapshot_dir, "current_distributions.json")
            
            # Convert numpy arrays to lists for JSON serialization
            serializable_distributions = {}
            for feature, dist in self.current_distributions.items():
                serializable_distributions[feature] = {
                    'data': dist['data'].tolist(),
                    'metadata': dist['metadata'],
                    'timestamp': dist['timestamp']
                }
            
            with open(distributions_file, 'w') as f:
                json.dump(serializable_distributions, f, indent=2)
            
            # Create a metadata file with snapshot info
            metadata = {
                'timestamp': datetime.now().isoformat(),
                'learning_paused': self.learning_paused,
                'pause_reason': self.pause_reason,
                'features_monitored': list(self.reference_distributions.keys())
            }
            
            metadata_file = os.path.join(snapshot_dir, "metadata.json")
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            logger.info(f"Daily snapshot taken: {snapshot_dir}")
            
            # Note: The actual model state and data samples would be saved by
            # the model training module, which would call a method in this class
            # to get the snapshot directory path.
            
            return snapshot_dir
            
        except Exception as e:
            logger.error(f"Error taking daily snapshot: {e}")
            return None
    
    def get_latest_snapshot_dir(self):
        """
        Get the path to the latest snapshot directory.
        
        Returns:
            str: Path to the latest snapshot directory, or None if none exists
        """
        try:
            snapshot_dirs = [d for d in os.listdir(self.config['snapshot_base_dir']) 
                           if d.startswith("snapshot_")]
            
            if not snapshot_dirs:
                return None
            
            # Sort by name (which includes timestamp)
            snapshot_dirs.sort(reverse=True)
            return os.path.join(self.config['snapshot_base_dir'], snapshot_dirs[0])
            
        except Exception as e:
            logger.error(f"Error getting latest snapshot directory: {e}")
            return None
    
    def list_available_snapshots(self):
        """
        List all available snapshots with their timestamps.
        
        Returns:
            list: List of dictionaries with snapshot info
        """
        try:
            snapshot_dirs = [d for d in os.listdir(self.config['snapshot_base_dir']) 
                           if d.startswith("snapshot_")]
            
            snapshots = []
            for dir_name in snapshot_dirs:
                # Extract timestamp from directory name
                timestamp_str = dir_name.replace("snapshot_", "")
                
                # Try to parse metadata for additional info
                metadata_file = os.path.join(self.config['snapshot_base_dir'], dir_name, "metadata.json")
                metadata = {}
                
                if os.path.exists(metadata_file):
                    try:
                        with open(metadata_file, 'r') as f:
                            metadata = json.load(f)
                    except Exception:
                        pass
                
                snapshots.append({
                    'directory': dir_name,
                    'date': timestamp_str,
                    'path': os.path.join(self.config['snapshot_base_dir'], dir_name),
                    'metadata': metadata
                })
            
            # Sort by date (newest first)
            snapshots.sort(key=lambda x: x['date'], reverse=True)
            return snapshots
            
        except Exception as e:
            logger.error(f"Error listing snapshots: {e}")
            return []
    
    def restore_from_snapshot(self, snapshot_id, target_dir=None):
        """
        Restore data and model state from a snapshot.
        
        Args:
            snapshot_id (str): Snapshot ID or directory name
            target_dir (str): Target directory for restoration (if None, use default)
            
        Returns:
            bool: Whether the restoration was successful
        """
        # Find the snapshot directory
        if snapshot_id.startswith("snapshot_"):
            snapshot_dir = os.path.join(self.config['snapshot_base_dir'], snapshot_id)
        else:
            # Assume it's a date in YYYYMMDD format
            snapshot_dir = os.path.join(self.config['snapshot_base_dir'], f"snapshot_{snapshot_id}")
        
        if not os.path.exists(snapshot_dir):
            logger.error(f"Snapshot directory not found: {snapshot_dir}")
            return False
        
        try:
            # Load drift metrics
            drift_file = os.path.join(snapshot_dir, "drift_metrics.json")
            if os.path.exists(drift_file):
                with open(drift_file, 'r') as f:
                    self.drift_metrics = json.load(f)
            
            # Load distributions
            distributions_file = os.path.join(snapshot_dir, "current_distributions.json")
            if os.path.exists(distributions_file):
                with open(distributions_file, 'r') as f:
                    serialized_distributions = json.load(f)
                
                # Convert lists back to numpy arrays
                for feature, dist in serialized_distributions.items():
                    self.current_distributions[feature] = {
                        'data': np.array(dist['data']),
                        'metadata': dist['metadata'],
                        'timestamp': dist['timestamp']
                    }
            
            logger.info(f"Restored monitoring state from snapshot: {snapshot_id}")
            
            # Note: The actual model state and data restoration would be handled
            # by the model training module, which would use the snapshot directory
            # path to find the necessary files.
            
            return True
            
        except Exception as e:
            logger.error(f"Error restoring from snapshot: {e}")
            return False
    
    def _generate_drift_visualization(self, drifted_features):
        """
        Generate visualizations of the detected drift.
        
        Args:
            drifted_features (list): List of features that exceeded the drift threshold
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            vis_dir = os.path.join(self.config['snapshot_base_dir'], "visualizations")
            os.makedirs(vis_dir, exist_ok=True)
            
            for feature in drifted_features:
                if feature not in self.reference_distributions or feature not in self.current_distributions:
                    continue
                
                ref_dist = self.reference_distributions[feature]['data']
                curr_dist = self.current_distributions[feature]['data']
                
                plt.figure(figsize=(10, 6))
                
                # Plot distributions
                sns.kdeplot(ref_dist, label="Reference", color="blue")
                sns.kdeplot(curr_dist, label="Current", color="red")
                
                plt.title(f"Distribution Drift: {feature}")
                plt.xlabel("Value")
                plt.ylabel("Density")
                plt.legend()
                
                # Save figure
                fig_path = os.path.join(vis_dir, f"drift_{feature}_{timestamp}.png")
                plt.savefig(fig_path)
                plt.close()
                
                logger.info(f"Drift visualization saved: {fig_path}")
                
                # Also create a time series of drift metrics if available
                if feature in self.drift_metrics and len(self.drift_metrics[feature]) > 1:
                    plt.figure(figsize=(10, 6))
                    
                    timestamps = [datetime.fromisoformat(m['timestamp']) for m in self.drift_metrics[feature]]
                    drift_values = [m['drift_percentage'] for m in self.drift_metrics[feature]]
                    
                    plt.plot(timestamps, drift_values, marker='o')
                    plt.axhline(y=self.config['max_drift_percentage'], color='r', linestyle='--', 
                               label=f"Threshold ({self.config['max_drift_percentage']}%)")
                    
                    plt.title(f"Drift History: {feature}")
                    plt.xlabel("Time")
                    plt.ylabel("Drift (%)")
                    plt.legend()
                    plt.grid(True)
                    
                    # Save figure
                    fig_path = os.path.join(vis_dir, f"drift_history_{feature}_{timestamp}.png")
                    plt.savefig(fig_path)
                    plt.close()
                    
                    logger.info(f"Drift history visualization saved: {fig_path}")
            
        except Exception as e:
            logger.error(f"Error generating drift visualization: {e}")
    
    def _send_notifications(self, notification_type, message):
        """
        Send notifications through configured channels.
        
        Args:
            notification_type (str): Type of notification
            message (str): Notification message
        """
        channels = self.config['notification_channels']
        
        for channel in channels:
            if channel == 'log':
                if notification_type.startswith("DATA_DRIFT"):
                    logger.warning(message)
                elif notification_type.startswith("LEARNING_PAUSED"):
                    logger.warning(message)
                elif notification_type.startswith("LEARNING_RESUMED"):
                    logger.info(message)
                else:
                    logger.info(message)
            
            # Other channels (email, webhook, etc.) would be implemented here
            # This would typically integrate with the alerting system
    
    def get_drift_metrics_history(self, feature_name=None, limit=100):
        """
        Get historical drift metrics for visualization or analysis.
        
        Args:
            feature_name (str): Name of the feature (if None, return all)
            limit (int): Maximum number of data points to return
            
        Returns:
            dict: Dictionary of drift metrics by feature
        """
        if feature_name:
            if feature_name in self.drift_metrics:
                return {feature_name: self.drift_metrics[feature_name][-limit:]}
            return {}
        
        # Return all features, limited to specified number of points
        return {feature: metrics[-limit:] for feature, metrics in self.drift_metrics.items()}


# Example usage
if __name__ == "__main__":
    # Example configuration
    config = {
        'max_drift_percentage': 5.0,
        'drift_check_interval': 60,  # Check every minute for demo
        'snapshot_base_dir': 'data/snapshots',
        'notification_channels': ['log'],
    }
    
    # Create monitor
    monitor = DataQualityMonitor(config)
    
    # Set reference distributions (normally this would be from baseline data)
    np.random.seed(42)
    reference_data = np.random.normal(100, 15, 1000)
    monitor.set_reference_distribution('example_feature', reference_data)
    
    # Start monitoring
    monitor.start_monitoring()
    
    try:
        # Simulate some data updates over time
        for i in range(10):
            # Gradually increase the mean to simulate drift
            current_data = np.random.normal(100 + i*3, 15, 1000)
            monitor.update_current_distribution('example_feature', current_data)
            
            # Wait a bit
            time.sleep(10)
            
            # Check if learning is paused
            is_paused, reason, message = monitor.is_learning_paused()
            if is_paused:
                print(f"Learning is paused: {message}")
                
                # Simulate manual resume after a few iterations
                if i > 5:
                    monitor.manually_resume_learning("admin", "Approved after review")
        
        # Take a snapshot
        snapshot_dir = monitor._take_daily_snapshot()
        print(f"Snapshot taken: {snapshot_dir}")
        
        # List available snapshots
        snapshots = monitor.list_available_snapshots()
        print(f"Available snapshots: {snapshots}")
        
    finally:
        # Stop monitoring
        monitor.stop_monitoring()
