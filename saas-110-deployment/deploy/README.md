# deploy/

This folder is where each lab's deploy artifacts land. Claude Code writes them for you during the lab.

Suggested layout once you've worked through the course:

```
deploy/
  lab2-static/           Cloud Storage + Cloud CDN bucket + load balancer (Terraform)
  lab3-function/         gcloud command + source zip (or Terraform) for Cloud Run functions
  lab4-container/        gcloud build + run deploy scripts; or Terraform
  lab5-domain/           Cloud DNS zone + managed certificate + Cloud Run domain mapping
  lab6-gke/              GKE Autopilot cluster + Kubernetes manifests (optional stretch)
```

Nothing is pre-filled — the point of the course is to build each shape from scratch so you understand what every line of config does.
