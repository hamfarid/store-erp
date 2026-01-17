# Release Workflow

This workflow guides the process of creating a new production release.

## Steps

1. **Verify All Tests Pass**
   - Run: `npm test` or `pytest`
   - Ensure 100% pass rate

2. **Check Code Coverage**
   - Run: `npm run coverage`
   - Ensure >= 80%

3. **Run Security Scan**
   - Run: `npm audit` or `safety check`
   - Fix all critical and high vulnerabilities

4. **Update Version**
   - Run: `npm version patch` (or `minor`, `major`)
   - Update CHANGELOG.md

5. **Build Production Assets**
   - Run: `npm run build`
   - Verify no errors

6. **Create Git Tag**
   - Run: `git tag -a v1.0.0 -m "Release v1.0.0"`
   - Push: `git push origin v1.0.0`

7. **Deploy to Staging**
   - Run: `kubectl apply -f k8s/staging/`
   - Verify deployment

8. **Run Smoke Tests**
   - Execute E2E tests on staging
   - Verify critical paths

9. **Deploy to Production**
   - Run: `kubectl apply -f k8s/production/`
   - Monitor logs and metrics

10. **Create Release Notes**
    - Document new features, bug fixes, and breaking changes
    - Publish on GitHub Releases
