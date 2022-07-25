<a id = "anchor"></a>
# Foodgram - онлайн сервис для публикации кулинарных рецептов.

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)  
http://foodgram.gotdns.ch/
### Описание

Приложение создано для публикации рецептов с описанием их приготовления и сортировкой по тегам. Для авторизованных пользователей открывается функционал создания рецептов, подписки на других авторов, добавления рецептов к числу понравившихся и в список покупок. Все авторизованные пользователи сайта могут распечатать список необходимых ингредиентов для приготовления в формате pdf.   

### Запуск проекта 
клонируйте репозиторий 
```
git clone git@github.com:andrey-kolesnik-moscow/foodgram-project-react.git
```
подключитесь к своему серверу через ssh
```
ssh <username>@<server IP>
```
установите Docker
```
sudo apt install docker.io
```
установите docker-compose для Linux
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
сделайте разрешения для docker-compose
```
sudo chmod +x /usr/local/bin/docker-compose
```
добавьте ip вашего сервера в файл .env
```
ALLOWED_HOSTS='localhost, 127.0.0.1, <server ip>'
CSRF_TRUSTED_ORIGINS='http://localhost, http://127.0.0.1, http://<server ip>'
``` 
скопируйте файлы на сервер из папки infra
```
scp infra/* <username>@<server IP>:/home/<server user>/<your folder>/
```
запустите сборку docker-compose
```
sudo docker-compose up -d
```

[В начало страницы](#anchor)