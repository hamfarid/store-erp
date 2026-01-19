#!/usr/bin/env python3
"""Create all missing prompt files based on logical categories"""

missing_prompts = {
    # 07-09: Advanced Development Tools
    "07_code_generation.md": """# Code Generation Prompt

## Purpose
Generate high-quality, production-ready code based on specifications.

## Instructions
1. Read requirements from docs/Task_List.md
2. Generate code following all rules in rules/
3. Include comprehensive docstrings
4. Add unit tests for all functions
5. Log all actions to system_log.md

## OSF Framework Application
- Security: Validate all inputs
- Correctness: Follow specifications exactly
- Reliability: Handle all edge cases

## Output
- Complete, working code files
- Unit test files
- Updated Task_List.md
""",
    
    "08_refactoring.md": """# Code Refactoring Prompt

## Purpose
Improve existing code quality without changing functionality.

## Instructions
1. Analyze code for violations of DRY principle
2. Extract repeated logic into helpers/
3. Improve naming for clarity
4. Add missing documentation
5. Optimize performance bottlenecks
6. Log all changes to system_log.md

## Zero-Tolerance Checks
- No duplicate code
- No undocumented functions
- No magic numbers

## Output
- Refactored code
- Updated documentation
- Performance improvement report
""",
    
    "09_code_review.md": """# Code Review Prompt

## Purpose
Perform comprehensive code review before merging.

## Instructions
1. Check all files against rules/
2. Verify test coverage >= 80%
3. Run linting and style checks
4. Check for security vulnerabilities
5. Verify documentation completeness
6. Log review results to system_log.md

## Review Checklist
- [ ] All tests pass
- [ ] No linting errors
- [ ] Security scan clean
- [ ] Documentation complete
- [ ] No TODO comments

## Output
- Review report in docs/
- List of required fixes
- Approval/rejection decision
""",
    
    # 13-19: Project Management
    "13_task_breakdown.md": """# Task Breakdown Prompt

## Purpose
Break down complex features into manageable tasks.

## Instructions
1. Read feature requirements
2. Identify all components (frontend, backend, database, tests)
3. Create step-by-step tasks in docs/Task_List.md
4. Estimate complexity for each task
5. Identify dependencies between tasks
6. Log breakdown to system_log.md

## Task Format
```markdown
- [ ] Task name (Complexity: Low/Medium/High)
  - Dependencies: [task_ids]
  - Components: frontend/backend/database/tests
  - Estimated time: X hours
```

## Output
- Updated Task_List.md
- Dependency graph
""",
    
    "14_sprint_planning.md": """# Sprint Planning Prompt

## Purpose
Plan development sprints with clear goals.

## Instructions
1. Review Task_List.md
2. Group tasks by sprint (1-2 weeks)
3. Prioritize by OSF Framework
4. Assign tasks to agents (Lead/Reviewer/Consultant)
5. Set sprint goals and success criteria
6. Log plan to system_log.md

## Sprint Structure
- Sprint goal
- Task list
- Success criteria
- Agent assignments

## Output
- Sprint plan in docs/
- Updated Task_List.md with sprint tags
""",
    
    "15_progress_tracking.md": """# Progress Tracking Prompt

## Purpose
Monitor project progress and identify blockers.

## Instructions
1. Review Task_List.md daily
2. Calculate completion percentage
3. Identify blocked tasks
4. Update docs/PROGRESS_TRACKER.md
5. Alert on delays or risks
6. Log status to system_log.md

## Metrics
- Tasks completed / total
- Test coverage %
- Documentation completeness %
- Blockers count

## Output
- Updated PROGRESS_TRACKER.md
- Daily status report
""",
    
    "16_risk_management.md": """# Risk Management Prompt

## Purpose
Identify and mitigate project risks.

## Instructions
1. Analyze codebase for technical debt
2. Identify security vulnerabilities
3. Check dependency versions
4. Review test coverage gaps
5. Document risks in docs/RISKS.md
6. Propose mitigation strategies
7. Log risks to system_log.md

## Risk Categories
- Security
- Performance
- Scalability
- Maintainability

## Output
- RISKS.md with mitigation plans
- Priority-ordered action items
""",
    
    "17_dependency_management.md": """# Dependency Management Prompt

## Purpose
Manage project dependencies safely.

## Instructions
1. Audit all dependencies
2. Check for known vulnerabilities
3. Update to latest secure versions
4. Document all dependencies
5. Create requirements.txt / package.json
6. Log changes to system_log.md

## Checks
- No deprecated packages
- No known CVEs
- License compatibility

## Output
- Updated dependency files
- Vulnerability report
- Upgrade recommendations
""",
    
    "18_version_control.md": """# Version Control Prompt

## Purpose
Manage Git workflow and versioning.

## Instructions
1. Follow conventional commit messages
2. Create feature branches
3. Perform code reviews before merge
4. Tag releases with semantic versioning
5. Maintain clean commit history
6. Log all Git operations to system_log.md

## Commit Message Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

## Output
- Clean Git history
- Tagged releases
- Updated CHANGELOG.md
""",
    
    "19_release_management.md": """# Release Management Prompt

## Purpose
Prepare and execute software releases.

## Instructions
1. Run full test suite
2. Update version numbers
3. Generate CHANGELOG.md
4. Create release notes
5. Tag release in Git
6. Deploy to staging
7. Verify deployment
8. Log release to system_log.md

## Release Checklist
- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version bumped
- [ ] Git tag created
- [ ] Deployment successful

## Output
- Release package
- Release notes
- Deployment report
""",
    
    # 25-29: Integration & DevOps
    "25_ci_cd.md": """# CI/CD Pipeline Prompt

## Purpose
Set up continuous integration and deployment.

## Instructions
1. Create CI/CD configuration (.github/workflows/, .gitlab-ci.yml)
2. Define build steps
3. Configure automated testing
4. Set up deployment stages
5. Add security scanning
6. Log pipeline setup to system_log.md

## Pipeline Stages
1. Build
2. Test
3. Security Scan
4. Deploy to Staging
5. Deploy to Production

## Output
- CI/CD configuration files
- Pipeline documentation
""",
    
    "26_docker.md": """# Docker Configuration Prompt

## Purpose
Containerize the application.

## Instructions
1. Create Dockerfile
2. Create docker-compose.yml
3. Optimize image size
4. Add health checks
5. Document Docker usage in .docs/
6. Log Docker setup to system_log.md

## Best Practices
- Multi-stage builds
- Non-root user
- Minimal base image
- .dockerignore file

## Output
- Dockerfile
- docker-compose.yml
- .docs/DOCKER.md
""",
    
    "27_monitoring.md": """# Monitoring & Logging Prompt

## Purpose
Set up application monitoring and logging.

## Instructions
1. Implement structured logging
2. Add health check endpoints
3. Set up metrics collection
4. Configure alerts
5. Document monitoring in docs/
6. Log setup to system_log.md

## Monitoring Areas
- Application health
- Performance metrics
- Error rates
- Resource usage

## Output
- Logging configuration
- Monitoring dashboard
- Alert rules
""",
    
    "28_performance.md": """# Performance Optimization Prompt

## Purpose
Optimize application performance.

## Instructions
1. Profile application
2. Identify bottlenecks
3. Optimize database queries
4. Implement caching
5. Optimize frontend assets
6. Document optimizations
7. Log improvements to system_log.md

## Optimization Areas
- Database queries
- API response times
- Frontend load time
- Memory usage

## Output
- Performance report
- Optimization recommendations
- Implementation plan
""",
    
    "29_backup_recovery.md": """# Backup & Recovery Prompt

## Purpose
Implement backup and disaster recovery.

## Instructions
1. Set up automated backups
2. Test backup restoration
3. Document recovery procedures
4. Create backup schedule
5. Verify backup integrity
6. Log backup operations to system_log.md

## Backup Strategy
- Database backups (daily)
- Code backups (Git)
- Configuration backups
- User data backups

## Output
- Backup scripts
- Recovery documentation
- Backup verification reports
""",
    
    # 32-39: Security & Compliance
    "32_encryption.md": """# Encryption Prompt

## Purpose
Implement encryption for data protection.

## Instructions
1. Encrypt sensitive data at rest
2. Use TLS for data in transit
3. Implement secure key management
4. Hash passwords with bcrypt/argon2
5. Document encryption methods
6. Log encryption setup to system_log.md

## Encryption Standards
- AES-256 for data at rest
- TLS 1.3 for transit
- Secure key rotation

## Output
- Encryption implementation
- Key management documentation
""",
    
    "33_authorization.md": """# Authorization Prompt

## Purpose
Implement role-based access control (RBAC).

## Instructions
1. Define user roles
2. Create permission matrix
3. Implement authorization middleware
4. Add role checks to endpoints
5. Document authorization model
6. Log setup to system_log.md

## RBAC Model
- Roles: Admin, User, Guest
- Permissions: Create, Read, Update, Delete
- Resources: All API endpoints

## Output
- Authorization middleware
- Permission documentation
""",
    
    "34_input_validation.md": """# Input Validation Prompt

## Purpose
Validate and sanitize all user inputs.

## Instructions
1. Define validation schemas
2. Implement server-side validation
3. Sanitize inputs to prevent XSS
4. Validate file uploads
5. Add rate limiting
6. Log validation setup to system_log.md

## Validation Rules
- Type checking
- Length limits
- Format validation
- Whitelist approach

## Output
- Validation schemas
- Sanitization functions
""",
    
    "35_audit_logging.md": """# Audit Logging Prompt

## Purpose
Log all security-relevant events.

## Instructions
1. Log authentication attempts
2. Log authorization failures
3. Log data modifications
4. Log admin actions
5. Implement log retention policy
6. Log audit setup to system_log.md

## Audit Events
- Login/logout
- Permission changes
- Data access
- Configuration changes

## Output
- Audit logging implementation
- Log analysis tools
""",
    
    "36_vulnerability_scanning.md": """# Vulnerability Scanning Prompt

## Purpose
Scan for security vulnerabilities.

## Instructions
1. Run dependency vulnerability scans
2. Perform static code analysis
3. Check for OWASP Top 10
4. Scan Docker images
5. Document findings
6. Log scan results to system_log.md

## Scanning Tools
- npm audit / pip-audit
- SonarQube
- Trivy (Docker)
- OWASP ZAP

## Output
- Vulnerability report
- Remediation plan
""",
    
    "37_penetration_testing.md": """# Penetration Testing Prompt

## Purpose
Perform security penetration testing.

## Instructions
1. Test authentication bypass
2. Test SQL injection
3. Test XSS vulnerabilities
4. Test CSRF protection
5. Document findings
6. Log test results to system_log.md

## Test Areas
- Authentication
- Authorization
- Input validation
- Session management

## Output
- Penetration test report
- Security fixes
""",
    
    "38_compliance.md": """# Compliance Prompt

## Purpose
Ensure regulatory compliance (GDPR, HIPAA, etc.).

## Instructions
1. Identify applicable regulations
2. Implement required controls
3. Document compliance measures
4. Create privacy policy
5. Implement data deletion
6. Log compliance setup to system_log.md

## Compliance Areas
- Data privacy
- Data retention
- User consent
- Data portability

## Output
- Compliance documentation
- Privacy policy
- Data handling procedures
""",
    
    "39_incident_response.md": """# Incident Response Prompt

## Purpose
Handle security incidents effectively.

## Instructions
1. Create incident response plan
2. Define escalation procedures
3. Set up incident logging
4. Document response steps
5. Conduct post-incident review
6. Log incidents to system_log.md

## Incident Types
- Data breach
- Service outage
- Security vulnerability
- Unauthorized access

## Output
- Incident response plan
- Incident log template
""",
    
    # 45-49: Testing & Quality
    "45_unit_testing.md": """# Unit Testing Prompt

## Purpose
Write comprehensive unit tests.

## Instructions
1. Test all functions and methods
2. Achieve >= 80% code coverage
3. Test edge cases and errors
4. Use mocking for dependencies
5. Document test cases
6. Log test results to system_log.md

## Test Structure
- Arrange: Set up test data
- Act: Execute function
- Assert: Verify results

## Output
- Unit test files
- Coverage report
""",
    
    "46_integration_testing.md": """# Integration Testing Prompt

## Purpose
Test component interactions.

## Instructions
1. Test API endpoints
2. Test database operations
3. Test service integrations
4. Test authentication flow
5. Document integration tests
6. Log test results to system_log.md

## Integration Points
- API + Database
- Frontend + Backend
- External services

## Output
- Integration test suite
- Test documentation
""",
    
    "47_load_testing.md": """# Load Testing Prompt

## Purpose
Test application performance under load.

## Instructions
1. Define load test scenarios
2. Set performance benchmarks
3. Run load tests
4. Analyze results
5. Identify bottlenecks
6. Log test results to system_log.md

## Load Test Scenarios
- Normal load
- Peak load
- Stress test
- Endurance test

## Output
- Load test report
- Performance recommendations
""",
    
    "48_regression_testing.md": """# Regression Testing Prompt

## Purpose
Ensure new changes don't break existing functionality.

## Instructions
1. Run full test suite
2. Test critical user paths
3. Verify bug fixes
4. Check for side effects
5. Document regression tests
6. Log test results to system_log.md

## Regression Test Coverage
- All existing features
- Previously fixed bugs
- Critical workflows

## Output
- Regression test results
- Bug reports
""",
    
    "49_acceptance_testing.md": """# Acceptance Testing Prompt

## Purpose
Verify requirements are met.

## Instructions
1. Review requirements
2. Create acceptance criteria
3. Test user stories
4. Verify business logic
5. Get stakeholder approval
6. Log test results to system_log.md

## Acceptance Criteria
- All requirements implemented
- User stories complete
- Business rules correct

## Output
- Acceptance test report
- Sign-off documentation
""",
    
    # 51-59: Advanced Features
    "51_api_versioning.md": """# API Versioning Prompt

## Purpose
Implement API versioning strategy.

## Instructions
1. Choose versioning strategy (URL/header)
2. Version all endpoints
3. Maintain backward compatibility
4. Document version changes
5. Deprecate old versions gracefully
6. Log versioning to system_log.md

## Versioning Strategy
- URL: /api/v1/, /api/v2/
- Semantic versioning
- Deprecation notices

## Output
- Versioned API endpoints
- Migration guide
""",
    
    "52_caching.md": """# Caching Strategy Prompt

## Purpose
Implement caching for performance.

## Instructions
1. Identify cacheable data
2. Choose caching strategy (Redis, Memcached)
3. Implement cache invalidation
4. Set cache TTL
5. Monitor cache hit rates
6. Log caching to system_log.md

## Caching Layers
- Database query cache
- API response cache
- Static asset cache

## Output
- Caching implementation
- Cache configuration
""",
    
    "53_rate_limiting.md": """# Rate Limiting Prompt

## Purpose
Protect API from abuse.

## Instructions
1. Define rate limits per endpoint
2. Implement rate limiting middleware
3. Return proper HTTP status codes
4. Add rate limit headers
5. Document rate limits
6. Log rate limiting to system_log.md

## Rate Limit Strategy
- Per user: 100 req/min
- Per IP: 1000 req/hour
- Sliding window algorithm

## Output
- Rate limiting middleware
- Rate limit documentation
""",
    
    "54_websockets.md": """# WebSocket Implementation Prompt

## Purpose
Implement real-time communication.

## Instructions
1. Set up WebSocket server
2. Implement authentication
3. Handle connection lifecycle
4. Implement message routing
5. Add error handling
6. Log WebSocket setup to system_log.md

## WebSocket Features
- Real-time updates
- Bidirectional communication
- Connection management

## Output
- WebSocket server
- Client integration code
""",
    
    "55_file_upload.md": """# File Upload Prompt

## Purpose
Implement secure file uploads.

## Instructions
1. Validate file types
2. Limit file sizes
3. Scan for malware
4. Store files securely
5. Generate unique filenames
6. Log uploads to system_log.md

## Security Measures
- Whitelist file types
- Virus scanning
- Separate storage
- Access control

## Output
- File upload endpoint
- Storage configuration
""",
    
    "56_email_system.md": """# Email System Prompt

## Purpose
Implement email functionality.

## Instructions
1. Set up email service (SMTP)
2. Create email templates
3. Implement email queue
4. Add unsubscribe functionality
5. Track email delivery
6. Log email operations to system_log.md

## Email Types
- Transactional
- Notifications
- Marketing

## Output
- Email service implementation
- Email templates
""",
    
    "57_search.md": """# Search Implementation Prompt

## Purpose
Implement search functionality.

## Instructions
1. Choose search engine (Elasticsearch, etc.)
2. Index searchable data
3. Implement search API
4. Add filters and sorting
5. Optimize search performance
6. Log search setup to system_log.md

## Search Features
- Full-text search
- Faceted search
- Auto-complete
- Relevance ranking

## Output
- Search API
- Search configuration
""",
    
    "58_notifications.md": """# Notification System Prompt

## Purpose
Implement notification system.

## Instructions
1. Design notification schema
2. Implement notification channels (email, push, SMS)
3. Add user preferences
4. Implement notification queue
5. Track notification delivery
6. Log notifications to system_log.md

## Notification Channels
- Email
- Push notifications
- SMS
- In-app

## Output
- Notification service
- User preferences API
""",
    
    "59_analytics.md": """# Analytics Implementation Prompt

## Purpose
Implement analytics and tracking.

## Instructions
1. Define analytics events
2. Implement event tracking
3. Set up analytics dashboard
4. Add user behavior tracking
5. Implement privacy controls
6. Log analytics setup to system_log.md

## Analytics Events
- Page views
- User actions
- Conversions
- Errors

## Output
- Analytics implementation
- Dashboard configuration
""",
    
    # 61-69: Advanced Topics
    "61_microservices.md": """# Microservices Architecture Prompt

## Purpose
Design and implement microservices.

## Instructions
1. Identify service boundaries
2. Design service APIs
3. Implement service discovery
4. Add inter-service communication
5. Implement circuit breakers
6. Log microservices setup to system_log.md

## Microservices Patterns
- API Gateway
- Service mesh
- Event-driven architecture

## Output
- Microservices architecture
- Service documentation
""",
    
    "62_graphql.md": """# GraphQL Implementation Prompt

## Purpose
Implement GraphQL API.

## Instructions
1. Define GraphQL schema
2. Implement resolvers
3. Add authentication
4. Implement data loaders
5. Add query optimization
6. Log GraphQL setup to system_log.md

## GraphQL Features
- Type system
- Queries and mutations
- Subscriptions
- Schema stitching

## Output
- GraphQL server
- Schema documentation
""",
    
    "63_message_queue.md": """# Message Queue Prompt

## Purpose
Implement message queue for async processing.

## Instructions
1. Choose message broker (RabbitMQ, Kafka)
2. Define message schemas
3. Implement producers and consumers
4. Add error handling and retries
5. Monitor queue health
6. Log queue setup to system_log.md

## Queue Patterns
- Work queues
- Pub/Sub
- RPC

## Output
- Message queue implementation
- Queue documentation
""",
    
    "64_data_migration.md": """# Data Migration Prompt

## Purpose
Migrate data safely.

## Instructions
1. Analyze source and target schemas
2. Create migration scripts
3. Implement data validation
4. Test migration on staging
5. Create rollback plan
6. Log migration to system_log.md

## Migration Steps
1. Backup data
2. Run migration
3. Validate results
4. Verify application

## Output
- Migration scripts
- Validation reports
""",
    
    "65_internationalization.md": """# Internationalization (i18n) Prompt

## Purpose
Support multiple languages.

## Instructions
1. Extract all text strings
2. Create translation files
3. Implement language switching
4. Format dates and numbers
5. Support RTL languages
6. Log i18n setup to system_log.md

## i18n Features
- Multiple languages
- Dynamic language switching
- Locale-specific formatting

## Output
- Translation files
- i18n configuration
""",
    
    "66_accessibility.md": """# Accessibility (a11y) Prompt

## Purpose
Ensure application accessibility.

## Instructions
1. Add ARIA labels
2. Ensure keyboard navigation
3. Add screen reader support
4. Check color contrast
5. Test with accessibility tools
6. Log a11y improvements to system_log.md

## Accessibility Standards
- WCAG 2.1 Level AA
- Semantic HTML
- Keyboard accessible

## Output
- Accessible components
- Accessibility report
""",
    
    "67_seo.md": """# SEO Optimization Prompt

## Purpose
Optimize for search engines.

## Instructions
1. Add meta tags
2. Implement structured data
3. Create sitemap.xml
4. Optimize page speed
5. Add canonical URLs
6. Log SEO setup to system_log.md

## SEO Elements
- Title tags
- Meta descriptions
- Open Graph tags
- Schema.org markup

## Output
- SEO-optimized pages
- Sitemap
""",
    
    "68_pwa.md": """# Progressive Web App (PWA) Prompt

## Purpose
Convert to Progressive Web App.

## Instructions
1. Create service worker
2. Add web app manifest
3. Implement offline support
4. Add push notifications
5. Make app installable
6. Log PWA setup to system_log.md

## PWA Features
- Offline functionality
- Push notifications
- App-like experience
- Installable

## Output
- Service worker
- Manifest file
""",
    
    "69_machine_learning.md": """# Machine Learning Integration Prompt

## Purpose
Integrate ML models into application.

## Instructions
1. Train or import ML model
2. Create prediction API
3. Implement model versioning
4. Add model monitoring
5. Handle model updates
6. Log ML setup to system_log.md

## ML Integration
- Model serving
- Feature engineering
- A/B testing
- Model monitoring

## Output
- ML API
- Model documentation
""",
}

# Create all missing files
created_count = 0
for filename, content in missing_prompts.items():
    filepath = filename
    with open(filepath, 'w') as f:
        f.write(content)
    created_count += 1
    print(f"✓ Created: {filename}")

print(f"\n{'='*70}")
print(f"✓ Successfully created {created_count} missing prompt files")
print(f"{'='*70}")
