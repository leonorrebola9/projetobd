-- Valores para a tabela Observation_Center
-- Criar Centro Padrão
INSERT INTO Observation_Center (name, latitude, longitude, altitude)
VALUES ('Minor Planet Center (General)', 0.0, 0.0, 0.0);
-- Guardar o ID
DECLARE @CenterID INT = SCOPE_IDENTITY();
-- Criar Equipamento Padrão
INSERT INTO Equipment (name, type, Center_ID)
VALUES ('Generic Telescope', 'Optical', @CenterID);


-- Valores para a tabela Software
INSERT INTO Software (Computer)
SELECT Computer
FROM dbo.MPCORB
WHERE Computer IS NOT NULL;


-- Valores para a tabela Asteroid
INSERT INTO Asteroid (full_name, H, albedo, diameter, diameter_sigma, pha, neo, epoch_cal)
SELECT 
    CAST(full_name AS VARCHAR(100)), -- Garante que o nome também passa para Varchar
    TRY_CAST(CAST(h AS VARCHAR(50)) AS FLOAT),
    TRY_CAST(CAST(albedo AS VARCHAR(50)) AS FLOAT),
    TRY_CAST(CAST(diameter AS VARCHAR(50)) AS FLOAT),
    TRY_CAST(CAST(diameter_sigma AS VARCHAR(50)) AS FLOAT),
    CAST(pha AS VARCHAR(5)),
    CAST(neo AS VARCHAR(5)),
    TRY_CAST(CAST(epoch_cal AS VARCHAR(50)) AS FLOAT)
FROM dbo.neo
WHERE full_name IS NOT NULL
  AND CAST(full_name AS VARCHAR(100)) NOT IN (SELECT full_name FROM Asteroid);


-- Valores para a tabela Orbital_Parameter
INSERT INTO Orbital_Parameter (
    Asteroid_ID, epoch, e, sigma_e, a, sigma_a, q, sigma_q, 
    i, sigma_i, M, sigma_ma, moid_ld, rms, tp_cal, sigma_tp
)
SELECT 
    A.Asteroid_ID,
    TRY_CAST(CAST(N.epoch AS VARCHAR(50)) AS FLOAT),
    TRY_CAST(CAST(N.e AS VARCHAR(50)) AS FLOAT),
    TRY_CAST(CAST(N.sigma_e AS VARCHAR(50)) AS FLOAT),
    TRY_CAST(CAST(N.a AS VARCHAR(50)) AS FLOAT),
    TRY_CAST(CAST(N.sigma_a AS VARCHAR(50)) AS FLOAT),
    TRY_CAST(CAST(N.q AS VARCHAR(50)) AS FLOAT),
    TRY_CAST(CAST(N.sigma_q AS VARCHAR(50)) AS FLOAT),
    TRY_CAST(CAST(N.i AS VARCHAR(50)) AS FLOAT),
    TRY_CAST(CAST(N.sigma_i AS VARCHAR(50)) AS FLOAT),
    TRY_CAST(CAST(N.ma AS VARCHAR(50)) AS FLOAT),       
    TRY_CAST(CAST(N.sigma_ma AS VARCHAR(50)) AS FLOAT),
    TRY_CAST(CAST(N.moid_ld AS VARCHAR(50)) AS FLOAT),
    TRY_CAST(CAST(N.rms AS VARCHAR(50)) AS FLOAT),
    TRY_CAST(CAST(N.tp_cal AS VARCHAR(50)) AS FLOAT),
    TRY_CAST(CAST(N.sigma_tp AS VARCHAR(50)) AS FLOAT)
FROM dbo.neo AS N
INNER JOIN Asteroid AS A 
    ON CAST(N.full_name AS VARCHAR(100)) = A.full_name;


-- Valores para a tabela Observation
-- Buscar ID do equipamento genérico
-- 1. Buscar ID do equipamento genérico (obrigatório para a Foreign Key)
DECLARE @EquipID INT = (SELECT TOP 1 Equipment_ID FROM Equipment);

INSERT INTO Observation (Asteroid_ID, Equipment_ID, Software_ID, arc, num_obs)
SELECT TOP 958524   -- podes ajustar
    A.Asteroid_ID,
    @EquipID,
    S.Software_ID,
    TRY_CAST(CAST(M.Arc AS VARCHAR(50)) AS FLOAT),
    TRY_CAST(CAST(M.Obs AS VARCHAR(50)) AS INT)
FROM dbo.MPCORB AS M
INNER JOIN dbo.neo AS N 
    ON CAST(M.Desn AS VARCHAR(50)) = CAST(N.pdes AS VARCHAR(50))
INNER JOIN Asteroid AS A 
    ON CAST(N.full_name AS VARCHAR(100)) = A.full_name
LEFT JOIN Software AS S 
    ON CAST(M.Computer AS VARCHAR(100)) = S.Computer;