# Container-to-Kubernetes CI/CD Deployment Pipeline

![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![Helm](https://img.shields.io/badge/Helm-0F1689?style=for-the-badge&logo=helm&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

**AWS CCP Certified** • **AZ-104 Certified** • **Terraform Associate (In Progress)** • **DevOps Portfolio Project**

## 🚀 Introduction

This project demonstrates my implementation of a **full CI/CD deployment pipeline** that takes a containerised Python application from code commit through to automated deployment on Kubernetes using Docker, Helm Charts, and GitHub Actions.

As part of my transition into DevOps engineering—having passed the **AZ-104 Azure Administrator** and **AWS Cloud Practitioner** certifications, and currently preparing for the **HashiCorp Terraform Associate**—this project represents my hands-on application of core DevOps concepts: containerisation, orchestration, automated pipelines, and security scanning.

## 📋 Project Overview

**Objective:** Build an automated pipeline that lints, tests, scans, builds, and deploys a containerised application to Kubernetes with zero manual intervention.

**Key Features:**
- ✅ **Multi-Stage Docker Build** – Tests run inside the build, production image is minimal (~150MB)
- ✅ **Non-Root Container** – Application runs as `appuser`, not root (security best practice)
- ✅ **Kubernetes Deployment** – Rolling updates with liveness/readiness probes for zero-downtime
- ✅ **Helm Chart** – Templated deployments with per-environment configs (dev/staging/prod)
- ✅ **CI/CD Pipeline** – GitHub Actions: lint → test → security scan → build → push → deploy
- ✅ **Security Scanning** – Trivy vulnerability scanning integrated into the pipeline
- ✅ **Auto-Scaling** – Horizontal Pod Autoscaler scales pods based on CPU utilisation

## 🛠️ Skills Demonstrated

| **Containerisation** | **Kubernetes & Helm** | **CI/CD & Automation** |
|:---------------------|:----------------------|:-----------------------|
| • Multi-stage Dockerfile | • Deployments & ReplicaSets | • GitHub Actions pipelines |
| • Layer caching optimisation | • Services & Ingress routing | • Automated unit testing (pytest) |
| • Non-root user security | • Liveness & readiness probes | • Trivy security scanning |
| • Docker Hub registry | • Resource requests & limits | • Docker image build & push |
| • Health check configuration | • Horizontal Pod Autoscaler | • Branch protection & PR workflow |
| • .dockerignore best practices | • Network policies | • Conventional commit messages |
| | • Helm templating & values | • Multi-environment deployment |

## 🚀 Quick Start

| **Step** | **Command** | **Description** |
|:---|:---|:---|
| **1. Clone** | `git clone https://github.com/Rabaanee/docker-k8s-deployment-pipeline.git`<br>`cd docker-k8s-deployment-pipeline` | Get the code locally |
| **2. Build Image** | `cd app && docker build -t deploy-tracker:v1.0.0 .` | Build container (runs tests inside) |
| **3. Run Container** | `docker run -d -p 5000:5000 deploy-tracker:v1.0.0` | Start the application |
| **4. Test** | `curl http://localhost:5000/health` | Verify it's running |
| **5. Start K8s** | `minikube start && minikube addons enable ingress` | Start local Kubernetes cluster |
| **6. Deploy** | `helm upgrade --install deploy-tracker helm/deploy-tracker/ -n dev --create-namespace -f helm/deploy-tracker/values-dev.yaml` | Deploy to Kubernetes with Helm |
| **7. Verify** | `kubectl get pods -n dev` | Check pods are running |

**Build Time:** ~2 minutes (Docker build including tests)

**Deployment Time:** ~30 seconds (Helm install to Kubernetes)

**Cost:** £0 (runs entirely on your local machine)

## 🏗️ Architecture Overview

The pipeline implements:
- Automated CI/CD from code push to Kubernetes deployment
- Multi-stage Docker builds with integrated testing
- Helm-based deployments with per-environment configuration
- Security scanning with Trivy in the pipeline
- Kubernetes health probes and auto-scaling

<img width="1466" height="2326" alt="k8s diagram drawio(2)" src="https://github.com/user-attachments/assets/31130e64-eed4-42f4-920b-837cf1adf3b2" />
Code Push ➜ Lint & Test ➜ Security Scan ➜ Build Image ➜ Push to Registry ➜ Deploy via Helm ➜ Kubernetes


## 📁 Project Structure
```
docker-k8s-deployment-pipeline/
├── app/                                # Python Flask application
│   ├── Dockerfile                      # Multi-stage: test → production
│   ├── app.py                          # REST API (Deployment Tracker)
│   ├── requirements.txt                # Pinned Python dependencies
│   ├── .dockerignore                   # Excludes unnecessary files
│   └── tests/
│       └── test_app.py                 # 12 unit tests (pytest)
│
├── helm/
│   └── deploy-tracker/                 # Custom Helm chart
│       ├── Chart.yaml                  # Chart metadata
│       ├── values.yaml                 # Default values
│       ├── values-dev.yaml             # Dev environment overrides
│       ├── values-staging.yaml         # Staging environment overrides
│       ├── values-prod.yaml            # Production environment overrides
│       └── templates/
│           ├── deployment.yaml         # Pod spec with probes & security
│           ├── service.yaml            # ClusterIP service
│           ├── ingress.yaml            # Nginx ingress routing
│           ├── hpa.yaml                # Horizontal Pod Autoscaler
│           └── networkpolicy.yaml      # Pod network restrictions
│
├── k8s/                                # Raw Kubernetes manifests
│   ├── namespace.yaml                  # Dev namespace
│   ├── deployment.yaml                 # Annotated deployment spec
│   ├── service.yaml                    # Service definition
│   └── ingress.yaml                    # Ingress routing
│
├── .github/workflows/
│   ├── ci.yml                          # CI: lint → test → scan → build → helm lint
│   └── cd-dev.yml                      # CD: build → push → deploy
│
├── docs/
│   ├── PIPELINE-DESIGN.md             # Pipeline stage explanations
│   └── screenshots/                   # Deployment evidence
│
├── BRANCHING-STRATEGY.md              # Git workflow documentation
└── README.md                          # This file
```

---

## 🚀 Deployment Phases

### Phase 1: Application & Unit Tests

**What I built:**
- Python Flask REST API — a Deployment Tracker with health, CRUD, and info endpoints
- 12 unit tests with pytest covering all endpoints and edge cases
- Pinned dependency versions for reproducible builds

#### 🔧 Application Code

```python
@app.route("/health", methods=["GET"])
def health():
    """
    Health check endpoint.
    Kubernetes uses this to determine if the pod is alive and ready.
    If this returns non-200, Kubernetes restarts the pod (liveness)
    or stops sending traffic (readiness).
    """
    return jsonify({
        "status": "healthy",
        "hostname": socket.gethostname(),
        "version": os.getenv("APP_VERSION", "0.1.0"),
        "environment": os.getenv("ENVIRONMENT", "development"),
    })
```

#### 📊 Tests Passing
<img width="956" height="696" alt="01-tests-passing" src="https://github.com/user-attachments/assets/a8b44fb9-32aa-40f0-a130-db25f260187f" />

**Why it matters:**
Unit tests are the first quality gate in the pipeline. If any test fails, the pipeline stops and code cannot be merged. This is called **shift-left testing** — catching bugs as early as possible before they reach production. The health endpoint is particularly critical because Kubernetes probes depend on it for pod lifecycle management.

---

### Phase 2: Docker Containerisation

**What I built:**
- Multi-stage Dockerfile — Stage 1 runs tests, Stage 2 creates a minimal production image
- Non-root user (`appuser`) for container security
- Built-in Docker health check
- Layer caching optimisation (COPY requirements.txt before code)

#### 🔧 Dockerfile (Multi-Stage Build)

```dockerfile
# Stage 1: TEST — Install everything, run tests
FROM python:3.11-slim AS test
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python -m pytest tests/ -v --tb=short

# Stage 2: PRODUCTION — Clean, minimal image
FROM python:3.11-slim AS production
WORKDIR /app
RUN groupadd -r appuser && useradd -r -g appuser appuser
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev .txt
COPY app.py .
USER appuser
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=3s \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
```

I separated the dependencies into requirements.txt and requirements-dev.txt to follow the principle of least privilege. Since tools like pytest are only needed for validation and not for running the API, excluding them from the final production image reduces the container's footprint and improves security by minimizing unnecessary installed packages."

#### 📊 Docker Build with Tests Running Inside
<img width="958" height="499" alt="03-docker-build-success" src="https://github.com/user-attachments/assets/2601f6e4-a011-43e2-a88f-2edde3767ee5" />#### 📊 Container Running as Non-Root User

## whoami output ##

<img width="957" height="97" alt="05-non-root-user" src="https://github.com/user-attachments/assets/d6a3d4de-53ec-474c-88c1-e9e5eae5cf0b" />

## Image Size ## 

<img width="740" height="65" alt="deploy tracker size" src="https://github.com/user-attachments/assets/7f8ee91b-26a8-460b-8997-e6f9c57f6bc0" />


**Why it matters:**
Multi-stage builds serve two purposes: tests run during every build (if tests fail, no image is created), and the production image only contains runtime dependencies — reducing size from ~900MB to ~217MB. Running as a non-root user is a fundamental container security practice. If an attacker exploits the application, they only get non-root access with limited permissions.

---

### Phase 3: Kubernetes Deployment

**What I built:**
- Kubernetes Deployment with rolling update strategy (zero-downtime)
- Liveness and readiness probes on `/health` endpoint
- Resource requests and limits (CPU/memory guardrails per pod)
- Pod security context (`runAsNonRoot: true`)
- ClusterIP Service and Nginx Ingress for traffic routing

#### 🔧 Key Deployment Configuration

```yaml
# Rolling update — zero-downtime deployments
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1         # Create 1 extra pod during update
    maxUnavailable: 0    # Never have fewer than desired replicas

# Liveness probe — "Is the container alive?"
# Failure → Kubernetes RESTARTS the container
livenessProbe:
  httpGet:
    path: /health
    port: 5000
  initialDelaySeconds: 10
  periodSeconds: 15

# Readiness probe — "Is the container ready for traffic?"
# Failure → Kubernetes STOPS sending traffic (no restart)
readinessProbe:
  httpGet:
    path: /health
    port: 5000
  initialDelaySeconds: 5
  periodSeconds: 10

# Resource limits — prevent a single pod consuming all cluster resources
resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 250m
    memory: 256Mi
```

#### 📊 Pods Running in Kubernetes
<img width="706" height="67" alt="06-kubectl-get-pods" src="https://github.com/user-attachments/assets/2bc201ac-c171-4c17-9f62-05a3874b6901" />

#### 📊 All Kubernetes Resources
<img width="722" height="229" alt="07-kubectl-get-all" src="https://github.com/user-attachments/assets/8028138c-fa92-42bd-a64e-695754ff4cd7" />

#### 📊 Application Responding via Kubernetes
<img width="990" height="328" alt="08-app-via-k8s" src="https://github.com/user-attachments/assets/fb6c1be2-53d0-44c5-9cc3-73025e9e78aa" />


**Why it matters:**
The rolling update strategy ensures users never experience downtime during deployments. Kubernetes creates the new pod first, waits for the readiness probe to pass, then terminates the old pod. If the new pod fails its health check, the old pods keep running — the deployment automatically rolls back. Resource limits prevent a single application from consuming all cluster resources, which is critical in shared clusters.

---

### Phase 4: Helm Chart

**What I built:**
- Custom Helm chart with templated Kubernetes resources
- Per-environment values files (dev/staging/prod) with different scaling configs
- Horizontal Pod Autoscaler that scales based on CPU utilisation
- Network Policy to restrict pod-to-pod communication

#### 🔧 Multi-Environment Configuration

```yaml
# values-dev.yaml (lightweight for development)
replicaCount: 1
autoscaling:
  enabled: false
resources:
  requests: { cpu: 50m, memory: 64Mi }

# values-staging.yaml (mirrors production patterns)
replicaCount: 2
autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 4

# values-prod.yaml (full production scale)
replicaCount: 3
autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
```

| Setting | Dev | Staging | Production |
|---------|:---:|:-------:|:----------:|
| Replicas | 1 | 2 | 3 |
| CPU Request | 50m | 100m | 200m |
| Memory Request | 64Mi | 128Mi | 256Mi |
| Auto-Scaling | ❌ Off | ✅ 2–4 pods | ✅ 3–10 pods |
| Target CPU | — | 75% | 70% |

#### 📊 Helm Deployment
<img width="998" height="175" alt="11-helm-install" src="https://github.com/user-attachments/assets/3d7b3c43-a2d4-4eb3-89da-d7871c694cd4" />

## Helm install output  ## 
<img src="https://github.com/user-attachments/assets/abaf497b-85a8-48a4-8352-c05a15a88d7d" width="400" alt="helm install" /> 

## Helm release list  ## 
<img src="https://github.com/user-attachments/assets/0e22f57a-d0a6-483e-82ed-0df454fd76a4" alt="helm list" /> 

**Why it matters:**
Helm solves the problem of managing multiple Kubernetes YAML files across environments. Instead of maintaining near-identical copies for dev/staging/prod, one chart template with different values files keeps everything consistent. The Horizontal Pod Autoscaler responds to real traffic patterns — scaling up during peak load and back down when quiet, optimising both performance and cost.

---

### Phase 5: CI Pipeline (GitHub Actions)

**What I built:**
- 5-stage CI pipeline triggered on every push and pull request
- Lint (flake8) → Unit Tests (pytest) → Security Scan (Trivy) → Docker Build → Helm Lint
- Pipeline fails on any stage failure — preventing broken code from being merged

#### 🔧 Pipeline Configuration

```yaml
jobs:
  lint:           # flake8 code style checks
  test:           # pytest unit tests (12 tests)
  security-scan:  # Trivy CVE scan — fails on CRITICAL/HIGH
  build:          # Docker multi-stage build (needs lint + test to pass first)
  helm-lint:      # Validates Helm chart templates for all environments
```

| Stage | Tool | Purpose | On Failure |
|-------|------|---------|------------|
| Lint | flake8 | Code style & common bugs | ❌ Pipeline stops |
| Test | pytest | 12 unit tests | ❌ Pipeline stops |
| Security Scan | Trivy | CVE scan on dependencies | ❌ Pipeline stops on CRITICAL/HIGH |
| Build Image | Docker | Multi-stage build (tests inside) | ❌ Pipeline stops |
| Helm Lint | Helm | Validate K8s templates | ❌ Pipeline stops |

#### 📊 CI Pipeline — All Stages Passing
<img width="1137" height="615" alt="14-ci-pipeline-green" src="https://github.com/user-attachments/assets/f5e472d6-12b4-43f6-b629-737f205b9391" />

#### 📊 Security Scan Results (Trivy)

<img width="1808" height="835" alt="16-trivy-scan" src="https://github.com/user-attachments/assets/bd86eb26-0e2c-4515-805e-0391e06652f5" />


#### 📊 Pull Request with CI Checks

PR with CI checks" src="https://github.com/user-attachments/assets/532f720b-c998-46d2-9226-226a2311030a" />

**Why it matters:**
The CI pipeline is the backbone of DevOps — it automatically validates every code change before it can be merged. Security scanning (Trivy) catches known vulnerabilities in dependencies, implementing **DevSecOps** by shifting security left into the pipeline rather than treating it as an afterthought. Branch protection rules ensure no code reaches `main` without passing all checks.

---

### Phase 6: CD Pipeline & Docker Hub

**What I built:**
- CD pipeline triggered on merge to `main`
- Builds final Docker image tagged with commit SHA (immutable tags)
- Pushes to Docker Hub container registry
- Deploys to dev environment via Helm

#### 📊 CD Pipeline — Build & Deploy

<!-- SCREENSHOT: GitHub → Actions showing the CD pipeline with build-and-push and deploy jobs -->
<img width="900" alt="CD Pipeline" src="https://github.com/user-attachments/assets/1643e555-53b3-44e6-9c56-bb903663d52c" />

#### 📊 Image Pushed to Docker Hub

<!-- SCREENSHOT: Docker Hub showing the deploy-tracker repository with image tags -->
<img width="700" alt="Docker Hub image" src="https://github.com/user-attachments/assets/2a6bf9d6-06e3-4e69-96fd-6153e85dada9" />

**Why it matters:**
Immutable image tags (using the commit SHA rather than `latest`) ensure every deployment is traceable back to the exact code that produced it. If something breaks in production, you know exactly which commit caused it and can roll back to the previous SHA. The CD pipeline turns a merge to `main` into a deployed application with zero manual steps.

---

---

## 🎯 Deployment Summary

**Pipeline Components:**

| Category | Component | Status |
|:---|:---|:---:|
| **Application** | Flask REST API (5 endpoints) | ✅ |
| | 12 unit tests (pytest) | ✅ |
| **Docker** | Multi-stage Dockerfile | ✅ |
| | Non-root user (appuser) | ✅ |
| | Docker health check | ✅ |
| | Image pushed to Docker Hub | ✅ |
| **Kubernetes** | Deployment with rolling updates | ✅ |
| | Liveness & readiness probes | ✅ |
| | Resource requests & limits | ✅ |
| | ClusterIP Service | ✅ |
| | Nginx Ingress | ✅ |
| | Pod security context | ✅ |
| **Helm** | Custom chart with templates | ✅ |
| | values-dev.yaml | ✅ |
| | values-staging.yaml | ✅ |
| | values-prod.yaml | ✅ |
| | Horizontal Pod Autoscaler | ✅ |
| | Network Policy | ✅ |
| **CI/CD** | CI: lint → test → scan → build → helm lint | ✅ |
| | CD: build → push → deploy | ✅ |
| | Trivy security scanning | ✅ |

---

## ✅ Architecture Validation

**Verified Configurations:**
- Docker multi-stage build runs tests and produces minimal image ✅
- Container runs as non-root user (appuser) ✅
- All 12 unit tests pass in CI pipeline ✅
- Trivy security scan passes with no CRITICAL/HIGH vulnerabilities ✅
- Kubernetes pods reach Running state with health probes passing ✅
- Helm chart deploys successfully with dev, staging, and prod values ✅
- CI pipeline blocks merge on any stage failure ✅
- CD pipeline builds, pushes, and deploys on merge to main ✅

**Entire pipeline managed through GitHub Actions with automated quality gates.**

---

## 📊 Project Metrics

| **Metric** | **Value** | **Insight** |
|-----------|----------|-------------|
| **Pipeline Stages** | 5 (CI) + 3 (CD) | Comprehensive quality gates |
| **Unit Tests** | 12 | Full endpoint coverage |
| **Docker Image Size** | ~150MB | Multi-stage build (vs ~900MB single-stage) |
| **Helm Templates** | 5 | Deployment, Service, Ingress, HPA, NetworkPolicy |
| **Environment Configs** | 3 | Dev, Staging, Production |
| **Security Scans** | Trivy (every build) | DevSecOps integrated |
| **Deployment Cost** | £0 | Runs entirely on local Minikube |
| **Build Time** | ~2 min | Docker build including tests |

## 🎯 What This Project Demonstrates to Employers

1. **Container Expertise:** Multi-stage builds, non-root security, health checks, registry management
2. **Kubernetes Proficiency:** Deployments, probes, HPA, network policies, resource management
3. **Helm Knowledge:** Custom charts, per-environment values, templating
4. **CI/CD Pipeline Design:** Automated quality gates from lint to deploy
5. **DevSecOps Thinking:** Security scanning integrated into the pipeline, not bolted on
6. **Git Best Practices:** PR workflow, conventional commits
7. **Documentation Skills:** Comprehensive, recruiter-friendly README with evidence

---


## 🎯 Key Takeaways

- **Multi-stage Docker builds** catch bugs early and produce minimal, secure images
- **Kubernetes probes** enable zero-downtime deployments and automatic recovery
- **Helm charts** make multi-environment deployments consistent and repeatable
- **CI/CD pipelines** automate quality gates so broken code never reaches production
- **Security scanning** in the pipeline implements DevSecOps from day one
- **Branch protection** enforces team discipline and code quality

---

## 🔮 Future Enhancements

- Replace Minikube with AWS EKS or Azure AKS for cloud-native deployment
- Add Prometheus and Grafana for cluster and application monitoring
- Implement GitOps with ArgoCD for declarative continuous delivery
- Add integration tests and end-to-end tests to the pipeline
- Implement canary or blue/green deployment strategies via Helm
- Add Slack/Teams notifications for deployment status

---

## 📫 Connect With Me

- **LinkedIn:** www.linkedin.com/in/Rabaanee-Ahmed
- **GitHub:** https://github.com/Rabaanee

*Open to DevOps engineering roles and eager to contribute to platform and infrastructure teams.*


























