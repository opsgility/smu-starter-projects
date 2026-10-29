# deploy/

This folder is where each lab's deploy artifacts land. Claude Code writes them for you during the lab.

Suggested layout once you've worked through the course:

```
deploy/
  lab2-static/           Static Web Apps workflow + config (GitHub Actions deploy)
  lab3-function/         Azure Functions app code + host.json + deploy script
  lab4-container/        Dockerfile shim + ACR build + Container Apps deploy (Bicep or az)
  lab5-domain/           Azure DNS zone + managed cert binding on Container Apps
  lab6-aks/              AKS cluster + Kubernetes manifests (optional stretch)
```

Nothing is pre-filled — the point of the course is to build each shape from scratch so you understand what every line of config does.
