CREATE DATABASE CRUD_VS;

USE CRUD_VS;

CREATE TABLE mainmysql_user (
    id INT AUTO_INCREMENT PRIMARY KEY,   -- auto increment id
    name VARCHAR(255) NOT NULL,          -- user name (required)
    email VARCHAR(255) NOT NULL,         -- user email (required)
    is_active BOOLEAN DEFAULT FALSE      -- default value = false
);

SELECT * FROM mainmysql_user;
