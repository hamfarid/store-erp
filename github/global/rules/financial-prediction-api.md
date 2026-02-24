# Rule: Financial Prediction API Standards

> **Applies To**: Gold Price Predictor Backend

## API Design
- FastAPI on Port 8001, API version: v2
- Repository Pattern + Service Layer architecture
- Response time target: <50ms (from current 85ms)

## Security Requirements
1. AWS Secrets Manager for all credentials (LRU cache, 32 secrets max)
2. JWT authentication (access + refresh tokens)
3. MFA/TOTP (RFC 6238) for admin operations
4. Rate Limiting: per-user + per-IP
5. Compliance: SOC 2, PCI DSS 3.2, NIST 800-63B

## Database
- PostgreSQL 14 with read/write splitting + read replicas
- 11 strategic indexes
- Query performance target: <12ms (from 158ms → 12ms achieved, 92.4% improvement)

## Cache Strategy
- Redis 7 (cluster mode)
- Hit rate target: 90%+ (from current 60-80%)
- Dual-layer cache: 5 min for breaking news, 30 min for analysis
- Pre-warming + TTL optimization + smart invalidation

## News Service
- Auto search for market news every 30 minutes
- Sentiment Analysis for each article
- High-impact event detection
- Arabic news sources required: Al Jazeera, Reuters Arabic, CNBC Arabia
- Dual-layer cache: 5 min (breaking) + 30 min (analysis)

## AI Assistants
- Goldy (Claude API): must integrate prediction + news + sentiment
- Free (Gemini API): enforce 10 msgs/day limit via ai_usage_limits
- New alert type: "AI Recommendation" when Goldy recommends buy/sell
- Weekly auto report: Sunday (portfolio performance, accuracy, top news, next week recommendations)
