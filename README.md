<h1 align="center">CBR-BACKEND</h1>
This is backend app on Flask for fetch and store data in database from https://cbr.ru/ API.

It takes takes the exchange rates for current month and store it in mysql database.
Also it provide Database scheme and migrations.

# Installation
## Docker
#### 1. Build Docker image
#### 2.  Define variables in your system:
- database_url (in format mysql://login:password@host/database)
- mysql_user - database user
- mysql_password - dabatase password
- mysql_host - database host
- mysql_db - database name

#### 3. Start a docker container and forward port 5000 to it
#### 4.  Backend provide REST API via http://host:5000/api/refresh for fetch new data from https://cbr.ru/ and store it to database.

## k8s GKE
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
Create secret for google cloud sql proxy.

If you use database on another cloud or own host you can skip this step
### 4. Create database
Create database in google cloud or in another cloud or own host
### 5. Deploy to k8s with kustomize
* kubectl apply -k kustomize/overlays/staging - for development enviroment 
* kubectl apply -k kustomize/overlays/prodaction - for production enviroment 
