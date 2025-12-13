USE projeto;
GO

-- 4. SP para Obrital_Parameter
CREATE OR ALTER PROCEDURE SP_InserirOrbitalParameter
    @Asteroid_ID INT,
    @epoch FLOAT,
    @e FLOAT,
    @a FLOAT,
    @q FLOAT,
    @i FLOAT,
    @M FLOAT,
    @moid_ld FLOAT,
    @rms FLOAT,
    @tp_cal FLOAT
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Verifica se já existem parâmetros orbitais para este asteroide
    -- Assumimos uma relação 1:1 (um asteroide tem um conjunto de parâmetros atuais)
    IF EXISTS (SELECT 1 FROM Orbital_Parameter WHERE Asteroid_ID = @Asteroid_ID)
    BEGIN
        -- Atualiza
        UPDATE Orbital_Parameter
        SET epoch = @epoch, e = @e, a = @a, q = @q, i = @i, 
            M = @M, moid_ld = @moid_ld, rms = @rms, tp_cal = @tp_cal
        WHERE Asteroid_ID = @Asteroid_ID;
        
        -- Retorna o ID existente
        SELECT Orbital_ID FROM Orbital_Parameter WHERE Asteroid_ID = @Asteroid_ID;
    END
    ELSE
    BEGIN
        -- Insere
        INSERT INTO Orbital_Parameter (Asteroid_ID, epoch, e, a, q, i, M, moid_ld, rms, tp_cal)
        VALUES (@Asteroid_ID, @epoch, @e, @a, @q, @i, @M, @moid_ld, @rms, @tp_cal);
        
        -- Retorna o novo ID
        SELECT SCOPE_IDENTITY() AS Orbital_ID;
    END
END
GO