# Challenges and Troubleshooting Record

This document records technical challenges encountered while developing and implementing the DevOps portfolio CI/CD project.

## 1. Python test discovery

**Problem:** Running `pytest -v` resulted in `ModuleNotFoundError: No module named 'app'`, although the application module could be imported using Python.

**Resolution:** I changed the command to `python -m pytest -v`. This executed pytest through the active Python environment and resolved the module discovery issue.

**Outcome:** All three application tests passed.

**Evidence:** Successful test execution in the project development workflow.

## 2. Static code analysis

**Problem:** The first Ruff check identified an import-ordering issue in `app/__init__.py`.

**Resolution:** I ran `ruff check . --fix` to correct the import ordering, then repeated `ruff check .`.

**Outcome:** Ruff reported that all checks passed.

**Learning:** Functional tests alone do not identify every maintainability or code-style issue. Static analysis provides an additional quality check.

## 3. Requirements file encoding

**Problem:** Git initially identified `requirements.txt` as a binary file after it was generated using PowerShell redirection.

**Cause:** The file had been written using UTF-16 encoding.

**Resolution:** I rewrote the file using UTF-8 encoding without a byte-order mark.

**Outcome:** Git subsequently displayed the file as normal text and showed its individual lines in the diff.

**Learning:** File encoding can affect version-control review and collaboration.

## 4. Docker image vulnerabilities

**Problem:** The initial Docker image scan identified High-severity vulnerabilities in the operating-system and Python package components.

**Resolution:** I updated the operating-system packages during the Docker build. Further investigation identified pip and its bundled dependencies among the remaining findings. I removed pip and its vendored packages from the final runtime image after installing the application requirements.

**Outcome:** The final image scan reported no High or Critical vulnerabilities under the configured Trivy scan settings.

**Learning:** A successful Docker build does not automatically mean that an image is secure. Scanning and remediation need to be part of the build process.

## 5. Docker build in GitHub Actions

**Problem:** The initial CI workflow could not complete its Docker build because the Dockerfile was not yet available in the GitHub repository.

**Resolution:** I added the Dockerfile to version control and pushed the updated project.

**Outcome:** The subsequent GitHub Actions run completed the Docker build and image security scan successfully.

**Learning:** The CI environment can only build from files available in the checked-out repository.

## 6. Minikube Kubernetes context

**Problem:** Minikube initially had a stale Kubernetes context, preventing normal cluster interaction.

**Resolution:** I ran `minikube update-context` and restarted Minikube with the Docker driver.

**Outcome:** The cluster became available, the node reached Ready status, and the portfolio deployment ran successfully.

## 7. Kubernetes resource monitoring

**Problem:** The commands `kubectl top nodes` and `kubectl top pods` initially returned `Metrics API not available`.

**Resolution:** I enabled the Minikube Metrics Server addon and waited for its deployment to become ready.

**Outcome:** Kubernetes resource usage became available, including CPU and memory measurements for the node and application pods.

**Learning:** Kubernetes resource monitoring requires a functioning metrics provider; the commands alone do not provide metrics.

## 8. Separation of hosted CI and local deployment

**Challenge:** GitHub-hosted Actions runners cannot directly access the Minikube cluster running on my local computer.

**Decision:** I used GitHub Actions for automated testing, static analysis, security scanning and Docker image building. I then loaded the built image into Minikube and deployed it locally.

**Outcome:** This provided a working CI pipeline and local Kubernetes deployment without requiring a paid cloud environment.

**Limitation:** Deployment to Minikube is not automatically triggered by the hosted GitHub Actions workflow.

**Possible improvement:** A self-hosted runner or a remotely accessible Kubernetes environment could be introduced to automate the deployment stage.

## Overall reflection

These challenges demonstrated that implementing a DevOps pipeline involves more than writing application code. Environment configuration, file encoding, security remediation, containerisation, cluster management and monitoring all require troubleshooting. Resolving these issues improved my understanding of how individual DevOps tools work together and why automation, repeatability and verification are important.
