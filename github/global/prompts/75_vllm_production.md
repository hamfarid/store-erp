# Prompt 75: vLLM — Production LLM Serving

> **Complements**: Ollama (Prompt 62 — development/easy setup)
> **Use Case**: High-throughput production inference

## When to Use vLLM vs Ollama
| Aspect | Ollama | vLLM |
|:-------|:-------|:-----|
| Setup | 1-command install | pip install |
| Speed | Good (single user) | 2.7x faster (batching) |
| Memory | Standard | 60-80% less (PagedAttention) |
| Batching | Sequential | Continuous batching |
| Best For | Development, testing | Production, multi-user |
| API | OpenAI-compatible | OpenAI-compatible |

## Recommended Strategy
- **Development/Testing**: Ollama (easy model management, 100+ models)
- **Production/Multi-User**: vLLM (PagedAttention, continuous batching)
- **Edge/Limited Resources**: llama.cpp (lightest, C++ speed)
- **GUI Testing**: LM Studio (desktop app)

## Model Recommendations for GAARA
| Model | Size | VRAM (Q4) | Best For |
|:------|:-----|:----------|:---------|
| Llama 3.1 8B | 8B | ~5 GB | Primary system engine |
| Mistral 7B | 7B | ~4.5 GB | Fast alternative |
| Qwen 2.5 7B | 7B | ~4.5 GB | Excellent Arabic support |
| CodeLlama 7B | 7B | ~4.5 GB | ERP code generation |
| BGE-M3 | 137M | ~0.5 GB | Embeddings (multilingual) |
| Llama 3.1 70B | 70B | ~40 GB* | Complex tasks (Q4) |

## Cost Comparison: Local vs API
- **OpenAI GPT-4o**: $15/M input + $60/M output ≈ $200-500/month
- **Local (RTX 4090 + Llama 3.1 8B)**: ~$30-50/month electricity
- **GPU cost**: $1,600-2,000 one-time → ROI in 3-4 months

## GPU Capabilities
- **RTX 4090 (24GB)**: All 7B-14B models, 70B with Q4 (slow)
- **RTX 3090 (24GB)**: Same as 4090 but 20-30% slower ($700-900 used)
- **RTX 5090 (32GB)**: All above + 70B Q4 comfortably, 67% faster than 4090
