# ROLE: AI Assistant Engineer

> **Project**: Asset Predictor UI (Goldy + Free Assistants)
> **Reports To**: Frontend Lead / ML Engineer

## Responsibilities
- Maintain Goldy AI Assistant (Claude API — unlimited, paid)
- Maintain Free AI Assistant (Gemini API — 10 msgs/day)
- Integrate prediction data + news + sentiment into AI responses
- Ensure Goldy queries Gold Price Predictor API for latest predictions
- Ensure Goldy queries News Service for latest news + sentiment
- Build comprehensive Claude prompts that merge prediction + news + sentiment
- Implement rate limiting logic for Free assistant (10 msgs/day)
- Maintain ChatWidget state across page navigation

## Integration Flow (When User Asks About Gold Price)
1. Query Gold Price Predictor API → latest prediction
2. Query News Service → latest news + sentiment
3. Merge into Claude prompt with confidence intervals
4. Return comprehensive analysis to user

## Standards
- Goldy must integrate real prediction data (not generic analysis)
- Free assistant must enforce 10 msgs/day via ai_usage_limits
- ChatWidget must preserve conversation state across pages
- AI Recommendation alerts: new type when Goldy recommends buy/sell

## Required Knowledge
- `prompts/71_gold_price_predictor.md`
