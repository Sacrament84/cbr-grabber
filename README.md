<h1>CBR-Grabber</h1>
This is Python app on Flask framework for fetch, store in database and show valute exchange rates from https://cbr.ru/ API.

Backend part takes the exchange rates for current month and store it in mysql database.
Frontend part takes stored data from database and show it in web page.
Forntend part can send update query to backend part via  REST API

Backend provide database schema and migrations

Applications designed to run in k8s cluster

# Installation
## k8s GKE
## Requirements:
* k8s cluster running in GCP cloud provider
* Jenkins CI/CD running in k8s cluster
* Sonarqube running in k8s cluster or any server
* Jenkins and sonarqube integration
* Mysql databse running in GCP with sql proxy API enabled
* Service account in k8s cluster with crossnamespace access to deployments, services, ingresess, hpa (defined in Jenkinsfile)
### 1. Define secrets in your cluster:
* database_url (in format mysql://login:password@host/database)
* mysql_user - database user
* mysql_password - dabatase password
* mysql_host - database host
* mysql_db - database name
### 2. Create namespaces:
* staging for dev branch 
* production for main branch
### 3. Create secret for Cloud Sql Proxy
Application uses a mysql database running in GCP, so you need a secret for the cloud sql proxy.
Create secret for google cloud sql proxy.
### 4. Create multibranch pipeline job in Jenkins 
* Create multibranch pipeline in Jenkins using Jenkinsfile in repo
