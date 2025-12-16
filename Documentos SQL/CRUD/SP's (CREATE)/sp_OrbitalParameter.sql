USE projeto;
GO

CREATE OR ALTER PROCEDURE SP_InserirOrbitalParameter
    -- 1. Lista Completa de Parâmetros (Adicionei os 'sigma')
    @Asteroid_ID INT,
    @epoch FLOAT,
    @e FLOAT,
    @sigma_e FLOAT = NULL, -- Novo (pode ser NULL se não tiveres o dado)
    @a FLOAT,
    @sigma_a FLOAT = NULL, -- Novo
    @q FLOAT,
    @sigma_q FLOAT = NULL, -- Novo
    @i FLOAT,
    @sigma_i FLOAT = NULL, -- Novo
    @M FLOAT,
    @sigma_ma FLOAT = NULL, -- Novo (sigma_ma na imagem)
    @moid_ld FLOAT,
    @rms FLOAT,
    @tp_cal FLOAT,
    @sigma_tp FLOAT = NULL -- Novo
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Verifica se já existem parâmetros orbitais para este asteroide
    IF EXISTS (SELECT 1 FROM Orbital_Parameter WHERE Asteroid_ID = @Asteroid_ID)
    BEGIN
        -- ATUALIZA (Incluindo as colunas sigma)
        UPDATE Orbital_Parameter
        SET 
            epoch = @epoch, 
            e = @e, 
            sigma_e = @sigma_e, -- Novo
            a = @a, 
            sigma_a = @sigma_a, -- Novo
            q = @q, 
            sigma_q = @sigma_q, -- Novo
            i = @i, 
            sigma_i = @sigma_i, -- Novo
            M = @M, 
            sigma_ma = @sigma_ma, -- Novo
            moid_ld = @moid_ld, 
            rms = @rms, 
            tp_cal = @tp_cal,
            sigma_tp = @sigma_tp -- Novo
        WHERE Asteroid_ID = @Asteroid_ID;
        
        -- Retorna o ID existente
        SELECT Orbital_ID FROM Orbital_Parameter WHERE Asteroid_ID = @Asteroid_ID;
    END
    ELSE
    BEGIN
        -- INSERE (Incluindo as colunas sigma)
        INSERT INTO Orbital_Parameter (
            Asteroid_ID, epoch, e, sigma_e, a, sigma_a, q, sigma_q, 
            i, sigma_i, M, sigma_ma, moid_ld, rms, tp_cal, sigma_tp
        )
        VALUES (
            @Asteroid_ID, @epoch, @e, @sigma_e, @a, @sigma_a, @q, @sigma_q, 
            @i, @sigma_i, @M, @sigma_ma, @moid_ld, @rms, @tp_cal, @sigma_tp
        );
        
        -- Retorna o novo ID
        SELECT SCOPE_IDENTITY() AS Orbital_ID;
    END
END
GO