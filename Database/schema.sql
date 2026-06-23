CREATE DATABASE kmp_task_management;

USE kmp_task_management;

-- USERS 
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY, --user id automatically generated
    username VARCHAR(50) UNIQUE NOT NULL, --user name can not be null and have to be unique
    password VARCHAR(255) NOT NULL, --password can not be null
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);

-- TASKS
CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY, --Task identifier
    title VARCHAR(200) NOT NULL, --title can not be null
    description TEXT, --Task description
    due_date DATETIME, --Task deadline 
    status ENUM('PENDING','COMPLETED') DEFAULT 'PENDING', --status. default "pending"

    created_by INT NOT NULL, --The user who created the task. By ID
    assigned_to INT, --User responsible for executing 

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 

    FOREIGN KEY (created_by) REFERENCES users(id), --foreign key to identify created_by using user id from users table
    FOREIGN KEY (assigned_to) REFERENCES users(id) --foreign key to identify assigned_to using user id from users table
);

-- SUBTASKS
CREATE TABLE subtasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task_id INT NOT NULL,
    