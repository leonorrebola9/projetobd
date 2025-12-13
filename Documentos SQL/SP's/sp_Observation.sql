USE projeto;
GO

-- 7. SP para Observation
CREATE OR ALTER PROCEDURE SP_InserirObservation
    @arc_days FLOAT,
    @num_obs INT,
    @Asteroid_ID INT,
    @Equipment_ID INT,
    @Software_ID INT
AS
BEGIN
    SET NOCOUNT ON;
    DECLARE @NewID INT;

    -- Tenta encontrar uma observação idêntica (mesmo asteroide, mesmo equipamento, mesmos valores)
    -- Isto evita duplicar dados se correres o script duas vezes
    SELECT @NewID = Observation_ID 
    FROM Observation 
    WHERE Asteroid_ID = @Asteroid_ID 
      AND Equipment_ID = @Equipment_ID 
      AND Software_ID = @Software_ID
      AND num_obs = @num_obs; -- Verificação extra para garantir que é o mesmo registo

    IF @NewID IS NULL
    BEGIN
        INSERT INTO Observation (arc_days, num_obs, Asteroid_ID, Equipment_ID, Software_ID)
        VALUES (@arc_days, @num_obs, @Asteroid_ID, @Equipment_ID, @Software_ID);

        SET @NewID = SCOPE_IDENTITY();
    END
    -- Nota: Geralmente observações históricas não se atualizam, ou existem ou não.

    SELECT @NewID AS Observation_ID;
END
GO