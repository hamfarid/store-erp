#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Enhanced model training module with advanced techniques for improving accuracy and performance.

This module implements state-of-the-art techniques for training deep learning models
for agricultural image analysis, including:
- Transfer learning with modern architectures
- Advanced regularization techniques
- Learning rate scheduling
- Model ensembling
- Knowledge distillation
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models, applications, optimizers
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau, TensorBoard
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix
import time
import json

# Ensure TensorFlow uses GPU efficiently
physical_devices = tf.config.list_physical_devices('GPU')
if physical_devices:
    try:
        for device in physical_devices:
            tf.config.experimental.set_memory_growth(device, True)
        print(f"Found {len(physical_devices)} GPU(s), memory growth enabled")
    except Exception as e:
        print(f"Error configuring GPU: {e}")
else:
    print("No GPU found, using CPU")

# --- Model Architectures ---

def create_disease_detection_model(input_shape=(224, 224, 3), num_classes=10, architecture="efficientnetb0", 
                                  weights="imagenet", dropout_rate=0.2, l2_reg=1e-4):
    """
    Creates a transfer learning model for disease detection using various architectures.
    
    Args:
        input_shape: Input image dimensions (height, width, channels)
        num_classes: Number of disease classes to predict
        architecture: Base architecture to use (efficientnetb0, resnet50, etc.)
        weights: Pre-trained weights to use (imagenet or None)
        dropout_rate: Dropout rate for regularization
        l2_reg: L2 regularization strength
        
    Returns:
        Compiled Keras model
    """
    # Select base model architecture
    if architecture == "efficientnetb0":
        base_model = applications.EfficientNetB0(weights=weights, include_top=False, input_shape=input_shape)
    elif architecture == "efficientnetb3":
        base_model = applications.EfficientNetB3(weights=weights, include_top=False, input_shape=input_shape)
    elif architecture == "resnet50":
        base_model = applications.ResNet50(weights=weights, include_top=False, input_shape=input_shape)
    elif architecture == "mobilenetv2":
        base_model = applications.MobileNetV2(weights=weights, include_top=False, input_shape=input_shape)
    elif architecture == "densenet121":
        base_model = applications.DenseNet121(weights=weights, include_top=False, input_shape=input_shape)
    else:
        raise ValueError(f"Unsupported architecture: {architecture}")
    
    # Freeze base model layers
    base_model.trainable = False
    
    # Create model
    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.BatchNormalization(),
        layers.Dropout(dropout_rate),
        layers.Dense(256, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(l2_reg)),
        layers.BatchNormalization(),
        layers.Dropout(dropout_rate),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    # Compile model
    model.compile(
        optimizer=optimizers.Adam(learning_rate=1e-3),
        loss='categorical_crossentropy',
        metrics=['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall()]
    )
    
    return model

def create_nutrient_deficiency_model(input_shape=(224, 224, 3), num_classes=8, architecture="efficientnetb0", 
                                    weights="imagenet", dropout_rate=0.2, l2_reg=1e-4):
    """
    Creates a transfer learning model for nutrient deficiency detection.
    Similar structure to disease detection but potentially with different hyperparameters.
    """
    # Similar to disease detection model but with different hyperparameters
    # For simplicity, we'll reuse the same function but in practice might have different architectures
    return create_disease_detection_model(
        input_shape=input_shape,
        num_classes=num_classes,
        architecture=architecture,
        weights=weights,
        dropout_rate=dropout_rate,
        l2_reg=l2_reg
    )

def create_soil_analysis_model(input_shape=(224, 224, 3), num_outputs=3, architecture="efficientnetb0", 
                              weights="imagenet", dropout_rate=0.3, l2_reg=1e-4):
    """
    Creates a model for soil analysis that outputs multiple continuous values.
    
    Args:
        input_shape: Input image dimensions
        num_outputs: Number of soil properties to predict (e.g., pH, organic matter, etc.)
        
    Returns:
        Compiled Keras model for regression
    """
    # Select base model architecture
    if architecture == "efficientnetb0":
        base_model = applications.EfficientNetB0(weights=weights, include_top=False, input_shape=input_shape)
    elif architecture == "mobilenetv2":
        base_model = applications.MobileNetV2(weights=weights, include_top=False, input_shape=input_shape)
    else:
        raise ValueError(f"Unsupported architecture for soil analysis: {architecture}")
    
    # Freeze base model layers
    base_model.trainable = False
    
    # Create model with regression outputs
    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.BatchNormalization(),
        layers.Dropout(dropout_rate),
        layers.Dense(128, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(l2_reg)),
        layers.BatchNormalization(),
        layers.Dropout(dropout_rate),
        layers.Dense(64, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(l2_reg)),
        layers.Dense(num_outputs)  # No activation for regression
    ])
    
    # Compile model for regression
    model.compile(
        optimizer=optimizers.Adam(learning_rate=1e-3),
        loss='mse',  # Mean squared error for regression
        metrics=['mae']  # Mean absolute error
    )
    
    return model

# --- Advanced Training Techniques ---

def get_callbacks(model_name, patience=10, min_delta=0.001, log_dir="logs"):
    """
    Creates a set of callbacks for training, including:
    - Model checkpointing
    - Early stopping
    - Learning rate reduction
    - TensorBoard logging
    
    Args:
        model_name: Name for saving model checkpoints
        patience: Number of epochs to wait for improvement before early stopping
        min_delta: Minimum change to qualify as improvement
        log_dir: Directory for TensorBoard logs
        
    Returns:
        List of Keras callbacks
    """
    # Create directories if they don't exist
    os.makedirs(f"models/{model_name}", exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)
    
    callbacks = [
        # Save best model
        ModelCheckpoint(
            filepath=f"models/{model_name}/best_model.h5",
            monitor='val_loss',
            save_best_only=True,
            mode='min',
            verbose=1
        ),
        # Early stopping to prevent overfitting
        EarlyStopping(
            monitor='val_loss',
            patience=patience,
            min_delta=min_delta,
            restore_best_weights=True,
            verbose=1
        ),
        # Reduce learning rate when plateau is reached
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=patience // 2,
            min_lr=1e-6,
            verbose=1
        ),
        # TensorBoard logging
        TensorBoard(
            log_dir=f"{log_dir}/{model_name}_{int(time.time())}",
            histogram_freq=1,
            update_freq='epoch'
        )
    ]
    
    return callbacks

def train_with_fine_tuning(model, train_data, val_data, epochs=50, fine_tune_epochs=30, 
                          fine_tune_at=0.7, callbacks=None, batch_size=32):
    """
    Trains a model with a two-phase approach:
    1. Train only the top layers with the base model frozen
    2. Fine-tune the top portion of the base model
    
    Args:
        model: Compiled Keras model
        train_data: Training data generator or dataset
        val_data: Validation data generator or dataset
        epochs: Number of epochs for initial training
        fine_tune_epochs: Number of epochs for fine-tuning
        fine_tune_at: Proportion of the base model to unfreeze (0.7 = unfreeze top 30%)
        callbacks: List of Keras callbacks
        batch_size: Batch size for training
        
    Returns:
        Training history and fine-tuning history
    """
    print("Phase 1: Training top layers...")
    history = model.fit(
        train_data,
        validation_data=val_data,
        epochs=epochs,
        callbacks=callbacks,
        batch_size=batch_size
    )
    
    # Get the base model (assuming it's the first layer in a Sequential model)
    base_model = model.layers[0]
    
    # Calculate how many layers to unfreeze
    if isinstance(base_model, tf.keras.Model):  # Check if it's a proper model
        total_layers = len(base_model.layers)
        fine_tune_from = int(total_layers * (1 - fine_tune_at))
        
        print(f"Phase 2: Fine-tuning from layer {fine_tune_from}/{total_layers}...")
        
        # Unfreeze the top layers of the base model
        base_model.trainable = True
        for layer in base_model.layers[:fine_tune_from]:
            layer.trainable = False
            
        # Recompile the model with a lower learning rate
        model.compile(
            optimizer=optimizers.Adam(learning_rate=1e-4),  # Lower learning rate for fine-tuning
            loss=model.loss,
            metrics=model.metrics
        )
        
        # Continue training with fine-tuning
        fine_tune_history = model.fit(
            train_data,
            validation_data=val_data,
            epochs=epochs + fine_tune_epochs,
            initial_epoch=epochs,
            callbacks=callbacks,
            batch_size=batch_size
        )
        
        # Combine histories
        combined_history = {}
        for key in history.history:
            combined_history[key] = history.history[key] + fine_tune_history.history[key]
            
        return combined_history
    else:
        print("Base model is not a proper Keras model, skipping fine-tuning")
        return history.history

# --- Model Ensembling ---

class ModelEnsemble:
    """
    Implements model ensembling for improved prediction accuracy.
    Supports various ensemble methods: averaging, weighted averaging, and stacking.
    """
    
    def __init__(self, models, ensemble_method='average', weights=None):
        """
        Initialize the ensemble.
        
        Args:
            models: List of trained Keras models
            ensemble_method: Method for combining predictions ('average', 'weighted', 'stacking')
            weights: Weights for weighted averaging (only used if method is 'weighted')
        """
        self.models = models
        self.method = ensemble_method
        
        if weights is None and ensemble_method == 'weighted':
            # Equal weights by default
            self.weights = [1/len(models)] * len(models)
        else:
            self.weights = weights
            
        self.meta_model = None  # For stacking
        
    def predict(self, X):
        """
        Make predictions using the ensemble.
        
        Args:
            X: Input data
            
        Returns:
            Ensemble predictions
        """
        if self.method == 'average':
            # Simple averaging
            predictions = [model.predict(X) for model in self.models]
            return np.mean(predictions, axis=0)
            
        elif self.method == 'weighted':
            # Weighted averaging
            predictions = [model.predict(X) * weight for model, weight in zip(self.models, self.weights)]
            return np.sum(predictions, axis=0)
            
        elif self.method == 'stacking' and self.meta_model is not None:
            # Stacking: use base models to generate features for meta-model
            base_predictions = np.hstack([model.predict(X) for model in self.models])
            return self.meta_model.predict(base_predictions)
            
        else:
            raise ValueError(f"Invalid ensemble method or meta-model not trained: {self.method}")
    
    def train_meta_model(self, X_train, y_train, X_val, y_val):
        """
        Train a meta-model for stacking ensemble.
        
        Args:
            X_train: Training data
            y_train: Training labels
            X_val: Validation data
            y_val: Validation labels
        """
        if self.method != 'stacking':
            print("Meta-model training is only used for stacking ensemble")
            return
            
        # Generate predictions from base models
        train_predictions = np.hstack([model.predict(X_train) for model in self.models])
        val_predictions = np.hstack([model.predict(X_val) for model in self.models])
        
        # Create a simple meta-model
        input_dim = train_predictions.shape[1]
        output_dim = y_train.shape[1] if len(y_train.shape) > 1 else 1
        
        self.meta_model = models.Sequential([
            layers.Dense(64, activation='relu', input_shape=(input_dim,)),
            layers.Dropout(0.3),
            layers.Dense(output_dim, activation='softmax' if output_dim > 1 else 'sigmoid')
        ])
        
        # Compile and train
        self.meta_model.compile(
            optimizer='adam',
            loss='categorical_crossentropy' if output_dim > 1 else 'binary_crossentropy',
            metrics=['accuracy']
        )
        
        self.meta_model.fit(
            train_predictions, y_train,
            validation_data=(val_predictions, y_val),
            epochs=50,
            callbacks=[EarlyStopping(patience=5, restore_best_weights=True)]
        )
        
        print("Meta-model trained successfully")

# --- Knowledge Distillation ---

def knowledge_distillation_loss(alpha=0.1, temperature=5.0):
    """
    Creates a knowledge distillation loss function.
    
    Args:
        alpha: Weight for distillation loss vs. standard loss (0-1)
        temperature: Temperature for softening probability distributions
        
    Returns:
        Custom loss function
    """
    def loss(y_true, y_pred):
        # y_pred is expected to be [student_logits, teacher_logits]
        y_pred_student, y_pred_teacher = y_pred
        
        # Standard categorical crossentropy for true labels
        student_loss = tf.keras.losses.categorical_crossentropy(
            y_true, y_pred_student, from_logits=True
        )
        
        # Soft targets from teacher
        teacher_pred = tf.nn.softmax(y_pred_teacher / temperature)
        student_pred = tf.nn.softmax(y_pred_student / temperature)
        
        # KL divergence for soft targets
        distillation_loss = tf.keras.losses.kullback_leibler_divergence(
            teacher_pred, student_pred
        ) * (temperature ** 2)
        
        # Combine losses
        return (1 - alpha) * student_loss + alpha * distillation_loss
    
    return loss

def create_distilled_model(teacher_model, input_shape=(224, 224, 3), num_classes=10, 
                          architecture="mobilenetv2", dropout_rate=0.2):
    """
    Creates a smaller student model that learns from a larger teacher model.
    
    Args:
        teacher_model: Trained teacher model
        input_shape: Input dimensions
        num_classes: Number of classes
        architecture: Base architecture for student (typically smaller than teacher)
        dropout_rate: Dropout rate
        
    Returns:
        Compiled student model
    """
    # Create a smaller student model
    if architecture == "mobilenetv2":
        base_model = applications.MobileNetV2(
            weights="imagenet", include_top=False, input_shape=input_shape
        )
    elif architecture == "efficientnetb0":
        base_model = applications.EfficientNetB0(
            weights="imagenet", include_top=False, input_shape=input_shape
        )
    else:
        raise ValueError(f"Unsupported architecture for student model: {architecture}")
    
    # Student model
    student_model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.BatchNormalization(),
        layers.Dropout(dropout_rate),
        layers.Dense(128, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(dropout_rate),
        layers.Dense(num_classes)  # No activation for logits
    ])
    
    # Create a custom model that outputs both student and teacher predictions
    input_layer = layers.Input(shape=input_shape)
    student_pred = student_model(input_layer)
    teacher_pred = teacher_model(input_layer)
    
    # Combined model for training
    distill_model = models.Model(
        inputs=input_layer,
        outputs=[student_pred, teacher_pred]
    )
    
    # Freeze the teacher model
    teacher_model.trainable = False
    
    # Compile with custom loss
    distill_model.compile(
        optimizer=optimizers.Adam(learning_rate=1e-3),
        loss=knowledge_distillation_loss(alpha=0.1, temperature=5.0),
        metrics=['accuracy']
    )
    
    return distill_model, student_model

# --- Model Evaluation and Visualization ---

def evaluate_model(model, test_data, class_names=None):
    """
    Evaluates a model and generates detailed performance metrics.
    
    Args:
        model: Trained Keras model
        test_data: Test dataset or generator
        class_names: List of class names for classification reports
        
    Returns:
        Dictionary of evaluation metrics
    """
    # Get predictions
    if hasattr(test_data, 'unbatch'):
        # TensorFlow dataset
        x_test = np.vstack([x for x, _ in test_data.unbatch()])
        y_test = np.vstack([y for _, y in test_data.unbatch()])
        y_pred = model.predict(x_test)
    else:
        # Assume it's a generator
        steps = test_data.samples // test_data.batch_size + 1
        y_pred = model.predict(test_data, steps=steps)
        y_test = test_data.classes
        
        # Convert to one-hot if needed
        if len(y_pred.shape) > 1 and y_pred.shape[1] > 1:
            y_test = tf.keras.utils.to_categorical(y_test, num_classes=y_pred.shape[1])
    
    # Calculate metrics
    results = {}
    
    # For classification
    if len(y_pred.shape) > 1 and y_pred.shape[1] > 1:
        # Convert predictions to class indices
        y_pred_classes = np.argmax(y_pred, axis=1)
        y_test_classes = np.argmax(y_test, axis=1) if len(y_test.shape) > 1 else y_test
        
        # Classification report
        if class_names is None:
            class_names = [f"Class {i}" for i in range(y_pred.shape[1])]
            
        report = classification_report(
            y_test_classes, y_pred_classes, 
            target_names=class_names, 
            output_dict=True
        )
        results['classification_report'] = report
        
        # Confusion matrix
        cm = confusion_matrix(y_test_classes, y_pred_classes)
        results['confusion_matrix'] = cm.tolist()  # Convert to list for JSON serialization
        
    # For regression
    else:
        # Mean absolute error
        mae = np.mean(np.abs(y_pred - y_test))
        results['mae'] = float(mae)
        
        # Mean squared error
        mse = np.mean(np.square(y_pred - y_test))
        results['mse'] = float(mse)
        
        # R-squared
        ss_total = np.sum(np.square(y_test - np.mean(y_test)))
        ss_residual = np.sum(np.square(y_test - y_pred))
        r2 = 1 - (ss_residual / ss_total)
        results['r2'] = float(r2)
    
    return results

def plot_training_history(history, save_path=None):
    """
    Plots training and validation metrics.
    
    Args:
        history: Training history from model.fit()
        save_path: Path to save the plot (if None, plot is displayed)
    """
    plt.figure(figsize=(12, 5))
    
    # Plot accuracy
    plt.subplot(1, 2, 1)
    if 'accuracy' in history:
        plt.plot(history['accuracy'], label='Training Accuracy')
    if 'val_accuracy' in history:
        plt.plot(history['val_accuracy'], label='Validation Accuracy')
    plt.title('Model Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    
    # Plot loss
    plt.subplot(1, 2, 2)
    if 'loss' in history:
        plt.plot(history['loss'], label='Training Loss')
    if 'val_loss' in history:
        plt.plot(history['val_loss'], label='Validation Loss')
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()

def plot_confusion_matrix(cm, class_names, save_path=None):
    """
    Plots a confusion matrix.
    
    Args:
        cm: Confusion matrix
        class_names: List of class names
        save_path: Path to save the plot (if None, plot is displayed)
    """
    plt.figure(figsize=(10, 8))
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('Confusion Matrix')
    plt.colorbar()
    
    tick_marks = np.arange(len(class_names))
    plt.xticks(tick_marks, class_names, rotation=45)
    plt.yticks(tick_marks, class_names)
    
    # Add text annotations
    thresh = cm.max() / 2.0
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(j, i, format(cm[i, j], 'd'),
                    horizontalalignment="center",
                    color="white" if cm[i, j] > thresh else "black")
    
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    
    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()

# --- Model Saving and Loading ---

def save_model_with_metadata(model, model_name, metadata=None):
    """
    Saves a model with its metadata.
    
    Args:
        model: Keras model to save
        model_name: Name for the model
        metadata: Dictionary of metadata to save with the model
    """
    # Create directory if it doesn't exist
    os.makedirs(f"models/{model_name}", exist_ok=True)
    
    # Save model
    model.save(f"models/{model_name}/model.h5")
    
    # Save metadata
    if metadata:
        with open(f"models/{model_name}/metadata.json", 'w') as f:
            json.dump(metadata, f, indent=4)
    
    print(f"Model saved to models/{model_name}/")

def load_model_with_metadata(model_name):
    """
    Loads a model and its metadata.
    
    Args:
        model_name: Name of the model to load
        
    Returns:
        Tuple of (model, metadata)
    """
    # Load model
    model = tf.keras.models.load_model(f"models/{model_name}/model.h5")
    
    # Load metadata if it exists
    metadata = None
    metadata_path = f"models/{model_name}/metadata.json"
    if os.path.exists(metadata_path):
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
    
    return model, metadata

# --- Example Usage ---
if __name__ == "__main__":
    print("Enhanced model training module loaded")
    
    # Example: Create a disease detection model
    model = create_disease_detection_model(
        input_shape=(224, 224, 3),
        num_classes=5,
        architecture="efficientnetb0"
    )
    
    print("Model created successfully")
    model.summary()
