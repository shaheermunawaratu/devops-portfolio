# DevOps Portfolio – CI/CD Pipeline

**Author:** Shaheer Munawar  
**Programme:** MSc Computing in DevOps – Atlantic Technological University  
**Repository:** https://github.com/shaheermunawaratu/devops-portfolio

## 1. Project Overview

This project demonstrates the design and implementation of a small CI/CD pipeline for a Flask-based developer portfolio website.

The project combines source control, automated testing, static code analysis, vulnerability scanning, Docker containerisation, local Kubernetes deployment and application monitoring.

The objective is to demonstrate how DevOps practices can improve software quality, consistency, security and operational visibility.

## 2. Application Features

The portfolio website includes:

- Home and personal introduction
- About and education
- Technical skills
- Projects
- Professional experience
- Contact section
- Application health endpoint
- Prometheus metrics endpoint

The application uses Python Flask for the backend and HTML, CSS and JavaScript for the frontend.

### Application endpoints

| Endpoint | Purpose |
|---|---|
| `/` | Portfolio homepage |
| `/health` | Application health check |
| `/metrics` | Prometheus metrics |

## 3. Technology Stack

| Area | Technology |
|---|---|
| Source control | Git and GitHub |
| CI automation | GitHub Actions |
| Backend | Python and Flask |
| Frontend | HTML, CSS and JavaScript |
| Automated testing | Pytest |
| Static analysis | Ruff |
| Security scanning | Trivy |
| Containerisation | Docker |
| Container orchestration | Kubernetes and Minikube |
| Metrics collection | Prometheus |
| Monitoring dashboards | Grafana |

## 4. CI/CD Architecture

The workflow follows this process:

1. Source code is maintained in GitHub.
2. A push to the `main` branch or a pull request triggers GitHub Actions.
3. Dependencies are installed.
4. Trivy scans the project filesystem for vulnerabilities.
5. Ruff performs static code analysis.
6. Pytest executes the automated application tests.
7. Docker builds the application image.
8. Trivy scans the resulting Docker image.
9. The developer loads the image into local Minikube and deploys the Kubernetes resources.
10. Prometheus collects application metrics, which are visualised in Grafana.

**Deployment note:** GitHub-hosted Actions runners cannot directly access the Minikube cluster running on the developer's local computer. Therefore, CI is automated through GitHub Actions, while the demonstrated local Kubernetes deployment is performed separately.

## 5. Project Structure

```text
devops-portfolio/
├── app/
│   ├── __init__.py
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── script.js
├── tests/
│   └── test_app.py
├── kubernetes/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── prometheus-config.yaml
│   ├── prometheus.yaml
│   └── grafana.yaml
├── monitoring/
├── evidence/
├── .github/
│   └── workflows/
│       └── ci.yml
├── .gitignore
├── Dockerfile
├── requirements.txt
├── run.py
└── README.md
```

## 6. Running the Application Locally

### Prerequisites

- Python 3.13
- Git

Clone the repository:

```bash
git clone https://github.com/shaheermunawaratu/devops-portfolio.git
cd devops-portfolio
```

Create and activate a virtual environment on Windows PowerShell:

```powershell
py -3.13 -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Start the application:

```powershell
python run.py
```

Open the application at:

`http://127.0.0.1:5000`

Test the health endpoint:

`http://127.0.0.1:5000/health`

## 7. Automated Testing and Code Quality

Run the automated tests:

```powershell
python -m pytest -v
```

Run static analysis:

```powershell
ruff check .
```

The project includes tests for the homepage, health endpoint and Prometheus metrics endpoint.

## 8. Docker Containerisation

Build the Docker image:

```powershell
docker build -t shaheer-devops-portfolio:v3 .
```

Run the container:

```powershell
docker run -d --name shaheer-portfolio -p 5000:5000 shaheer-devops-portfolio:v3
```

Check the running container:

```powershell
docker ps
```

Test its health endpoint:

`http://localhost:5000/health`

To stop and remove the container:

```powershell
docker stop shaheer-portfolio
docker rm shaheer-portfolio
```

## 9. Security Scanning

Trivy is integrated into GitHub Actions to perform:

- Filesystem vulnerability scanning
- Docker image vulnerability scanning

The workflow checks for High and Critical severity vulnerabilities and ignores unfixed findings.

The Docker image was also reviewed and improved following the initial scan findings. The final scan reported no High or Critical vulnerabilities under the configured scan settings.

Security scanning is not a guarantee that an application is completely secure; it provides an additional automated check against known vulnerabilities.

## 10. Kubernetes Deployment

### Prerequisites

- Docker Desktop
- Minikube
- kubectl

Start the local Kubernetes cluster:

```powershell
minikube start --driver=docker --cpus=2 --memory=2048
```

Load the Docker image into Minikube:

```powershell
minikube image load shaheer-devops-portfolio:v3
```

Apply the application deployment and service:

```powershell
kubectl apply -f .\kubernetes\deployment.yaml
kubectl apply -f .\kubernetes\service.yaml
```

Check the deployment:

```powershell
kubectl rollout status deployment/portfolio
kubectl get pods
kubectl get services
```

Access the application:

```powershell
kubectl port-forward service/portfolio-service 8080:80
```

Open:

`http://127.0.0.1:8080`

The Kubernetes deployment includes readiness and liveness probes using the application's `/health` endpoint, together with CPU and memory resource requests and limits.

## 11. Prometheus Monitoring

Deploy Prometheus:

```powershell
kubectl apply -f .\kubernetes\prometheus-config.yaml
kubectl apply -f .\kubernetes\prometheus.yaml
kubectl rollout status deployment/prometheus
```

Access the Prometheus interface:

```powershell
kubectl port-forward service/prometheus 9090:9090
```

Open:

`http://127.0.0.1:9090`

Example Prometheus queries:

```promql
up{job="portfolio"}
```

```promql
portfolio_http_requests_total
```

```promql
sum(rate(portfolio_http_requests_total[5m]))
```

The application exposes request counters, allowing Prometheus to collect information about HTTP requests.

## 12. Grafana Monitoring Dashboard

Grafana uses Prometheus as its data source.

Before deploying Grafana, create the Kubernetes Secret containing the administrator credentials:

```powershell
$SecurePassword = Read-Host "Enter a Grafana password" -AsSecureString
$BSTR = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($SecurePassword)
$PlainPassword = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($BSTR)

kubectl create secret generic grafana-admin `
  --from-literal=admin-user=admin `
  --from-literal=admin-password="$PlainPassword"

[Runtime.InteropServices.Marshal]::ZeroFreeBSTR($BSTR)
Remove-Variable SecurePassword, BSTR, PlainPassword
```

Deploy Grafana:

```powershell
kubectl apply -f .\kubernetes\grafana.yaml
kubectl rollout status deployment/grafana
```

Access Grafana:

```powershell
kubectl port-forward service/grafana 3000:3000
```

Open:

`http://127.0.0.1:3000`

Sign in using the administrator credentials created above.

The project dashboard includes application request metrics, application availability and HTTP request rate.

## 13. Kubernetes Resource Monitoring and Logs

Enable the Minikube Metrics Server addon:

```powershell
minikube addons enable metrics-server
```

View node resource usage:

```powershell
kubectl top nodes
```

View pod resource usage:

```powershell
kubectl top pods
```

View application logs:

```powershell
kubectl logs deployment/portfolio --tail=30
```

## 14. Evidence

The `evidence` directory contains screenshots and documentation demonstrating the project implementation, including:

- Git history and repository configuration
- Successful GitHub Actions pipeline executions
- Automated testing and code quality checks
- Trivy security scanning
- Docker image build and container execution
- Kubernetes deployment and pod status
- Prometheus metrics and target availability
- Grafana monitoring dashboards
- Kubernetes resource usage and application logs
- Technical challenges and troubleshooting

## 15. Limitations and Future Improvements

The project uses a local single-node Minikube cluster rather than a production cloud Kubernetes environment. Kubernetes deployment is performed manually after the hosted CI workflow completes.

Potential improvements include:

- Automating deployment through a self-hosted runner or remote Kubernetes cluster.
- Publishing versioned Docker images to a container registry.
- Adding persistent storage for Prometheus and Grafana.
- Provisioning Grafana dashboards as code.
- Expanding automated test coverage.
- Introducing more comprehensive application security and integration tests.
- Adding centralised log aggregation.

## 16. Conclusion

This project demonstrates the practical integration of source control, automated CI checks, security scanning, Docker, Kubernetes and monitoring.

It provides a working example of how DevOps tools can support a repeatable software development and deployment workflow while highlighting areas for further improvement.
