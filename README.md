<h1>CBR-Grabber</h1>
This is Python app on Flask framework for fetch, store in database and show valute exchange rates from https://cbr.ru/ API.

Backend part takes the exchange rates for current month and store it in mysql database.
Frontend part takes stored data from database and show it in web page.
Forntend part can send update query to backend part via  REST API

Backend provide database schema and migrations

Applications designed to run in k8s cluster

# Installation
## k8s GKE
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
