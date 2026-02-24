# Prompt Verification Patterns Guide (2026 Edition)

## 1. Introduction
This guide outlines advanced prompt verification patterns for ensuring factual accuracy and logical consistency in AI responses, based on the "2026 Engineer's Playbook for Trustworthy AI Systems".

## 2. Chain-of-Verification (CoVe)
### Steps
1.  **Draft Initial Response**: Generate a preliminary answer.
2.  **Generate Verification Questions**: Identify key claims and formulate questions.
3.  **Answer Independently**: Answer each question in a fresh context.
4.  **Regenerate Response**: Incorporate verified facts into the final answer.

### Benefits
*   Reduces hallucination frequency.
*   Prevents confirmation bias.

## 3. Self-Consistency Sampling
### Method
1.  Generate multiple reasoning paths via temperature sampling.
2.  Select the answer by majority vote.

### Benefits
*   Improves proof validity (+8.3%).
*   Enhances symbolic reasoning accuracy (+9.6%).
*   Increases numerical stability (+42.8%).

## 4. Multi-Agent Debate
### Framework
1.  **Extract Atomic Claims**: Break down the response into individual claims.
2.  **Retrieve Evidence**: Search for supporting information.
3.  **Run Debates**: Flexible multi-round debates among agents.
4.  **Validate Claims**: Confirm or refute each claim.

### Benefits
*   Reduces hallucination by 60–80%.
*   Improves factual correctness.

## 5. Consultant-Evaluator Pattern
### Process
1.  **Consultant**: Generates a response.
2.  **Evaluator**: Critiques the response based on criteria.
3.  **Refinement**: Consultant revises the response (max 1-2 iterations).

### Benefits
*   Efficient verification.
*   Minimal benefit from additional rounds.

## 6. Conclusion
Combine CoVe, Self-Consistency, and Multi-Agent Debate for robust prompt verification. Use the Consultant-Evaluator pattern for efficient refinement.
