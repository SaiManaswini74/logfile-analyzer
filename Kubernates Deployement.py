import yaml

def generate_deployment(app_name, image, replicas, container_port):
    """Generate Kubernetes Deployment manifest for the application."""
    deployment = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
            "name": app_name,
            "labels": {
                "app": app_name
            }
        },
        "spec": {
            "replicas": replicas,
            "selector": {
                "matchLabels": {
                    "app": app_name
                }
            },
            "template": {
                "metadata": {
                    "labels": {
                        "app": app_name
                    }
                },
                "spec": {
                    "containers": [
                        {
                            "name": app_name,
                            "image": image,
                            "ports": [
                                {"containerPort": container_port}
                            ]
                        }
                    ]
                }
            }
        }
    }
    return deployment

def generate_service(app_name, service_port, target_port):
    """Generate Kubernetes Service manifest to expose the application."""
    service = {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {
            "name": app_name,
            "labels": {
                "app": app_name
            }
        },
        "spec": {
            "selector": {
                "app": app_name
            },
            "ports": [
                {
                    "protocol": "TCP",
                    "port": service_port,
                    "targetPort": target_port
                }
            ],
            "type": "ClusterIP"  # Use "LoadBalancer" for external exposure
        }
    }
    return service

def main():
    # Configuration for the Wisecow app
    app_name = "wisecow-app"
    image = "wisecow-app:latest"  # Replace with the actual image name in your registry
    replicas = 3
    container_port = 8000
    service_port = 80

    # Generate deployment and service manifests
    deployment_manifest = generate_deployment(app_name, image, replicas, container_port)
    service_manifest = generate_service(app_name, service_port, container_port)

    # Write deployment and service manifests to YAML files
    with open(f"{app_name}_deployment.yaml", "w") as dep_file:
        yaml.dump(deployment_manifest, dep_file)
    with open(f"{app_name}_service.yaml", "w") as svc_file:
        yaml.dump(service_manifest, svc_file)
    
    print(f"Generated Kubernetes manifests: {app_name}_deployment.yaml and {app_name}_service.yaml")

if __name__ == "__main__":
    main()
