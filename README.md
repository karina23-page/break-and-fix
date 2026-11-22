# 🧪 DevOps Troubleshooting Lab

> A hands-on DevOps project focused on intentionally breaking, diagnosing, and fixing infrastructure and CI/CD issues in a Kubernetes-based application environment.

## 🎯 Project Overview

This project uses a Movie Journal web application as a testing environment for practicing real-world DevOps troubleshooting.

The infrastructure is deployed using Terraform and Ansible on AWS. The application runs in Docker containers on Kubernetes (K3s), with Jenkins handling CI/CD and Prometheus and Grafana providing monitoring.

The main goal is to understand how infrastructure and application failures occur, identify their root causes, implement fixes, and verify that the system is working correctly.

**This is an intentionally break-and-fix project.** Failures are introduced deliberately to practice systematic troubleshooting.
## 🏗️ Architecture

The project includes the following components:

- **AWS EC2:** Hosts the application infrastructure and Jenkins.
- **Terraform:** Provisions AWS resources.
- **Ansible:** Configures the servers.
- **Docker:** Builds and packages the application.
- **Jenkins:** Automates the CI/CD pipeline.
- **Kubernetes (K3s):** Runs the application and PostgreSQL database.
- **Prometheus & Grafana:** Provide metrics collection and monitoring.

### CI/CD Workflow

GitHub Push → GitHub Webhook → Jenkins → Docker Build → Docker Hub → Kubernetes Deployment

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| Cloud | AWS EC2, VPC, Security Groups, S3 |
| Infrastructure as Code | Terraform |
| Configuration Management | Ansible |
| CI/CD | Jenkins, GitHub |
| Containers | Docker, Docker Hub |
| Orchestration | Kubernetes (K3s) |
| Application | Python, Flask, PostgreSQL |
| Monitoring | Prometheus, Grafana |

## 🚀 Deployment & Setup

<details>
<summary><b>Step 1: Clone the Repository</b></summary>

```bash
git clone https://github.com/karina23-page/movie-journal
cd movie-journal
```

</details>

<details>
<summary><b>Step 2: Create AWS Resources</b></summary>

Create an S3 bucket for Terraform remote state.

```bash
aws s3 mb s3://my-movie-tfstate-bucket --region eu-north-1
```

Make sure the bucket name matches the one configured in:

```text
terraform/backend.tf
```

Example:

```hcl
terraform {
  backend "s3" {
    bucket = "my-movie-tfstate-bucket"
    key    = "movie-app/terraform.tfstate"
    region = "eu-north-1"
  }
}
```

> **Important:** The S3 bucket must exist before running `terraform init`.

</details>

<details>
<summary><b>Step 3: Create SSH Key and Docker Hub Token</b></summary>

Before provisioning and configuring the servers, make sure you have:

### SSH Key

Create an SSH key for accessing the EC2 instances and save it as:

```text
~/.ssh/movies
```

The corresponding public key should be used when creating the EC2 instances.

### Docker Hub Token

Create a Docker Hub access token that Jenkins will use to authenticate with Docker Hub.

You will add this token to Jenkins in a later step.

</details>

<details>
<summary><b>Step 4: Provision AWS Infrastructure (Terraform)</b></summary>

Go to the Terraform directory:

```bash
cd terraform
```

Initialize Terraform:

```bash
terraform init
```

Create the infrastructure:

```bash
terraform plan
terraform apply
```

Terraform provisions the required AWS infrastructure, including:

- VPC and networking
- Security Groups
- Jenkins EC2 instance
- Movie application EC2 instance

After Terraform finishes, note the public IP addresses from the Terraform outputs.

</details>

<details>
<summary><b>Step 5: Update the Ansible Inventory</b></summary>

After Terraform creates the EC2 instances, update:

```text
ansible/inventory.txt
```

with the public IP addresses of the newly created servers.

The inventory should also specify the SSH user and private key:

```ini
[movies]
13.51.139.216 ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/movies

[jenkins]
56.228.39.83 ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/movies
```

Replace the IP addresses with the actual public IP addresses returned by Terraform.

> **Important:** If the EC2 instances are recreated and receive new IP addresses, update `inventory.txt` before running the Ansible playbooks.

</details>

<details>
<summary><b>Step 6: Configure Server Instances (Ansible)</b></summary>

From the Ansible directory:

```bash
cd ../ansible
```

Install and configure Jenkins:

```bash
ansible-playbook -i templates/inventory.txt jenkins.yml
```

Provision Docker and K3s on the movie application server:

```bash
ansible-playbook -i templates/inventory.txt movies.yml
```

</details>

<details>
<summary><b>Step 7: Update IP Address in the Jenkinsfile</b></summary>

Open:

```text
Jenkinsfile
```

Update the hardcoded `SERVER_IP` with the **public IP address of the movie application server** created by Terraform.

For example:

```groovy
environment {
    SERVER_IP = '13.51.139.216'
}
```

Replace `13.51.139.216` with your actual movie server IP address.

</details>

<details>
<summary><b>Step 8: Configure Jenkins Plugins</b></summary>

Open Jenkins:

```text
http://<JENKINS_PUBLIC_IP>:8080
```

Install the plugins required by the pipeline, including:

- **Git**
- **GitHub**
- **Credentials Binding**
- **SSH Agent**
- **Pipeline**
- **Docker Pipeline**
- **Kubernetes CLI** if required by the Jenkinsfile

</details>

<details>
<summary><b>Step 9: Add Jenkins Credentials</b></summary>

Go to:

```text
Jenkins → Manage Jenkins → Credentials
```

Add the credentials created earlier:

### Docker Hub

```text
ID: movie-docker-token-id
```

Use your Docker Hub username and access token.

### SSH Key

```text
ID: movie-ec2-key
```

Add the private SSH key used to access the movie application server.

> **Important:** The credential IDs must match the IDs referenced in the `Jenkinsfile`.

</details>

<details>
<summary><b>Step 10: Configure Jenkins Pipeline</b></summary>

Create a new Jenkins Pipeline job:

```text
New Item → Pipeline
```

Select:

```text
Definition:
Pipeline script from SCM

SCM:
Git

Repository:
https://github.com/your_username/movie-journal

Script Path:
Jenkinsfile
```

Enable:

```text
GitHub hook trigger for GITScm polling
```

</details>

<details>
<summary><b>Step 11: Configure the GitHub Webhook</b></summary>

Open:

```text
GitHub Repository → Settings → Webhooks
```

Add:

```text
http://<JENKINS_PUBLIC_IP>:8080/github-webhook/
```

Replace `<JENKINS_PUBLIC_IP>` with the public IP address of the Jenkins server.

Set the content type to:

```text
application/json
```

Select:

```text
Just the push event
```

</details>

<details>
<summary><b>Step 12: Trigger the Automated Deployment</b></summary>

Make a change to the repository and push it to GitHub:

```bash
git add .
git commit -m "feat: trigger deployment pipeline"
git push origin main
```

The GitHub webhook triggers Jenkins.

The pipeline then:

1. Pulls the latest source code.
2. Builds the Docker image.
3. Pushes the image to Docker Hub.
4. Connects to the K3s server.
5. Updates the Kubernetes deployment.
6. Waits for the rollout to complete.

Monitor the deployment from:

```text
Jenkins → Pipeline Job → Console Output
```

</details>

<details>
<summary><b>Step 13: Verify and Access the Application</b></summary>

After the Jenkins pipeline completes successfully, verify the Kubernetes resources:

```bash
kubectl get pods -n movie-space
kubectl get services -n movie-space
kubectl get ingress -n movie-space
```

Check the Ingress output:

```bash
kubectl get ingress -n movie-space
```

The application can then be accessed through the configured Ingress address or domain.

For example:

```text
http://<MOVIE_SERVER_IP>
```

Open the address in a browser to access the Movie Journal website. 🎬

</details>

## 🔧 Troubleshooting Scenarios

Each incident has its own documentation containing the observed symptoms, diagnostic steps, root cause, implemented fix, and verification.

| # | Incident | Documentation |
|---|---|---|
| 01 | CreateContainerConfigError | [View incident](docs/incidents/01-createcontainerconfigerror/) |
| 02 | Database Connection Failure | [View incident](docs/incidents/02-database-connection/) |
| 03 | 502 Bad Gateway | [View incident](docs/incidents/03-502-bad-gateway/) |
| 04 | ImagePullBackOff | [View incident](docs/incidents/04-imagepullbackoff/) |
| 05 | Broken Deployment & Rollback | [View incident](docs/incidents/05-broken-deployment-rollback/) |
| 06 | Database Authentication Failure | [View incident](docs/incidents/06-database-authentication/) |
| 07 | Pod Pending | [View incident](docs/incidents/07-pod-pending/) |
| 08 | Health Probe Failure | [View incident](docs/incidents/08-health-probe-failure/) |
| 09 | Jenkins Pipeline Failure | [View incident](docs/incidents/09-jenkins-pipeline-failure/) |
| 10 | Terraform Failure | [View incident](docs/incidents/10-terraform-failure/) |
| 11 | Configuration Drift | [View incident](docs/incidents/11-configuration-drift/) |

## 📚 Key Learning Areas

- Diagnosing Kubernetes workload and networking failures.
- Troubleshooting application-to-database connectivity.
- Investigating Docker image and container startup issues.
- Debugging Jenkins pipelines and deployment failures.
- Identifying Terraform configuration errors.
- Detecting configuration drift and recovering from failed deployments.
- Verifying fixes through logs, Kubernetes resources, and monitoring tools.


**Observe → Investigate → Identify the Root Cause → Fix → Verify**

This lab demonstrates practical troubleshooting, infrastructure automation, and the ability to explain why a system failed and how it was restored.