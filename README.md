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
## Создание кластера и первичная настройка
1. Создать проект в GCP 
2. Активировать API Kubernetes, Compute Engine, Cloud SQL
3. Создать Сервис аккаунт и сервис ключ в этом аккаунте.
4. На своей локальной машине настроить gcloud и kubectl используя сервис ключ проекта
5. Скачать код проекта из Github
6. Развернуть инфраструктуру кластера и базы данных из папки infra
7. Настроить kubectl для работы с новым кластером (gcloud container clusters get-credentials cbr-grabber-gke --zone europe-west3-c)
8. Создать сервис аккаунт для sql-proxy для доступа утилиты sql-proxy к базе данных
9. Создать ключ доступа в сервис аккаунте из прошлого шага
10. Создать секрет в кластере с данным ключем (kubectl create secret generic sa-key --from-file=service_account.json=key.json -n production), где key.json это ключ созданный в шаге 9
11. Установить на хостовую машину менеджер пакетов helm (https://helm.sh/docs/intro/install/)
12. Установить ингресс контроллер nginx
helm upgrade --install ingress-nginx ingress-nginx \
  --repo https://kubernetes.github.io/ingress-nginx \
  --namespace nginx
13. Получаем внешний ип адрес балансера nginx  и прописываем нужные вам днс имена для jenkins, prod, dev версий приложения, графаны и других утилит нужных вам в кластере. 
14. Устанавливаем cert-manager для управления сертификатами, чтобы наше приложение работало по https протоколу.
kubectl apply -f https://github.com/jetstack/cert-manager/releases/download/v1.7.0/cert-manager.yaml
15. Деплоим issuer для сертификатов в кластер (kubectl apply -f yaml_other/issuer.yaml)
## Установка Jenkins
1. Деплоим файлы из папки jenkins (kubectl apply -f jenkins/)
1a. Если Дженскинс был уже настроен ранее - отредактировать файл jenkins-pv.yaml и изменить имя диска покдлючаемого с настройками.
2. Настраиваем связку Дженкинс и Кластер через kubeconfig (редактируем адрес кластера в окружении и заводим секрет с конфигом кластера)
3. Создаем секрет в кластере для kaniko для того чтобы он мог пушить имеджи в регистри
(kubectl create secret generic kaniko-secret --from-file=kaniko-key.json=kaniko.key -n jenkins) где kaniko.key содержит ключ сервис аккаунта в GCP с доступом в имедж регистри.
Развертка приложения
Развернуть приложение можно сделав любое изменение в коде и запушив его в гитхаб. (в случае настроеннго вебхука)
Либо вручную запустив сборку и деплой в Дженкинс

Мониторинг
1. Склонируем оператор Прометеуса - git clone https://github.com/prometheus-operator/kube-prometheus.git и перейдем в папку cd kube-prometheus
2. Создадим необходимые ресурсы в кластере - kubectl create -f manifests/setup
3. Развернем стак мониторинга - kubectl create -f manifests/
4. Развернем игресс для удобного доступа к дашборду Графаны - kubectl apply -f yaml_other/ingress-grafana.yaml (Отредактируйте этот файл для указания своего домена)
Логирование
1. helm repo add grafana https://grafana.github.io/helm-charts
2. helm repo update
3. helm upgrade --install loki grafana/loki-stack --namespace=monitoring
4. Добавляем источник данных в графане - http://loki.monitoring:3100
