"""
Reviewer Agent for Autonomous Multi-Agent System

Uses Anthropic Claude for code review and testing.
"""

import os
from typing import Dict, Any, Optional
from anthropic import Anthropic
from base_agent import BaseAgent


class ReviewerAgent(BaseAgent):
    """Reviewer Agent using Anthropic Claude"""
    
    def __init__(self, name: str = "Reviewer", model: str = "claude-3-5-sonnet-20241022"):
        """
        Initialize Reviewer Agent
        
        Args:
            name: Agent name
            model: Claude model to use
        """
        super().__init__(name, "Code Reviewer & Tester", model)
        
        # Initialize Claude client
        self.client = Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))
        
        # System prompt
        self.system_prompt = """You are a Code Reviewer and Tester in an autonomous multi-agent system.

Your responsibilities:
1. Review code for quality, security, and maintainability
2. Write comprehensive tests (aim for 95%+ coverage)
3. Identify potential bugs and issues
4. Suggest improvements
5. Ensure code follows best practices

Core principles:
- Be thorough and critical
- Focus on quality over speed
- Check for security vulnerabilities
- Ensure proper error handling
- Verify test coverage
- Follow Global Guidelines v10.3.0

When reviewing code:
1. Check code quality and readability
2. Identify potential bugs
3. Check for security issues
4. Verify error handling
5. Assess performance
6. Write comprehensive tests
7. Provide actionable feedback
"""
    
    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute a task
        
        Args:
            task: Task description
            context: Additional context
            
        Returns:
            Task result
        """
        # Build prompt
        prompt = self._build_prompt(task, context)
        
        # Add to history
        self.add_to_history("user", prompt)
        
        try:
            # Call Claude
            response = self.client.messages.create(
                model=self.model,
                max_tokens=8192,
                temperature=0.7,
                system=self.system_prompt,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            result_text = response.content[0].text
            
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
        prompt = ""
        
        # Add context
        if context:
            if "code" in context:
                prompt += f"## Code to Review\n\n```python\n{context['code']}\n```\n\n"
            
            if "requirements" in context:
                prompt += f"## Requirements\n\n{context['requirements']}\n\n"
        
        # Add task
        prompt += f"## Task\n\n{task}\n\n"
        
        return prompt
    
    def _parse_result(self, result_text: str) -> Dict[str, Any]:
        """Parse result from response"""
        result = {
            "review": result_text,
            "issues": [],
            "suggestions": [],
            "tests": ""
        }
        
        # Simple parsing (can be enhanced)
        if "```python" in result_text:
            # Extract code blocks
            parts = result_text.split("```python")
            if len(parts) > 1:
                test_code = parts[1].split("```")[0].strip()
                result["tests"] = test_code
        
        return result
    
    def review_code(self, code: str, requirements: str = "") -> Dict[str, Any]:
        """
        Review code
        
        Args:
            code: Code to review
            requirements: Original requirements
            
        Returns:
            Review result
        """
        task = """Review this code and provide:

1. **Code Quality Assessment** (1-10 score)
2. **Issues Found** (bugs, security, performance)
3. **Suggestions for Improvement**
4. **Test Coverage Assessment**
5. **Overall Recommendation** (approve/needs changes/reject)

Be thorough and critical. Focus on quality.
"""
        
        context = {
            "code": code,
            "requirements": requirements
        }
        
        return self.execute(task, context)
    
    def write_tests(self, code: str, requirements: str = "") -> Dict[str, Any]:
        """
        Write tests for code
        
        Args:
            code: Code to test
            requirements: Original requirements
            
        Returns:
            Tests
        """
        task = """Write comprehensive tests for this code.

Requirements:
1. Use pytest framework
2. Aim for 95%+ coverage
3. Test happy paths
4. Test edge cases
5. Test error handling
6. Include fixtures if needed
7. Add clear docstrings

Provide complete, runnable test code.
"""
        
        context = {
            "code": code,
            "requirements": requirements
        }
        
        return self.execute(task, context)


if __name__ == "__main__":
    # Test
    reviewer = ReviewerAgent()
    print(reviewer)
    
    # Test review
    code = """
def add(a, b):
    return a + b
"""
    
    result = reviewer.review_code(code)
    print(result)

