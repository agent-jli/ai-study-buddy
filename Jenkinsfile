// =============================================================================
// AI STUDY BUDDY - JENKINS CI/CD PIPELINE
// =============================================================================
// This file defines an automated deployment pipeline that:
// 1. Gets your code from GitHub
// 2. Builds a Docker container with your app
// 3. Pushes it to DockerHub 
// 4. Deploys it to Kubernetes via ArgoCD
// =============================================================================

pipeline {
    // Use different agents for different stages
    agent none
    
    // Environment variables used throughout the pipeline
    // Think of these as "settings" that all stages can access
    environment {
        // Where to store your Docker image (like your app's address on DockerHub)
        DOCKER_HUB_REPO = "slithice/studybuddy"
        
        // Jenkins credential ID for DockerHub login (stored securely in Jenkins)
        DOCKER_HUB_CREDENTIALS_ID = "dockerhub-token"
        
        // Create unique image tags using Jenkins build number (v1, v2, v3, etc.)
        IMAGE_TAG = "v${BUILD_NUMBER}"
    }
    
    // The actual work happens in these stages (think of them as steps)
    stages {
        
        // STAGE 1: Get the latest code from GitHub
        stage('Checkout Github') {
            agent any
            steps {
                echo 'Checking out code from GitHub...'
                // Download your latest code from the main branch
                // Uses the 'github-token' credential stored in Jenkins
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/agent-jli/ai-study-buddy.git']])
            }
        }        
        
        // STAGE 2: Build your app into a Docker container
        stage('Build Docker Image') {
            agent any
            steps {
                script {
                    echo 'Building Docker image...'
                    // This reads your Dockerfile and creates a container image
                    // Like packaging your app into a shipping container
                    dockerImage = docker.build("${DOCKER_HUB_REPO}:${IMAGE_TAG}")
                }
            }
        }
        
        // STAGE 3: Upload the container to DockerHub (like GitHub for containers)
        stage('Push Image to DockerHub') {
            agent any
            steps {
                script {
                    echo 'Pushing Docker image to DockerHub...'
                    // Login to DockerHub and upload your container image
                    // So Kubernetes can download it later
                    docker.withRegistry('https://registry.hub.docker.com', "${DOCKER_HUB_CREDENTIALS_ID}") {
                        dockerImage.push("${IMAGE_TAG}")
                        dockerImage.push("latest")  // Also push as latest
                    }
                }
            }
        }
        
        // STAGE 4 & 5: Update and Commit Deployment YAML (combined to preserve changes)
        stage('Update and Commit Deployment YAML') {
            agent any
            steps {
                script {
                    // Replace the old image tag with the new one in deployment.yaml
                    sh '''
                    echo "Updating image tag to ${IMAGE_TAG}"
                    sed -i "s|image: slithice/studybuddy:.*|image: slithice/studybuddy:${IMAGE_TAG}|g" manifests/deployment.yaml
                    echo "Updated deployment.yaml:"
                    grep "image: slithice/studybuddy" manifests/deployment.yaml
                    '''
                    
                    // Use GitHub credentials to push changes back to your repo
                    withCredentials([usernamePassword(credentialsId: 'github-token', usernameVariable: 'GIT_USER', passwordVariable: 'GIT_PASS')]) {
                        sh '''
                        # Configure git with your identity
                        git config user.name "agent-jli"
                        git config user.email "liyike1988@gmail.com"
                        
                        # Force git to see the change
                        echo "Before git add:"
                        git status manifests/deployment.yaml
                        
                        # Force add the file even if git thinks it's unchanged
                        git add -f manifests/deployment.yaml
                        
                        # Show what we're committing
                        git diff --cached manifests/deployment.yaml
                        
                        # Commit the change
                        git commit -m "Update image tag to ${IMAGE_TAG} [skip ci]"
                        
                        # Push back to GitHub main branch
                        git push https://${GIT_USER}:${GIT_PASS}@github.com/agent-jli/ai-study-buddy.git HEAD:main
                        
                        # Don't restore placeholder - ArgoCD needs to see the actual image tag
                        echo "Deployment updated with ${IMAGE_TAG} - ArgoCD will sync this version"
                        '''
                    }
                }
            }
        }
        
        // STAGE 7: Deploy your app to Kubernetes cluster
        stage('Apply Kubernetes & Sync App with ArgoCD') {
            agent {
                docker {
                    image 'alpine/k8s:1.33.4'
                    args '--user root --network host'
                }
            }
            steps {
                script {
                    // Connect to your Kubernetes cluster using stored credentials
                    kubeconfig(credentialsId: 'kubeconfig', serverUrl: 'https://192.168.49.2:8443') {
                        sh '''
                        # Install ArgoCD CLI (kubectl already available in alpine/k8s image)
                        curl -sSL -o /usr/local/bin/argocd https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
                        chmod +x /usr/local/bin/argocd
                        
                        # Login to ArgoCD (GitOps tool that manages deployments)
                        argocd login 34.16.92.116:31704 --username admin --password $(kubectl get secret -n argocd argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d) --insecure
                        
                        # Sync the app with ArgoCD (deploy the new version)
                        echo "Syncing ArgoCD app..."
                        argocd app sync study-buddy
                        
                        echo "Checking sync status..."
                        argocd app get study-buddy
                        
                        echo "Checking deployment status..."
                        kubectl get deployment llmops-app -n argocd -o wide
                        kubectl get pods -n argocd -l app=llmops-app
                        
                        echo "Force rolling restart to ensure new image is used..."
                        kubectl rollout restart deployment/llmops-app -n argocd
                        kubectl rollout status deployment/llmops-app -n argocd
                        '''
                    }
                }
            }
        }
    }
}

// =============================================================================
// WHAT HAPPENS WHEN YOU PUSH CODE:
// =============================================================================
// 1. Jenkins detects your git push
// 2. Downloads your latest code  
// 3. Builds it into a Docker container (using your Dockerfile with uv)
// 4. Uploads container to DockerHub
// 5. Updates Kubernetes deployment file with new version number
// 6. Commits that change back to GitHub
// 7. Tells ArgoCD to deploy the new version to your cluster
// 8. Your users see the updated app!
// =============================================================================