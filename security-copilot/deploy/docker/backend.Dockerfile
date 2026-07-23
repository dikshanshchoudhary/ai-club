FROM python:3.12-slim
ARG TARGETARCH
ARG TRIVY_VERSION=0.72.0
ARG GITLEAKS_VERSION=8.30.1
WORKDIR /app
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl git gzip tar \
    && rm -rf /var/lib/apt/lists/*
RUN python -m pip install --no-cache-dir semgrep checkov \
    && case "${TARGETARCH:-amd64}" in \
         amd64) TRIVY_ARCH="64bit"; GITLEAKS_ARCH="x64" ;; \
         arm64) TRIVY_ARCH="ARM64"; GITLEAKS_ARCH="arm64" ;; \
         *) echo "Unsupported architecture: ${TARGETARCH}"; exit 1 ;; \
       esac \
    && curl -fsSL "https://github.com/aquasecurity/trivy/releases/download/v${TRIVY_VERSION}/trivy_${TRIVY_VERSION}_Linux-${TRIVY_ARCH}.tar.gz" -o /tmp/trivy.tar.gz \
    && tar -xzf /tmp/trivy.tar.gz -C /usr/local/bin trivy \
    && curl -fsSL "https://github.com/gitleaks/gitleaks/releases/download/v${GITLEAKS_VERSION}/gitleaks_${GITLEAKS_VERSION}_linux_${GITLEAKS_ARCH}.tar.gz" -o /tmp/gitleaks.tar.gz \
    && tar -xzf /tmp/gitleaks.tar.gz -C /usr/local/bin gitleaks \
    && chmod +x /usr/local/bin/trivy /usr/local/bin/gitleaks \
    && rm -f /tmp/trivy.tar.gz /tmp/gitleaks.tar.gz \
    && semgrep --version \
    && checkov --version \
    && trivy --version \
    && gitleaks version
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
