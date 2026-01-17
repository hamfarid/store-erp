# 🤖 Autonomous Multi-Agent System - Augment Integration Guide

**Version:** 1.0.0  
**Date:** November 5, 2025

---

## 🎯 Overview

This guide provides step-by-step instructions on how to integrate and use the **Autonomous Multi-Agent System** directly within **Augment**.

There are three methods to do this, ranging from simple manual execution to full, seamless integration. We recommend starting with Method 1 to test the system and then moving to Method 3 for the best experience.

### The Goal

The goal is to enable this workflow:

```
User (in Augment) → Augment → Orchestrator → Agents (Gemini, Claude, ChatGPT)
```

This allows you to trigger a fully autonomous software development process from a single command within your Augment chat interface.

### Prerequisites

Before you begin, ensure you have:

1.  **Cloned the repository**:
    ```bash
    git clone https://github.com/hamfarid/global.git ~/.global
    ```
2.  **Installed dependencies**:
    ```bash
    cd ~/.global/autonomous-multiagent-system
    pip install -r requirements.txt
    ```
3.  **Configured API Keys**:
    -   Copy the example `.env` file:
        ```bash
        cp .env.example .env
        ```
    -   Edit the `.env` file and add your API keys:
        ```
        # .env
        GEMINI_API_KEY="your_google_gemini_api_key"
        ANTHROPIC_API_KEY="your_anthropic_claude_api_key"
        OPENAI_API_KEY="your_openai_chatgpt_api_key"
        ```
    -   **This is a critical step! The system will not work without these keys.**

---

## Method 1: Direct Script Execution (Manual)

This is the simplest way to run the system. You manually tell Augment to execute the `augment_interface.py` script.

### How It Works

You provide a command to Augment, which runs the Python script in the shell. The script's output is then displayed in the chat.

### Step-by-Step

1.  **Open Augment Chat**.
2.  **Paste the following command**, modifying the requirement and project name as needed:

    ```
    Run this command and show me the results:

    cd ~/.global/autonomous-multiagent-system && \
    python augment_interface.py "Build a simple REST API for a blog with Flask" "blog-api"
    ```

3.  **For a complex project** that requires architectural consultation, add the `--consult` flag:

    ```
    Run this command and show me the results:

    cd ~/.global/autonomous-multiagent-system && \
    python augment_interface.py "Build a microservices-based e-commerce platform" "ecommerce-platform" --consult
    ```

### Pros & Cons

-   **Pros**:
    -   ✅ Simple to use.
    -   ✅ No setup required beyond the initial prerequisites.
    -   ✅ Good for testing and one-off builds.
-   **Cons**:
    -   ❌ Not automated; you have to type the full command each time.
    -   ❌ Verbose.

---

## Method 2: Augment Rule (`@autonomous`)

This method uses a custom Augment Rule to automatically trigger the system when you use a keyword like `@autonomous`.

### How It Works

The `auto-autonomous-builder.md` rule file you have tells Augment that whenever a message starts with `@autonomous`, it should execute the `augment_interface.py` script with the rest of the message as the requirement.

### Step-by-Step

1.  **Ensure the rule is in place**:
    -   The rule file should be at `~/.global/.augment/rules/auto-autonomous-builder.md`.
    -   If you followed the setup, it's already there!

2.  **Reload Augment** to ensure it loads the new rule.

3.  **Open Augment Chat**.

4.  **Use the `@autonomous` keyword** followed by your requirement:

    ```
    @autonomous Build a REST API for user authentication with JWT
    ```

5.  **Augment will automatically**: 
    -   Parse your message.
    -   Construct the full shell command.
    -   Execute the `augment_interface.py` script.
    -   Display the formatted results.

### Pros & Cons

-   **Pros**:
    -   ✅ Semi-automated and very convenient.
    -   ✅ Clean and simple syntax (`@autonomous ...`).
    -   ✅ Feels much more integrated.
-   **Cons**:
    -   ❌ Relies on Augment's ability to correctly parse the message and execute shell commands.

---

## Method 3: MCP Server Integration (Recommended)

This is the most robust and seamless method. It exposes the autonomous system as a native **Tool** that any MCP-compatible client (including Augment) can use.

### How It Works

You run the `mcp_server.py` script, which registers the `autonomous-builder` tool. Augment can then see and call this tool directly, providing a structured way to pass inputs and receive outputs.

### Step-by-Step

1.  **Register the MCP Server**:
    -   You need to tell your MCP client (Augment) about this new server.
    -   Add the configuration from `mcp_config.json` to your global MCP configuration file.
    -   The location of this file depends on your MCP client setup, but it's often a central `config.json`.

    **Add this to your MCP configuration:**
    ```json
    {
      "mcpServers": {
        "autonomous-builder": {
          "command": "python3",
          "args": [
            "/home/ubuntu/.global/autonomous-multiagent-system/mcp_server.py"
          ],
          "description": "Autonomous multi-agent project builder using Gemini, Claude, and ChatGPT",
          "env": {
            "PYTHONPATH": "/home/ubuntu/.global/autonomous-multiagent-system"
          }
        }
      }
    }
    ```

2.  **Restart your MCP client/Augment** to connect to the new server.

3.  **Open Augment Chat**.

4.  **Instruct Augment to use the tool**:

    ```
    Use the autonomous-builder tool to build a project.

    - Requirement: "Build a web scraper for Hacker News headlines"
    - Project Name: "hacker-news-scraper"
    ```

    Or more naturally:

    ```
    Use the autonomous builder to create a Hacker News scraper project named 'hacker-news-scraper'.
    ```

5.  **Augment will**: 
    -   Identify the `autonomous-builder` tool.
    -   Call the `build_project` function on the MCP server.
    -   Pass the `requirement` and `project_name` as structured arguments.
    -   Receive a structured response and display it.

### Pros & Cons

-   **Pros**:
    -   ✅ **Fully integrated and seamless**.
    -   ✅ **Most robust method**; uses a structured API instead of shell commands.
    -   ✅ Exposes the system as a reusable tool for other MCP clients.
    -   ✅ Provides other useful tools like `list_projects` and `get_project_info`.
-   **Cons**:
    -   ❌ Requires one-time setup of the MCP server configuration.

---

## 📊 Summary of Methods

| Method                  | How to Use                                                                                             | Best For                                       |
| ----------------------- | ------------------------------------------------------------------------------------------------------ | ---------------------------------------------- |
| **1. Direct Script**    | `Run command: python augment_interface.py ...`                                                         | Quick tests, one-off builds                    |
| **2. Augment Rule**     | `@autonomous Build a ...`                                                                              | Frequent, convenient use                       |
| **3. MCP Server**       | `Use autonomous-builder to ...`                                                                        | **Recommended for robust, daily use**          |


## 🐛 Troubleshooting

-   **"API key not found"**: Double-check your `~/.global/autonomous-multiagent-system/.env` file. Ensure the keys are correct and have no extra spaces or quotes.
-   **"Command not found"**: Make sure you are in the correct directory (`cd ~/.global/autonomous-multiagent-system`) or are using absolute paths.
-   **"mcp server not connecting"**: Verify your MCP configuration file is correct and that you have restarted your MCP client.
-   **"Agent failed"**: Check the API usage/quotas for Gemini, Claude, and OpenAI. The system relies on these external services.

🚀 **Happy Autonomous Coding!** 🚀

