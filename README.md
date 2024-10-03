# Effective Mobile Task

## Описание

Проект **Effective Mobile** представляет собой API для управления продуктами и заказами. 
Выполнено с фреймворком FastApi и БД Postgresql с помощью асинхронных вызовов. 


## Установка

1. Клонировать репозиторий и перейти в него в командной строке:

    ```bash
    git clone https://github.com/kirillkiselev-slim/effectivemobile_rest_api/
    cd effectivemobile_rest_api
    ```

2. Создать и активировать виртуальное окружение:

    ```bash
    python3 -m venv env
    ```

    * **Для Linux/macOS:**

        ```bash
        source env/bin/activate
        ```

    * **Для Windows:**

        ```bash
        source env/scripts/activate
        ```

3. Обновить `pip`:

    ```bash
    python3 -m pip install --upgrade pip
    ```

5. Скачайте зависимости локально для тестов:

```bash
pip install -r requirements.txt
```


6. Установите переменные окружения (чтобы пройти тесты - установите переменную окружения для локальной БД):

    ```text
   DATABASE_URL=postgresql+asyncpg://<your_username>:<your_password>@postgres/warehouse
   POSTGRES_DB=warehouse
   POSTGRES_USER=<your_username>
   POSTGRES_PASS=<your_password>
    ```
   
### **Важно: Запуск в Docker**:
```text
DATABASE_URL=postgresql+asyncpg://<your_username>:<your_password>@postgres/warehouse
```
### **Важно: Запуск локально**:
```text

DATABASE_URL=postgresql+asyncpg://<your_username>:<your_password>@localhost/warehouse
```

7. Пройдитесь тестами по проекту:

    ```bash
    pytest app/tests/v1
    ```

8. Запустить Docker Compose для сборки и запуска контейнеров Postgresql и FastApi приложения
(чтобы запустить docker compose - поменяйте переменную окружения для БД на 
`DATABASE_URL=postgresql+asyncpg://<your_username>:<your_password>@postgres/warehouse`):

   ```bash
    docker compose up --build
    ```

Это автоматически соберет образы и запустит контейнеры для PostgreSQL и backend-приложения.

## Примеры запросов

### 1-й пример

**Method:** `POST`  
**Endpoint:** `/api/v1/orders`

**Body:**

```json
{
  "status": "В процессе",
  "products": {
    "1": 2,
    "2": 3
  }
}
```
**Response:**

```json
{
  "id": 1,
  "created_at": "2024-10-02T20:51:26.865216Z",
  "status": "string",
  "products": {
    "1": 2,
    "2": 3
  }
}
```

### 2-й пример

**Method:** `PATCH`  
**Endpoint:** `/api/v1/orders/{order_id}/status`

**Body:**

```json
{
  "status": "отправлен"
}
```

**Response:**

```json
{
  "id": 1,
  "created_at": "2024-10-02T20:51:26.865216Z",
  "status": "отправлен",
  "products": {
    "1": 2,
    "2": 3
  }
}
```

### Валидация и логика:

~~~
1. При создании продукта нужно учитывать, что такое имя еще не существует.
2. При создании заказа АПИ проверяет наличие достаточного количества товара на складе.
3. В случае недостаточного количества товара, АПИ – возвращает ошибку с соответствующим сообщением.
4. Статусы могут быть только в статусах в процессе|отправлен|доставлен .
5. Цена и кол-во продукта или кол-во продуктов в заказе также проверяется.
~~~

### Использованные технологии

* Python 3.12
* FastApi 0.115.0
* Alembic 1.13.3
* Pytest 8.3.3
* SQLAlchemy 2.0.35
* Docker
* Docker-compose
* Postgres

### Автор

[Кирилл Киселев](https://github.com/kirillkiselev-slim)



