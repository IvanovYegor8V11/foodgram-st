
## **Установка и запуск проекта**

### **1. Установка Docker**
Скачать приложение docker на вашу локальную машину.

### **2. Скачивание репозитория**
Скачать данный репозиторий на вашу локальную машину.

### **3. Загрузка образов и контейнеров**
Для настройки базы данных необходимо в папке infra создать файл .env и заполнить его следующими данными:

```bash
POSTGRES_USER=django_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=django_foodgram

DB_HOST=db
DB_PORT=5432
```

Пароль можно указать свой.


Находясь в папке infra, в консоли выполнить следующую команду:

```bash
docker-compose up --build -d
```

Загрузка образов и контейнеров может идти достаточно долго.

### **4. Предзагрузка тестовых данных**
После того как образы и контейнеры соберутся, необходимо, находясь в папке infra, в строгом порядке выполнить следующие команды:

```bash
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py load_ingredients
docker-compose exec backend python manage.py collectstatic --no-input
```

В результате выполнения этих команд в приложении выполнятся миграции и загрузятся ингредиенты.

### **5. Работа с сайтом**
Сайт доступен через [localhost](http://localhost) или через [127.0.0.1](http://127.0.0.1)

Работа с админ-панелью осуществляется через [localhost/admin](http://localhost/admin).
Чтобы создать нового суперпользователя, необходимо выполнить команду:

```bash
docker-compose exec backend python manage.py createsuperuser
```

Если вдруг пропали рецепты или интерфейс админ-панели на сайте, то можно попробовать очистить кэш и cookie.
