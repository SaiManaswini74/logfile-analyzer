import os
import yaml

def generate_github_actions_workflow(docker_image, registry_user, registry_password_secret, k8s_deployment, k8s_namespace="default"):
    """Generates a GitHub Actions workflow for CI/CD."""
    workflow = {
        "name": "CI/CD Pipeline",
        "on": {
            "push": {
                "branches": ["main"]
            }
        },
        "jobs": {
            "build-and-push": {
                "runs-on": "ubuntu-latest",
                "steps": [
                    {
                        "name": "Checkout code",
                        "uses": "actions/checkout@v2"
                    },
                    {
                        "name": "Log in to Docker Hub",
                        "uses": "docker/login-action@v2",
                        "with": {
                            "username": registry_user,
                            "password": f"${{{{ secrets.{registry_password_secret} }}}}"
                        }
                    },
                    {
                        "name": "Build and tag Docker image",
                        "run": f"docker build -t {docker_image}:latest ."
                    },
                    {
                        "name": "Push Docker image to registry",
                        "run": f"docker push {docker_image}:latest"
                    }
                ]
            },
            "deploy-to-k8s": {
                "runs-on": "ubuntu-latest",
                "needs": "build-and-push",
                "steps": [
                    {
                        "name": "Checkout code",
                        "uses": "actions/checkout@v2"
                    },
                    {
                        "name": "Set up kubectl",
                        "uses": "azure/setup-kubectl@v3",
                        "with": {
                            "version": "latest"
                        }
                    },
                    {
                        "name": "Deploy to Kubernetes",
                        "env": {
                            "KUBECONFIG": "${{ secrets.KUBECONFIG }}"
                        },
                        "run": f"kubectl set image deployment/{k8s_deployment} {k8s_deployment}={docker_image}:latest -n {k8s_namespace}"
                    }
                ]
            }
        }
    }
    return workflow

def save_workflow_file(workflow, filename=".github/workflows/ci-cd.yml"):
    """Save the workflow to a YAML file."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as file:
        yaml.dump(workflow, file)
    print(f"Workflow saved to {filename}")

def main():
    # Configuration for the workflow
    docker_image = "your-docker-registry/wisecow-app"
    registry_user = "DOCKER_USERNAME"
    registry_password_secret = "DOCKER_PASSWORD"  # This should be a GitHub secret name
    k8s_deployment = "wisecow-deployment"
    k8s_namespace = "default"  # Adjust if necessary

    # Generate and save the GitHub Actions workflow
    workflow = generate_github_actions_workflow(docker_image, registry_user, registry_password_secret, k8s_deployment, k8s_namespace)
    save_workflow_file(workflow)

if __name__ == "__main__":
    main()
