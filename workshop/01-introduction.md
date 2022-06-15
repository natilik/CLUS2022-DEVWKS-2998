## Introduction
Welcome to our workshop where we will be flexing our Kubernetes cluster with Flux. We couldn't choose better application for flexing - we will use Chuck Norris App.

Let me introduce you Flux first. Flux is based on a set of Kubernetes API extensions (“custom resources”), which control how git repositories and other sources of configuration are applied into the cluster (“synced”). Today we will focus on git repository as the only source hence mentioning GitOps but it can be also helm repository. As new application code and manifests are pushed into a repository or set of repositories monitored by Flux, the cluster state is updated automatically. Flux allows you to update, create or delete Kubernetes resources as necessary.

So how Flux fits into GitOps world? Before we will answer let's have a look on what GitOps actually stands for. GitOps is an operational framework that takes DevOps best practices used for application development such as version control, collaboration, compliance, and CI/CD tooling, and applies them to infrastructure automation. This will allow to address some of the challenges we see in operating Kubernetes with the traditional tools like `kubectl` or `helm`.

Traditional tools like `kubectl` or `helm` have following challenges:
- RBAC rules for every user who needs use theme
- No single source for manifests (deployments, services, secrets etc.)
- No change control or tracking on any changes to Kubernetes

In this workshop we will be covering the following areas:
- Install Flux client
- Create GitHub Token
- Bootstrap Flux
- Create a Flux Source Repository for `dev` and `prod` environments.
- Create Flux Kustomization Custom Resources to orchestrate the deployment of the stateful application in dev and production environments.
- Check the difference between `dev` and `prod` settings in the Kubernetes cluster
- Create Flux Kustomization
- Check the difference between the dev and production in the Kubernetes cluster
- Deploy Chuck Norris app version 1 into dev and prod
- Test Chuck Norris App version 1
- Deploy Chuck Norris app version 2 in dev and test
- Deploy Chuck Norris app version 2 in prod
