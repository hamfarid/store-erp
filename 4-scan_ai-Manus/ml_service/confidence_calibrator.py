"""
Confidence Calibrator
======================

Purpose: Calibrate ML model confidence scores for more reliable predictions.
Implements temperature scaling and Platt scaling for confidence calibration.

Problem Solved:
Neural networks often produce overconfident predictions. This module
calibrates confidence scores so that a 90% confidence means the model
is correct 90% of the time (reliability diagram alignment).

Features:
- Temperature scaling (simple, effective)
- Platt scaling (logistic regression)
- Isotonic regression
- Calibration metrics (ECE, MCE, reliability diagrams)
- Per-class calibration

Usage:
    from confidence_calibrator import ConfidenceCalibrator
    
    calibrator = ConfidenceCalibrator(method="temperature")
    calibrator.fit(val_logits, val_labels)
    
    # Calibrate new predictions
    calibrated_probs = calibrator.calibrate(raw_probs)

Author: Global System v35.0
Date: 2026-01-17
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

# Configure logger
logger = logging.getLogger(__name__)


class ConfidenceCalibrator:
    """
    Calibrator for ML confidence scores.
    
    Supports multiple calibration methods:
    - temperature: Simple temperature scaling
    - platt: Logistic regression (Platt scaling)
    - isotonic: Non-parametric isotonic regression
    
    Example:
        >>> calibrator = ConfidenceCalibrator(method="temperature")
        >>> calibrator.fit(validation_probs, validation_labels)
        >>> calibrated = calibrator.calibrate(test_probs)
    """
    
    def __init__(self, method: str = "temperature"):
        """
        Initialize calibrator.
        
        Args:
            method: Calibration method ("temperature", "platt", "isotonic")
        """
        self.method = method
        self.is_fitted = False
        
        # Temperature scaling parameters
        self.temperature: float = 1.0
        
        # Platt scaling parameters
        self.platt_a: float = 0.0
        self.platt_b: float = 1.0
        
        # Isotonic regression model
        self._isotonic_model = None
        
        # Per-class temperatures
        self.per_class_temps: Dict[int, float] = {}
        
        # Metrics
        self.ece_before: float = 0.0
        self.ece_after: float = 0.0
    
    def fit(
        self, 
        probs: np.ndarray, 
        labels: np.ndarray,
        n_bins: int = 15
    ) -> "ConfidenceCalibrator":
        """
        Fit calibrator on validation data.
        
        Args:
            probs: Predicted probabilities, shape (n_samples,) or (n_samples, n_classes)
            labels: True labels, shape (n_samples,)
            n_bins: Number of bins for calibration
            
        Returns:
            self: Fitted calibrator
        """
        probs = np.asarray(probs)
        labels = np.asarray(labels)
        
        # Calculate ECE before calibration
        self.ece_before = self._expected_calibration_error(probs, labels, n_bins)
        logger.info(f"ECE before calibration: {self.ece_before:.4f}")
        
        if self.method == "temperature":
            self._fit_temperature(probs, labels)
        elif self.method == "platt":
            self._fit_platt(probs, labels)
        elif self.method == "isotonic":
            self._fit_isotonic(probs, labels)
        else:
            raise ValueError(f"Unknown method: {self.method}")
        
        # Calculate ECE after calibration
        calibrated = self.calibrate(probs)
        self.ece_after = self._expected_calibration_error(calibrated, labels, n_bins)
        logger.info(f"ECE after calibration: {self.ece_after:.4f}")
        
        self.is_fitted = True
        return self
    
    def _fit_temperature(
        self, 
        probs: np.ndarray, 
        labels: np.ndarray
    ) -> None:
        """
        Fit temperature scaling.
        
        Finds optimal temperature T that minimizes NLL.
        Calibrated prob = softmax(logits / T)
        For binary: calibrated = sigmoid(logit / T)
        
        Uses simple grid search for robustness.
        """
        best_temp = 1.0
        best_nll = float('inf')
        
        # Grid search over temperatures
        for temp in np.linspace(0.1, 5.0, 50):
            calibrated = self._apply_temperature(probs, temp)
            nll = self._negative_log_likelihood(calibrated, labels)
            
            if nll < best_nll:
                best_nll = nll
                best_temp = temp
        
        self.temperature = best_temp
        logger.info(f"Optimal temperature: {self.temperature:.4f}")
    
    def _fit_platt(
        self, 
        probs: np.ndarray, 
        labels: np.ndarray
    ) -> None:
        """
        Fit Platt scaling (logistic regression).
        
        Learns A and B such that:
        calibrated = sigmoid(A * logit + B)
        """
        # Convert probs to logits
        eps = 1e-7
        probs = np.clip(probs, eps, 1 - eps)
        
        if probs.ndim > 1:
            probs = probs[:, 1] if probs.shape[1] == 2 else probs.max(axis=1)
        
        logits = np.log(probs / (1 - probs))
        
        # Simple gradient descent for Platt parameters
        a, b = 1.0, 0.0
        lr = 0.01
        
        for _ in range(1000):
            pred = 1 / (1 + np.exp(-(a * logits + b)))
            pred = np.clip(pred, eps, 1 - eps)
            
            # Gradient
            diff = pred - labels
            grad_a = np.mean(diff * logits)
            grad_b = np.mean(diff)
            
            a -= lr * grad_a
            b -= lr * grad_b
        
        self.platt_a = a
        self.platt_b = b
        logger.info(f"Platt parameters: a={a:.4f}, b={b:.4f}")
    
    def _fit_isotonic(
        self, 
        probs: np.ndarray, 
        labels: np.ndarray
    ) -> None:
        """
        Fit isotonic regression.
        
        Non-parametric method that learns a monotonic mapping.
        """
        if probs.ndim > 1:
            probs = probs[:, 1] if probs.shape[1] == 2 else probs.max(axis=1)
        
        try:
            from sklearn.isotonic import IsotonicRegression
            
            self._isotonic_model = IsotonicRegression(
                out_of_bounds='clip'
            ).fit(probs, labels)
            
            logger.info("Fitted isotonic regression model")
        except ImportError:
            logger.warning("sklearn not available, falling back to temperature")
            self._fit_temperature(probs, labels)
    
    def calibrate(
        self, 
        probs: np.ndarray,
        class_id: Optional[int] = None
    ) -> np.ndarray:
        """
        Calibrate confidence scores.
        
        Args:
            probs: Raw probabilities to calibrate
            class_id: Optional class for per-class calibration
            
        Returns:
            Calibrated probabilities
        """
        probs = np.asarray(probs)
        
        if self.method == "temperature":
            temp = self.per_class_temps.get(class_id, self.temperature)
            return self._apply_temperature(probs, temp)
        
        elif self.method == "platt":
            return self._apply_platt(probs)
        
        elif self.method == "isotonic":
            return self._apply_isotonic(probs)
        
        return probs
    
    def _apply_temperature(
        self, 
        probs: np.ndarray, 
        temperature: float
    ) -> np.ndarray:
        """Apply temperature scaling to probabilities."""
        eps = 1e-7
        probs = np.clip(probs, eps, 1 - eps)
        
        if probs.ndim == 1:
            # Binary case: convert to logit, scale, convert back
            logits = np.log(probs / (1 - probs))
            scaled_logits = logits / temperature
            return 1 / (1 + np.exp(-scaled_logits))
        else:
            # Multi-class: apply softmax with temperature
            logits = np.log(probs)
            scaled_logits = logits / temperature
            exp_logits = np.exp(scaled_logits - scaled_logits.max(axis=1, keepdims=True))
            return exp_logits / exp_logits.sum(axis=1, keepdims=True)
    
    def _apply_platt(self, probs: np.ndarray) -> np.ndarray:
        """Apply Platt scaling to probabilities."""
        eps = 1e-7
        probs = np.clip(probs, eps, 1 - eps)
        
        if probs.ndim > 1:
            probs = probs[:, 1] if probs.shape[1] == 2 else probs.max(axis=1)
        
        logits = np.log(probs / (1 - probs))
        scaled = self.platt_a * logits + self.platt_b
        return 1 / (1 + np.exp(-scaled))
    
    def _apply_isotonic(self, probs: np.ndarray) -> np.ndarray:
        """Apply isotonic regression to probabilities."""
        if self._isotonic_model is None:
            return probs
        
        if probs.ndim > 1:
            probs = probs[:, 1] if probs.shape[1] == 2 else probs.max(axis=1)
        
        return self._isotonic_model.predict(probs)
    
    def _expected_calibration_error(
        self, 
        probs: np.ndarray, 
        labels: np.ndarray,
        n_bins: int = 15
    ) -> float:
        """
        Calculate Expected Calibration Error (ECE).
        
        ECE measures the difference between predicted confidence
        and actual accuracy, averaged over confidence bins.
        
        Args:
            probs: Predicted probabilities
            labels: True labels
            n_bins: Number of calibration bins
            
        Returns:
            ECE value (lower is better, 0 is perfect)
        """
        if probs.ndim > 1:
            confidences = probs.max(axis=1)
            predictions = probs.argmax(axis=1)
        else:
            confidences = np.maximum(probs, 1 - probs)
            predictions = (probs > 0.5).astype(int)
        
        accuracies = (predictions == labels).astype(float)
        
        # Bin boundaries
        bin_boundaries = np.linspace(0, 1, n_bins + 1)
        ece = 0.0
        
        for i in range(n_bins):
            # Get samples in this bin
            in_bin = (confidences > bin_boundaries[i]) & \
                     (confidences <= bin_boundaries[i + 1])
            
            if in_bin.sum() > 0:
                avg_confidence = confidences[in_bin].mean()
                avg_accuracy = accuracies[in_bin].mean()
                bin_weight = in_bin.sum() / len(confidences)
                
                ece += bin_weight * abs(avg_accuracy - avg_confidence)
        
        return ece
    
    def _negative_log_likelihood(
        self, 
        probs: np.ndarray, 
        labels: np.ndarray
    ) -> float:
        """Calculate negative log likelihood."""
        eps = 1e-7
        probs = np.clip(probs, eps, 1 - eps)
        
        if probs.ndim == 1:
            nll = -np.mean(
                labels * np.log(probs) + (1 - labels) * np.log(1 - probs)
            )
        else:
            nll = -np.mean(np.log(probs[np.arange(len(labels)), labels]))
        
        return nll
    
    def get_reliability_diagram_data(
        self, 
        probs: np.ndarray, 
        labels: np.ndarray,
        n_bins: int = 10
    ) -> Dict[str, List[float]]:
        """
        Get data for plotting reliability diagram.
        
        Returns:
            Dictionary with bin_midpoints, accuracies, confidences, counts
        """
        if probs.ndim > 1:
            confidences = probs.max(axis=1)
            predictions = probs.argmax(axis=1)
        else:
            confidences = np.maximum(probs, 1 - probs)
            predictions = (probs > 0.5).astype(int)
        
        accuracies = (predictions == labels).astype(float)
        
        bin_boundaries = np.linspace(0, 1, n_bins + 1)
        bin_midpoints = []
        bin_accuracies = []
        bin_confidences = []
        bin_counts = []
        
        for i in range(n_bins):
            in_bin = (confidences > bin_boundaries[i]) & \
                     (confidences <= bin_boundaries[i + 1])
            
            bin_midpoints.append((bin_boundaries[i] + bin_boundaries[i + 1]) / 2)
            
            if in_bin.sum() > 0:
                bin_accuracies.append(accuracies[in_bin].mean())
                bin_confidences.append(confidences[in_bin].mean())
                bin_counts.append(int(in_bin.sum()))
            else:
                bin_accuracies.append(0)
                bin_confidences.append(0)
                bin_counts.append(0)
        
        return {
            "bin_midpoints": bin_midpoints,
            "accuracies": bin_accuracies,
            "confidences": bin_confidences,
            "counts": bin_counts
        }
    
    def save(self, path: str) -> None:
        """Save calibrator to file."""
        data = {
            "method": self.method,
            "temperature": self.temperature,
            "platt_a": self.platt_a,
            "platt_b": self.platt_b,
            "per_class_temps": self.per_class_temps,
            "ece_before": self.ece_before,
            "ece_after": self.ece_after,
            "is_fitted": self.is_fitted
        }
        
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Saved calibrator to {path}")
    
    @classmethod
    def load(cls, path: str) -> "ConfidenceCalibrator":
        """Load calibrator from file."""
        with open(path, 'r') as f:
            data = json.load(f)
        
        calibrator = cls(method=data["method"])
        calibrator.temperature = data["temperature"]
        calibrator.platt_a = data["platt_a"]
        calibrator.platt_b = data["platt_b"]
        calibrator.per_class_temps = data.get("per_class_temps", {})
        calibrator.ece_before = data["ece_before"]
        calibrator.ece_after = data["ece_after"]
        calibrator.is_fitted = data["is_fitted"]
        
        logger.info(f"Loaded calibrator from {path}")
        return calibrator
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get calibration metrics."""
        return {
            "method": self.method,
            "is_fitted": self.is_fitted,
            "ece_before": self.ece_before,
            "ece_after": self.ece_after,
            "ece_improvement": self.ece_before - self.ece_after,
            "temperature": self.temperature if self.method == "temperature" else None,
            "platt_params": {"a": self.platt_a, "b": self.platt_b} if self.method == "platt" else None
        }


def calibrate_predictions(
    predictions: List[Dict[str, Any]],
    calibrator: ConfidenceCalibrator
) -> List[Dict[str, Any]]:
    """
    Calibrate a list of prediction dictionaries.
    
    Args:
        predictions: List of predictions with 'confidence' key
        calibrator: Fitted calibrator
        
    Returns:
        Predictions with calibrated confidence
    """
    calibrated = []
    
    for pred in predictions:
        new_pred = pred.copy()
        
        if 'confidence' in pred:
            raw_conf = pred['confidence']
            calibrated_conf = float(calibrator.calibrate(np.array([raw_conf]))[0])
            
            new_pred['confidence'] = calibrated_conf
            new_pred['raw_confidence'] = raw_conf
        
        calibrated.append(new_pred)
    
    return calibrated
