## Introduction
In this part you will perform the following tasks:
- Create a Flux Source Repository for `dev` and `prod` environments.
- Create Flux Kustomization Custom Resources to orchestrate the deployment of the stateful application in dev and production environments.
- Check the difference between `dev` and `prod` settings in the Kubernetes cluster

## Create Flux Source Git Repositories
The Flux Source API defines a set of Kubernetes objects that cluster admins and various automated operators can interact with to offload the Git and Helm repositories operations to a dedicated controller.

You will create Flux Git Repositories to expose the latest synchronized state from Git as an artifact. These repositories will be monitored by Flux and the source controller will reconcile the application state in Kubernetes upon changes in the Git repository, in accordance to the Kustomization definition.

You are going to create 2 Flux Source Repositories: one for `dev` environment and one for `prod` environment.

Let's start with forking application repository `https://github.com/natilik/CLUS2022-DEVWKS-2998.git`. This repository will represents our application.

```bash
cd /root
git clone https://$GITHUB_USER:$GITHUB_TOKEN@github.com/$GITHUB_USER/CLUS2022-DEVWKS-2998.git
```

```bash
tree /root/CLUS2022-DEVWKS-2998
```

```
├── README.md
├── chuck-norris-app-src
│   ├── Dockerfile
│   ├── app.yaml
│   ├── main.py
│   ├── requirements.txt
│   ├── static
│   │   └── img
│   │       └── up.png
│   └── templates
│       ├── chuck.html
│       └── norris.html
├── env
│   └── prod
│       ├── deployment.yaml
│       └── service.yaml
└── workshop
    ├── 01-introduction.md
    ├── 02-create-flux-git-repos.md
    ├── 03-create-flux-kustomization.md
    ├── 04-deploy-chuck-norris-app-v2.md
    └── images
        ├── chuck-norris-app-v1.png
        └── chuck-norris-app-v2.png
```

Run command `git branch -r` in the repository `CLUS2022-DEVWKS-2998` to see that we have two branches - `main` and `dev`. This will be important to know for our next steps.

After you will fork the repository run the following command to create configuration for our `dev` environment:
```bash
mkdir /root/natilik-fleet/clusters/clus2022/apps
cd /root/natilik-fleet/clusters/clus2022
flux create source git dev \
--url https://github.com/$GITHUB_USER/CLUS2022-DEVWKS-2998.git \
--branch dev \
--interval 30s \
--export \
| tee apps/dev.yaml
```

You should see this:
```yaml
apiVersion: source.toolkit.fluxcd.io/v1beta2
kind: GitRepository
metadata:
  name: dev
  namespace: flux-system
spec:
  interval: 30s
  ref:
    branch: dev
  url: https://github.com/$GITHUB_USER/CLUS2022-DEVWKS-2998.git
```

Let's also create the second one for `prod` environment. Run the following command:
```bash
flux create source git prod \
--url https://github.com/$GITHUB_USER/CLUS2022-DEVWKS-2998.git \
--branch main \
--interval 30s \
--export \
| tee apps/prod.yaml
```

You should see this:
```yaml
apiVersion: source.toolkit.fluxcd.io/v1beta2
kind: GitRepository
metadata:
  name: prod
  namespace: flux-system
spec:
  interval: 30s
  ref:
    branch: main
  url: https://github.com/$GITHUB_USER/CLUS2022-DEVWKS-2998.git
```

We have now defined source for our applications. Flux will monitor git repository `https://github.com/$GITHUB_USER/CLUS2022-DEVWKS-2998.git` and its two branches. Branch `dev` will represent `dev` environment and branch `main` will represent `prod` environment. Now let’s link our new git repositories with our Kubernetes environment.
