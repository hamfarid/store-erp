"""
Lead Agent for Autonomous Multi-Agent System

Uses Google Gemini as the main decision maker and code writer.
"""

import os
from typing import Dict, Any, Optional
from google import genai
from base_agent import BaseAgent


class LeadAgent(BaseAgent):
    """Lead Agent using Google Gemini"""
    
    def __init__(self, name: str = "Lead", model: str = "gemini-2.0-flash-exp"):
        """
        Initialize Lead Agent
        
        Args:
            name: Agent name
            model: Gemini model to use
        """
        super().__init__(name, "Lead Developer", model)
        
        # Initialize Gemini client
        self.client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))
        
        # System prompt
        self.system_prompt = """You are a Lead Developer in an autonomous multi-agent system.

Your responsibilities:
1. Design system architecture
2. Write high-quality code
3. Make architectural decisions
4. Coordinate with other agents
5. Ensure code quality and maintainability

Core principles:
- Always choose the BEST solution, not the easiest
- Follow Global Guidelines v10.3.0
- Use Memory to save decisions
- Check past errors before coding
- Use helper files (definitions, classes, modules)
- Write clean, maintainable code
- Aim for 95%+ test coverage

Environment Separation (CRITICAL):
- YOUR tools: ~/.global/memory/, ~/.global/mcp/, ~/.global/errors/, ~/.global/helpers/
- USER's project: ~/user-project/
- NEVER mix them!

When given a task:
1. Check Memory for context
2. Check past errors
3. Load helper files
4. Design solution
5. Write code
6. Save decisions to Memory
7. Return result with explanation
"""
    
    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute a task
        
        Args:
            task: Task description
            context: Additional context (memory, errors, helpers)
            
        Returns:
            Task result with code, explanation, decisions
        """
        # Build prompt with context
        prompt = self._build_prompt(task, context)
        
        # Add to history
        self.add_to_history("user", prompt)
        
        try:
            # Call Gemini
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config={
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "max_output_tokens": 8192
                }
            )
            
            result_text = response.text
            
            # Add to history
            self.add_to_history("assistant", result_text)
            
            # Parse result
            result = self._parse_result(result_text)
            
            return {
                "success": True,
                "agent": self.name,
                "result": result,
                "raw_response": result_text
            }
            
        except Exception as e:
            error_msg = f"Error executing task: {str(e)}"
            print(f"❌ {error_msg}")
            
            return {
                "success": False,
                "agent": self.name,
                "error": error_msg
            }
    
    def _build_prompt(self, task: str, context: Optional[Dict[str, Any]]) -> str:
        """Build prompt with context"""
        prompt = f"{self.system_prompt}\n\n"
        
        # Add context
        if context:
            if "memory" in context:
                prompt += f"## Memory Context\n\n{context['memory']}\n\n"
            
            if "past_errors" in context:
                prompt += f"## Past Errors (DO NOT REPEAT)\n\n{context['past_errors']}\n\n"
            
            if "helpers" in context:
                prompt += f"## Available Helpers\n\n{context['helpers']}\n\n"
        
        # Add task
        prompt += f"## Task\n\n{task}\n\n"
        
        # Add instructions
        prompt += """## Instructions

1. Analyze the task carefully
2. Check Memory for relevant context
3. Review past errors to avoid repetition
4. Use available helpers when appropriate
5. Design the BEST solution (not easiest)
6. Write clean, well-documented code
7. Explain your decisions
8. Suggest what to save to Memory

Provide your response in this format:

### Analysis
[Your analysis of the task]

### Design Decisions
[Key architectural decisions]

### Code
```python
# Your code here
```

### Explanation
[Explanation of your approach]

### Memory Updates
[What should be saved to Memory]

### Next Steps
[What should happen next]
"""
        
        return prompt
    
    def _parse_result(self, result_text: str) -> Dict[str, Any]:
        """Parse result from response"""
        # Simple parsing (can be enhanced)
        result = {
            "analysis": "",
            "decisions": "",
            "code": "",
            "explanation": "",
            "memory_updates": "",
            "next_steps": ""
        }
        
        # Extract sections (basic implementation)
        sections = result_text.split("###")
        for section in sections:
            section = section.strip()
            if section.startswith("Analysis"):
                result["analysis"] = section.replace("Analysis", "").strip()
            elif section.startswith("Design Decisions"):
                result["decisions"] = section.replace("Design Decisions", "").strip()
            elif section.startswith("Code"):
                result["code"] = section.replace("Code", "").strip()
            elif section.startswith("Explanation"):
                result["explanation"] = section.replace("Explanation", "").strip()
            elif section.startswith("Memory Updates"):
                result["memory_updates"] = section.replace("Memory Updates", "").strip()
            elif section.startswith("Next Steps"):
                result["next_steps"] = section.replace("Next Steps", "").strip()
        
        return result
    
    def review_code(self, code: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Review code
        
        Args:
            code: Code to review
            context: Additional context
            
        Returns:
            Review result
        """
        task = f"""Review this code for quality, maintainability, and potential issues:

```python
{code}
```

Provide:
1. Code quality assessment
2. Potential issues
3. Suggestions for improvement
4. Security concerns
5. Performance considerations
"""
        
        return self.execute(task, context)


if __name__ == "__main__":
    # Test
    lead = LeadAgent()
    print(lead)
    
    # Test task
    result = lead.execute("Write a function to validate email addresses")
    print(result)

