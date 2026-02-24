# Data Privacy & GDPR Compliance Rules — ML Extension

> See the primary rule: [`rules/data-privacy-gdpr.md`](../data-privacy-gdpr.md)
>
> This file extends the base GDPR rules with ML-specific requirements.

## ML-Specific Additions

1. **Training Data**: All training datasets must be anonymized or have explicit consent
2. **Model Outputs**: Predictions containing PII must be encrypted at rest
3. **Data Lineage**: Full lineage tracking from source to model output (see `templates/ml/TEMPLATE-data-lineage.md`)
4. **Right to Erasure**: Models trained on user data must support retraining without specific user records
5. **Bias Audit**: Regular bias audits on demographic attributes per GDPR Article 22
