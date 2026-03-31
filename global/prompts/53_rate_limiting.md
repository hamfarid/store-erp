# Rate Limiting Prompt

## Purpose
Protect API from abuse.

## Instructions
1. Define rate limits per endpoint
2. Implement rate limiting middleware
3. Return proper HTTP status codes
4. Add rate limit headers
5. Document rate limits
6. Log rate limiting to system_log.md

## Rate Limit Strategy
- Per user: 100 req/min
- Per IP: 1000 req/hour
- Sliding window algorithm

## Output
- Rate limiting middleware
- Rate limit documentation
