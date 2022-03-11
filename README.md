<h1>CBR-Grabber</h1>
This is Python app on Flask framework for fetch, store in database and show valute exchange rates from https://cbr.ru/ API.

Backend part takes the exchange rates for current month and store it in mysql database.
Frontend part takes stored data from database and show it in web page.
Forntend part can send update query to backend part via  REST API

Backend provide database schema and migrations

Applications designed to run in k8s cluster

# Installation

Создание кластера и первичная настройка
1. Создать проект в GCP
2. Активировать API Kubernetes, Compute Engine, Cloud SQL
3. Создать Сервис аккаунт и сервис ключ в этом аккаунте.
4. На своей локальной машине настроить gcloud и kubectl используя сервис ключ проекта
5. Скачать код проекта из Github
5а. Отредактируйте файлы yaml_ns/db-secret-production.yaml yaml_ns/db-secret-staging.yaml Впишите пароли юзеров для баз данных production и staging 
6. Развернуть инфраструктуру кластера из папки infra/gke
7. Настроить kubectl для работы с новым кластером (gcloud container clusters get-credentials cbr-grabber-gke --zone europe-west3-c)
8. Создать сервис аккаунт для sql-proxy для доступа утилиты sql-proxy к базе данных
9. Создать ключ доступа в сервис аккаунте из прошлого шага
10. Создать секрет в кластере с данным ключем для production окружения (kubectl create secret generic sa-key --from-file=service_account.json=key.json -n production), где key.json это ключ созданный в шаге 9
10а. Создать секрет в кластере с данным ключем для staging окружения (kubectl create secret generic sa-key --from-file=service_account.json=key.json -n staging), где key.json это ключ созданный в шаге 9
10б.Разворачиваем базу данных с помощью терраформ из папки mysql
Перед началом развертки предоставляем пароли для пользователей production, staging, root
11. Установить на хостовую машину менеджер пакетов helm (https://helm.sh/docs/intro/install/)
12. Установить ингресс контроллер nginx
helm upgrade --install ingress-nginx ingress-nginx \
  --repo https://kubernetes.github.io/ingress-nginx \
  --namespace nginx
13. Получаем внешний ип адрес балансера nginx и прописываем нужные вам днс имена для jenkins, prod, dev версий приложения, графаны и других утилит нужных вам в кластере. 
14. Устанавливаем cert-manager для управления сертификатами, чтобы наше приложение работало по https протоколу.
kubectl apply -f https://github.com/jetstack/cert-manager/releases/download/v1.7.0/cert-manager.yaml
15. Деплоим issuer для сертификатов в кластер (kubectl apply -f yaml_other/issuer.yaml)
Установка Jenkins
1. Если Дженскинс был уже настроен ранее - отредактировать файл jenkins-pv.yaml и изменить имя подключаемого диска с настройками.
1а. Деплоим файлы из папки jenkins (kubectl apply -f jenkins/)
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
