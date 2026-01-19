#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Metrics collector module for the Agricultural AI System.

This module is responsible for collecting various metrics from the system,
including system resources, application performance, and model metrics.
"""

import os
import time
import psutil
import logging
import platform
import threading
import json
from datetime import datetime
import numpy as np
from collections import deque

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('metrics_collector')

class MetricsCollector:
    """
    Collects and stores metrics from various sources.
    
    This class is responsible for gathering metrics about system resources,
    application performance, and model performance. It runs in a separate thread
    and periodically collects metrics based on the configured intervals.
    """
    
    def __init__(self, config=None):
        """
        Initialize the metrics collector.
        
        Args:
            config (dict): Configuration dictionary with collection intervals and settings
        """
        self.config = config or {}
        
        # Default configuration
        self.default_config = {
            'system_metrics_interval': 60,  # seconds
            'app_metrics_interval': 30,     # seconds
            'model_metrics_interval': 3600, # seconds (1 hour)
            'metrics_history_size': 1000,   # number of data points to keep
            'metrics_file': 'metrics.json', # file to save metrics
            'metrics_dir': 'logs/metrics',  # directory to save metrics files
        }
        
        # Merge with provided config
        for key, value in self.default_config.items():
            if key not in self.config:
                self.config[key] = value
        
        # Create metrics storage
        self.system_metrics = {
            'cpu_usage': deque(maxlen=self.config['metrics_history_size']),
            'memory_usage': deque(maxlen=self.config['metrics_history_size']),
            'disk_usage': deque(maxlen=self.config['metrics_history_size']),
            'network_io': deque(maxlen=self.config['metrics_history_size']),
        }
        
        self.app_metrics = {
            'request_count': deque(maxlen=self.config['metrics_history_size']),
            'error_count': deque(maxlen=self.config['metrics_history_size']),
            'response_times': deque(maxlen=self.config['metrics_history_size']),
            'queue_size': deque(maxlen=self.config['metrics_history_size']),
        }
        
        self.model_metrics = {
            'accuracy': deque(maxlen=self.config['metrics_history_size']),
            'inference_times': deque(maxlen=self.config['metrics_history_size']),
            'model_drift': deque(maxlen=self.config['metrics_history_size']),
        }
        
        # Initialize counters
        self.request_counter = 0
        self.error_counter = 0
        self.response_times_buffer = []
        self.queue_size = 0
        
        # Create metrics directory if it doesn't exist
        os.makedirs(self.config['metrics_dir'], exist_ok=True)
        
        # Thread control
        self.running = False
        self.collection_thread = None
        self.lock = threading.Lock()
        
        # Network IO baseline
        self.last_net_io = psutil.net_io_counters()
        self.last_net_io_time = time.time()
        
        logger.info("Metrics collector initialized")
    
    def start(self):
        """Start the metrics collection thread."""
        if self.running:
            logger.warning("Metrics collector is already running")
            return
        
        self.running = True
        self.collection_thread = threading.Thread(target=self._collection_loop, daemon=True)
        self.collection_thread.start()
        logger.info("Metrics collection started")
    
    def stop(self):
        """Stop the metrics collection thread."""
        self.running = False
        if self.collection_thread:
            self.collection_thread.join(timeout=5.0)
            logger.info("Metrics collection stopped")
    
    def _collection_loop(self):
        """Main collection loop that runs in a separate thread."""
        system_last_time = 0
        app_last_time = 0
        model_last_time = 0
        
        while self.running:
            current_time = time.time()
            
            # Collect system metrics
            if current_time - system_last_time >= self.config['system_metrics_interval']:
                self._collect_system_metrics()
                system_last_time = current_time
            
            # Collect application metrics
            if current_time - app_last_time >= self.config['app_metrics_interval']:
                self._collect_app_metrics()
                app_last_time = current_time
            
            # Collect model metrics
            if current_time - model_last_time >= self.config['model_metrics_interval']:
                self._collect_model_metrics()
                model_last_time = current_time
            
            # Save metrics periodically
            if current_time % (self.config.get('save_interval', 300)) < 1:  # Every 5 minutes by default
                self.save_metrics()
            
            # Sleep to avoid high CPU usage
            time.sleep(1)
    
    def _collect_system_metrics(self):
        """Collect system resource metrics."""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            
            # Network IO
            current_net_io = psutil.net_io_counters()
            current_time = time.time()
            
            # Calculate network throughput (bytes/sec)
            time_diff = current_time - self.last_net_io_time
            if time_diff > 0:
                bytes_sent = (current_net_io.bytes_sent - self.last_net_io.bytes_sent) / time_diff
                bytes_recv = (current_net_io.bytes_recv - self.last_net_io.bytes_recv) / time_diff
                network_throughput = bytes_sent + bytes_recv
            else:
                network_throughput = 0
            
            self.last_net_io = current_net_io
            self.last_net_io_time = current_time
            
            # Store metrics with timestamp
            timestamp = datetime.now().isoformat()
            
            with self.lock:
                self.system_metrics['cpu_usage'].append((timestamp, cpu_percent))
                self.system_metrics['memory_usage'].append((timestamp, memory_percent))
                self.system_metrics['disk_usage'].append((timestamp, disk_percent))
                self.system_metrics['network_io'].append((timestamp, network_throughput))
            
            logger.debug(f"Collected system metrics: CPU={cpu_percent}%, Memory={memory_percent}%, Disk={disk_percent}%")
        
        except Exception as e:
            logger.error(f"Error collecting system metrics: {e}")
    
    def _collect_app_metrics(self):
        """Collect application performance metrics."""
        try:
            timestamp = datetime.now().isoformat()
            
            with self.lock:
                # Request rate (requests per minute)
                request_rate = self.request_counter / (self.config['app_metrics_interval'] / 60)
                self.app_metrics['request_count'].append((timestamp, request_rate))
                self.request_counter = 0
                
                # Error rate (errors per minute)
                error_rate = self.error_counter / (self.config['app_metrics_interval'] / 60)
                self.app_metrics['error_count'].append((timestamp, error_rate))
                self.error_counter = 0
                
                # Response times
                if self.response_times_buffer:
                    avg_response_time = sum(self.response_times_buffer) / len(self.response_times_buffer)
                    if len(self.response_times_buffer) > 1:
                        p95_response_time = np.percentile(self.response_times_buffer, 95)
                        p99_response_time = np.percentile(self.response_times_buffer, 99)
                    else:
                        p95_response_time = avg_response_time
                        p99_response_time = avg_response_time
                    
                    self.app_metrics['response_times'].append((
                        timestamp, 
                        {
                            'avg': avg_response_time,
                            'p95': p95_response_time,
                            'p99': p99_response_time
                        }
                    ))
                    self.response_times_buffer = []
                
                # Queue size
                self.app_metrics['queue_size'].append((timestamp, self.queue_size))
            
            logger.debug(f"Collected app metrics: Requests={request_rate}/min, Errors={error_rate}/min")
        
        except Exception as e:
            logger.error(f"Error collecting application metrics: {e}")
    
    def _collect_model_metrics(self):
        """
        Collect model performance metrics.
        
        Note: This is a placeholder. In a real implementation, this would
        involve evaluating models on validation data or monitoring inference metrics.
        """
        # This is a placeholder. In a real implementation, you would:
        # 1. Periodically evaluate models on validation data
        # 2. Calculate accuracy, precision, recall, etc.
        # 3. Measure inference times
        # 4. Detect model drift by comparing with baseline performance
        
        logger.debug("Model metrics collection is a placeholder - implement actual model evaluation")
    
    def record_request(self, response_time=None, is_error=False):
        """
        Record a request to the system.
        
        Args:
            response_time (float): Response time in seconds
            is_error (bool): Whether the request resulted in an error
        """
        with self.lock:
            self.request_counter += 1
            if is_error:
                self.error_counter += 1
            if response_time is not None:
                self.response_times_buffer.append(response_time)
    
    def update_queue_size(self, size):
        """
        Update the current queue size.
        
        Args:
            size (int): Current size of the request queue
        """
        with self.lock:
            self.queue_size = size
    
    def record_model_metrics(self, model_name, metrics):
        """
        Record metrics for a specific model.
        
        Args:
            model_name (str): Name of the model
            metrics (dict): Dictionary of metrics (accuracy, inference_time, etc.)
        """
        timestamp = datetime.now().isoformat()
        
        with self.lock:
            if 'accuracy' in metrics:
                self.model_metrics['accuracy'].append((timestamp, {model_name: metrics['accuracy']}))
            
            if 'inference_time' in metrics:
                self.model_metrics['inference_times'].append((timestamp, {model_name: metrics['inference_time']}))
            
            # Model drift would require comparing with baseline performance
            # This is a simplified placeholder
            if 'drift' in metrics:
                self.model_metrics['model_drift'].append((timestamp, {model_name: metrics['drift']}))
    
    def get_latest_metrics(self):
        """
        Get the latest metrics for all categories.
        
        Returns:
            dict: Dictionary containing the latest metrics
        """
        with self.lock:
            latest_metrics = {
                'system': {},
                'application': {},
                'model': {}
            }
            
            # Get latest system metrics
            for metric_name, metric_data in self.system_metrics.items():
                if metric_data:
                    latest_metrics['system'][metric_name] = metric_data[-1][1]
            
            # Get latest application metrics
            for metric_name, metric_data in self.app_metrics.items():
                if metric_data:
                    latest_metrics['application'][metric_name] = metric_data[-1][1]
            
            # Get latest model metrics
            for metric_name, metric_data in self.model_metrics.items():
                if metric_data:
                    latest_metrics['model'][metric_name] = metric_data[-1][1]
            
            return latest_metrics
    
    def get_metrics_history(self, metric_type, metric_name, limit=100):
        """
        Get historical data for a specific metric.
        
        Args:
            metric_type (str): Type of metric ('system', 'app', or 'model')
            metric_name (str): Name of the specific metric
            limit (int): Maximum number of data points to return
            
        Returns:
            list: List of (timestamp, value) tuples
        """
        with self.lock:
            if metric_type == 'system' and metric_name in self.system_metrics:
                data = list(self.system_metrics[metric_name])
            elif metric_type == 'app' and metric_name in self.app_metrics:
                data = list(self.app_metrics[metric_name])
            elif metric_type == 'model' and metric_name in self.model_metrics:
                data = list(self.model_metrics[metric_name])
            else:
                return []
            
            # Return the most recent 'limit' data points
            return data[-limit:]
    
    def save_metrics(self):
        """Save current metrics to a file."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(self.config['metrics_dir'], f"metrics_{timestamp}.json")
            
            with self.lock:
                # Convert deque objects to lists for serialization
                metrics_data = {
                    'timestamp': datetime.now().isoformat(),
                    'system': {k: list(v) for k, v in self.system_metrics.items()},
                    'application': {k: list(v) for k, v in self.app_metrics.items()},
                    'model': {k: list(v) for k, v in self.model_metrics.items()},
                }
            
            with open(filename, 'w') as f:
                json.dump(metrics_data, f, indent=2)
            
            logger.info(f"Metrics saved to {filename}")
        
        except Exception as e:
            logger.error(f"Error saving metrics: {e}")
    
    def get_system_info(self):
        """
        Get detailed system information.
        
        Returns:
            dict: Dictionary containing system information
        """
        try:
            info = {
                'platform': platform.platform(),
                'python_version': platform.python_version(),
                'processor': platform.processor(),
                'cpu_count': psutil.cpu_count(logical=True),
                'physical_cpu_count': psutil.cpu_count(logical=False),
                'memory_total': psutil.virtual_memory().total,
                'disk_total': psutil.disk_usage('/').total,
                'hostname': platform.node(),
            }
            
            # Try to get GPU information if available
            try:
                import GPUtil
                gpus = GPUtil.getGPUs()
                if gpus:
                    info['gpus'] = [{
                        'name': gpu.name,
                        'memory_total': gpu.memoryTotal,
                        'driver': gpu.driver,
                    } for gpu in gpus]
            except (ImportError, Exception):
                info['gpus'] = []
            
            return info
        
        except Exception as e:
            logger.error(f"Error getting system info: {e}")
            return {}


# Example usage
if __name__ == "__main__":
    # Example configuration
    config = {
        'system_metrics_interval': 10,  # seconds
        'app_metrics_interval': 5,      # seconds
        'model_metrics_interval': 60,   # seconds
        'metrics_history_size': 100,    # number of data points to keep
        'metrics_dir': 'logs/metrics',  # directory to save metrics files
    }
    
    # Create and start metrics collector
    collector = MetricsCollector(config)
    collector.start()
    
    try:
        # Simulate some requests
        for i in range(20):
            # Simulate a request with random response time
            response_time = 0.1 + (0.5 * random.random())
            is_error = random.random() < 0.1  # 10% chance of error
            collector.record_request(response_time, is_error)
            
            # Simulate queue size changes
            collector.update_queue_size(random.randint(0, 10))
            
            # Sleep for a bit
            time.sleep(1)
        
        # Simulate recording model metrics
        collector.record_model_metrics('disease_detection', {
            'accuracy': 0.92,
            'inference_time': 0.15,
            'drift': 0.02
        })
        
        # Get and print latest metrics
        latest = collector.get_latest_metrics()
        print("Latest metrics:")
        print(json.dumps(latest, indent=2))
        
        # Save metrics
        collector.save_metrics()
        
    finally:
        # Stop the collector
        collector.stop()
