USE projeto;
GO

-- 7. SP para Observation
CREATE OR ALTER PROCEDURE SP_InserirObservation
    @arc FLOAT,       
    @num_obs INT,
    @Asteroid_ID INT,
    @Equipment_ID INT,
    @Software_ID INT
AS
BEGIN
    SET NOCOUNT ON;
    DECLARE @NewID INT;

    -- Tenta encontrar uma observação idêntica
    SELECT @NewID = Observation_ID 
    FROM Observation 
    WHERE Asteroid_ID = @Asteroid_ID 
      AND Equipment_ID = @Equipment_ID 
      AND Software_ID = @Software_ID
      AND num_obs = @num_obs;

    IF @NewID IS NULL
    BEGIN
        -- CORRIGIDO: Inserir na coluna 'arc' e não 'arc_days'
        INSERT INTO Observation (arc, num_obs, Asteroid_ID, Equipment_ID, Software_ID)
        VALUES (@arc, @num_obs, @Asteroid_ID, @Equipment_ID, @Software_ID);

        SET @NewID = SCOPE_IDENTITY();
    END

    SELECT @NewID AS Observation_ID;
END
GO