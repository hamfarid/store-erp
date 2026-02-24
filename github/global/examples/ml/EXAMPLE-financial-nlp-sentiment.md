# EXAMPLE-financial-nlp-sentiment.md
# Governance: ML/AI Application Framework (Feb 2026)
# Reference: FinBERT (ProsusAI/finbert)

## 1. Project Structure
```
financial-nlp-sentiment/
├── configs/
│   ├── config.yaml          # Hyperparameters, paths
│   └── logging.yaml         # Logging configuration
├── data/
│   ├── raw/                 # Immutable raw data (Financial PhraseBank)
│   ├── processed/           # Cleaned and tokenized data
│   └── splits/              # Train/Val/Test splits (stratified)
├── src/
│   ├── data/                # Data loading and preprocessing scripts
│   ├── models/              # Model definition (FinBERT)
│   ├── training/            # Training loop and evaluation
│   └── serving/             # FastAPI serving code
├── notebooks/               # EDA and experimentation notebooks
├── tests/                   # Unit and integration tests
├── Dockerfile               # Multi-stage build
├── requirements.txt         # Pinned dependencies
└── README.md                # Project documentation
```

## 2. Preprocessing Rules
*   **Tokenization:** Use `BertTokenizer` (uncased) with `max_length=512`.
*   **Normalization:**
    *   Convert tickers to `[TICKER]` token.
    *   Convert numbers to `[NUM]` token.
    *   Preserve currency symbols (`$`, `€`, `£`).
*   **Cleaning:** Remove HTML tags, URLs, and non-ASCII characters.

## 3. Model Architecture
*   **Base Model:** `ProsusAI/finbert` (110M parameters).
*   **Task:** Sequence Classification (3 classes: Positive, Negative, Neutral).
*   **Loss Function:** CrossEntropyLoss (weighted for class imbalance).
*   **Optimizer:** AdamW (learning rate: 2e-5).

## 4. Evaluation Requirements
*   **Primary Metric:** Macro-F1 Score (due to class imbalance).
*   **Secondary Metrics:** Accuracy, Precision, Recall per class.
*   **Confusion Matrix:** Mandatory analysis of misclassifications (especially Positive <-> Negative).
*   **Bias Check:** Verify performance across different sectors/industries.

## 5. Governance Checkpoints
*   **Data Validation:** Check for nulls, duplicates, and valid labels (0, 1, 2).
*   **Drift Detection:** Monitor input text distribution (embedding drift) and prediction confidence.
*   **Model Card:** Document model limitations (e.g., specific to financial news, not social media).
