-- Видалення таблиць, якщо вони вже існують.
-- Використовується CASCADE, щоб видалити залежні дані в інших таблицях.
DROP TABLE IF EXISTS tasks CASCADE;
DROP TABLE IF EXISTS status CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Створення таблиці користувачів (users).
-- Ця таблиця зберігає дані про користувачів системи.
CREATE TABLE users (
    id SERIAL PRIMARY KEY,              -- Унікальний ідентифікатор користувача (автоінкремент).
    fullname VARCHAR(100) NOT NULL,     -- Повне ім'я користувача (обов'язкове поле).
    email VARCHAR(100) UNIQUE NOT NULL  -- Унікальна електронна адреса (обов'язково).
);

-- Створення таблиці статусів (status).
-- Ця таблиця зберігає перелік можливих статусів для завдань.
CREATE TABLE status (
    id SERIAL PRIMARY KEY,           -- Унікальний ідентифікатор статусу (автоінкремент).
    name VARCHAR(50) UNIQUE NOT NULL -- Унікальна назва статусу (обов'язково).
    -- Приклади значень: 'new', 'in progress', 'completed'.
);

-- Створення таблиці завдань (tasks).
-- Містить дані про завдання, які можуть бути призначені користувачам.
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,           -- Унікальний ідентифікатор завдання (автоінкремент).
    title VARCHAR(100) NOT NULL,     -- Назва завдання (обов'язково).
    description TEXT,                -- Опис завдання (НЕ обов'язково).
    status_id INTEGER NOT NULL REFERENCES status (id) 
        ON DELETE RESTRICT           -- Обмеження: статус не можна видалити, якщо він використовується в завданні.
        ON UPDATE CASCADE,           -- Якщо ідентифікатор статусу змінено, він автоматично оновиться у цій таблиці.
    user_id INTEGER NOT NULL REFERENCES users (id) 
        ON DELETE CASCADE            -- Якщо користувача видалено, усі його завдання автоматично видаляються.
        ON UPDATE CASCADE            -- Якщо ідентифікатор користувача змінено, він автоматично оновиться.
);
