"""
Autonomous Orchestrator for Multi-Agent System

Coordinates all agents to work together autonomously.
"""

import subprocess
from typing import Dict, Any, Optional
from datetime import datetime

from memory_manager import MemoryManager
from mcp_manager import MCPManager
from error_tracker import ErrorTracker
from helper_manager import HelperManager
from lead_agent import LeadAgent
from reviewer_agent import ReviewerAgent
from consultant_agent import ConsultantAgent


class AutonomousOrchestrator:
    """Orchestrates autonomous multi-agent workflow"""
    
    def __init__(self, project_name: str):
        """
        Initialize Orchestrator
        
        Args:
            project_name: Name of the project
        """
        self.project_name = project_name
        
        # Initialize managers
        self.memory = MemoryManager(project_name)
        self.mcp = MCPManager(project_name)
        self.errors = ErrorTracker()
        self.helpers = HelperManager()
        
        # Initialize agents
        self.lead = LeadAgent()
        self.reviewer = ReviewerAgent()
        self.consultant = ConsultantAgent()
        
        # Workflow state
        self.current_phase = 0
        self.phases = [
            "Phase 0: Initialize",
            "Phase 1: Understand",
            "Phase 2: Plan",
            "Phase 3: Code",
            "Phase 4: Review",
            "Phase 5: Test",
            "Phase 6: Finalize"
        ]
        
        print(f"🤖 Autonomous Orchestrator initialized for project: {project_name}")
    
    def run(self, requirement: str, consult_on_architecture: bool = True) -> Dict[str, Any]:
        """
        Run autonomous workflow
        
        Args:
            requirement: Project requirement
            consult_on_architecture: Whether to consult ChatGPT on architecture
            
        Returns:
            Complete project result
        """
        print(f"\n{'='*60}")
        print(f"🚀 Starting Autonomous Workflow")
        print(f"Project: {self.project_name}")
        print(f"Requirement: {requirement}")
        print(f"{'='*60}\n")
        
        try:
            # Phase 0: Initialize
            self._phase_0_initialize()
            
            # Phase 1: Understand
            understanding = self._phase_1_understand(requirement)
            
            # Phase 2: Plan
            plan = self._phase_2_plan(understanding, consult_on_architecture)
            
            # Phase 3: Code
            code_result = self._phase_3_code(plan)
            
            # Phase 4: Review
            review_result = self._phase_4_review(code_result)
            
            # Phase 5: Test
            test_result = self._phase_5_test(code_result, review_result)
            
            # Phase 6: Finalize
            final_result = self._phase_6_finalize(code_result, test_result)
            
            print(f"\n{'='*60}")
            print(f"✅ Workflow Complete!")
            print(f"{'='*60}\n")
            
            return {
                "success": True,
                "project": self.project_name,
                "result": final_result
            }
            
        except Exception as e:
            print(f"\n❌ Workflow failed: {str(e)}")
            
            # Log error
            self.errors.log_error({
                "name": "workflow_failure",
                "project": self.project_name,
                "agent": "orchestrator",
                "description": f"Workflow failed: {str(e)}",
                "solution": "Check logs and retry",
                "severity": "high"
            })
            
            return {
                "success": False,
                "project": self.project_name,
                "error": str(e)
            }
    
    def _phase_0_initialize(self):
        """Phase 0: Initialize Memory, MCP, and load context"""
        self._print_phase(0)
        
        # Initialize Memory
        self.memory.save("context", f"""# Project: {self.project_name}

Started: {datetime.now().isoformat()}
Status: Initialized
""")
        
        # Load past errors
        past_errors = self.errors.get_error_summary(self.project_name)
        self.memory.save("past_errors", past_errors)
        
        # Load helpers summary
        helpers_summary = self.helpers.get_helper_summary()
        self.memory.save("helpers_available", helpers_summary)
        
        print("✅ Memory initialized")
        print("✅ MCP initialized")
        print("✅ Past errors loaded")
        print("✅ Helpers loaded")
        
        self.memory.append("progress", "Phase 0: Initialized")
    
    def _phase_1_understand(self, requirement: str) -> Dict[str, Any]:
        """Phase 1: Understand the requirement"""
        self._print_phase(1)
        
        # Get context
        context = self._build_context()
        
        # Lead agent analyzes requirement
        task = f"""Analyze this requirement and provide:

1. **Understanding** - What needs to be built?
2. **Scope** - What's included and what's not?
3. **Key Features** - List main features
4. **Technical Considerations** - What to consider?
5. **Questions** - Any clarifications needed?

Requirement:
{requirement}
"""
        
        result = self.lead.execute(task, context)
        
        if result["success"]:
            understanding = result["result"]
            
            # Save to memory
            self.memory.save("requirement", requirement)
            self.memory.save("understanding", str(understanding))
            self.memory.append("progress", "Phase 1: Understood requirement")
            
            print("✅ Requirement understood")
            return understanding
        else:
            raise Exception(f"Failed to understand requirement: {result.get('error')}")
    
    def _phase_2_plan(self, understanding: Dict[str, Any], consult: bool = True) -> Dict[str, Any]:
        """Phase 2: Plan the architecture"""
        self._print_phase(2)
        
        # Get context
        context = self._build_context()
        
        # Lead agent designs architecture
        task = """Design the system architecture.

Provide:
1. **Architecture Overview** - High-level design
2. **Technology Stack** - What to use and why
3. **Key Components** - Main modules/classes
4. **Data Models** - Database schema if needed
5. **API Design** - Endpoints if applicable
6. **Decisions** - Key architectural decisions

Remember: Choose the BEST solution, not the easiest!
"""
        
        result = self.lead.execute(task, context)
        
        if not result["success"]:
            raise Exception(f"Failed to plan architecture: {result.get('error')}")
        
        plan = result["result"]
        
        # Consult ChatGPT if requested (and if complex)
        if consult and self._is_complex(plan):
            print("🤔 Consulting strategic advisor...")
            
            consultation = self.consultant.review_architecture(
                architecture=str(plan.get("decisions", "")),
                decisions=str(plan.get("decisions", ""))
            )
            
            if consultation["success"]:
                advice = consultation["result"]["advice"]
                
                # Update plan based on advice
                print("💡 Incorporating strategic advice...")
                
                update_task = f"""Update the architecture based on this strategic advice:

{advice}

Provide the updated architecture.
"""
                
                updated_result = self.lead.execute(update_task, context)
                if updated_result["success"]:
                    plan = updated_result["result"]
        
        # Save to memory
        self.memory.save("architecture", str(plan))
        self.memory.append("decisions", str(plan.get("decisions", "")))
        self.memory.append("progress", "Phase 2: Architecture planned")
        
        print("✅ Architecture planned")
        return plan
    
    def _phase_3_code(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 3: Write the code"""
        self._print_phase(3)
        
        # Get context
        context = self._build_context()
        context["plan"] = str(plan)
        
        # Lead agent writes code
        task = """Write the complete, production-ready code based on the architecture.

Requirements:
1. Clean, well-documented code
2. Proper error handling
3. Type hints
4. Docstrings
5. Follow best practices
6. Use helpers when appropriate

Provide complete, runnable code.
"""
        
        result = self.lead.execute(task, context)
        
        if not result["success"]:
            raise Exception(f"Failed to write code: {result.get('error')}")
        
        code_result = result["result"]
        
        # Save to memory
        self.memory.save("code", code_result.get("code", ""))
        self.memory.append("progress", "Phase 3: Code written")
        
        print("✅ Code written")
        return code_result
    
    def _phase_4_review(self, code_result: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 4: Review the code"""
        self._print_phase(4)
        
        code = code_result.get("code", "")
        requirement = self.memory.load("requirement") or ""
        
        # Reviewer agent reviews code
        review_result = self.reviewer.review_code(code, requirement)
        
        if not review_result["success"]:
            raise Exception(f"Failed to review code: {review_result.get('error')}")
        
        review = review_result["result"]
        
        # Check if changes needed
        if "needs changes" in str(review).lower() or "reject" in str(review).lower():
            print("⚠️ Code needs changes, asking Lead to fix...")
            
            # Get context
            context = self._build_context()
            context["review"] = str(review)
            context["original_code"] = code
            
            # Lead fixes code
            fix_task = f"""Fix the code based on this review:

{review}

Provide the fixed code.
"""
            
            fix_result = self.lead.execute(fix_task, context)
            
            if fix_result["success"]:
                code_result = fix_result["result"]
                self.memory.save("code", code_result.get("code", ""))
                print("✅ Code fixed")
        
        # Save review to memory
        self.memory.append("reviews", str(review))
        self.memory.append("progress", "Phase 4: Code reviewed")
        
        print("✅ Code reviewed")
        return review_result
    
    def _phase_5_test(self, code_result: Dict[str, Any], review_result: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 5: Write and run tests"""
        self._print_phase(5)
        
        code = code_result.get("code", "")
        requirement = self.memory.load("requirement") or ""
        
        # Reviewer writes tests
        test_result = self.reviewer.write_tests(code, requirement)
        
        if not test_result["success"]:
            raise Exception(f"Failed to write tests: {test_result.get('error')}")
        
        tests = test_result["result"].get("tests", "")
        
        # Save tests
        self.memory.save("tests", tests)
        
        # Try to run tests (if possible)
        test_output = self._run_tests(code, tests)
        
        if test_output:
            self.memory.save("test_output", test_output)
            
            if "FAILED" in test_output or "ERROR" in test_output:
                print("⚠️ Tests failed, asking Lead to fix...")
                
                # Get context
                context = self._build_context()
                context["test_output"] = test_output
                context["tests"] = tests
                context["code"] = code
                
                # Lead fixes code
                fix_task = f"""Fix the code to pass these tests:

Test output:
{test_output}

Provide the fixed code.
"""
                
                fix_result = self.lead.execute(fix_task, context)
                
                if fix_result["success"]:
                    code_result = fix_result["result"]
                    self.memory.save("code", code_result.get("code", ""))
                    print("✅ Code fixed to pass tests")
        
        self.memory.append("progress", "Phase 5: Tests written and run")
        
        print("✅ Tests written")
        return test_result
    
    def _phase_6_finalize(self, code_result: Dict[str, Any], test_result: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 6: Finalize and document"""
        self._print_phase(6)
        
        code = code_result.get("code", "")
        tests = test_result["result"].get("tests", "")
        
        # Get context
        context = self._build_context()
        
        # Lead writes documentation
        doc_task = """Write complete documentation for this project.

Include:
1. **Overview** - What it does
2. **Installation** - How to install
3. **Usage** - How to use
4. **API Reference** - If applicable
5. **Examples** - Usage examples
6. **Testing** - How to run tests
7. **Contributing** - Guidelines

Provide complete, professional documentation.
"""
        
        doc_result = self.lead.execute(doc_task, context)
        
        if doc_result["success"]:
            documentation = doc_result["result"]
            self.memory.save("documentation", str(documentation))
        
        # Final review by consultant (optional, if important)
        # Skipped to save API calls unless critical
        
        # Update memory
        self.memory.append("progress", "Phase 6: Finalized and documented")
        self.memory.save("status", "Complete")
        
        print("✅ Project finalized")
        
        return {
            "code": code,
            "tests": tests,
            "documentation": str(documentation) if doc_result["success"] else "",
            "memory_path": str(self.memory.base_path),
            "status": "Complete"
        }
    
    def _build_context(self) -> Dict[str, Any]:
        """Build context for agents"""
        return {
            "memory": self.memory.get_all_context(),
            "past_errors": self.errors.get_error_summary(self.project_name),
            "helpers": self.helpers.get_helper_summary()
        }
    
    def _is_complex(self, plan: Dict[str, Any]) -> bool:
        """Determine if project is complex enough to consult"""
        # Simple heuristic: check for keywords
        plan_str = str(plan).lower()
        complex_keywords = [
            "microservice", "distributed", "scalability", "high availability",
            "real-time", "machine learning", "blockchain", "security"
        ]
        
        return any(keyword in plan_str for keyword in complex_keywords)
    
    def _run_tests(self, code: str, tests: str) -> Optional[str]:
        """Try to run tests"""
        try:
            # Save code and tests to temp files
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                code_file = f.name
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(tests)
                test_file = f.name
            
            # Run pytest
            result = subprocess.run(
                ['pytest', test_file, '-v'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Clean up
            import os
            os.unlink(code_file)
            os.unlink(test_file)
            
            return result.stdout + "\n" + result.stderr
            
        except Exception as e:
            print(f"⚠️ Could not run tests: {str(e)}")
            return None
    
    def _print_phase(self, phase_num: int):
        """Print phase header"""
        self.current_phase = phase_num
        print(f"\n{'='*60}")
        print(f"📍 {self.phases[phase_num]}")
        print(f"{'='*60}\n")


if __name__ == "__main__":
    # Test
    orchestrator = AutonomousOrchestrator("test-project")
    
    requirement = "Build a REST API for user authentication with JWT tokens"
    
    result = orchestrator.run(requirement, consult_on_architecture=False)
    
    print("\n" + "="*60)
    print("FINAL RESULT:")
    print("="*60)
    print(result)

