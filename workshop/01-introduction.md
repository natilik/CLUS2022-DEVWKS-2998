## Introduction
Welcome to our workshop where we will be flexing our Kubernetes cluster with Flux. We couldn't choose better application for flexing - we will use Chuck Norris App.

Let me introduce you Flux first. Flux is based on a set of Kubernetes API extensions (“custom resources”), which control how git repositories and other sources of configuration are applied into the cluster (“synced”). Today we will focus on git repository as the only source hence mentioning GitOps but it can be also helm repository. As new application code and manifests are pushed into a repository or set of repositories monitored by Flux, the cluster state is updated automatically. Flux allows you to update, create or delete Kubernetes resources as necessary.

So how Flux fits into GitOps world? Before we will answer let's have a look on what GitOps actually stands for. GitOps is an operational framework that takes DevOps best practices used for application development such as version control, collaboration, compliance, and CI/CD tooling, and applies them to infrastructure automation. This will allow to address some of the challenges we see in operating Kubernetes with the traditional tools like `kubectl` or `helm`.

Traditional tools like `kubectl` or `helm` have following challenges:
- RBAC rules for every user who needs use theme
- No single source for manifests (deployments, services, secrets etc.)
- No change control or tracking on any changes to Kubernetes

In the first part of our workshop we will be doing following tasks:
- Explain what is Flux and GitOps
- Install Flux client
- Create GitHub Token
- Bootstrap Flux

## Flux pre-requirements
We have pre-built Kubernetes cluster for you. It is standard `kind` (Kubernetes in Docker) cluster.

First, let's get familiar with your freshly deployed Kubernetes cluster. You can use the `kubectl` command line tool to interact with the cluster.

Run the following command to display the nodes in your cluster:
```bash
kubectl get nodes -o wide
```

You should see this:
```
NAME                 STATUS   ROLES                  AGE   VERSION   INTERNAL-IP   EXTERNAL-IP   OS-IMAGE       KERNEL-VERSION     CONTAINER-RUNTIME
kind-control-plane   Ready    control-plane,master   68s   v1.23.4   172.19.0.2    <none>        Ubuntu 21.10   5.10.76-linuxkit   containerd://1.5.10

```

Now that you know your cluster is working let's install Flux. Run the following command to install the Flux CLI:
```bash
curl -s https://fluxcd.io/install.sh | bash
```

Verify that the Flux CLI has been installed by executing the following command:
```bash
flux --version
```

Using Flux bootstrap command you can install Flux on a Kubernetes cluster and configure it to manage itself from a Git repository. If the Flux components are present on the cluster, the bootstrap command will perform an upgrade if needed. The bootstrap is idempotent, it’s safe to run the command as many times as you want.

Let's check that your cluster meets Flux requirements. Run the following command to perform the pre-flight check:
```bash
flux check --pre
```

You should see this:
```
► checking prerequisites
✔ Kubernetes 1.24.0 >=1.20.6-0
✔ prerequisites checks passed
```

For the next steps we will need your GitHub account.

It comes with a constraint for this challenge though, you need a Github user along with a Github personal access token. We're assuming that you already have a Github account.

To create a personal access token, navigate to GitHub and go to your GitHub profile by clicking on your profile icon at the top right, and click on Settings. Then click on Developer settings at the bottom of the left menu and click on Personal access tokens. For security sake, Select 7 days as the token's expiration time. Only select repo as the scope, as this is what is required by Flux. Finally, click on Generate token at the bottom and copy the token to the clipboard by clicking on the blue rectangles located next to your token.

Now let's export your GitHub personal access token and username by running the following commands:
```bash
export GITHUB_TOKEN=<your-token>
export GITHUB_USER=<your-username>
```

## Install Flux
Now we can bootstrap Flux on Kubernetes cluster. It is pretty straight forward.

Execute the following command to bootstrap Flux in your cluster:
```bash
flux bootstrap github \
  --owner=$GITHUB_USER \
  --repository=natilik-fleet \
  --branch=main \
  --path=./clusters/clus2022 \
  --personal
```

This will create new repository `natilik-fleet` which will contain Flux configuration:
```
► connecting to github.com
✔ repository "https://github.com/maty0609/natilik-fleet" created
► cloning branch "main" from Git repository "https://github.com/maty0609/natilik-fleet.git"
✔ cloned repository
► generating component manifests
✔ generated component manifests
✔ committed sync manifests to "main" ("2833b6216aad408beebd87f16101e43f8807b7b6")
► pushing component manifests to "https://github.com/maty0609/natilik-fleet.git"
✔ installed components
✔ reconciled components
► determining if source secret "flux-system/flux-system" exists
► generating source secret
✔ public key: ecdsa-sha2-nistp384 AAAAE2VjZHNhLXNoYTItbmlzdHAzODQAAAAIbmlzdHAzODQAAABhBJl8sMuXFC53GPAxV5D0cEGifqBt6QvYAXL536He5hooWwjIJgtgjbWsms1rSPAY+qJpMtWZDFFIUWgVqgzdHmNfyF7xCJXOts4HJ5yQf28mrBWcQPGh5sQollHzrP1LMg==
✔ configured deploy key "flux-system-main-flux-system-./clusters/clus2022" for "https://github.com/maty0609/natilik-fleet"
► applying source secret "flux-system/flux-system"
✔ reconciled source secret
► generating sync manifests
✔ generated sync manifests
✔ committed sync manifests to "main" ("6eb7049b2520391500839fec2a0fcda503a09255")
► pushing sync manifests to "https://github.com/maty0609/natilik-fleet.git"
► applying sync manifests
✔ reconciled sync configuration
◎ waiting for Kustomization "flux-system/flux-system" to be reconciled
✔ Kustomization reconciled successfully
► confirming components are healthy
✔ helm-controller: deployment ready
✔ kustomize-controller: deployment ready
✔ notification-controller: deployment ready
✔ source-controller: deployment ready
✔ all components are healthy
```

If you go to your GitHub account you should see new repository called `natilik-fleet`. It contains all necessary information about Flux components for our new cluster called `clus2022`.

Now let’s verify that the Flux components have been installed in the `flux-system` namespace by executing the following command:
```bash
kubectl get pods -n flux-system
```

The command output should look something like this:
```
NAME                                      READY   STATUS    RESTARTS   AGE
helm-controller-6ddb885bb4-zfsq7          1/1     Running   0          61s
kustomize-controller-584f5c8f9d-lkchb     1/1     Running   0          61s
notification-controller-8fd67fcff-q5wt5   1/1     Running   0          60s
source-controller-67df67fc7-hkg85         1/1     Running   0          60s
```

Let's clone our new repo so we can work locally:
```bash
cd /root
git clone https://$GITHUB_USER:$GITHUB_TOKEN@github.com/$GITHUB_USER/natilik-fleet
```

After it will be downloaded let's check what's the structure of the repository:
```bash
tree /root/natilik-fleet/
```

```
/root/natilik-fleet/
└── clusters
    └── clus2022
        └── flux-system
            ├── gotk-components.yaml
            ├── gotk-sync.yaml
            └── kustomization.yaml
```

Nice one! Congratulations. You have now finished the first part of this session where you have installed and successfully initiated Flux on your `clus2022` Kubernetes cluster. Now we should be ready to start using Flux to deploy our new Chuck Norris app.
