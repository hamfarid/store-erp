# Prompt 67: Image Processing & OCR

> **Scope**: Image analysis, OCR, screenshots for GAARA-AI
> **Container**: gaara-image (port 8003)

## Capabilities

| Capability | Tool | Notes |
|:-----------|:-----|:------|
| OCR (Arabic) | EasyOCR | Primary — supports Arabic + English simultaneously |
| OCR (English) | EasyOCR + Tesseract | Tesseract as fallback |
| Image Analysis | CLIP / Florence-2 | Describe image, answer questions, tag objects |
| Screenshots | Playwright | Full-page website screenshots |
| Image Editing | OpenCV + Pillow | Resize, crop, watermark, format conversion |

## Arabic OCR Priority
- EasyOCR is the primary OCR engine — it handles Arabic natively
- Always set `languages=['ar', 'en']` for bilingual documents
- For pure English documents, Tesseract can be faster

## Rules
- All image models run in ONNX format on CPU
- Maximum image size: configurable (default 10MB)
- Screenshots: default 1920x1080, configurable width/height
- OCR output includes: text, language detected, confidence, bounding regions
- CLIP analysis returns: description, tags, objects detected
