USE projeto;
GO

-- 6. SP para Alert
CREATE OR ALTER PROCEDURE SP_InserirAlert
    @priority VARCHAR(50),
    @torino_scale INT,
    @status VARCHAR(20),
    @dap DATE,
    @Asteroid_ID INT,
    @Orbital_ID INT
AS
BEGIN
    SET NOCOUNT ON;
    DECLARE @NewID INT;

    -- Verifica se já existe um alerta para este asteroide nesta data específica
    SELECT @NewID = Alert_ID 
    FROM Alert 
    WHERE Asteroid_ID = @Asteroid_ID AND dap = @dap;

    IF @NewID IS NULL
    BEGIN
        INSERT INTO Alert (priority, torino_scale, status, dap, Asteroid_ID, Orbital_ID)
        VALUES (@priority, @torino_scale, @status, @dap, @Asteroid_ID, @Orbital_ID);

        SET @NewID = SCOPE_IDENTITY();
    END
    ELSE
    BEGIN
        -- Atualiza o estado do alerta existente
        UPDATE Alert 
        SET priority = @priority, torino_scale = @torino_scale, status = @status, Orbital_ID = @Orbital_ID
        WHERE Alert_ID = @NewID;
    END

    SELECT @NewID AS Alert_ID;
END
GO