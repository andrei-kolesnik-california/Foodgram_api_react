<a id = "anchor"></a>
# Foodgram - online service for publishing culinary recipes.

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)  
http://foodgram.gotdns.ch/
### Description

🍳 **Foodgram** is a vibrant, full-stack recipe sharing platform that brings food lovers together! Built with modern web technologies, this application allows users to discover, create, and share delicious culinary recipes with the world.

**✨ Key Features:**
- **Recipe Publishing**: Share your favorite recipes with detailed cooking instructions and beautiful photos
- **Smart Tagging System**: Organize and discover recipes by categories, cuisines, and dietary preferences
- **Social Features**: Follow your favorite chefs, like recipes, and build your culinary community
- **Shopping Lists**: Automatically generate shopping lists from your saved recipes
- **PDF Export**: Print ingredient lists and cooking instructions for offline use
- **Responsive Design**: Enjoy the platform on any device - desktop, tablet, or mobile

**🔐 User Experience:**
- **Public Access**: Browse and search recipes without registration
- **Authenticated Users**: Create recipes, follow authors, build favorites, and manage shopping lists
- **Seamless Workflow**: From recipe discovery to grocery shopping, everything is connected

Perfect for food bloggers, home cooks, and anyone passionate about cooking and sharing culinary experiences!   

### Project Launch 
clone the repository 
```
git clone git@github.com:andrey-kolesnik-moscow/foodgram-project-react.git
```
connect to your server via ssh
```
ssh <username>@<server IP>
```
install Docker
```
sudo apt install docker.io
```
install docker-compose for Linux
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
set permissions for docker-compose
```
sudo chmod +x /usr/local/bin/docker-compose
```
add your server IP to the .env file
```
ALLOWED_HOSTS='localhost, 127.0.0.1, <server ip>'
CSRF_TRUSTED_ORIGINS='http://localhost, http://127.0.0.1, http://<server ip>'
``` 
copy files to the server from the infra folder
```
scp infra/* <username>@<server IP>:/home/<server user>/<your folder>/
```
start docker-compose build
```
sudo docker-compose up -d
```

[Back to top](#anchor)