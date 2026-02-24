# Guide: Plant Disease Diagnosis Pipeline (v26.0)

> **Scope**: End-to-End Disease Detection Workflow
> **Audience**: Data Scientists, Agricultural Engineers, Developers
> **Version**: v26.0.2 (Diamond 32)

## 1. Purpose

This guide provides a comprehensive walkthrough of the multi-view plant disease diagnosis pipeline, from image capture through classification and similarity search, with specific guidance for agricultural applications.

## 2. Pipeline Overview

`Image Capture → Preprocessing → Multi-View Generation → Feature Extraction → Classification → Explainability → Similarity Search → Report Generation`

## 3. Image Capture Standards

### 3.1 Camera Requirements
- **Minimum resolution**: 1280×960 pixels (1.2 MP).
- **Recommended**: 2048×1536 pixels (3 MP) for fine lesion detail.
- **Format**: JPEG (quality ≥ 85) or PNG (lossless for research).
- **Lighting**: Diffuse natural light preferred. Avoid direct flash (creates specular highlights).

### 3.2 Capture Protocol
- **Distance**: 15-30 cm from leaf surface.
- **Angle**: Perpendicular to leaf surface (minimize perspective distortion).
- **Background**: Solid contrasting color (white/black board) for lab. Not controlled for field.
- **Include**: Both healthy and affected areas of the same plant when possible.
- **Metadata**: GPS coordinates, date/time, plant species, growth stage.

## 4. Preprocessing Pipeline

### 4.1 Step 1: Image Validation
- Check resolution ≥ 1280×960.
- Check file size (reject < 50KB as likely corrupt, flag > 20MB as unusually large).
- Check format (JPEG, PNG, TIFF accepted).

### 4.2 Step 2: Color Space Conversion
- RGB → HSV for disease region segmentation (see `rules/ml/RULES-image-binarization.md`).
- HSV ranges per disease type defined in Section 4.2 of binarization rules.

### 4.3 Step 3: Binarization (5 Views)
- Generate 5 binary views per image: Green Mask, Disease Mask, Edge Binary, Texture Binary, Saturation Binary.
- See `rules/ml/RULES-image-binarization.md` Section 5.

### 4.4 Step 4: Quality Gates
- Foreground ratio: 5-60%.
- Contour count: 1-50.
- Reject images failing quality gates with specific error codes.

## 5. Multi-View Generation

### 5.1 Crop Strategy
- Select based on scenario per `rules/ml/RULES-multi-crop-augmentation.md` Section 5 Decision Matrix.
- For production evaluation: 10-crop + TTA = 10 views minimum.

### 5.2 Multi-Scale Processing
- For high-accuracy applications, process at 3 scales (224, 256, 384) with weighted aggregation.

## 6. Disease Identification Guide

### 6.1 Common Tomato Diseases
- **Early Blight (Alternaria solani)**: Dark brown concentric rings (“target spots”) on older leaves. HSV: H=10-20, S=50-200, V=20-150.
- **Late Blight (Phytophthora infestans)**: Water-soaked gray-green lesions, white fuzzy growth on underside. HSV: H=60-100, S=20-60, V=40-120.
- **Powdery Mildew**: White powdery coating on leaf surface. HSV: S < 30, V > 200.
- **Bacterial Spot (Xanthomonas)**: Small dark angular spots bounded by leaf veins.
- **Leaf Curl (TYLCV)**: Upward curling, yellowing, stunted growth. Virus — no direct lesion.

### 6.2 Common Potato Diseases
- **Late Blight (Phytophthora)**: Same pathogen as tomato. Dark water-soaked lesions.
- **Early Blight (Alternaria)**: Concentric ring lesions on lower leaves first.
- **Black Scurf (Rhizoctonia)**: Dark sclerotia on tuber surface.

### 6.3 Common Cucumber/Melon Diseases
- **Downy Mildew**: Angular yellow patches on upper leaf, gray-purple sporulation on underside.
- **Powdery Mildew**: White powdery patches, typically starts on lower leaves.

## 7. Classification & Similarity Search

### 7.1 Classification Pipeline
- **Model**: DINOv2 ViT-B/14 + classification head.
- **Output**: Softmax probability per disease class.
- **Confidence threshold**: ≥ 0.6 for automatic classification, < 0.6 flagged for human review.

### 7.2 Similarity Search
- **Embedding**: DINOv2 768d L2-normalized vectors.
- **Vector DB**: Per selection criteria in `rules/ml/RULES-embedding-storage.md`.
- **Return**: Top-5 most similar images with disease labels and confidence scores.
- **Match threshold**: cosine > 0.85 for same-disease confirmation.

## 8. Explainability (GradCAM)
- Generate GradCAM heatmap per `rules/ml/RULES-gradcam-heatmap.md`.
- Validate overlap ≥ 70% with leaf region, BAR < 30%.
- Include heatmap visualization in diagnosis report.

## 9. Report Generation
- Each diagnosis report includes: original image, binary mask, GradCAM overlay, top-3 disease predictions with confidence scores, top-5 similar historical images, and recommended treatment actions.

## 10. Cross-References
- **Binarization**: `rules/ml/RULES-image-binarization.md`
- **Multi-Crop**: `rules/ml/RULES-multi-crop-augmentation.md`
- **Embeddings**: `rules/ml/RULES-embedding-storage.md`
- **GradCAM**: `rules/ml/RULES-gradcam-heatmap.md`
- **Master Rules**: `rules/ml/RULES-plant-disease-analysis.md`
- **Example**: `examples/ml/EXAMPLE-multi-view-plant-disease.md`
