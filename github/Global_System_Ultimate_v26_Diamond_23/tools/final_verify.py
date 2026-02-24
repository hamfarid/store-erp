#!/usr/bin/env python3
import os
import sys
import re

# Load Version
try:
    with open(os.path.join(os.path.dirname(__file__), "../VERSION"), "r") as f:
        VERSION = f.read().strip()
except FileNotFoundError:
    VERSION = "UNKNOWN"

# Final Verification Script for Global System Ultimate
# Reads version dynamically from VERSION file

def verify_file_content(path, required_strings):
    """Verifies that a file contains specific strings."""
    if not os.path.exists(path):
        print(f"❌ Missing File: {path}")
        return False
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        missing = [s for s in required_strings if s not in content]
        
        if missing:
            print(f"❌ File {path} missing content: {missing}")
            return False
        
        print(f"✅ Verified {path}")
        return True
    except Exception as e:
        print(f"❌ Error reading {path}: {e}")
        return False

def main():
    print(f"🛡️ Running Final Verification for {VERSION}...")
    
    # Determine BOOTSTRAP filename based on version (e.g., v15.9.8 -> BOOTSTRAP_v15.9.md)
    # We assume the BOOTSTRAP file uses the MAJOR.MINOR version
    version_parts = VERSION.split('.')
    if len(version_parts) >= 2:
        bootstrap_version = f"{version_parts[0]}.{version_parts[1]}"
    else:
        bootstrap_version = VERSION
        
    bootstrap_filename = f"BOOTSTRAP_{bootstrap_version}.md"
    
    # Define checks: (Relative Path, [Required Strings])
    # Note: We check for the VERSION string itself in key files to ensure they are updated
    checks = [
        ("AGENTS.md", ["Global System Ultimate", "Platform Configuration", "Augment", "Windsurf", "Cursor", "Kiro", "Gemini CLI", "Devin", "Roo Code", "Aider", "OpenLLMetry", "Helicone"]),
        (bootstrap_filename, [f"GLOBAL_PROFESSIONAL_CORE_PROMPT_{VERSION}.md"]),
        (f"prompts/GLOBAL_PROFESSIONAL_CORE_PROMPT_{VERSION}.md", ["global_system/prompts/", "global_system/docs/", "global_system/scripts/"]),
        ("tools/sentinel.py", ["check_structured_output", "check_halt_protocol"]),
        ("tools/speckit.py", ["generate_plan", "4-Block Pattern"]),
        ("tools/sync_mcp_config.py", []), # Just check existence
        ("scripts/preflight_check.py", ["Preflight Check"]),
        ("knowledge/core/project_lifecycle.md", ["Project Lifecycle", "Phases"]),
        ("package.json", ["\"pnpm\": \">="]),
        ("infrastructure/docker/Dockerfile.python", ["uv", "distroless", "UV_COMPILE_BYTECODE=1"]),
        ("infrastructure/k8s/deployment.yaml", ["maxUnavailable: 0", "nvidia.com/gpu"]),
        ("infrastructure/iac/main.tf", ["terraform", "backend \"s3\"", "encrypt = true"]),
        ("infrastructure/iac/trivy.yaml", ["severity", "HIGH", "CRITICAL"]),
        ("knowledge/protocols/container_signing.md", ["Cosign", "Keyless Signing", "ClusterImagePolicy"]),
        (".dockerignore", [".git", "node_modules", ".env"]),
        ("CLAUDE.md", ["See @AGENTS.md"]),
        (".cursor/rules/master.mdc", ["See @AGENTS.md", "globs: *"]),
        (".github/copilot-instructions.md", ["See @AGENTS.md", "Core Directives"]),
        ("config/mcp_config.json", ["augment", "context7", "sentry"]),
        ("rules/dependency_management.md", ["uv", "pnpm", "SHA", "Socket.dev", "Trivy", "pip-audit"]),
        ("knowledge/protocols/safe_updates.md", ["Feature Flags", "Blue-Green"]),
        ("knowledge/protocols/future_proof_architecture.md", ["Decoupled Services", "Plugin Pattern", "Sidecar Pattern"]),
        ("rules/99_anti_hallucination.md", ["RAG for Code", "HALT", "Guardian Agents"]),
        ("knowledge/core/memory.md", ["Session Memory", "Memory Bank Pattern"]),
        # Area 5: Testing & Verification
        ("tests/conftest.py", ["pytest", "mock_env"]),
        ("tests/e2e/playwright.config.ts", ["playwright", "fullyParallel"]),
        ("tools/evals/template_eval.py", ["eval_feature_x", "Metric: Exact Match"]),
        ("tools/evals/promptfoo.yaml", ["prompts:", "providers:", "assert:"]),
        (".pre-commit-config.yaml", ["gitleaks", "ruff", "biome-check"]),
        ("knowledge/protocols/cross_check.md", ["CrossCheck Protocol", "Co-Authored-By", "mcp-code-crosscheck"]),
        # Area 6: Security
        ("knowledge/owasp_llm_2025.md", ["LLM01: Prompt Injection", "LLM08: Excessive Agency"]),
        ("rules/security_policy.md", ["SAIF 2.0", "Secure the AI Supply Chain"]),
        ("tools/security_scan.py", ["API Key Leak", "Insecure Eval"]),
        # Area 7: Swarm
        ("global_system/roles/architect.md", ["Role: Architect", "C4 diagrams"]),
        ("global_system/roles/developer.md", ["Role: Developer", "EDD"]),
        ("global_system/roles/reviewer.md", ["Role: Reviewer", "Code Review"]),
        ("global_system/workflows/swarm_protocol.md", ["Swarm Protocol", "Chain-of-Vibes"]),
        # Area 4: Platform Configs (New)
        (".claude/settings.json", ["permissions", "hooks", "pre_commit"])
    ]
    
    # Get the root directory of the project (assuming script is in tools/)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    all_passed = True
    for rel_path, requirements in checks:
        full_path = os.path.join(project_root, rel_path)
        if not verify_file_content(full_path, requirements):
            all_passed = False
            
    if all_passed:
        print(f"\n🎉 ALL SYSTEMS GO! {VERSION} is ready for deployment.")
        sys.exit(0)
    else:
        print("\n❌ VERIFICATION FAILED. Fix issues before deployment.")
        sys.exit(1)

if __name__ == "__main__":
    main()
