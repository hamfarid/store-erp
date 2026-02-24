# Prompt 68: AI Avatar & Text-to-Speech

> **Scope**: TTS and talking avatar generation for GAARA-AI
> **Container**: gaara-avatar (port 8004)

## TTS Engines

| Engine | Strength | Arabic | Notes |
|:-------|:---------|:-------|:------|
| Bark | High quality, multilingual | Good | Slow on CPU, best with GPU |
| Coqui TTS | Fast, customizable | Moderate | Better for real-time |

## Avatar Pipeline
```
Text Input → TTS Engine (Bark/Coqui → Arabic audio)
→ Avatar Engine (SadTalker → animate face from reference image)
→ Lip Sync (Wav2Lip → match lip movement to audio)
→ Output MP4 video
```

## Use Cases
- Present plant diagnosis results as talking avatar
- Summarize market intelligence reports via video
- Generate training videos for farm workers (Arabic)
- Present any AI output in human-friendly video format

## Rules
- Default language: Arabic (ar)
- CPU-first: use lightweight TTS models initially
- Avatar generation is always a Celery task (takes 30-120 seconds)
- Video output: MP4 format, configurable quality
- Audio preview available before full video generation
