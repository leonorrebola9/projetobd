-- ALTERAÇÃO NO SEU SP_InserirAsteroide
CREATE PROCEDURE SP_InserirAsteroide
    @full_name VARCHAR(100),
    @neo CHAR(1),
    @pha CHAR(1),
    @diameter FLOAT,
    @H FLOAT,
    @albedo FLOAT
AS
BEGIN
    DECLARE @AsteroidID INT;

    -- 1. TENTA OBTER O ID SE JÁ EXISTIR (baseado no full_name)
    SELECT @AsteroidID = Asteroid_ID FROM Asteroid WHERE full_name = @full_name;

    -- 2. SE NÃO EXISTIR, INSERE UM NOVO ASTEROIDE
    IF @AsteroidID IS NULL
    BEGIN
        INSERT INTO Asteroid (full_name, neo, pha, diameter, H, albedo)
        VALUES (@full_name, @neo, @pha, @diameter, @H, @albedo);
        
        -- Obtém o ID que acabou de ser gerado
        SET @AsteroidID = SCOPE_IDENTITY();
    END
    -- ELSE: O asteroide já existe, @AsteroidID contém o ID existente.

    -- 3. RETORNA O ID (existente ou novo) para o Python usar nas tabelas filhas
    SELECT @AsteroidID AS Resulting_Asteroid_ID;
END
GO