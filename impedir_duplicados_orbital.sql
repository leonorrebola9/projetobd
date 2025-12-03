USE projeto;
GO

CREATE OR ALTER PROCEDURE SP_InserirOrbitalParameter
    -- Parâmetros que vêm do Python (total de 9 parâmetros de input)
    @Asteroid_ID INT,           -- 1. FK
    @Orbital_id VARCHAR(255),   -- 2. Não inserido, mas passado pelo Python
    @epoch FLOAT,               -- 3.
    @e FLOAT,                   -- 4.
    @a FLOAT,                   -- 5.
    @i FLOAT,                   -- 6.
    @M FLOAT,                   -- 7.
    @moid_ld FLOAT,             -- 8.
    @rms FLOAT                  -- 9.
AS
BEGIN
    -- Lista de Colunas (O Orbital_ID não é incluído, pois é IDENTITY)
    INSERT INTO Orbital_Parameter (
        Asteroid_ID, epoch, e, a, q, i, M, moid_ld, rms, tp_cal
    )
    VALUES (
        @Asteroid_ID,
        @epoch,
        @e,
        @a,
        0.0,                    -- q FLOAT NOT NULL (Valor Fixo)
        @i,
        @M,
        @moid_ld,
        @rms,
        0.0                     -- tp_cal FLOAT NOT NULL (Valor Fixo)
    );
END
GO

-- Deve retornar o novo ID (ex: 1)
EXEC SP_InserirAsteroide 
    @full_name = 'AsteroideTeste1', 
    @neo = '0', 
    @pha = '0', 
    @diameter = 1.0, 
    @H = 15.0, 
    @albedo = 0.5;

-- Se o anterior funcionou, este deve retornar o mesmo ID (ex: 1)
EXEC SP_InserirAsteroide 
    @full_name = 'AsteroideTeste1', 
    @neo = '0', 
    @pha = '0', 
    @diameter = 1.0, 
    @H = 15.0, 
    @albedo = 0.5;