USE projeto;
GO

-- 3. SP para Asteroid
CREATE OR ALTER PROCEDURE SP_InserirAsteroid
    @full_name VARCHAR(100),
    @neo CHAR(1),
    @pha CHAR(1),
    @diameter FLOAT,
    @H FLOAT,
    @albedo FLOAT
AS
BEGIN
    SET NOCOUNT ON;
    DECLARE @NewID INT;

    -- 1. Verifica se já existe pelo NOME COMPLETO
    SELECT @NewID = Asteroid_ID FROM Asteroid WHERE full_name = @full_name;

    -- 2. Se não existir, insere
    IF @NewID IS NULL
    BEGIN
        INSERT INTO Asteroid (full_name, neo, pha, diameter, H, albedo)
        VALUES (@full_name, @neo, @pha, @diameter, @H, @albedo);

        SET @NewID = SCOPE_IDENTITY(); -- Guarda o ID criado
    END
    ELSE
    BEGIN
        -- Se já existe, atualiza os dados
        UPDATE Asteroid 
        SET diameter = @diameter, H = @H, albedo = @albedo, pha = @pha, neo = @neo
        WHERE Asteroid_ID = @NewID;
    END

    -- 3. Retorna o ID interno para o Python
    SELECT @NewID AS Asteroid_ID;
END
GO