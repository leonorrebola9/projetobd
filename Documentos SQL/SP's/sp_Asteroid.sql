USE projeto;
GO

-- 3. SP para Asteroid (Atualizada com colunas da imagem)
CREATE OR ALTER PROCEDURE SP_InserirAsteroid
    @full_name VARCHAR(100),
    @neo CHAR(1),
    @pha CHAR(1),
    @diameter FLOAT,
    @H FLOAT,
    @albedo FLOAT,
    -- Novos campos detetados na imagem:
    @diameter_sigma FLOAT = NULL, -- Pode ser NULL
    @epoch_cal FLOAT = NULL       -- Pode ser NULL
AS
BEGIN
    SET NOCOUNT ON;
    DECLARE @NewID INT;

    -- 1. Verifica se já existe pelo NOME COMPLETO
    SELECT @NewID = Asteroid_ID FROM Asteroid WHERE full_name = @full_name;

    -- 2. Se não existir, insere (INCLUINDO OS NOVOS CAMPOS)
    IF @NewID IS NULL
    BEGIN
        INSERT INTO Asteroid (
            full_name, neo, pha, diameter, H, albedo, 
            diameter_sigma, epoch_cal
        )
        VALUES (
            @full_name, @neo, @pha, @diameter, @H, @albedo, 
            @diameter_sigma, @epoch_cal
        );

        SET @NewID = SCOPE_IDENTITY(); -- Guarda o ID criado
    END
    ELSE
    BEGIN
        -- Se já existe, atualiza os dados todos (INCLUINDO OS NOVOS)
        UPDATE Asteroid 
        SET 
            diameter = @diameter, 
            H = @H, 
            albedo = @albedo, 
            pha = @pha, 
            neo = @neo,
            diameter_sigma = @diameter_sigma, -- Novo
            epoch_cal = @epoch_cal            -- Novo
        WHERE Asteroid_ID = @NewID;
    END

    -- 3. Retorna o ID interno para a aplicação
    SELECT @NewID AS Asteroid_ID;
END
GO