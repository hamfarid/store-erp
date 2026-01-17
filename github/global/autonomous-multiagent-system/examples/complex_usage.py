"""
Complex Usage Example for Autonomous Multi-Agent System

This example shows how to use the system for a complex project
that requires strategic consultation.
"""

import sys
sys.path.insert(0, '../src')

from orchestrator import AutonomousOrchestrator


def main():
    """Run a complex autonomous workflow"""
    
    # Create orchestrator
    orchestrator = AutonomousOrchestrator("user-auth-api")
    
    # Define requirement
    requirement = """
Build a RESTful API for user authentication with the following features:

1. User Registration
   - Email validation
   - Password hashing (bcrypt)
   - Email verification

2. User Login
   - JWT token generation
   - Refresh tokens
   - Rate limiting

3. Password Reset
   - Email-based reset
   - Secure token generation
   - Expiration handling

4. Security
   - HTTPS only
   - CORS configuration
   - Input validation
   - SQL injection prevention

5. Database
   - PostgreSQL
   - User model
   - Token model
   - Migrations

6. Testing
   - 95%+ coverage
   - Unit tests
   - Integration tests
   - Security tests

7. Documentation
   - API documentation
   - Setup guide
   - Usage examples

Technology Stack:
- Flask (Python)
- PostgreSQL
- JWT
- bcrypt
- pytest
"""
    
    # Run autonomous workflow with consultation
    result = orchestrator.run(
        requirement=requirement,
        consult_on_architecture=True  # Complex project, consult ChatGPT
    )
    
    # Print result
    if result["success"]:
        print("\n✅ Project completed successfully!")
        print(f"\nMemory saved to: {result['result']['memory_path']}")
        print(f"\nStatus: {result['result']['status']}")
        
        # Save files
        with open('generated_code.py', 'w') as f:
            f.write(result['result']['code'])
        
        with open('generated_tests.py', 'w') as f:
            f.write(result['result']['tests'])
        
        with open('generated_docs.md', 'w') as f:
            f.write(result['result']['documentation'])
        
        print("\n📁 Files saved:")
        print("- generated_code.py")
        print("- generated_tests.py")
        print("- generated_docs.md")
        
    else:
        print(f"\n❌ Project failed: {result['error']}")


if __name__ == "__main__":
    main()

