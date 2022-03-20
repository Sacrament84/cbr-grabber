<h1>CBR-Grabber</h1>
This is Python app on Flask framework for fetch, store in database and show valute exchange rates from https://cbr.ru/ API.

Backend part takes the exchange rates for current month and store it in mysql database.
Frontend part takes stored data from database and show it in web page.
Forntend part can send update query to backend part via  REST API

Backend provide database schema and migrations

Applications designed to run in k8s cluster

# Installation
## k8s GKE
## Create Cluster and initial setup
1. Create GCP Project
2. Activate Kubernetes API, Compute Engine API, Cloud SQL API
3. Create service account with admin access to k8s and Compute Engine. Create service json key in it
4. On your local machine install gcloud cli, kubectl cli and terraform (https://cloud.google.com/sdk/docs/install) (https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/) (https://learn.hashicorp.com/tutorials/terraform/install-cli)
5. Git clone app code from github (git clone https://github.com/Sacrament84/cbr-grabber)
7. Deploy Cluster and Mysql infrastructure from folders infra/cluster infra/mysql using terraform ( terraform init, terraform apply )
8. Setup kubectl to work with your new cluster ( gcloud container clusters get-credentials cbr-grabber-gke --zone europe-west3-c )
9. Deploy namespaces from infra/yaml_ns/ns.yaml ( kubectl apply -f infra/yaml_ns/ns.yaml )
10. Create service account for SQL Proxy with access to Cloud SQL API and json key in it
11. Create kubernetes secrets for production and staging enviroments with json key from previous step ( kubectl create secret generic sa-key --from-file=service_account.json=key.json -n production ) ( kubectl create secret generic sa-key --from-file=service_account.json=key.json -n staging )
12. Install Helm on your host machine ( https://helm.sh/docs/intro/install/ )
13. Install nginx ingress controller with helm ( helm upgrade --install ingress-nginx ingress-nginx --repo https://kubernetes.github.io/ingress-nginx --namespace nginx )
14. Take external ingress controller ip address and create dns records for production, staging, jenkins, grafana 
15. Install cert-manager ( kubectl apply -f https://github.com/jetstack/cert-manager/releases/download/v1.7.0/cert-manager.yaml )
17. Deploy certificate issuer ( kubectl apply -f infra/yaml_other/issuer.yaml )
## Install Jenkins
1. Deploy files from jenkins dir ( kubectl apply -f infra/jenkins ) If Jenkins was installed edit jenkins-pv.yaml and change jenkins pv to attach it to new deploy
## Monitoring
1. Clone Repo Prometheus operator ( git clone https://github.com/prometheus-operator/kube-prometheus.git ) and go to kube-prometheus folder
2. Create resources ( kubectl create -f manifests/setup )
3. Deploy monitoring stack ( kubectl create -f manifests/ )
4. Deploy grafana ingress ( kubectl apply -f yaml_other/ingress-grafana.yaml ) Edit this file to change grafana host
## Logs
1. Add helm repo ( helm repo add grafana https://grafana.github.io/helm-charts )
2. Update repo ( helm repo update )
3. Install Grafana-Loki stack ( helm upgrade --install loki grafana/loki-stack --namespace=monitoring )
4. Go to Grafana setting and add loki source http://loki.monitoring:3100
