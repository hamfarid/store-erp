# 🔗 Chain-of-Vibes (CoV) Protocol

> **Definition**: A Human-in-the-Loop (HITL) workflow where the AI iteratively aligns with the user's implicit intent ("vibe") through rapid feedback cycles.
> **Goal**: Minimize the gap between what the user *says* and what they *mean*.

## 1. The Philosophy
*   **Traditional AI**: User Prompt -> AI Execution -> Result (Often misaligned).
*   **Chain-of-Vibes**: User Prompt -> AI Proposal -> User Vibe Check -> AI Adjustment -> Execution.

## 2. The Workflow

### Phase 1: The Vibe Check (Proposal)
*   **Trigger**: Any complex task or design decision.
*   **Action**: Before writing code, the AI generates a high-level proposal or mock-up.
*   **Output**: "Here is my plan. Does this match the vibe you're looking for?"
*   **User Input**: "Too formal", "Make it pop", "Simpler".

### Phase 2: The Alignment (Adjustment)
*   **Action**: AI interprets the feedback (even vague terms like "pop") and adjusts the plan.
*   **Technique**: Use `style_transfer` or `tone_adjustment` prompts.
*   **Output**: "Updated plan based on 'pop'. Added gradients and bold typography. Better?"

### Phase 3: The Execution (Build)
*   **Trigger**: User says "Yes", "Go", or "Looks good".
*   **Action**: Execute the plan with the aligned context.

## 3. Vibe Keywords & Translation

| User Says | AI Translates To |
| :--- | :--- |
| "Make it pop" | High contrast, bold colors, animations, modern UI. |
| "Clean" | Minimalist, whitespace, sans-serif fonts, flat design. |
| "Professional" | Blue/Grey palette, structured layout, serif/sans mix. |
| "Playful" | Rounded corners, bright colors, illustrations, bounce animations. |
| "MVP" | Core functionality only, no polish, speed over style. |
| "Robust" | Error handling, logging, tests, edge case coverage. |

## 4. When to Use CoV
*   **UI/UX Design**: Always.
*   **Content Writing**: Always.
*   **Architecture**: For high-level decisions (Monolith vs Microservices).
*   **Refactoring**: When the goal is "readability" or "modernization".

## 5. Anti-Patterns
*   ❌ **The Steamroller**: Ignoring user feedback and pushing the original plan.
*   ❌ **The Yes-Man**: Agreeing without understanding ("Okay, I will make it pop" -> changes nothing).
*   ❌ **The Over-Engineer**: Asking for 20 clarifications for a simple request.

## 6. Integration with Speckit
*   **Speckit Plan**: The `plan` step MUST include a "Vibe Check" gate.
*   **Speckit Verify**: The `verify` step checks if the final output matches the agreed-upon vibe.
