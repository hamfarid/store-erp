#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Advanced visualization module for the Agricultural AI System.

This module provides functions for creating interactive and static visualizations
for model performance, analysis results, and monitoring metrics.
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
from plotly.subplots import make_subplots
from sklearn.metrics import confusion_matrix, roc_curve, precision_recall_curve, auc
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('visualizer')

# Set default Plotly template for consistent styling
pio.templates.default = "plotly_white"

class Visualizer:
    """
    Creates and manages visualizations for the Agricultural AI System.
    
    This class provides methods for generating various types of visualizations,
    including model performance metrics, analysis results, and system monitoring data.
    """
    
    def __init__(self, config=None):
        """
        Initialize the visualizer.
        
        Args:
            config (dict): Configuration dictionary with visualization settings
        """
        self.config = config or {}
        
        # Default configuration
        self.default_config = {
            'output_dir': 'static/visualizations',
            'dpi': 300,  # For static images
            'fig_width': 10,
            'fig_height': 8,
            'color_palette': 'viridis',
            'interactive_height': 600,
            'interactive_width': 800,
        }
        
        # Merge with provided config
        for key, value in self.default_config.items():
            if key not in self.config:
                self.config[key] = value
        
        # Create output directory if it doesn't exist
        os.makedirs(self.config['output_dir'], exist_ok=True)
        
        # Set seaborn style
        sns.set_style("whitegrid")
        sns.set_palette(self.config['color_palette'])
        
        logger.info("Visualizer initialized")
    
    # --- Model Performance Visualizations ---
    
    def create_confusion_matrix(self, y_true, y_pred, class_names=None, title="Confusion Matrix", 
                               normalize=False, save_path=None, return_fig=False):
        """
        Create a confusion matrix visualization using Seaborn.
        
        Args:
            y_true (array-like): True labels
            y_pred (array-like): Predicted labels
            class_names (list): List of class names
            title (str): Plot title
            normalize (bool): Whether to normalize the confusion matrix
            save_path (str): Path to save the figure (if None, uses default location)
            return_fig (bool): Whether to return the figure object
            
        Returns:
            matplotlib.figure.Figure if return_fig is True, otherwise None
        """
        # Compute confusion matrix
        cm = confusion_matrix(y_true, y_pred)
        
        # Normalize if requested
        if normalize:
            cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
            fmt = '.2f'
        else:
            fmt = 'd'
        
        # Create figure
        plt.figure(figsize=(self.config['fig_width'], self.config['fig_height']))
        
        # Plot confusion matrix
        ax = sns.heatmap(cm, annot=True, fmt=fmt, cmap='Blues',
                         xticklabels=class_names, yticklabels=class_names)
        
        # Set labels and title
        ax.set_xlabel('Predicted')
        ax.set_ylabel('True')
        ax.set_title(title)
        
        # Tight layout
        plt.tight_layout()
        
        # Save figure if path is provided
        if save_path is None and not return_fig:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = os.path.join(self.config['output_dir'], f"confusion_matrix_{timestamp}.png")
        
        if save_path:
            plt.savefig(save_path, dpi=self.config['dpi'], bbox_inches='tight')
            logger.info(f"Confusion matrix saved to {save_path}")
            
        if return_fig:
            fig = plt.gcf()
            plt.close()
            return fig
        else:
            plt.close()
            return save_path
    
    def create_roc_curve(self, y_true, y_score, class_names=None, title="ROC Curve", 
                        multi_class=False, save_path=None, return_fig=False, as_json=False):
        """
        Create a ROC curve visualization using Plotly.
        
        Args:
            y_true (array-like): True labels (one-hot encoded for multi-class)
            y_score (array-like): Predicted probabilities
            class_names (list): List of class names
            title (str): Plot title
            multi_class (bool): Whether this is a multi-class problem
            save_path (str): Path to save the figure (if None, uses default location)
            return_fig (bool): Whether to return the figure object
            as_json (bool): Whether to return the figure as JSON (for web display)
            
        Returns:
            plotly.graph_objects.Figure, JSON string, or path depending on parameters
        """
        # Initialize figure
        fig = go.Figure()
        
        # For binary classification
        if not multi_class:
            fpr, tpr, _ = roc_curve(y_true, y_score)
            roc_auc = auc(fpr, tpr)
            
            # Add trace
            fig.add_trace(go.Scatter(
                x=fpr, y=tpr,
                mode='lines',
                name=f'ROC curve (AUC = {roc_auc:.3f})',
                line=dict(width=2, color='blue'),
            ))
            
        # For multi-class classification
        else:
            if class_names is None:
                n_classes = y_score.shape[1] if len(y_score.shape) > 1 else 2
                class_names = [f"Class {i}" for i in range(n_classes)]
            
            # Compute ROC curve and ROC area for each class
            for i, class_name in enumerate(class_names):
                if len(y_true.shape) > 1:  # One-hot encoded
                    fpr, tpr, _ = roc_curve(y_true[:, i], y_score[:, i])
                else:  # Binary or single column
                    fpr, tpr, _ = roc_curve((y_true == i).astype(int), 
                                           y_score[:, i] if len(y_score.shape) > 1 else y_score)
                roc_auc = auc(fpr, tpr)
                
                # Add trace for each class
                fig.add_trace(go.Scatter(
                    x=fpr, y=tpr,
                    mode='lines',
                    name=f'{class_name} (AUC = {roc_auc:.3f})',
                ))
        
        # Add diagonal line (random classifier)
        fig.add_trace(go.Scatter(
            x=[0, 1], y=[0, 1],
            mode='lines',
            name='Random',
            line=dict(dash='dash', width=1, color='gray'),
        ))
        
        # Update layout
        fig.update_layout(
            title=title,
            xaxis_title='False Positive Rate',
            yaxis_title='True Positive Rate',
            legend=dict(x=0.01, y=0.99, bgcolor='rgba(255,255,255,0.8)'),
            width=self.config['interactive_width'],
            height=self.config['interactive_height'],
            hovermode='closest',
        )
        
        # Save or return figure
        if save_path is None and not return_fig and not as_json:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = os.path.join(self.config['output_dir'], f"roc_curve_{timestamp}")
            
        if save_path:
            # Save as HTML
            html_path = f"{save_path}.html"
            fig.write_html(html_path)
            logger.info(f"ROC curve saved as HTML to {html_path}")
            
            # Save as PNG
            png_path = f"{save_path}.png"
            fig.write_image(png_path)
            logger.info(f"ROC curve saved as PNG to {png_path}")
            
            return html_path
            
        if as_json:
            return fig.to_json()
            
        if return_fig:
            return fig
    
    def create_precision_recall_curve(self, y_true, y_score, class_names=None, title="Precision-Recall Curve", 
                                     multi_class=False, save_path=None, return_fig=False, as_json=False):
        """
        Create a Precision-Recall curve visualization using Plotly.
        
        Args:
            y_true (array-like): True labels (one-hot encoded for multi-class)
            y_score (array-like): Predicted probabilities
            class_names (list): List of class names
            title (str): Plot title
            multi_class (bool): Whether this is a multi-class problem
            save_path (str): Path to save the figure (if None, uses default location)
            return_fig (bool): Whether to return the figure object
            as_json (bool): Whether to return the figure as JSON (for web display)
            
        Returns:
            plotly.graph_objects.Figure, JSON string, or path depending on parameters
        """
        # Initialize figure
        fig = go.Figure()
        
        # For binary classification
        if not multi_class:
            precision, recall, _ = precision_recall_curve(y_true, y_score)
            pr_auc = auc(recall, precision)
            
            # Add trace
            fig.add_trace(go.Scatter(
                x=recall, y=precision,
                mode='lines',
                name=f'PR curve (AUC = {pr_auc:.3f})',
                line=dict(width=2, color='blue'),
            ))
            
        # For multi-class classification
        else:
            if class_names is None:
                n_classes = y_score.shape[1] if len(y_score.shape) > 1 else 2
                class_names = [f"Class {i}" for i in range(n_classes)]
            
            # Compute PR curve for each class
            for i, class_name in enumerate(class_names):
                if len(y_true.shape) > 1:  # One-hot encoded
                    precision, recall, _ = precision_recall_curve(y_true[:, i], y_score[:, i])
                else:  # Binary or single column
                    precision, recall, _ = precision_recall_curve((y_true == i).astype(int), 
                                                                y_score[:, i] if len(y_score.shape) > 1 else y_score)
                pr_auc = auc(recall, precision)
                
                # Add trace for each class
                fig.add_trace(go.Scatter(
                    x=recall, y=precision,
                    mode='lines',
                    name=f'{class_name} (AUC = {pr_auc:.3f})',
                ))
        
        # Update layout
        fig.update_layout(
            title=title,
            xaxis_title='Recall',
            yaxis_title='Precision',
            legend=dict(x=0.01, y=0.01, bgcolor='rgba(255,255,255,0.8)'),
            width=self.config['interactive_width'],
            height=self.config['interactive_height'],
            hovermode='closest',
        )
        
        # Save or return figure
        if save_path is None and not return_fig and not as_json:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = os.path.join(self.config['output_dir'], f"pr_curve_{timestamp}")
            
        if save_path:
            # Save as HTML
            html_path = f"{save_path}.html"
            fig.write_html(html_path)
            logger.info(f"PR curve saved as HTML to {html_path}")
            
            # Save as PNG
            png_path = f"{save_path}.png"
            fig.write_image(png_path)
            logger.info(f"PR curve saved as PNG to {png_path}")
            
            return html_path
            
        if as_json:
            return fig.to_json()
            
        if return_fig:
            return fig
    
    # --- Analysis Results Visualizations ---
    
    def create_comparative_analysis_chart(self, standard_results, primitive_results, 
                                         title="Comparative Analysis", 
                                         save_path=None, return_fig=False, as_json=False):
        """
        Create a comparative bar chart for standard vs. primitive analysis results.
        
        Args:
            standard_results (dict): Results from standard analysis
            primitive_results (dict): Results from primitive analysis
            title (str): Plot title
            save_path (str): Path to save the figure (if None, uses default location)
            return_fig (bool): Whether to return the figure object
            as_json (bool): Whether to return the figure as JSON (for web display)
            
        Returns:
            plotly.graph_objects.Figure, JSON string, or path depending on parameters
        """
        # Extract disease detection results
        std_diseases = standard_results.get('disease_detection', [])
        prim_diseases = primitive_results.get('disease_detection', [])
        
        # Extract nutrient analysis results
        std_nutrients = standard_results.get('nutrient_analysis', [])
        prim_nutrients = primitive_results.get('nutrient_analysis', [])
        
        # Combine all detections
        all_detections = set()
        for detection in std_diseases + prim_diseases + std_nutrients + prim_nutrients:
            if isinstance(detection, dict) and 'name' in detection:
                all_detections.add(detection['name'])
        
        # Create data for plotting
        detection_names = list(all_detections)
        std_confidences = []
        prim_confidences = []
        
        # Get confidence values for each detection
        for name in detection_names:
            # Standard analysis
            std_conf = 0
            for detection in std_diseases + std_nutrients:
                if isinstance(detection, dict) and detection.get('name') == name:
                    std_conf = detection.get('confidence', 0) * 100  # Convert to percentage
                    break
            std_confidences.append(std_conf)
            
            # Primitive analysis
            prim_conf = 0
            for detection in prim_diseases + prim_nutrients:
                if isinstance(detection, dict) and detection.get('name') == name:
                    prim_conf = detection.get('confidence', 0) * 100  # Convert to percentage
                    break
            prim_confidences.append(prim_conf)
        
        # Create figure
        fig = go.Figure()
        
        # Add traces
        fig.add_trace(go.Bar(
            x=detection_names,
            y=std_confidences,
            name='Standard Analysis',
            marker_color='blue',
        ))
        
        fig.add_trace(go.Bar(
            x=detection_names,
            y=prim_confidences,
            name='Primitive Analysis',
            marker_color='green',
        ))
        
        # Update layout
        fig.update_layout(
            title=title,
            xaxis_title='Detection',
            yaxis_title='Confidence (%)',
            barmode='group',
            width=self.config['interactive_width'],
            height=self.config['interactive_height'],
            hovermode='closest',
        )
        
        # Save or return figure
        if save_path is None and not return_fig and not as_json:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = os.path.join(self.config['output_dir'], f"comparative_analysis_{timestamp}")
            
        if save_path:
            # Save as HTML
            html_path = f"{save_path}.html"
            fig.write_html(html_path)
            logger.info(f"Comparative analysis chart saved as HTML to {html_path}")
            
            # Save as PNG
            png_path = f"{save_path}.png"
            fig.write_image(png_path)
            logger.info(f"Comparative analysis chart saved as PNG to {png_path}")
            
            return html_path
            
        if as_json:
            return fig.to_json()
            
        if return_fig:
            return fig
    
    def create_segmentation_visualization(self, original_image, segmented_image, 
                                         title="Image Segmentation", 
                                         save_path=None, return_fig=False, as_json=False):
        """
        Create a visualization showing original image and its segmentation.
        
        Args:
            original_image (numpy.ndarray): Original image
            segmented_image (numpy.ndarray): Segmented image (can be RGB or labeled)
            title (str): Plot title
            save_path (str): Path to save the figure (if None, uses default location)
            return_fig (bool): Whether to return the figure object
            as_json (bool): Whether to return the figure as JSON (for web display)
            
        Returns:
            plotly.graph_objects.Figure, JSON string, or path depending on parameters
        """
        # Create figure with subplots
        fig = make_subplots(rows=1, cols=2, subplot_titles=["Original", "Segmented"])
        
        # Add original image
        fig.add_trace(
            go.Image(z=original_image),
            row=1, col=1
        )
        
        # Add segmented image
        fig.add_trace(
            go.Image(z=segmented_image),
            row=1, col=2
        )
        
        # Update layout
        fig.update_layout(
            title=title,
            width=self.config['interactive_width'],
            height=self.config['interactive_height'],
        )
        
        # Save or return figure
        if save_path is None and not return_fig and not as_json:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = os.path.join(self.config['output_dir'], f"segmentation_{timestamp}")
            
        if save_path:
            # Save as HTML
            html_path = f"{save_path}.html"
            fig.write_html(html_path)
            logger.info(f"Segmentation visualization saved as HTML to {html_path}")
            
            # Save as PNG
            png_path = f"{save_path}.png"
            fig.write_image(png_path)
            logger.info(f"Segmentation visualization saved as PNG to {png_path}")
            
            return html_path
            
        if as_json:
            return fig.to_json()
            
        if return_fig:
            return fig
    
    # --- Monitoring Visualizations ---
    
    def create_system_metrics_dashboard(self, metrics_data, time_range=None, 
                                       save_path=None, return_fig=False, as_json=False):
        """
        Create a dashboard visualization for system metrics.
        
        Args:
            metrics_data (dict): Dictionary containing system metrics data
            time_range (tuple): Optional (start_time, end_time) for filtering
            save_path (str): Path to save the figure (if None, uses default location)
            return_fig (bool): Whether to return the figure object
            as_json (bool): Whether to return the figure as JSON (for web display)
            
        Returns:
            plotly.graph_objects.Figure, JSON string, or path depending on parameters
        """
        # Create figure with subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=["CPU Usage (%)", "Memory Usage (%)", "Disk Usage (%)", "Network I/O (bytes/s)"],
            vertical_spacing=0.1
        )
        
        # Extract metrics
        cpu_data = metrics_data.get('system', {}).get('cpu_usage', [])
        memory_data = metrics_data.get('system', {}).get('memory_usage', [])
        disk_data = metrics_data.get('system', {}).get('disk_usage', [])
        network_data = metrics_data.get('system', {}).get('network_io', [])
        
        # Filter by time range if provided
        if time_range:
            start_time, end_time = time_range
            
            def filter_by_time(data):
                return [(t, v) for t, v in data if start_time <= t <= end_time]
            
            cpu_data = filter_by_time(cpu_data)
            memory_data = filter_by_time(memory_data)
            disk_data = filter_by_time(disk_data)
            network_data = filter_by_time(network_data)
        
        # Add CPU usage trace
        if cpu_data:
            timestamps, values = zip(*cpu_data)
            fig.add_trace(
                go.Scatter(x=timestamps, y=values, mode='lines', name='CPU Usage'),
                row=1, col=1
            )
        
        # Add Memory usage trace
        if memory_data:
            timestamps, values = zip(*memory_data)
            fig.add_trace(
                go.Scatter(x=timestamps, y=values, mode='lines', name='Memory Usage'),
                row=1, col=2
            )
        
        # Add Disk usage trace
        if disk_data:
            timestamps, values = zip(*disk_data)
            fig.add_trace(
                go.Scatter(x=timestamps, y=values, mode='lines', name='Disk Usage'),
                row=2, col=1
            )
        
        # Add Network I/O trace
        if network_data:
            timestamps, values = zip(*network_data)
            fig.add_trace(
                go.Scatter(x=timestamps, y=values, mode='lines', name='Network I/O'),
                row=2, col=2
            )
        
        # Update layout
        fig.update_layout(
            title="System Metrics Dashboard",
            showlegend=False,
            width=self.config['interactive_width'],
            height=self.config['interactive_height'],
            hovermode='closest',
        )
        
        # Update y-axis ranges
        fig.update_yaxes(range=[0, 100], row=1, col=1)  # CPU
        fig.update_yaxes(range=[0, 100], row=1, col=2)  # Memory
        fig.update_yaxes(range=[0, 100], row=2, col=1)  # Disk
        
        # Save or return figure
        if save_path is None and not return_fig and not as_json:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = os.path.join(self.config['output_dir'], f"system_metrics_{timestamp}")
            
        if save_path:
            # Save as HTML
            html_path = f"{save_path}.html"
            fig.write_html(html_path)
            logger.info(f"System metrics dashboard saved as HTML to {html_path}")
            
            # Save as PNG
            png_path = f"{save_path}.png"
            fig.write_image(png_path)
            logger.info(f"System metrics dashboard saved as PNG to {png_path}")
            
            return html_path
            
        if as_json:
            return fig.to_json()
            
        if return_fig:
            return fig
    
    def create_application_metrics_dashboard(self, metrics_data, time_range=None, 
                                           save_path=None, return_fig=False, as_json=False):
        """
        Create a dashboard visualization for application metrics.
        
        Args:
            metrics_data (dict): Dictionary containing application metrics data
            time_range (tuple): Optional (start_time, end_time) for filtering
            save_path (str): Path to save the figure (if None, uses default location)
            return_fig (bool): Whether to return the figure object
            as_json (bool): Whether to return the figure as JSON (for web display)
            
        Returns:
            plotly.graph_objects.Figure, JSON string, or path depending on parameters
        """
        # Create figure with subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=["Request Rate (req/min)", "Error Rate (err/min)", "Response Time (s)", "Queue Size"],
            vertical_spacing=0.1
        )
        
        # Extract metrics
        request_data = metrics_data.get('application', {}).get('request_count', [])
        error_data = metrics_data.get('application', {}).get('error_count', [])
        response_time_data = metrics_data.get('application', {}).get('response_times', [])
        queue_data = metrics_data.get('application', {}).get('queue_size', [])
        
        # Filter by time range if provided
        if time_range:
            start_time, end_time = time_range
            
            def filter_by_time(data):
                return [(t, v) for t, v in data if start_time <= t <= end_time]
            
            request_data = filter_by_time(request_data)
            error_data = filter_by_time(error_data)
            response_time_data = filter_by_time(response_time_data)
            queue_data = filter_by_time(queue_data)
        
        # Add Request Rate trace
        if request_data:
            timestamps, values = zip(*request_data)
            fig.add_trace(
                go.Scatter(x=timestamps, y=values, mode='lines', name='Request Rate'),
                row=1, col=1
            )
        
        # Add Error Rate trace
        if error_data:
            timestamps, values = zip(*error_data)
            fig.add_trace(
                go.Scatter(x=timestamps, y=values, mode='lines', name='Error Rate'),
                row=1, col=2
            )
        
        # Add Response Time traces
        if response_time_data:
            timestamps = []
            avg_values = []
            p95_values = []
            p99_values = []
            
            for t, data in response_time_data:
                timestamps.append(t)
                if isinstance(data, dict):
                    avg_values.append(data.get('avg', 0))
                    p95_values.append(data.get('p95', 0))
                    p99_values.append(data.get('p99', 0))
                else:
                    avg_values.append(data)
                    p95_values.append(data)
                    p99_values.append(data)
            
            fig.add_trace(
                go.Scatter(x=timestamps, y=avg_values, mode='lines', name='Avg Response Time'),
                row=2, col=1
            )
            
            fig.add_trace(
                go.Scatter(x=timestamps, y=p95_values, mode='lines', name='P95 Response Time', line=dict(dash='dash')),
                row=2, col=1
            )
            
            fig.add_trace(
                go.Scatter(x=timestamps, y=p99_values, mode='lines', name='P99 Response Time', line=dict(dash='dot')),
                row=2, col=1
            )
        
        # Add Queue Size trace
        if queue_data:
            timestamps, values = zip(*queue_data)
            fig.add_trace(
                go.Scatter(x=timestamps, y=values, mode='lines', name='Queue Size'),
                row=2, col=2
            )
        
        # Update layout
        fig.update_layout(
            title="Application Metrics Dashboard",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            width=self.config['interactive_width'],
            height=self.config['interactive_height'],
            hovermode='closest',
        )
        
        # Save or return figure
        if save_path is None and not return_fig and not as_json:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = os.path.join(self.config['output_dir'], f"application_metrics_{timestamp}")
            
        if save_path:
            # Save as HTML
            html_path = f"{save_path}.html"
            fig.write_html(html_path)
            logger.info(f"Application metrics dashboard saved as HTML to {html_path}")
            
            # Save as PNG
            png_path = f"{save_path}.png"
            fig.write_image(png_path)
            logger.info(f"Application metrics dashboard saved as PNG to {png_path}")
            
            return html_path
            
        if as_json:
            return fig.to_json()
            
        if return_fig:
            return fig
    
    # --- Utility Methods ---
    
    def save_figure_as_json(self, fig, filename=None):
        """
        Save a Plotly figure as JSON for web display.
        
        Args:
            fig (plotly.graph_objects.Figure): Figure to save
            filename (str): Filename (without extension)
            
        Returns:
            str: Path to the saved JSON file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"figure_{timestamp}"
        
        # Ensure it has .json extension
        if not filename.endswith('.json'):
            filename = f"{filename}.json"
        
        # Create full path
        filepath = os.path.join(self.config['output_dir'], filename)
        
        # Save as JSON
        with open(filepath, 'w') as f:
            f.write(fig.to_json())
        
        logger.info(f"Figure saved as JSON to {filepath}")
        return filepath
    
    def create_model_performance_summary(self, model_name, metrics, save_path=None):
        """
        Create a comprehensive model performance summary with multiple visualizations.
        
        Args:
            model_name (str): Name of the model
            metrics (dict): Dictionary containing model metrics
            save_path (str): Directory to save visualizations
            
        Returns:
            dict: Paths to generated visualizations
        """
        if save_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = os.path.join(self.config['output_dir'], f"{model_name}_{timestamp}")
        
        os.makedirs(save_path, exist_ok=True)
        
        results = {}
        
        # Create confusion matrix
        if 'y_true' in metrics and 'y_pred' in metrics:
            cm_path = os.path.join(save_path, "confusion_matrix.png")
            self.create_confusion_matrix(
                metrics['y_true'], 
                metrics['y_pred'],
                class_names=metrics.get('class_names'),
                title=f"{model_name} - Confusion Matrix",
                save_path=cm_path
            )
            results['confusion_matrix'] = cm_path
        
        # Create ROC curve
        if 'y_true' in metrics and 'y_score' in metrics:
            roc_path = os.path.join(save_path, "roc_curve")
            self.create_roc_curve(
                metrics['y_true'], 
                metrics['y_score'],
                class_names=metrics.get('class_names'),
                title=f"{model_name} - ROC Curve",
                multi_class=metrics.get('multi_class', False),
                save_path=roc_path
            )
            results['roc_curve_html'] = f"{roc_path}.html"
            results['roc_curve_png'] = f"{roc_path}.png"
        
        # Create Precision-Recall curve
        if 'y_true' in metrics and 'y_score' in metrics:
            pr_path = os.path.join(save_path, "pr_curve")
            self.create_precision_recall_curve(
                metrics['y_true'], 
                metrics['y_score'],
                class_names=metrics.get('class_names'),
                title=f"{model_name} - Precision-Recall Curve",
                multi_class=metrics.get('multi_class', False),
                save_path=pr_path
            )
            results['pr_curve_html'] = f"{pr_path}.html"
            results['pr_curve_png'] = f"{pr_path}.png"
        
        # Create summary JSON
        summary = {
            'model_name': model_name,
            'timestamp': datetime.now().isoformat(),
            'metrics': {k: v for k, v in metrics.items() if k not in ['y_true', 'y_pred', 'y_score']},
            'visualizations': results
        }
        
        summary_path = os.path.join(save_path, "summary.json")
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        results['summary'] = summary_path
        
        logger.info(f"Model performance summary created at {save_path}")
        return results


# Example usage
if __name__ == "__main__":
    # Create visualizer
    visualizer = Visualizer()
    
    # Example: Create a confusion matrix
    y_true = [0, 1, 2, 0, 1, 2, 0, 2, 2, 0]
    y_pred = [0, 2, 1, 0, 1, 2, 0, 2, 2, 1]
    class_names = ['Healthy', 'Bacterial Blight', 'Powdery Mildew']
    
    cm_path = visualizer.create_confusion_matrix(
        y_true, y_pred, class_names=class_names,
        title="Example Confusion Matrix"
    )
    print(f"Confusion matrix saved to: {cm_path}")
    
    # Example: Create ROC curve
    import numpy as np
    from sklearn.datasets import make_classification
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import label_binarize
    
    # Generate sample data
    X, y = make_classification(n_samples=1000, n_classes=3, n_features=20, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Train a model
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    
    # Get predictions
    y_score = clf.predict_proba(X_test)
    
    # Binarize the labels for multi-class ROC
    y_test_bin = label_binarize(y_test, classes=[0, 1, 2])
    
    # Create ROC curve
    roc_path = visualizer.create_roc_curve(
        y_test_bin, y_score,
        class_names=['Class 0', 'Class 1', 'Class 2'],
        title="Example ROC Curve",
        multi_class=True
    )
    print(f"ROC curve saved to: {roc_path}")
    
    # Example: Create system metrics dashboard
    # Simulate some metrics data
    import random
    from datetime import datetime, timedelta
    
    # Generate timestamps for the last 24 hours
    timestamps = [(datetime.now() - timedelta(hours=i)).isoformat() for i in range(24, 0, -1)]
    
    # Generate random metrics
    cpu_data = [(t, random.uniform(10, 90)) for t in timestamps]
    memory_data = [(t, random.uniform(20, 80)) for t in timestamps]
    disk_data = [(t, random.uniform(30, 70)) for t in timestamps]
    network_data = [(t, random.uniform(1000, 10000)) for t in timestamps]
    
    metrics_data = {
        'system': {
            'cpu_usage': cpu_data,
            'memory_usage': memory_data,
            'disk_usage': disk_data,
            'network_io': network_data
        }
    }
    
    # Create dashboard
    dashboard_path = visualizer.create_system_metrics_dashboard(metrics_data)
    print(f"System metrics dashboard saved to: {dashboard_path}")
