CREATE TABLE users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    surname VARCHAR(50) NOT NULL,
    [user] VARCHAR(50) NOT NULL UNIQUE,
    passw VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT GETDATE() 
    );

    select * from users;