"""
Consultant Agent for Autonomous Multi-Agent System

Uses OpenAI ChatGPT for strategic advice and final review.
"""

import os
from typing import Dict, Any, Optional
from openai import OpenAI
from base_agent import BaseAgent


class ConsultantAgent(BaseAgent):
    """Consultant Agent using OpenAI ChatGPT"""
    
    def __init__(self, name: str = "Consultant", model: str = "gpt-4o"):
        """
        Initialize Consultant Agent
        
        Args:
            name: Agent name
            model: ChatGPT model to use
        """
        super().__init__(name, "Strategic Consultant", model)
        
        # Initialize OpenAI client
        self.client = OpenAI(
            api_key=os.environ.get('OPENAI_API_KEY'),
            base_url=os.environ.get('OPENAI_API_BASE')
        )
        
        # System prompt
        self.system_prompt = """You are a Strategic Consultant in an autonomous multi-agent system.

Your responsibilities:
1. Provide strategic architectural advice
2. Review complex design decisions
3. Suggest best practices and patterns
4. Perform final quality review
5. Identify potential long-term issues

Core principles:
- Think strategically and long-term
- Focus on maintainability and scalability
- Consider business and technical trade-offs
- Provide actionable, high-level guidance
- Follow Global Guidelines v10.3.0

When consulted:
1. Understand the bigger picture
2. Consider long-term implications
3. Evaluate trade-offs
4. Provide clear recommendations
5. Explain reasoning
6. Suggest alternatives if needed

Note: You are consulted sparingly (limited API calls), so make your advice count!
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
            # Call ChatGPT
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=4096
            )
            
            result_text = response.choices[0].message.content
            
            # Add to history
            self.add_to_history("assistant", result_text)
            
            return {
                "success": True,
                "agent": self.name,
                "result": {"advice": result_text},
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
            if "architecture" in context:
                prompt += f"## Proposed Architecture\n\n{context['architecture']}\n\n"
            
            if "decisions" in context:
                prompt += f"## Key Decisions\n\n{context['decisions']}\n\n"
            
            if "concerns" in context:
                prompt += f"## Concerns\n\n{context['concerns']}\n\n"
        
        # Add task
        prompt += f"## Consultation Request\n\n{task}\n\n"
        
        # Add instructions
        prompt += """## Please Provide

1. **Strategic Assessment** - Is this the right approach?
2. **Potential Issues** - What could go wrong long-term?
3. **Recommendations** - What should be done?
4. **Alternatives** - Are there better options?
5. **Trade-offs** - What are the pros/cons?

Be concise but thorough. Focus on strategic value.
"""
        
        return prompt
    
    def review_architecture(self, architecture: str, decisions: str = "") -> Dict[str, Any]:
        """
        Review architecture
        
        Args:
            architecture: Proposed architecture
            decisions: Key decisions
            
        Returns:
            Review result
        """
        task = "Review this architecture and provide strategic feedback."
        
        context = {
            "architecture": architecture,
            "decisions": decisions
        }
        
        return self.execute(task, context)
    
    def final_review(self, code: str, tests: str, documentation: str) -> Dict[str, Any]:
        """
        Perform final review
        
        Args:
            code: Final code
            tests: Test code
            documentation: Documentation
            
        Returns:
            Final review result
        """
        task = """Perform a final strategic review of this project.

Consider:
1. Overall quality and completeness
2. Long-term maintainability
3. Scalability concerns
4. Security posture
5. Documentation quality
6. Production readiness

Provide:
- Overall assessment (1-10)
- Key strengths
- Key concerns
- Recommendations before deployment
- Final verdict (ready/needs work/not ready)
"""
        
        context = {
            "code": f"```python\n{code}\n```",
            "tests": f"```python\n{tests}\n```",
            "documentation": documentation
        }
        
        return self.execute(task, context)


if __name__ == "__main__":
    # Test
    consultant = ConsultantAgent()
    print(consultant)
    
    # Test consultation
    result = consultant.review_architecture(
        architecture="Microservices with REST APIs",
        decisions="Using Flask, PostgreSQL, Redis"
    )
    print(result)

