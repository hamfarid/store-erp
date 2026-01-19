### Security hardening (ethical hacking / OWASP baseline)

This repo includes **baseline protections** to reduce common findings from automated “ethical hacking” scans:

- **Security headers & CSP**: set in `backend/src/core/middleware.py`
- **Trusted hosts** (production): enabled in `backend/src/core/app_factory.py`
- **Rate limiting**: via `slowapi`
- **Request/body size limits**: enforced early in `backend/src/core/middleware.py`
- **Upload validation** (type sniffing + Pillow verify + decompression bomb protection): in `backend/src/utils/image_validation.py` and enforced in `backend/src/api/v1/upload.py`

### “Buffer overflow” note (web context)

Python/FastAPI itself is memory-safe, but **oversized/hostile payloads** can trigger crashes or extreme memory usage in native dependencies (image/ML libs).  
This is why we enforce:

- **Max request size** (`MAX_JSON_BODY_SIZE`, `MAX_MULTIPART_BODY_SIZE`)
- **Max image pixels** (`MAX_IMAGE_PIXELS`)
- **Upload content validation** (magic bytes + `Pillow.verify()`)

### Config (ENV)

Add to `.env` (backend):

- **MAX_JSON_BODY_SIZE**: default `2MB`
- **MAX_MULTIPART_BODY_SIZE**: default `60MB` (should be >= `MAX_FILE_SIZE`)
- **MAX_IMAGE_PIXELS**: default `20000000` (20MP)

### Run security scans (recommended)

From repo root:

- **Windows (PowerShell)**:
  - `powershell -ExecutionPolicy Bypass -File .\scripts\security-scan.ps1`
- **macOS/Linux**:
  - `bash ./scripts/security-scan.sh`

What it runs:

- **Frontend**: `npm audit --omit=dev --audit-level=high`
- **Backend deps**: `safety check` (if installed)
- **Backend SAST**: `bandit` (if installed)
- **Optional**: `semgrep scan --config auto` (if installed)

If a tool is missing, install:

- `pip install -r backend/requirements-test.txt`

### Dev-server note (Vite/esbuild advisory)

`npm audit` may report an `esbuild` advisory that impacts the **Vite dev server**.

Mitigation applied in this repo:
- `frontend` now binds dev/preview to **localhost by default** (see `frontend/package.json` scripts).
- Only use `npm run dev:host` / `npm run preview:host` on a trusted network.

