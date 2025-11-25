## Решение тестового задания для 'MStroy'
### Контактные данные
    Зайнуллин Айзат Маратович
    Тел: 89872674912
    ТГ: https://t.me/laneryel
    Почта: aizat9@list.ru

1) Собираем приложение и запускаем  
    ![alt text](screens/image.png)
    ![alt text](screens/image-1.png)

2) Видим, что контейнер фронтенда упал  
    ![alt text](screens/image-2.png)

3) Смотрим логи, чтобы узнать в чем проблема   
    ![alt text](screens/image-3.png)  
    Что-то не так с блоком `upstream` в `nginx.conf`

4) Дополняем `nginx.conf` и пересобираем приложение  
    ![alt text](screens/image-4.png)

5) Снова контейнер упал, смотрим логи  
    ![alt text](screens/image-5.png)    
    Хост `python-backend` не найден  

6) Снова корректируем `nginx.conf` согласно имени сервиса в `docker-compose.yaml` и пересобираем  
    ![alt text](screens/image-6.png)  

7) Отлично. Все работает, но нет списка кошек, значит подключение к БД отсутствует  
    ![alt text](screens/image-7.png)  
    ![alt text](screens/image-8.png)  

8) Смотрим логи бэкенда, убедждаемся что подключение отсутствует  
    ![alt text](screens/image-9.png)  
    Не найден хост `mongo-db`

9) Корректируем `docker-compose.yaml`, меняя имя сервиса `mongodb --> mongo-db`  
    ![alt text](screens/image-10.png)  

10) Также корректируем сеть, подключая все сервисы к одной  
    ![alt text](screens/image-11.png)

11) Плюс правильно прописываем путь в данной строке в файле `app.js`, т.к. nginx проксирует на 88 порт  
    ![alt text](screens/image-12.png)  

12) Все работает  
    ![alt text](screens/image-13.png)
    ![alt text](screens/image-14.png)
    ![alt text](screens/image-15.png)