USE projeto;
GO

-- 8. SP para Astronomer
CREATE OR ALTER PROCEDURE SP_InserirAstronomer
    @name VARCHAR(100),
    @Observation_ID INT,
    @Center_ID INT
AS
BEGIN
    SET NOCOUNT ON;
    DECLARE @NewID INT;

    -- Verifica se este astrónomo já está associado a esta observação específica
    SELECT @NewID = Astronomer_ID 
    FROM Astronomer 
    WHERE name = @name AND Observation_ID = @Observation_ID;

    IF @NewID IS NULL
    BEGIN
        INSERT INTO Astronomer (name, Observation_ID, Center_ID)
        VALUES (@name, @Observation_ID, @Center_ID);

        SET @NewID = SCOPE_IDENTITY();
    END

    SELECT @NewID AS Astronomer_ID;
END
GO