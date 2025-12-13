CREATE SCHEMA Logins
GO

-- 2. Criar a tabela DENTRO desse Schema
CREATE TABLE Logins.Users (
    users_id INT IDENTITY(1,1) PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(64) NOT NULL,
    );
GO