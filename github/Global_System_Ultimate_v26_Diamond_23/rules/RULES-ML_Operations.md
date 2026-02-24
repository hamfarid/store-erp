# Rules: ML Operations

## 1. Data Integrity
- Always validate input data before processing.
- Use version control for datasets (DVC).

## 2. Model Training
- Log all experiments using MLflow or Weights & Biases.
- Implement early stopping to prevent overfitting.
- Use cross-validation for robust evaluation.

## 3. Deployment
- Containerize models using Docker.
- Monitor model drift in production.
- Implement A/B testing for new model versions.
