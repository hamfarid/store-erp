# Workflow 13: Avatar Presentation Pipeline

> **Trigger**: Any AI output can be converted to avatar video
> **Modules Involved**: API Gateway → LLM → Avatar (TTS + Video)

## Steps

### Step 1: Script Generation
- Receive AI output (diagnosis report, search summary, learning report)
- Send to Ollama LLM:
  - "Convert this into a natural Arabic script for a 1-2 minute presentation: {content}"
- LLM returns spoken-language Arabic script

### Step 2: Text-to-Speech
- Send script to TTS engine (Bark for quality, Coqui for speed)
- Generate Arabic audio (WAV format)
- Return audio for preview

### Step 3: Avatar Video Generation
- Reference image (GAARA AI avatar face)
- SadTalker: animate face using audio waveform
- Wav2Lip: fine-tune lip synchronization
- Output: MP4 video with talking avatar

### Step 4: Delivery
- Store video in MinIO object storage
- Return video URL to user
- Save to gallery (PostgreSQL AIAvatarVideo model)

## Performance Notes
- CPU: 30-120 seconds per 1 minute of video
- GPU: 10-30 seconds per 1 minute of video
- Always a Celery task (ai_tasks queue)
- Audio preview available before full video generation
