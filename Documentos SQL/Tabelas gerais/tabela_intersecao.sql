USE projeto;
GO

-- Criar a tabela dbo.dados e eliminar caso exista
IF OBJECT_ID('dbo.dados', 'U') IS NOT NULL 
    DROP TABLE dbo.dados;
GO

-- Colunas a usar para cada tabela
SELECT 
    -- Colunas proveniente de dbo.neo
    N.h,
    N.albedo,
    CAST(N.name AS VARCHAR(200)) AS Name_Neo, 
    N.diameter,
    N.diameter_sigma,
    N.pha,
    N.neo,
    N.epoch_cal,
    N.sigma_i,
    N.i,
    N.epoch,
    N.e,
    N.sigma_e,
    N.moid_ld,
    N.rms,
    N.a,
    N.sigma_a,
    N.q,
    N.sigma_q,
    N.tp_cal,
    N.sigma_tp,

    -- Colunas proveniente de dbo.MPCORB
    M.Arc,
    M.Opp,
    M.Computer,
    M.Obs,
    M.M AS Mean_Anomaly_MPCORB, 
    
    -- Nome MPCORB
    LTRIM(RTRIM(CAST(M.Nome AS VARCHAR(MAX)))) AS Name_MPCORB

-- Inserção dos dados para dbo.dados
INTO dbo.dados 
FROM dbo.neo AS N
INNER JOIN dbo.MPCORB AS M
    ON REPLACE(REPLACE(REPLACE(CAST(N.name AS VARCHAR(MAX)), ' ', ''), '(', ''), ')', '') 
       = 
       REPLACE(REPLACE(REPLACE(CAST(M.Nome AS VARCHAR(MAX)), ' ', ''), '(', ''), ')', '');

-- Criar Primary Key
ALTER TABLE dbo.dados ADD id INT IDENTITY PRIMARY KEY;