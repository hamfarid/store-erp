#!/usr/bin/env python3
"""
Code Reviewer MCP Server
------------------------
An MCP server that provides code review, bug finding, and optimization suggestions
using the available AI models (Gemini/Anthropic) via their APIs.

Tools:
- review_file(path): Performs a general code review.
- find_bugs(path): Focuses on identifying potential bugs and logic errors.
- optimize_code(path): Suggests performance and readability improvements.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any

# Try to import MCP SDK
try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    # Fallback for when MCP is not installed yet (during setup)
    print("MCP SDK not found. Please install 'mcp' package.")
    sys.exit(1)

# Initialize FastMCP
mcp = FastMCP("CodeReviewer")

# --- Helper Functions ---

def read_file_content(file_path: str) -> str:
    """Reads the content of a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def call_ai_model(prompt: str, system_instruction: str) -> str:
    """
    Calls the available AI model (Gemini or Anthropic) to process the code.
    This function abstracts the API call logic.
    """
    # Check for API keys
    gemini_key = os.environ.get("GEMINI_API_KEY")
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")

    if gemini_key:
        try:
            # Use Google GenAI SDK
            import google.generativeai as genai
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel('gemini-2.0-flash') # Use a fast model
            response = model.generate_content(f"{system_instruction}\n\n{prompt}")
            return response.text
        except Exception as e:
            return f"Gemini API Error: {str(e)}"
            
    elif anthropic_key:
        try:
            # Use Anthropic SDK
            import anthropic
            client = anthropic.Anthropic(api_key=anthropic_key)
            message = client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=4000,
                system=system_instruction,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        except Exception as e:
            return f"Anthropic API Error: {str(e)}"
    
    else:
        return "Error: No API keys found (GEMINI_API_KEY or ANTHROPIC_API_KEY)."

# --- MCP Tools ---

@mcp.tool()
def review_file(file_path: str) -> str:
    """
    Performs a comprehensive code review of the specified file.
    Checks for style, logic, security, and best practices.
    """
    code = read_file_content(file_path)
    if code.startswith("Error"):
        return code

    system_prompt = """
    You are an expert Senior Software Engineer and Code Reviewer.
    Review the provided code for:
    1. Code Quality & Style (PEP8, etc.)
    2. Logic & Correctness
    3. Security Vulnerabilities
    4. Error Handling
    5. Maintainability
    
    Provide clear, actionable feedback with line numbers if possible.
    """
    
    return call_ai_model(f"Review this code:\n\n{code}", system_prompt)

@mcp.tool()
def find_bugs(file_path: str) -> str:
    """
    Analyzes the file specifically to find bugs, logical errors, and edge cases.
    """
    code = read_file_content(file_path)
    if code.startswith("Error"):
        return code

    system_prompt = """
    You are an expert Bug Hunter.
    Analyze the provided code and identify:
    1. Logical errors
    2. Potential runtime exceptions
    3. Edge cases that are not handled
    4. Resource leaks
    5. Race conditions (if applicable)
    
    List the bugs found with severity levels (High/Medium/Low).
    """
    
    return call_ai_model(f"Find bugs in this code:\n\n{code}", system_prompt)

@mcp.tool()
def optimize_code(file_path: str) -> str:
    """
    Suggests optimizations for performance, memory usage, and readability.
    """
    code = read_file_content(file_path)
    if code.startswith("Error"):
        return code

    system_prompt = """
    You are an expert Performance Engineer.
    Analyze the provided code and suggest optimizations for:
    1. Time Complexity (Big O)
    2. Memory Usage
    3. Readability & Pythonic idioms
    4. Database queries (if any)
    
    Provide the optimized code snippets where applicable.
    """
    
    return call_ai_model(f"Optimize this code:\n\n{code}", system_prompt)

if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
