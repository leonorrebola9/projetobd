USE projeto;
GO

-- Garante que não há nomes duplicados
ALTER TABLE Asteroid
ADD CONSTRAINT UQ_Asteroid_FullName UNIQUE (full_name);
GO