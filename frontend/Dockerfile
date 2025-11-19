FROM nginx:alpine

WORKDIR /usr/share/nginx/html

# Копируем статические файлы
COPY . .

# Копируем конфигурацию nginx
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 88
#для Nginx не требуется менять пользователя, 
#так как официальный образ Nginx уже настроен на запуск процессов в своей учетной записи,
#которая по умолчанию имеет необходимые права для работы