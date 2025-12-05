USE projeto;
GO

-- 1. SP para Observation_Center
CREATE OR ALTER PROCEDURE SP_InserirObservationCenter
    @name VARCHAR(100),
    @latitude FLOAT,
    @longitude FLOAT,
    @altitude FLOAT
AS
BEGIN
    SET NOCOUNT ON;
    DECLARE @NewID INT;

    -- 1. Verifica se o centro já existe pelo NOME
    SELECT @NewID = Center_ID FROM Observation_Center WHERE name = @name;

    -- 2. Se não existir, insere
    IF @NewID IS NULL
    BEGIN
        INSERT INTO Observation_Center (name, latitude, longitude, altitude)
        VALUES (@name, @latitude, @longitude, @altitude);

        SET @NewID = SCOPE_IDENTITY();
    END
    ELSE
    BEGIN
        -- Se já existe, atualiza coordenadas (caso tenham sido corrigidas)
        UPDATE Observation_Center 
        SET latitude = @latitude, longitude = @longitude, altitude = @altitude
        WHERE Center_ID = @NewID;
    END

    -- 3. Retorna o ID
    SELECT @NewID AS Center_ID;
END
GO