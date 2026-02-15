# CI/CD Pipeline Design

## Why Each Stage Exists

### Lint (flake8)
Catches style issues and common bugs. Fast to run (~5 seconds).
Prevents "works on my machine" style inconsistencies.

### Unit Tests (pytest)
Validates business logic. If a test fails, the code is broken.
Runs in ~10 seconds, catches most bugs before they reach production.

### Security Scan (Trivy)
Scans dependencies for known CVEs (Common Vulnerabilities and Exposures).
Fails on CRITICAL and HIGH severity findings.
This is DevSecOps — security is part of the pipeline, not an afterthought.

### Docker Build
Validates the Dockerfile and runs tests inside the container.
Multi-stage build ensures the production image is clean and minimal.

### Helm Lint
Validates the Kubernetes deployment templates.
Templates are rendered with all environment values to catch errors early.

## Rollback Procedure
If a bad deployment reaches dev/staging:
1. `helm rollback deploy-tracker <previous-revision> -n dev`
2. Investigate the failure in pod logs: `kubectl logs -n dev -l app=deploy-tracker`
3. Fix in a new feature branch → PR → CI → merge → redeploy