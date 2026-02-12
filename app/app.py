"""
Deployment Tracker API
A simple REST API that tracks software deployments.
Built to demonstrate containerisation, Kubernetes deployment, and CI/CD pipelines.
"""

from flask import Flask, jsonify, request
import os
import datetime
import socket

app = Flask(__name__)

# In-memory store — in production this would be a database
# For this project, in-memory is fine because the focus is on
# the infrastructure and pipeline, not the data persistence
deployments = []


@app.route("/health", methods=["GET"])
def health():
    """
    Health check endpoint.

    WHY THIS EXISTS:
    Kubernetes uses this to determine if your pod is alive and ready
    to receive traffic. If this returns non-200, Kubernetes will:
    - Liveness probe failure: restart the pod
    - Readiness probe failure: stop sending traffic to this pod

    This is a CRITICAL concept in Kubernetes — every production app needs this.
    """
    return jsonify(
        {
            "status": "healthy",
            "hostname": socket.gethostname(),  # Shows which pod responded
            "version": os.getenv("APP_VERSION", "0.1.0"),
            "environment": os.getenv("ENVIRONMENT", "development"),
            "timestamp": datetime.datetime.utcnow().isoformat(),
        }
    )


@app.route("/api/deployments", methods=["GET"])
def get_deployments():
    """List all recorded deployments."""
    return jsonify({"count": len(deployments), "deployments": deployments})


@app.route("/api/deployments", methods=["POST"])
def create_deployment():
    """
    Record a new deployment.

    Example request body:
    {
        "service": "web-frontend",
        "version": "2.1.0",
        "environment": "production",
        "deployed_by": "github-actions"
    }
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    deployment = {
        "id": len(deployments) + 1,
        "service": data.get("service", "unknown"),
        "version": data.get("version", "0.0.0"),
        "environment": data.get("environment", "dev"),
        "deployed_by": data.get("deployed_by", "manual"),
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "status": "success",
    }

    deployments.append(deployment)
    return jsonify(deployment), 201


@app.route("/api/info", methods=["GET"])
def info():
    """Application metadata — useful for debugging which version is running where."""
    return jsonify(
        {
            "app": "deployment-tracker",
            "version": os.getenv("APP_VERSION", "0.1.0"),
            "environment": os.getenv("ENVIRONMENT", "development"),
            "hostname": socket.gethostname(),
        }
    )


@app.route("/", methods=["GET"])
def root():
    """Root endpoint — simple landing page."""
    return jsonify(
        {
            "message": "Deployment Tracker API",
            "endpoints": {
                "health": "/health",
                "list_deployments": "GET /api/deployments",
                "create_deployment": "POST /api/deployments",
                "app_info": "/api/info",
            },
        }
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
