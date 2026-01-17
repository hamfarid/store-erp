#!/usr/bin/env python3
"""
Augment Interface for Autonomous Multi-Agent System

This script provides a simple interface for Augment to interact with the
autonomous multi-agent orchestrator.

Usage:
    python augment_interface.py "requirement" "project-name" [--consult]

Example:
    python augment_interface.py "Build a REST API for user auth" "auth-api"
    python augment_interface.py "Build a complex microservices system" "my-system" --consult
"""

import sys
import json
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from orchestrator import AutonomousOrchestrator


def print_banner():
    """Print a nice banner"""
    print("\n" + "="*60)
    print("🤖 Autonomous Multi-Agent System v1.0.0")
    print("="*60 + "\n")


def print_phase(phase_name: str, agent: str = None):
    """Print current phase"""
    agent_str = f" ({agent})" if agent else ""
    print(f"\n{'─'*60}")
    print(f"📍 {phase_name}{agent_str}")
    print(f"{'─'*60}\n")


def print_result(result: dict):
    """Print the result in a nice format"""
    print("\n" + "="*60)
    if result["success"]:
        print("✅ Project completed successfully!")
    else:
        print("❌ Project failed!")
    print("="*60 + "\n")
    
    if result["success"]:
        data = result["result"]
        
        # Code
        print("📝 GENERATED CODE:")
        print("─"*60)
        print(data.get("code", "No code generated"))
        print()
        
        # Tests
        print("🧪 GENERATED TESTS:")
        print("─"*60)
        print(data.get("tests", "No tests generated"))
        print()
        
        # Documentation
        print("📖 DOCUMENTATION:")
        print("─"*60)
        print(data.get("documentation", "No documentation generated"))
        print()
        
        # Architecture (if available)
        if "architecture" in data:
            print("🏗️ ARCHITECTURE:")
            print("─"*60)
            print(data["architecture"])
            print()
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")
        if "details" in result:
            print(f"Details: {result['details']}")


def main():
    """Main entry point"""
    # Parse arguments
    if len(sys.argv) < 3:
        print("Usage: python augment_interface.py \"requirement\" \"project-name\" [--consult]")
        print("\nExample:")
        print("  python augment_interface.py \"Build a REST API for user auth\" \"auth-api\"")
        sys.exit(1)
    
    requirement = sys.argv[1]
    project_name = sys.argv[2]
    consult = "--consult" in sys.argv
    
    # Print banner
    print_banner()
    
    print(f"📋 Requirement: {requirement}")
    print(f"📁 Project: {project_name}")
    print(f"💡 Consult on architecture: {'Yes' if consult else 'No'}")
    
    # Check API keys
    print("\n🔑 Checking API keys...")
    from dotenv import load_dotenv
    load_dotenv()
    
    gemini_key = os.getenv("GEMINI_API_KEY")
    claude_key = os.getenv("ANTHROPIC_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if not gemini_key:
        print("❌ GEMINI_API_KEY not found in environment!")
        print("Please set it in .env file or environment variables.")
        sys.exit(1)
    
    if not claude_key:
        print("⚠️  ANTHROPIC_API_KEY not found (Reviewer Agent will be limited)")
    
    if not openai_key and consult:
        print("⚠️  OPENAI_API_KEY not found (Consultant Agent will be unavailable)")
    
    print("✅ API keys configured")
    
    # Create orchestrator
    print("\n🎭 Initializing orchestrator...")
    try:
        orchestrator = AutonomousOrchestrator(project_name)
        print("✅ Orchestrator initialized")
    except Exception as e:
        print(f"❌ Failed to initialize orchestrator: {e}")
        sys.exit(1)
    
    # Run the orchestrator
    print("\n🚀 Starting autonomous build process...\n")
    
    try:
        result = orchestrator.run(
            requirement=requirement,
            consult_on_architecture=consult
        )
        
        # Print result
        print_result(result)
        
        # Also output as JSON for programmatic access
        print("\n" + "="*60)
        print("📊 JSON OUTPUT (for programmatic access):")
        print("="*60)
        print(json.dumps(result, indent=2))
        
        # Exit with appropriate code
        sys.exit(0 if result["success"] else 1)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Build interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

