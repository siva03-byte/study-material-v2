-- ======================================
-- ROLE ENUM TYPE
-- ======================================

CREATE TYPE user_role AS ENUM ('student','teacher','admin');

CREATE TYPE note_type_enum AS ENUM ('online','written','video');

-- ======================================
-- USERS TABLE
-- ======================================

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role user_role NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ======================================
-- DEPARTMENTS TABLE
-- ======================================

CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL
);

-- ======================================
-- SUBJECTS TABLE
-- ======================================

CREATE TABLE subjects (
    id SERIAL PRIMARY KEY,
    subject_name VARCHAR(150) NOT NULL,
    department_id INTEGER REFERENCES departments(id) ON DELETE CASCADE
);

-- ======================================
-- TOPICS TABLE
-- ======================================

CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    topic_name VARCHAR(200) NOT NULL,
    subject_id INTEGER REFERENCES subjects(id) ON DELETE CASCADE
);

-- ======================================
-- NOTES TABLE
-- ======================================

CREATE TABLE notes (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    file_path VARCHAR(255),
    video_link VARCHAR(255),
    note_type note_type_enum NOT NULL,
    subject_id INTEGER REFERENCES subjects(id) ON DELETE CASCADE,
    topic_id INTEGER REFERENCES topics(id) ON DELETE CASCADE,
    uploaded_by INTEGER REFERENCES users(id) ON DELETE CASCADE,
    downloads INTEGER DEFAULT 0,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ======================================
-- DOWNLOAD LOG TABLE
-- ======================================

CREATE TABLE downloads (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    note_id INTEGER REFERENCES notes(id),
    downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ======================================
-- SAMPLE DATA
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
('System Admin','admin@mail.com','admin123','admin'),
('Student User','student@mail.com','123456','student');

-- Notes
INSERT INTO notes (title,file_path,video_link,note_type,subject_id,topic_id,uploaded_by) VALUES
('Linked List Notes','uploads/linkedlist.pdf',NULL,'written',1,1,1),
('Stack Tutorial Video',NULL,'https://youtube.com/video','video',1,2,1),
('SQL Introduction','uploads/sql_notes.pdf',NULL,'online',3,4,1);