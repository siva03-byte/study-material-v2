-- ===============================================================================
-- DATABASE CREATION
-- ======================================

CREATE DATABASE study_material_db;
USE study_material_db;

-- ======================================
-- USERS TABLE
-- ======================================

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('student','teacher','admin') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ======================================
-- DEPARTMENTS TABLE
-- ======================================

CREATE TABLE departments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL
);

-- ======================================
-- SUBJECTS TABLE
-- ======================================

CREATE TABLE subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subject_name VARCHAR(150) NOT NULL,
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES departments(id)
        ON DELETE CASCADE
);

-- ======================================
-- TOPICS TABLE
-- ======================================

CREATE TABLE topics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    topic_name VARCHAR(200) NOT NULL,
    subject_id INT,
    FOREIGN KEY (subject_id) REFERENCES subjects(id)
        ON DELETE CASCADE
);

-- ======================================
-- NOTES TABLE
-- ======================================
-- ======================================
-- NOTES TABLE
-- ======================================

CREATE TABLE notes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    file_path VARCHAR(255),
    video_link VARCHAR(255),
    note_type ENUM('online','written','video') NOT NULL,
    subject_id INT,
    topic_id INT,
    uploaded_by INT,
    downloads INT DEFAULT 0,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (subject_id) REFERENCES subjects(id)
        ON DELETE CASCADE,

    FOREIGN KEY (topic_id) REFERENCES topics(id)
        ON DELETE CASCADE,

    FOREIGN KEY (uploaded_by) REFERENCES users(id)
        ON DELETE CASCADE
);

-- ======================================
-- DOWNLOAD LOG TABLE
-- ======================================

CREATE TABLE downloads (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    note_id INT,
    downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (note_id) REFERENCES notes(id)
);

-- ======================================
-- SAMPLE DATA INSERTION
-- ======================================

-- Departments
INSERT INTO departments (department_name) VALUES
('Computer Science'),
('Information Technology'),
('Electronics and Communication'),
('Mechanical Engineering');

-- Subjects
INSERT INTO subjects (subject_name, department_id) VALUES
('Data Structures',1),
('Operating Systems',1),
('Database Management System',1),
('Computer Networks',2),
('Digital Electronics',3);

-- Topics
INSERT INTO topics (topic_name, subject_id) VALUES
('Linked List',1),
('Stack and Queue',1),
('Process Management',2),
('SQL Basics',3),
('Normalization',3),
('OSI Model',4);

-- Users
INSERT INTO users (name,email,password,role) VALUES
('Admin Teacher','teacher1@mail.com','123456','teacher'),

-- Notes
INSERT INTO notes (title,file_path,note_type,subject_id,topic_id,uploaded_by) VALUES
('Linked List Notes','uploads/linkedlist.pdf','written',1,1,1),
('Stack Tutorial Video','https://youtube.com/video','video',1,2,1),
('SQL Introduction','uploads/sql_notes.pdf','online',3,4,1);
