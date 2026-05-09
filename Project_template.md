## Изучите [README.md](.\README.md) файл и структуру проекта.

# Задание 1

1. Спроектируйте to be архитектуру КиноБездны, разделив всю систему на отдельные домены и организовав интеграционное взаимодействие и единую точку вызова сервисов.
Результат представьте в виде контейнерной диаграммы в нотации С4.
Добавьте ссылку на файл в этот шаблон
[C4 Container Diagram](//www.plantuml.com/plantuml/png/bLPlRnF74txlJx6_I3_9bXmx0Ie5NX6I5298Qt0GKjz4vykId6BVMVS7SAjAc02bSaNKIfMggeBIgkfRsy5WJ6A-mkutwZopllWu7vKh9VBkxExCCy_ycRiSX9OVHerwxd-EQzUZNIdsmx0PN2gNVUj-QSy9zwDQ54ZVzjnGkc79zXhbPjroyMOn27VhJgsyTc6n0j7jhHlbXXM4qYVHpXgzi1nN-gKczET29wnBSIOLwuwrvriDiIZMQD-mLckj813vRM_nYXIhlhtlXD8E8ryMShcAz0FFpGD8KIpSffy5-bKlrLYzrp-ej_JRLrtzI0sm5-g3Ue-jVgp6-g4wqPsaZGLIM6qHpCRE5IzoTos_bRVvsC8nAKu28i_2kvxVM2Y8Rt8v8SJKXNpJznwqwFvgPLDSjK9vtsg9igX0AghIl-VO4ZYlUepsP_LQ3TKf0JiI17MilrCZrHMghv-eCPrrIqBzJXvq2VnGlTM7Qg0VmHTuGgwH9wUY6lgMkrSd_ZvtzWIzUg-FS6UisxX3gm6PE2M5xuGw8Jt7zAohdz9gI5PvyvWsiApRk3B6RPYazrq1VERXYEwILhRRfzEsxX30bmprDKlVg25ePvXGIWuD5cb1tAjZeOQ4YtKy1IRzYFuFzNCex-g7-Xdz7vAGF3NuzFCIHIR5SCDplJeb8V6tDLac6Fs5G35txC8WvKqi18WXYSO4c83GUa2E_0av0Us3mPZfh7Gw0XiYZwGB2iKujt3sXfxpMSLgDQWup37Z-G32r2Y-K8rgWUqxpT3ntA006cS39aoCOp1ZslQnv7lz-1Pso70Y3T4VgnESY2tldYE3J09ni1EOR6GQ8SX8pz-oOivnPL90RP-G_wGxP9U8ORi8tqmIPR8Be3X4eiCLtG4rAVr5mQIUuYsEYu9M0_KEUKAFZeqqmqrv3_mdtDnWmVnkjibyJtVOq3i424d3oN8IPtZY2jKSaXtWo7ygVmIU2hR7fJkAIxSlhbjt3onJ2eWeF-Z5dCJb2xtiSO-ZFgBh-4F67fEjXs06hC3khE_hjNpJ2y8zNw9rLSooUlF6maSxiNo1tVyBXg0AvgUX67mY-q5-CHMaL0tmZMJQqse4YI4PR-0uNf9RgO12EklIpKX6Cdy0xj1TcvQzBmsLy84Nubnf-Jnxz2Fh7Y4Q72DcytjJwHpAFqX2mC3h9S7ri6ZIfIWmKCusJLF5apqzVA5wfBMD4gLeJtiTkTu6VFs4JPzE6Xk_Mzpr7VeLP0srUQ8F6SSexd62X63jjJuKoGpyP6P_xNa7KZPvy7tbUTTvlP3Ug5_XE2cBHmoC7G450iMT1e4t96POOQvt8kUCtjkRK7j7rdZ5TJCsQSDcE7W26qDj7DtP04nDVdisTZSUX7dpQR5ZsTmJKPzEU2sgYLKZ46kRvRLrjlnAzTWcHjQwPnzGoEAACSbQv7Q80aJFvJxABlDHiYwdlFI5CJUbGDoIUquG-Yr0JUBSjq7z9wyBlb5ol4Aolk91amtueyX3aB9vi18W455D-guCgLkNnPRZEWSaO2Clc0rsabQ9O8ynPr5VP1q630Cdd0BFkFlsaWq528jYqqNlCCCZTqlM9vzPySVDjUtjIammLxJk0CIjZUfstFaG7ggBbQMb9IY1ZidhnFnMBqsXwZOWc1QPqYjuo1P5F4-BugF12RD0GpOI9b8JRZv3aocO1tRn_valfKAsgSIKcTyKJw8aTjOu9IRHlDNVPe12JPcRwJCivs_KSpJcL3C7hksrIlcp2-VFJPnD4VfV0QOCe2l4Gpt385jCyyhTYEbDpzJq54PaTYDR5eJg9zlHSFv67mEwk7GHWFuTJyOGJoEoALEZ1X3XsoZT8fDptRYKiiy09WQJlN_E3XzhExUyicoyIVHsNitNpBDGfLis6bzsb6Qwdkx4O5OI3rznIqwErko7kUgrB-_itDYukl75UhwGkopTtQXH_mS0)
   [скриншот](screenshots/task-1_C4%20Container%20Diagram.png) (на всякий случай приложил картинку дополнительно)
# Задание 2

### 1. Proxy
Команда КиноБездны уже выделила сервис метаданных о фильмах movies и вам необходимо реализовать бесшовный переход с применением паттерна Strangler Fig в части реализации прокси-сервиса (API Gateway), с помощью которого можно будет постепенно переключать траффик, используя фиче-флаг.


Реализуйте сервис на любом языке программирования в ./src/microservices/proxy.
Конфигурация для запуска сервиса через docker-compose уже добавлена
```yaml
  proxy-service:
    build:
      context: ./src/microservices/proxy
      dockerfile: Dockerfile
    container_name: cinemaabyss-proxy-service
    depends_on:
      - monolith
      - movies-service
      - events-service
    ports:
      - "8000:8000"
    environment:
      PORT: 8000
      MONOLITH_URL: http://monolith:8080
      #монолит
      MOVIES_SERVICE_URL: http://movies-service:8081 #сервис movies
      EVENTS_SERVICE_URL: http://events-service:8082 
      GRADUAL_MIGRATION: "true" # вкл/выкл простого фиче-флага
      MOVIES_MIGRATION_PERCENT: "50" # процент миграции
    networks:
      - cinemaabyss-network
```

- После реализации запустите postman тесты - они все должны быть зеленые (кроме events).

  
- Отправьте запросы к API Gateway:
   ```bash
   curl http://localhost:8000/api/movies
   ```
- Протестируйте постепенный переход, изменив переменную окружения MOVIES_MIGRATION_PERCENT в файле docker-compose.yml.


### 2. Kafka
 Вам как архитектуру нужно также проверить гипотезу насколько просто реализовать применение Kafka в данной архитектуре.

Для этого нужно сделать MVP сервис events, который будет при вызове API создавать и сам же читать сообщения в топике Kafka.

    - Разработайте сервис на любом языке программирования с consumer'ами и producer'ами.
    - Реализуйте простой API, при вызове которого будут создаваться события User/Payment/Movie и обрабатываться внутри сервиса с записью в лог
    - Добавьте в docker-compose новый сервис, kafka там уже есть

Необходимые тесты для проверки этого API вызываются при запуске npm run test:local из папки tests/postman 
Приложите скриншот тестов и скриншот состояния топиков Kafka из UI http://localhost:8090 
[скриншот](screenshots/task-2.1.png)
[скриншот](screenshots/task-2.2.png)
[скриншот](screenshots/task-2.3.png)
[скриншот](screenshots/task-2.4.png)
[скриншот](screenshots/task-2.5_CI.png)

# Задание 3

Команда начала переезд в Kubernetes для лучшего масштабирования и повышения надежности. 
Вам, как архитектору осталось самое сложное:
 - реализовать CI/CD для сборки прокси сервиса
 - реализовать необходимые конфигурационные файлы для переключения трафика.


### CI/CD

 В папке .github/worflows доработайте деплой новых сервисов proxy и events в docker-build-push.yml , чтобы api-tests при сборке отрабатывали корректно при отправке коммита в ваш репозиторий.

Нужно доработать 
```yaml
on:
  push:
    branches: [ main ]
    paths:
      - 'src/**'
      - '.github/workflows/docker-build-push.yml'
  release:
    types: [published]
```
и добавить необходимые шаги в блок
```yaml
jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Log in to the Container registry
        uses: docker/login-action@v2
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

```
Как только сборка отработает и в github registry появятся ваши образы, можно переходить к блоку настройки Kubernetes
Успешным результатом данного шага является "зеленая" сборка и "зеленые" тесты


### Proxy в Kubernetes

#### Шаг 1
Для деплоя в kubernetes необходимо залогиниться в docker registry Github'а.
1. Создайте Personal Access Token (PAT) https://github.com/settings/tokens . Создавайте class с правом read:packages
2. В src/kubernetes/*.yaml (event-service, monolith, movies-service и proxy-service)  отредактируйте путь до ваших образов 
```bash
 spec:
      containers:
      - name: events-service
        image: ghcr.io/ваш логин/имя репозитория/events-service:latest
```
3. Добавьте в секрет src/kubernetes/dockerconfigsecret.yaml в поле
```bash
 .dockerconfigjson: значение в base64 файла ~/.docker/config.json
```

4. Если в ~/.docker/config.json нет значения для аутентификации
```json
{
        "auths": {
                "ghcr.io": {
                       тут пусто
                }
        }
}
```
то выполните 

и добавьте

```json 
 "auth": "имя пользователя:токен в base64"
```

Чтобы получить значение в base64 можно выполнить команду
```bash
 echo -n ваш_логин:ваш_токен | base64
```

После заполнения config.json, также прогоните содержимое через base64

```bash
cat .docker/config.json | base64
```

и полученное значение добавляем в

```bash
 .dockerconfigjson: значение в base64 файла ~/.docker/config.json
```

#### Шаг 2

  Доработайте src/kubernetes/event-service.yaml и src/kubernetes/proxy-service.yaml

  - Необходимо создать Deployment и Service 
  - Доработайте ingress.yaml, чтобы можно было с помощью тестов проверить создание событий
  - Выполните дальшейшие шаги для поднятия кластера:

  1. Создайте namespace:
  ```bash
  kubectl apply -f src/kubernetes/namespace.yaml
  ```
  2. Создайте секреты и переменные
  ```bash
  kubectl apply -f src/kubernetes/configmap.yaml
  kubectl apply -f src/kubernetes/secret.yaml
  kubectl apply -f src/kubernetes/dockerconfigsecret.yaml
  kubectl apply -f src/kubernetes/postgres-init-configmap.yaml
  ```

  3. Разверните базу данных:
  ```bash
  kubectl apply -f src/kubernetes/postgres.yaml
  ```

  На этом этапе если вызвать команду
  ```bash
  kubectl -n cinemaabyss get pod
  ```
  Вы увидите

  NAME         READY   STATUS    
  postgres-0   1/1     Running   

  4. Разверните Kafka:
  ```bash
  kubectl apply -f src/kubernetes/kafka/kafka.yaml
  ```

  Проверьте, теперь должно быть запущено 3 пода, если что-то не так, то посмотрите логи
  ```bash
  kubectl -n cinemaabyss logs имя_пода (например - kafka-0)
  ```

  5. Разверните монолит:
  ```bash
  kubectl apply -f src/kubernetes/monolith.yaml
  ```
  6. Разверните микросервисы:
  ```bash
  kubectl apply -f src/kubernetes/movies-service.yaml
  kubectl apply -f src/kubernetes/events-service.yaml
  ```
  7. Разверните прокси-сервис:
  ```bash
  kubectl apply -f src/kubernetes/proxy-service.yaml
  ```

  После запуска и поднятия подов вывод команды 
  ```bash
  kubectl -n cinemaabyss get pod
  ```

  Будет наподобие такого

```bash
  NAME                              READY   STATUS    

  events-service-7587c6dfd5-6whzx   1/1     Running  

  kafka-0                           1/1     Running   

  monolith-8476598495-wmtmw         1/1     Running  

  movies-service-6d5697c584-4qfqs   1/1     Running  

  postgres-0                        1/1     Running  

  proxy-service-577d6c549b-6qfcv    1/1     Running  

  zookeeper-0                       1/1     Running 
```

  8. Добавим ingress

  - добавьте аддон
  ```bash
  minikube addons enable ingress
  ```
  ```bash
  kubectl apply -f src/kubernetes/ingress.yaml
  ```
  9. Добавьте в /etc/hosts
  127.0.0.1 cinemaabyss.example.com

  10. Вызовите
  ```bash
  minikube tunnel
  ```
  11. Вызовите https://cinemaabyss.example.com/api/movies
  Вы должны увидеть вывод списка фильмов
  Можно поэкспериментировать со значением   MOVIES_MIGRATION_PERCENT в src/kubernetes/configmap.yaml и убедится, что вызовы movies уходят полностью в новый сервис

  12. Запустите тесты из папки tests/postman
  ```bash
   npm run test:kubernetes
  ```
  Часть тестов с health-чек упадет, но создание событий отработает.
  Откройте логи event-service и сделайте скриншот обработки событий

#### Шаг 3
Добавьте сюда скриншота вывода при вызове https://cinemaabyss.example.com/api/movies и  скриншот вывода event-service после вызова тестов.

[скриншот](screenshots/task-3.1.png)
[скриншот](screenshots/task-3.2.png)

# Задание 4
Для простоты дальнейшего обновления и развертывания вам как архитектуру необходимо так же реализовать helm-чарты для прокси-сервиса и проверить работу 

Для этого:
1. Перейдите в директорию helm и отредактируйте файл values.yaml

```yaml
# Proxy service configuration
proxyService:
  enabled: true
  image:
    repository: ghcr.io/db-exp/cinemaabysstest/proxy-service
    tag: latest
    pullPolicy: Always
  replicas: 1
  resources:
    limits:
      cpu: 300m
      memory: 256Mi
    requests:
      cpu: 100m
      memory: 128Mi
  service:
    port: 80
    targetPort: 8000
    type: ClusterIP
```

- Вместо ghcr.io/db-exp/cinemaabysstest/proxy-service напишите свой путь до образа для всех сервисов
- для imagePullSecret проставьте свое значение (скопируйте из конфигурации kubernetes)
  ```yaml
  imagePullSecrets:
      dockerconfigjson: ewoJImF1dGhzIjogewoJCSJnaGNyLmlvIjogewoJCQkiYXV0aCI6ICJaR0l0Wlhod09tZG9jRjl2UTJocVZIa3dhMWhKVDIxWmFVZHJOV2hRUW10aFVXbFZSbTVaTjJRMFNYUjRZMWM9IgoJCX0KCX0sCgkiY3JlZHNTdG9yZSI6ICJkZXNrdG9wIiwKCSJjdXJyZW50Q29udGV4dCI6ICJkZXNrdG9wLWxpbnV4IiwKCSJwbHVnaW5zIjogewoJCSIteC1jbGktaGludHMiOiB7CgkJCSJlbmFibGVkIjogInRydWUiCgkJfQoJfSwKCSJmZWF0dXJlcyI6IHsKCQkiaG9va3MiOiAidHJ1ZSIKCX0KfQ==
  ```

2. В папке ./templates/services заполните шаблоны для proxy-service.yaml и events-service.yaml (опирайтесь на свою kubernetes конфигурацию - смысл helm'а сделать шаблоны для быстрого обновления и установки)

```yaml
template:
    metadata:
      labels:
        app: proxy-service
    spec:
      containers:
       Тут ваша конфигурация
```

3. Проверьте установку
Сначала удалим установку руками

```bash
kubectl delete all --all -n cinemaabyss
kubectl delete  namespace cinemaabyss
```
Запустите 
```bash
helm install cinemaabyss .\src\kubernetes\helm --namespace cinemaabyss --create-namespace
```
Если в процессе будет ошибка
```code
[2025-04-08 21:43:38,780] ERROR Fatal error during KafkaServer startup. Prepare to shutdown (kafka.server.KafkaServer)
kafka.common.InconsistentClusterIdException: The Cluster ID OkOjGPrdRimp8nkFohYkCw doesn't match stored clusterId Some(sbkcoiSiQV2h_mQpwy05zQ) in meta.properties. The broker is trying to join the wrong cluster. Configured zookeeper.connect may be wrong.
```

Проверьте развертывание:
```bash
kubectl get pods -n cinemaabyss
minikube tunnel
```

Потом вызовите 
https://cinemaabyss.example.com/api/movies
и приложите скриншот развертывания helm и вывода https://cinemaabyss.example.com/api/movies

[скриншот](screenshots/task-4.1_kubectl%20get%20pods%20-n%20cinemaabyss.png)
[скриншот](screenshots/task-4.2_cinemaabyss.example.com_api_movies%20.png)
## Удаляем все

```bash
kubectl delete all --all -n cinemaabyss
kubectl delete namespace cinemaabyss
```
