### 1. Initial Setup

- **Push code to GitHub**  
  Push your project code to a GitHub repository.

- **Create a Dockerfile**  
  Write a `Dockerfile` in the root of your project to containerize the app.

- **Create Kubernetes Manifest Directory**  
  Make a directory named `manifests/` to store all Kubernetes deployment YAML files.

- **Create a VM Instance on Google Cloud**

  - Go to VM Instances and click **"Create Instance"**
  - Name: `gitops`
  - Machine Type:
    - Series: `E2`
    - Preset: `Standard`
    - Memory: `16 GB RAM`
  - Boot Disk:
    - Change size to `256 GB`
    - Image: Select **Ubuntu 24.04 LTS**
  - Networking:
    - Enable HTTP and HTTPS traffic

- **Create the Instance**

- **Connect to the VM**
  - Use the **SSH** option provided to connect to the VM from the browser.



### 2. Configure VM Instance

- **Clone your GitHub repo**

  ```bash
  git clone https://github.com/data-guru0/TESTING-9.git
  ls
  cd TESTING-9
  ls  # You should see the contents of your project
  ```

- **Install Docker**

  - Search: "Install Docker on Ubuntu"
  - Open the first official Docker website (docs.docker.com)
  - Scroll down and copy the **first big command block** and paste into your VM terminal
  - Then copy and paste the **second command block**
  - Then run the **third command** to test Docker:

    ```bash
    docker run hello-world
    ```

- **Run Docker without sudo**

  - On the same page, scroll to: **"Post-installation steps for Linux"**
  - Paste all 4 commands one by one to allow Docker without `sudo`
  - Last command is for testing

- **Enable Docker to start on boot**

  - On the same page, scroll down to: **"Configure Docker to start on boot"**
  - Copy and paste the command block (2 commands):

    ```bash
    sudo systemctl enable docker.service
    sudo systemctl enable containerd.service
    ```

- **Verify Docker Setup**

  ```bash
  systemctl status docker       # You should see "active (running)"
  docker ps                     # No container should be running
  docker ps -a                 # Should show "hello-world" exited container
  ```


### 3. Configure Minikube inside VM

- **Install Minikube**

  - Open browser and search: `Install Minikube`
  - Open the first official site (minikube.sigs.k8s.io) with `minikube start` on it
  - Choose:
    - **OS:** Linux
    - **Architecture:** *x86*
    - Select **Binary download**
  - Reminder: You have already done this on Windows, so you're familiar with how Minikube works

- **Install Minikube Binary on VM**

  - Copy and paste the installation commands from the website into your VM terminal

- **Start Minikube Cluster**

  ```bash
  minikube start
  ```

  - This uses Docker internally, which is why Docker was installed first

- **Install kubectl**

  - Search: `Install kubectl`
  - Run the first command with `curl` from the official Kubernetes docs
  - Run the second command to validate the download
  - Instead of installing manually, go to the **Snap section** (below on the same page)

  ```bash
  sudo snap install kubectl --classic
  ```

  - Verify installation:

    ```bash
    kubectl version --client
    ```

- **Check Minikube Status**

  ```bash
  minikube status         # Should show all components running
  kubectl get nodes       # Should show minikube node
  kubectl cluster-info    # Cluster info
  docker ps               # Minikube container should be running
  ```


### 4. Jenkins Setup

- **Run Jenkins in Docker (DIND Mode)**

  - First, check existing networks:

    ```bash
    docker network ls
    ```

  - Ensure Jenkins runs on the **same Docker network** as Minikube.

  - Run Jenkins container:

    ```bash
    docker run -d --name jenkins \
    -p 8080:8080 \
    -p 50000:50000 \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v $(which docker):/usr/bin/docker \
    -u root \
    -e DOCKER_GID=$(getent group docker | cut -d: -f3) \
    --network minikube \
    jenkins/jenkins:lts
    ```

- **Verify Jenkins Container**

  ```bash
  docker ps                  # Jenkins container should be running
  docker logs jenkins        # Copy the admin password shown here
  ```

- **Access Jenkins Web UI**

  - Go to your VM dashboard in GCP
  - Copy the **External IP (public DNS)** and open:  
    `http://<EXTERNAL_IP>:8080`

  - If the page doesn't load, set a **firewall rule**:

    - GCP → VPC Network → Firewall → **Create Firewall Rule**
      - Name: `allow-jenkins`
      - Description: Allow all traffic (for Jenkins demo)
      - Logs: Off
      - Network: `default`
      - Direction: `ingress`
      - Action: `allow`
      - Targets: `All instances`
      - Source IP ranges: `0.0.0.0/0`
      - Allowed protocols and ports: `all`

- **Jenkins Setup Steps**

  - Paste the initial password from `docker logs jenkins`
  - Click **Install Suggested Plugins**
  - Create Admin User
  - Skip agent security warning (ignore for now)

- **Install Required Plugins**

  - Navigate to: **Manage Jenkins → Plugins**
    - Install:
      - Docker
      - Docker Pipeline
      - Kubernetes

- **Restart Jenkins**

  ```bash
  docker restart jenkins
  ```

  - Log in again after restart

- **Install Python and Pip inside Jenkins Container**

  ```bash
  docker exec -it jenkins bash
  apt update -y
  apt install -y python3
  python3 --version
  ln -s /usr/bin/python3 /usr/bin/python
  python --version
  apt install -y python3-pip
  apt install -y python3-venv
  exit
  ```

- **Restart Jenkins Again**

  ```bash
  docker restart jenkins
  ```

✅ Jenkins is now fully set up and ready to use!

### 5. GitHub Integration with Jenkins

---

#### 🔐 Generate GitHub Personal Access Token

- Go to: **GitHub → Settings → Developer Settings → Personal access tokens → Generate new token**
- Select **classic token** and give it the following permissions:

  ```
  admin:org
  admin:org_hook
  admin:public_key
  admin:repo_hook
  repo
  workflow
  ```

---

#### 🔑 Add GitHub Credentials to Jenkins

- Go to: **Manage Jenkins → Credentials → Global → Add Credentials**
  - **Username**: Your GitHub username
  - **Password**: The token you just generated
  - **ID**: `github-token`
  - **Description**: `github-token`

---

#### 🚀 Create a New Pipeline Job in Jenkins

1. Go to Jenkins Dashboard → **New Item**
2. Enter **Name**: `gitops`
3. Select **Pipeline**
4. Scroll to the **Pipeline** section:
   - Select **Pipeline from SCM**
   - Choose **Git**
   - **Repository URL**: Your GitHub repo link
   - **Credentials**: Select the `github-token` credential
   - **Branch**: `main`

---

#### 🧱 Create Jenkinsfile in VM

- Open **Pipeline Syntax Generator** in a new tab (for reference)
- On your VM terminal:

  ```bash
  vi Jenkinsfile
  ```

- Paste the following Jenkins pipeline code:

  ```groovy
  pipeline {
      agent any
      stages {
          stage('Checkout Github') {
              steps {
                  echo 'Checking out code from GitHub...'
                  checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/data-guru0/GitOPS-testing.git']])
              }
          }        
          stage('Build Docker Image') {
              steps {
                  echo 'Building Docker image...'
              }
          }
          stage('Push Image to DockerHub') {
              steps {
                  echo 'Pushing Docker image to DockerHub...'
              }
          }
          stage('Install Kubectl & ArgoCD CLI') {
              steps {
                  echo 'Installing Kubectl and ArgoCD CLI...'
              }
          }
          stage('Apply Kubernetes & Sync App with ArgoCD') {
              steps {
                  echo 'Applying Kubernetes and syncing with ArgoCD...'
              }
          }
      }
  }
  ```

- Save and exit:
  
  - Press `Esc`, then type `:wq!` and hit `Enter`

---

#### 🔃 Push Jenkinsfile to GitHub

```bash
git config --global user.email "gyrogodnon@gmail.com"
git config --global user.name "data-guru0"

git add .
git commit -m "commit"
git push origin main
```

- When prompted:
  - **Username**: `data-guru0`
  - **Password**: GitHub token (paste, it's invisible)

---

#### ✅ Final Jenkins Test

- Go back to Jenkins Dashboard
- Click on your `gitops` pipeline
- Click **Build Now**

If successful ✅, GitHub is now **fully integrated** with Jenkins!

---

### 6. Build and Push Docker Image to DockerHub

---

#### ⚙️ Configure Docker Tool in Jenkins

1. Go to **Jenkins Dashboard → Manage Jenkins → Tools**
2. Scroll down to **Docker Installations**
3. Click **Add Docker**
   - **Name**: `Docker`
   - ✅ Check **Install automatically**
   - Select **Install from docker.com**
4. Click **Apply and Save**

---

#### 💻 Sync Local Code from GitHub

In VS Code terminal:

```bash
git pull origin main
```

---

#### 🐳 Create DockerHub Repository

1. Go to [https://hub.docker.com](https://hub.docker.com)
2. Create a new repository, e.g., `dataguru97/testing-9`

---

#### 🔐 Generate DockerHub Access Token

1. Go to **DockerHub Account → Account Settings → Security → New Access Token**
2. Name it appropriately and give it **Read/Write** permission
3. Copy the generated token

---

#### ➕ Add DockerHub Credentials to Jenkins

1. Go to **Jenkins → Manage Jenkins → Credentials → Global → Add Credentials**
   - **Username**: DockerHub username (e.g., `dataguru97`)
   - **Password**: The DockerHub token
   - **ID**: `gitops-dockerhub`
   - **Description**: `DockerHub Access Token`

---

#### 🧱 Update `Jenkinsfile` in VS Code

Add an `environment` block at the top of the pipeline:

Update the `Build Docker Image` and `Push Image to DockerHub` stages like given in Jenkinsfile in repo

---

#### 🔁 Push Changes to GitHub

```bash
git add .
git commit -m "Add Docker build and push stages"
git push origin main
```

---

#### 🚀 Trigger Jenkins Pipeline

1. Go to Jenkins Dashboard
2. Click on your pipeline (`gitops`)
3. Click **Build Now**

✅ If successful, your image will be available on DockerHub:  
`https://hub.docker.com/r/dataguru97/testing-9`

---


### 7. Install and Configure ArgoCD - Part 1

---

#### 🧾 Step 1: Check Existing Namespaces

```bash
kubectl get namespace
```

---

#### 🆕 Step 2: Create New Namespace for ArgoCD

```bash
kubectl create ns argocd
```

✅ Run the first command again to verify the namespace is created.

---

#### 📦 Step 3: Install ArgoCD

Apply the ArgoCD installation manifest from GitHub:

```bash
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

---

#### 🔍 Step 4: Validate ArgoCD Components

Check all resources inside the `argocd` namespace:

```bash
kubectl get all -n argocd
```

✅ Wait until all resources (pods, deployments, replicasets, etc.) are in **Running** or **Completed** state.  
⛔ Do **not proceed** if anything is in **Pending** or **CrashLoopBackOff** state.

---

#### 🔌 Step 5: Check ArgoCD Service Type

```bash
kubectl get svc -n argocd
```

You’ll notice that `argocd-server` is of type **ClusterIP**, which is only accessible within the cluster.

We need to change it to **NodePort** to access the UI externally.

---

#### 🔧 Step 6: Change ClusterIP to NodePort

Edit the service:

```bash
kubectl edit svc argocd-server -n argocd
```

- Find: `type: ClusterIP`
- Replace with: `type: NodePort`

Then press:
- `Ctrl + X` → `Y` → `Enter` (or `:wq!` if in Vim)

Now re-run:

```bash
kubectl get svc -n argocd
```

✅ You will now see `argocd-server` with a **NodePort**, such as `31704`.

---

#### 🌐 Step 7: Access ArgoCD UI in Browser

Open a **new SSH terminal** and run:

```bash
kubectl port-forward --address 0.0.0.0 service/argocd-server 31704:80 -n argocd
```

- Now open your browser
- Enter: `http://<VM_PUBLIC_IP>:31704`
- You may see a privacy warning—proceed anyway

✅ You’ll land on the ArgoCD **login page**

---

#### 🔐 Step 8: Get ArgoCD Admin Password

Open another terminal and run:

```bash
kubectl get secret -n argocd argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

- **Username**: `admin`
- **Password**: (copy from above)

Login and you’re now inside the ArgoCD UI 🎉

---

### 8. Install and Configure ArgoCD – Part 2

---

#### ⚙️ Step 1: Locate Your Kubernetes Config File ( Already given this file in Course Materials Download from there )



Go to the root directory:

```bash
cd ~
ls -la
```

You’ll see a hidden directory `.kube/` — this stores your Kubernetes configuration.

Check the content:

```bash
ls -la .kube/
cat .kube/config
```

Copy the entire content of `.kube/config` into a Notepad for backup and modification.

---

#### 🔐 Step 2: Convert File Paths to Base64 Encoded Strings

The `config` file references files like:

- `/home/gyrogodnon/.minikube/ca.crt`
- `/home/gyrogodnon/.minikube/profiles/minikube/client.crt`
- `/home/gyrogodnon/.minikube/profiles/minikube/client.key`

We'll **inline** the actual base64 content instead of using file paths.

##### 🤔 Why Do We Need Base64 Conversion?

Converting certificate files to base64 and embedding them directly solves several important issues:

**🚀 Portability**
- The config file becomes self-contained with no external dependencies
- File paths like `/home/gyrogodnon/.minikube/ca.crt` are specific to your local machine
- Moving the config to another machine/environment would break these file references

**🔄 CI/CD Pipeline Compatibility**
- Jenkins, GitHub Actions, or other CI systems can use the config seamlessly
- No need to manage and transfer separate certificate files
- Everything needed is contained in one portable file

**📦 Container/Docker Deployment**
- Easier to mount as a single config file in containers
- Eliminates the need to manage multiple certificate files in container images
- Simplifies deployment processes

**🔐 Security & Management**
- Single file to secure, backup, and manage
- Easier to store as a Kubernetes secret or environment variable
- Reduces the risk of missing or misplaced certificate files

**📋 How It Works:**
- Takes the binary certificate content and encodes it as a text string
- Replaces file path references (`certificate-authority`, `client-certificate`, `client-key`) with actual certificate data (`certificate-authority-data`, `client-certificate-data`, `client-key-data`)
- Creates a standard, portable Kubernetes configuration

---

#### 📝 Step 3: Save Edited Kubeconfig File

- Save this new file as `kubeconfig` (no `.txt` extension) in your **Downloads** folder.

Now open Git Bash and run:

```bash
cd ~/Downloads
vi config
```

Paste the full edited config content.

Save it:

- Press `Esc`, then type `:wq!` and hit Enter.

---

#### 🔒 Step 4: Add kubeconfig as Secret File in Jenkins

- Go to **Jenkins Dashboard → Manage Jenkins → Credentials**
- Select: **Global → Add Credentials**
- Choose: **Kind: Secret file**
- Upload your edited `config` file
- Set:
  - **ID**: `kubeconfig`
  - **Description**: `kubeconfig`

Click Save ✅

---

#### ☁️ Step 5: Set Up Kubernetes Cluster Access in Jenkins Pipeline

1. Go to Jenkins Dashboard → Pipelines → Open your `GitOps` pipeline
2. Click **Configure**
3. Scroll down to **Pipeline section**
4. Click **Pipeline Syntax** → Opens in a new tab
5. Select:
   - **Sample Step**: `kubernetes deploy`
   - **Kubeconfig**: select `kubeconfig` credential
   - **Server URL**: Get from this command:
     ```bash
     kubectl cluster-info
     ```
     (e.g., `https://192.168.49.2:8443`)
6. Generate the script

Copy the generated script and paste/save it — you’ll use it in your Jenkinsfile in the next stage.

---

✅ At this point, your Jenkins instance is fully connected to your Kubernetes cluster using a secure kubeconfig setup.

---

# 9. Install and Configure ArgoCd - Part 3


### Step 1: Install `kubectl` and ArgoCD CLI on Docker Container

- Open **VS Code** and navigate to your **Jenkinsfile**.
- Copy-paste the code snippet you have for installing **ArgoCD** and **kubectl**.
- This snippet will be used in the pipeline.

---

### Step 2: Apply Kubernetes & Sync App with ArgoCD Stage

- Inside the pipeline stage, create a script block.
- Paste the copied installation commands inside the script.
- Replace the placeholder IP address with your **own ArgoCD server IP**.
  
```groovy
sh '''
argocd login 34.72.5.170:31704 --username admin --password $(kubectl get secret -n argocd argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d) --insecure
'''
````

> **Note:** Change `34.72.5.170:31704` to your ArgoCD server IP and port.

---

### Step 3: Connect GitHub Repository to ArgoCD

1. Open **ArgoCD UI** → Go to **Settings** → **Repositories** → **Connect Repo** via HTTPS.
2. Fill in details:

   * **Type:** git
   * **Name:** anything you want
   * **Project:** default
   * **Repo URL:** `https://github.com/data-guru0/GitOPS-testing.git`
   * **Username & Password:** Provide GitHub username and token (optional but recommended)
3. Click **Connect**.
4. You should see a success message confirming the GitHub repo is connected to ArgoCD.

---

### Important:

```groovy
kubectl create secret generic groq-api-secret \
  --from-literal=GROQ_API_KEY="" \
  -n argocd
```

### Step 4: Create a New Application in ArgoCD

* Go to **Applications** → Click **New App**.
* Fill in the form:

  * **Name:** Gitops (or any name you prefer)
  * **Project:** default
  * **Sync Policy:** Automatic
  * Tick **Sync Pipeline Resources** and **Self Heal**.
  * Leave other settings as default.
  * **Repository URL:** select your connected repo.
  * **Revision:** `main`