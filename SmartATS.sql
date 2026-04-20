CREATE DATABASE attendance_db;
USE attendance_db;
CREATE TABLE attendance (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(50),
    date DATE,
    time TIME
);
SELECT * FROM attendance;