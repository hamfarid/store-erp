# Workflow: Context Engineering

## 1. Overview
This workflow outlines the process for designing and optimizing the information architecture that feeds the AI system.

## 2. Steps
1.  **Analyze Request**: Understand the user's query and the required output.
2.  **Retrieve Context**: Gather relevant information from the knowledge base.
3.  **Filter Context**: Remove irrelevant or redundant information.
4.  **Compress Context**: Reduce the size of the context to fit within the token limit.
5.  **Provide Context**: Feed the optimized context to the AI system.

## 3. Tools
*   `retrieve_context`: Gather relevant information from the knowledge base.
*   `compress_context`: Reduce the size of the context.
*   `detect_hallucinations`: Identify potential hallucinations.

## 4. Roles
*   **Context Engineer**: Designs and optimizes the context.
*   **Fact-Checker**: Verifies the accuracy of the context.
*   **Logic Reviewer**: Checks for logical consistency.

## 5. Output
*   **Optimized Context**: The final, relevant, and concise context.
*   **Context Log**: A record of all context engineering activities.
