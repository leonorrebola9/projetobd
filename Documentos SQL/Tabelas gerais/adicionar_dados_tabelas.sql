-- Inserir dados na tabela dbo.Software
USE projeto;
GO

INSERT INTO Software (Computer)
SELECT DISTINCT 
    CAST(Computer AS VARCHAR(100)) -- O segredo: Converter para VARCHAR
FROM dbo.dados
WHERE Computer IS NOT NULL 
  AND NOT EXISTS (
      SELECT 1 FROM Software S 
      WHERE S.Computer = CAST(dbo.dados.Computer AS VARCHAR(100))
  );

-- Inserir dados na tabela dbo.Asteroid
USE projeto;
GO

INSERT INTO Asteroid (full_name, diameter, albedo, pha, neo, h)
SELECT DISTINCT 
    CAST(Name_Neo AS VARCHAR(MAX)), -- Nome
    CAST(diameter AS VARCHAR(MAX)), -- Diâmetro (se for TEXT, tem de levar CAST)
    CAST(albedo   AS VARCHAR(MAX)), -- Albedo
    CAST(pha      AS VARCHAR(MAX)), -- PHA
    CAST(neo      AS VARCHAR(MAX)), -- NEO
    CAST(h        AS VARCHAR(MAX))  -- H
FROM dbo.dados
WHERE NOT EXISTS (
    SELECT 1 FROM Asteroid A 
    WHERE CAST(A.full_name AS VARCHAR(MAX)) = CAST(dbo.dados.Name_Neo AS VARCHAR(MAX))
);

-- Inserir dados na tabela dbo.Orbital_Parameter
USE projeto;
GO

INSERT INTO Orbital_Parameter (
    Asteroid_ID, 
    e, 
    a, 
    i, 
    q, 
    M,      
    epoch, 
    moid_ld
)
SELECT 
    A.Asteroid_ID,
    TRY_CAST(CAST(D.e AS VARCHAR(MAX)) AS FLOAT),
    TRY_CAST(CAST(D.a AS VARCHAR(MAX)) AS FLOAT),
    TRY_CAST(CAST(D.i AS VARCHAR(MAX)) AS FLOAT),
    TRY_CAST(CAST(D.q AS VARCHAR(MAX)) AS FLOAT),
    TRY_CAST(CAST(D.Mean_Anomaly_MPCORB AS VARCHAR(MAX)) AS FLOAT),
    TRY_CAST(CAST(D.epoch AS VARCHAR(MAX)) AS FLOAT),
    TRY_CAST(CAST(D.moid_ld AS VARCHAR(MAX)) AS FLOAT)

FROM dbo.dados AS D
INNER JOIN Asteroid AS A 
    ON CAST(A.full_name AS VARCHAR(MAX)) = CAST(D.Name_Neo AS VARCHAR(MAX))
WHERE NOT EXISTS (
    SELECT 1 FROM Orbital_Parameter OP WHERE OP.Asteroid_ID = A.Asteroid_ID
);
-- Adicionar coluna rms a Orbiatl_Parameter (esquecimento)
USE projeto;
GO

-- 1. Adicionar coluna rms se não existir
IF COL_LENGTH('Orbital_Parameter', 'rms') IS NULL
BEGIN
    ALTER TABLE Orbital_Parameter ADD rms FLOAT;
END
GO
-- 2. Preencher o rms vindo da tabela dados
UPDATE OP
SET OP.rms = TRY_CAST(CAST(D.rms AS VARCHAR(MAX)) AS FLOAT)
FROM Orbital_Parameter OP
INNER JOIN Asteroid A ON OP.Asteroid_ID = A.Asteroid_ID
INNER JOIN dbo.dados D ON CAST(A.full_name AS VARCHAR(MAX)) = CAST(D.Name_Neo AS VARCHAR(MAX));

-- Inserção de dados na dbo.Observation
USE projeto;
GO

DECLARE @DefaultEquipID INT = 1; -- Generic Telescope

INSERT INTO Observation (Asteroid_ID, Software_ID, Equipment_ID, num_obs, arc)
SELECT 
    A.Asteroid_ID,
    S.Software_ID,
    @DefaultEquipID,
    
    TRY_CAST(CAST(D.Obs AS VARCHAR(MAX)) AS INT),
    
    TRY_CAST(CAST(D.Arc AS VARCHAR(MAX)) AS FLOAT)

FROM dbo.dados AS D
INNER JOIN Asteroid AS A 
    ON CAST(A.full_name AS VARCHAR(MAX)) = CAST(D.Name_Neo AS VARCHAR(MAX))
LEFT JOIN Software AS S 
    ON CAST(S.Computer AS VARCHAR(MAX)) = CAST(D.Computer AS VARCHAR(MAX)) 
-- Evita duplicados
WHERE NOT EXISTS (
    SELECT 1 FROM Observation O 
    WHERE O.Asteroid_ID = A.Asteroid_ID
);