# 🎬 Movie Journal

> **End-to-End DevOps Project** featuring Flask, Docker, Kubernetes (K3s), Jenkins, Terraform, Ansible, Prometheus, Grafana, & AWS.

---

## 📌 Overview

**Movie Journal** is a full-stack web application that allows movie enthusiasts to catalogue their favorite films, manage custom posters, track memorable scenes, and write detailed reviews. 

While the application itself is feature-rich, **the primary objective of this repository is to demonstrate a production-grade, automated CI/CD and Infrastructure-as-Code (IaC) workflow**—from bare-metal AWS provisioning to zero-downtime Kubernetes deployments.

---

## 🚀 Features

- **Film Management:** Add, review, and delete movies with custom ratings.
- **Rich Media Storage:** Upload custom poster art, backdrop imagery, and memorable scene snapshots.
- **Interactive UI:** Responsive, dark-themed interface built for fast browsing.
- **Relational Backend:** Powered by PostgreSQL and SQLAlchemy for reliable data persistence.

---

## 🛠️ Tech Stack & Tools

| Domain | Technologies |
| :--- | :--- |
| **Application** | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white) ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71100?style=flat-square&logo=sqlalchemy&logoColor=white) |
| **DevOps & CI/CD** | ![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white) ![Kubernetes](https://img.shields.io/badge/K3s-326CE5?style=flat-square&logo=kubernetes&logoColor=white) ![Jenkins](https://img.shields.io/badge/Jenkins-D24939?style=flat-square&logo=jenkins&logoColor=white) |
| **Infrastructure** | ![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=flat-square&logo=terraform&logoColor=white) ![Ansible](https://img.shields.io/badge/Ansible-EE0000?style=flat-square&logo=ansible&logoColor=white) ![AWS](https://img.shields.io/badge/AWS_EC2-FF9900?style=flat-square&logo=amazon-aws&logoColor=white) |
| **Observability** | ![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=flat-square&logo=prometheus&logoColor=white) ![Grafana](https://img.shields.io/badge/Grafana-F46800?style=flat-square&logo=grafana&logoColor=white) |

---

## 🏗️ Architecture & Pipeline Flow

```mermaid
graph TD
    A[Developer Git Push] -->|GitHub Webhook| B[Jenkins EC2 Instance]
    B -->|Build Image| C[Docker Engine]
    C -->|Push Image| D[Docker Hub Registry]
    B -->|SSH Trigger| E[K3s Cluster EC2]
    E -->|kubectl set image| F[Kubernetes Deployment]
    F --> G[Flask Application Pods]
    G <--> H[(PostgreSQL Database)]
```

### CI/CD Deployment Stages

```
Git Push ➔ GitHub Webhook ➔ Jenkins Build ➔ Docker Push ➔ SSH to Cluster ➔ Rolling K8s Update
```

---

## 📁 Project Structure

```text
movies/
├── 📁 ansible/        # Configuration management playbooks
├── 📁 kubernetes/     # Manifests (Deployments, Services, Ingress, Secrets)
├── 📁 monitoring/     # Prometheus & Grafana Helm values
├── 📁 static/         # Frontend CSS, JS, and image uploads
├── 📁 templates/      # Jinja2 HTML templates
├── 📁 terraform/      # AWS Infrastructure provisioning (VPC, EC2, SG)
├── Dockerfile         # App containerization specification
├── Jenkinsfile        # CI/CD pipeline definitions
├── movies.py          # Main Flask application entrypoint
├── seed_movies.py    # Database seeding utility
└── requirements.txt   # Python dependencies
```

---

## ☸️ Kubernetes Infrastructure

The cluster is managed via K3s and utilizes the following native Kubernetes resources:

- **Namespace:** Isolated environment for application resources.
- **Deployments:** Scalable web application and PostgreSQL instances.
- **Services:** Internal ClusterIP communication channels.
- **ConfigMap & Secret:** Safe separation of application configs and environment variables.
- **Ingress:** HTTP routing and external access management.

---

## 📊 Observability & Monitoring

The observability suite is deployed via **Helm**:
- **Prometheus:** Metrics scraping using `prometheus_flask_exporter`.
- **Grafana:** Visual dashboards tracking HTTP requests, latency, memory usage, and cluster health.

---

## ⚡ Deployment & Setup Guide

<details>
<summary><b>Step 1: Provision Cloud Infrastructure (Terraform)</b></summary>

```bash
git clone https://github.com/your-username/movie-journal.git
cd movie-journal/terraform

# Initialize and create AWS VPC, Security Groups, and EC2 instances
terraform init
terraform apply
```
</details>

<details>
<summary><b>Step 2: Configure Server Instances (Ansible)</b></summary>

Update the `ansible/inventory` file with your target server IP addresses:

```bash
cd ../ansible

# Install Jenkins on the CI/CD server
ansible-playbook -i inventory jenkins.yml

# Provision Docker & K3s on the target application node
ansible-playbook -i inventory movies.yml
```
</details>

<details>
<summary><b>Step 3: Setup Jenkins CI/CD Pipeline</b></summary>

1. Access Jenkins via `http://<JENKINS_PUBLIC_IP>:8080`.
2. Configure Credentials:
   - `movie-docker-token-id`: Docker Hub credentials.
   - `movie-ec2-key`: Private SSH key for the K3s server.
3. Create a **Pipeline Job** pointing to the repository's `Jenkinsfile`.
4. Register the Webhook in GitHub Settings:
   `http://<JENKINS_PUBLIC_IP>:8080/github-webhook/`
</details>

<details>
<summary><b>Step 4: Trigger Automated Build</b></summary>

```bash
git add .
git commit -m "feat: trigger deployment pipeline"
git push origin main
```
</details>
