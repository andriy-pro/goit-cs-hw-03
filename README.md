# goit-cs-hw-03
Repository for the homework solution from the GoIT course 'Computer Systems and Their Fundamentals', HW-3.


Створення контейнера:
docker run --name postgress-cs-hw-03 -p 5432:5432 -e POSTGRES_PASSWORD=goit -d postgres

Запуск контейнера, якщо він був створений раніше, але зараз не працює (наприклад, після перезапуску):
docker start postgress-cs-hw-03

Для зручності роботи у терміналі, було встановлено PostgreSQL Client (Ubuntu):
sudo apt update
sudo apt install postgresql-client-common postgresql-client
psql --version

Підключення до сервера PostgreSQL для перевірки:
psql -h localhost -p 5432 -U postgres

Список доступних баз даних (в консолі PostgreSQL):
\l

Створення бази даних
CREATE DATABASE task_management;

Виконання скрипту schema.sql:
psql -h localhost -p 5432 -U postgres -d task_management -f schema.sql

Якщо потрібно підключитися до бази даних task_management для перевірки її структури:
psql -h localhost -p 5432 -U postgres -d task_management

Список створених таблиць:
\dt

Видали дані з таблиць (із урахуванням залежностей):
TRUNCATE TABLE tasks, users, status RESTART IDENTITY CASCADE;

Перевірка кількості записів у таблицях:
SELECT COUNT(*) FROM tasks;
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM status;

