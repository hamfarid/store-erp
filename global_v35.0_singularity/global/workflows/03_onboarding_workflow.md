# Onboarding Workflow

This workflow helps new developers get up to speed with the project.

## Steps

1. **Read Core Documentation**
   - Read: `README.md`
   - Read: `docs/ARCHITECTURE.md`
   - Read: `GLOBAL_PROFESSIONAL_CORE_PROMPT_v15.0.md`

2. **Set Up Development Environment**
   - Install dependencies: `npm install` or `pip install -r requirements.txt`
   - Set up environment variables (copy `.env.example` to `.env`)
   - Set up database: `npm run db:setup`

3. **Run the Application Locally**
   - Start backend: `npm run dev:backend`
   - Start frontend: `npm run dev:frontend`
   - Verify application runs without errors

4. **Run Tests**
   - Run unit tests: `npm test`
   - Run E2E tests: `npm run test:e2e`
   - Ensure all tests pass

5. **Explore the Codebase**
   - Review: `docs/PROJECT_MAPS.md`
   - Understand folder structure
   - Identify key components and modules

6. **Complete a Starter Task**
   - Pick a "good first issue" from the issue tracker
   - Create a feature branch
   - Implement the fix/feature
   - Write tests
   - Submit a pull request

7. **Review Team Workflows**
   - Read: `docs/CONTRIBUTING.md`
   - Understand Git workflow
   - Learn code review process
