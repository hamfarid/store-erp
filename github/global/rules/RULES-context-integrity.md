# Rules: Context Integrity

## 1. Overview
These rules govern the management and integrity of the AI system's context, ensuring that it remains accurate, relevant, and free from "poisoning" or "distraction".

## 2. Mandatory Context Checks
1.  **Relevance Check**: Ensure that all context provided to the AI is directly relevant to the user's query.
2.  **Poisoning Scan**: Check for any information that could lead to hallucinations or errors.
3.  **Distraction Check**: Remove any superfluous or irrelevant information.
4.  **Clash Detection**: Identify and resolve any contradictory information.

## 3. Context Management
*   **Write**: Persist information outside the context window whenever possible.
*   **Select**: Pull only the most relevant context for each query.
*   **Compress**: Use summarization and compaction to reduce context size.
*   **Isolate**: Split context across specialized agents to prevent overload.

## 4. Handling Issues
*   **Correction**: If an issue is detected, correct it immediately.
*   **Removal**: If information is deemed irrelevant or harmful, remove it from the context.
*   **Feedback**: Provide feedback to the AI system to improve future context management.

## 5. Documentation
*   **Context Log**: Maintain a log of all context management activities.
*   **Issue Tracker**: Keep a record of all context-related issues and their resolutions.
