# Prompt Loading Priority Order — Global System v26.0.2 Diamond 32

> **Rule**: Load prompts in this order based on available context window.
> **Total Active Prompts**: 106

## Tier 1: Always Load (~5K tokens)
```
1. rules/00-iron-rules.md
2. AGENTS.md (Section 1-3 only)
3. BOOTSTRAP.md (Section 4: GAARA-AI modules)
```

## Tier 2: Load for Any GAARA-AI Work (~12K tokens)
```
4. prompts/60_gaara_ai_architecture.md
5. prompts/61_fastapi_gateway.md
6. prompts/64_celery_task_management.md
```

## Tier 3: Load per Module (~3-5K each)
```
For LLM work:     prompts/62_ollama_llm_integration.md
For RAG/KB work:   prompts/63_rag_pipeline.md
For Plant work:    prompts/65_plant_doctor_ai.md
For Scraping:      prompts/66_web_scraping_pipeline.md
For Image/OCR:     prompts/67_image_processing_ocr.md
For Avatar/TTS:    prompts/68_avatar_tts.md
For Monitoring:    prompts/69_drift_detection.md
For Networking:    prompts/70_tailscale_cloudflare.md
```

## Tier 3b: Load per Project
```
For Gold Predictor:   prompts/71_gold_price_predictor.md
For Gaara Scan:       prompts/72_gaara_scan_plant_disease.md
For Settings Page:    prompts/73_gaara_ai_settings_page.md
For DUIX Avatar:      prompts/74_duix_avatar_advanced.md
For vLLM:            prompts/75_vllm_production.md
```

## Tier 4: General Development
```
prompts/07_code_generation.md
prompts/09_code_review.md
prompts/20_backend.md
prompts/22_database.md
prompts/26_docker.md
prompts/27_monitoring.md
prompts/30_frontend.md
prompts/31_authentication.md
prompts/41_testing.md
prompts/50_deployment.md
prompts/78_ci_cd_pipeline.md
prompts/79_logging_strategy.md
prompts/100_system_health_check.md
```

## Tier 5: As Needed
All remaining prompts (01-59, 76-77, 80-99, 101-103) loaded only when relevant to specific task.

## Full Prompt Index
See `prompts/README.md` for complete listing of all 106 prompts.
