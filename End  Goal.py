import os
import yaml

# Define the project structure
project_structure = {
    "wisecow_app": [
        "app.py",
        "Dockerfile",
        "k8s": [
            "deployment.yaml",
            "service.yaml",
            "ingress.yaml"
        ],
        ".github": [
            "workflows/ci-cd.yml"
        ],
        "README.md"
    ]
}

# Application source code (Flask app)
app_code = """\
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify(message="Welcome to the secure Wisecow App!")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
"""

# Dockerfile content
dockerfile_content = """\
FROM python:3.9-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir flask
EXPOSE 8000
CMD ["python", "app.py"]
"""

# Kubernetes Deployment YAML
deployment_yaml = {
    "apiVersion": "apps/v1",
    "kind": "Deployment",
    "metadata": {"name": "wisecow-app", "labels": {"app": "wisecow"}},
    "spec": {
        "replicas": 3,
        "selector": {"matchLabels": {"app": "wisecow"}},
        "template": {
            "metadata": {"labels": {"app": "wisecow"}},
            "spec": {
                "containers": [{
                    "name": "wisecow-app",
                    "image": "wisecow-app:latest",
                    "ports": [{"containerPort": 8000}]
                }]
            }
        }
    }
}

# Kubernetes Service YAML
service_yaml = {
    "apiVersion": "v1",
    "kind": "Service",
    "metadata": {"name": "wisecow-service"},
    "spec": {
        "selector": {"app": "wisecow"},
        "ports": [{"protocol": "TCP", "port": 80, "targetPort": 8000}],
        "type": "ClusterIP"
    }
}

# Kubernetes Ingress YAML for TLS
ingress_yaml = {
    "apiVersion": "networking.k8s.io/v1",
    "kind": "Ingress",
    "metadata": {
        "name": "wisecow-ingress",
        "annotations": {
            "kubernetes.io/ingress.class": "nginx",
            "cert-manager.io/cluster-issuer": "letsencrypt-prod"  # Replace with your cluster issuer
        }
    },
    "spec": {
        "tls": [{"hosts": ["wisecow.example.com"], "secretName": "wisecow-tls"}],  # Replace domain with actual
        "rules": [{
            "host": "wisecow.example.com",
            "http": {
                "paths": [{
                    "path": "/",
                    "pathType": "Prefix",
                    "backend": {
                        "service": {"name": "wisecow-service", "port": {"number": 80}}
                    }
                }]
            }
        }]
    }
}

# GitHub Actions CI/CD workflow
ci_cd_workflow = {
    "name": "CI/CD Pipeline",
    "on": {"push": {"branches": ["main"]}},
    "jobs": {
        "build-and-push": {
            "runs-on": "ubuntu-latest",
            "steps": [
                {"name": "Checkout code", "uses": "actions/checkout@v2"},
                {"name": "Log in to Docker Hub", "uses": "docker/login-action@v2",
                 "with": {"username": "${{ secrets.DOCKER_USERNAME }}", "password": "${{ secrets.DOCKER_PASSWORD }}"}},
                {"name": "Build Docker image", "run": "docker build -t wisecow-app:latest ."},
                {"name": "Push Docker image", "run": "docker push wisecow-app:latest"}
            ]
        },
        "deploy": {
            "runs-on": "ubuntu-latest",
            "needs": "build-and-push",
            "steps": [
                {"name": "Checkout code", "uses": "actions/checkout@v2"},
                {"name": "Set up kubectl", "uses": "azure/setup-kubectl@v3", "with": {"version": "latest"}},
                {"name": "Deploy to Kubernetes", "env": {"KUBECONFIG": "${{ secrets.KUBECONFIG }}"},
                 "run": "kubectl apply -f k8s/"}
            ]
        }
    }
}

# README content
readme_content = """\
# Wisecow Application

## Overview
This repository contains the Wisecow application with Docker, Kubernetes, and CI/CD setup. It includes:
- A Dockerfile for containerizing the application
- Kubernetes manifests for deployment, service, and TLS-secured ingress
- GitHub Actions CI/CD pipeline configuration
"""

# Function to create directory structure and add content
def create_project_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, list):
            os.makedirs(path, exist_ok=True)
            for subcontent in content:
                subpath = os.path.join(path, subcontent)
                if isinstance(subcontent, dict):
                    create_project_structure(path, subcontent)
                else:
                    with open(subpath, "w") as f:
                        if subcontent == "app.py":
                            f.write(app_code)
                        elif subcontent == "Dockerfile":
                            f.write(dockerfile_content)
                        elif subcontent == "README.md":
                            f.write(readme_content)
                        elif subcontent == "deployment.yaml":
                            yaml.dump(deployment_yaml, f)
                        elif subcontent == "service.yaml":
                            yaml.dump(service_yaml, f)
                        elif subcontent == "ingress.yaml":
                            yaml.dump(ingress_yaml, f)
                        elif subcontent == "ci-cd.yml":
                            yaml.dump(ci_cd_workflow, f)
        else:
            with open(path, "w") as f:
                f.write(content)

# Create project structure
create_project_structure(".", project_structure)

print("Project structure created. You can now initialize a Git repository and push to GitHub.")
