"""
Simple Usage Example for Autonomous Multi-Agent System

This example shows how to use the system for a simple project.
"""

import sys
sys.path.insert(0, '../src')

from orchestrator import AutonomousOrchestrator


def main():
    """Run a simple autonomous workflow"""
    
    # Create orchestrator
    orchestrator = AutonomousOrchestrator("email-validator")
    
    # Define requirement
    requirement = """
Build a Python function to validate email addresses.

Requirements:
1. Check format (user@domain.com)
2. Check for common typos
3. Return True/False
4. Include comprehensive tests
5. Add docstrings
"""
    
    # Run autonomous workflow
    result = orchestrator.run(
        requirement=requirement,
        consult_on_architecture=False  # Simple project, no need for consultant
    )
    
    # Print result
    if result["success"]:
        print("\n✅ Project completed successfully!")
        print(f"\nMemory saved to: {result['result']['memory_path']}")
        print(f"\nCode:\n{result['result']['code']}")
        print(f"\nTests:\n{result['result']['tests']}")
    else:
        print(f"\n❌ Project failed: {result['error']}")


if __name__ == "__main__":
    main()

