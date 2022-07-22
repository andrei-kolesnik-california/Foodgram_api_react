<a id = "anchor"></a>
# Продуктовый помощник — полноценное приложение с серверной частью и пользовательским интерфейсом.
http://foodgram.gotdns.ch/
### Описание

Приложение создано для публикации рецептов с описанием их приготовления и сортировкой по тегам. Для авторизованных пользователей открывается функционал создания рецептов, подписки на других авторов, добавления рецептов к числу понравившихся и в список покупок. Также все авторизованные пользователи сайта могут распечатать список необходимых ингредиентов для приготовления в формате pdf.   
***
### Технологии
* Python 3.8.3 
* Django 2.2.16 
* djangorestframework 3.12.4  
Полный список используемых технологий -> requirements.txt
***
### Запуск проекта 
клонируйте репозиторий 
```
git clone git@github.com:andrey-kolesnik-moscow/foodgram-project-react.git
```
подключитесь к своему серверу через ssh
```
ssh <server user>@<server IP>
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
скопируйте файлы на сервер из папки infra
```
scp infra/* <server user>@<server IP>:/home/<server user>/<your folder>/
```
запустите сборку docker-compose
```
sudo docker-compose up -d
```

[В начало страницы](#anchor)