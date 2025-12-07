USE projeto;
GO

-- 1. Importar as estações reais da tabela impact
INSERT INTO Observation_Center (name, latitude, longitude, altitude)
SELECT DISTINCT 
    TRIM(CAST(Discovery_station AS VARCHAR(200))), 
    0, 0, 0 -- Coordenadas desconhecidas, metemos a zero
FROM dbo.impact
WHERE Discovery_station IS NOT NULL  
-- Garante que não inserimos repetidos nem o Genérico que já lá está
  AND TRIM(CAST(Discovery_station AS VARCHAR(200))) NOT IN (SELECT name FROM Observation_Center);

-- 2. Criar equipamentos para as estações para estarem na tabela Equipment
INSERT INTO Equipment (name, type, Center_ID)
SELECT 
    LEFT(name + ' Telescope', 100), 
    'Optical', 
    Center_ID
FROM Observation_Center
WHERE name <> 'Minor Planet Center (General)' -- Ignora o Genérico antigo
  AND name NOT IN (SELECT REPLACE(name, ' Telescope', '') FROM Equipment);

-- 3. Distribuição aleatória (CORRIGIDO COM CROSS APPLY E CHECKSUM)
-- Descobrir qual é o ID do equipamento genérico criado anteriormente
DECLARE @GenericID INT = (SELECT TOP 1 Equipment_ID FROM Equipment WHERE name = 'Generic Telescope');

-- Update com um ID random (Usando CROSS APPLY para forçar linha-a-linha)
UPDATE Obs
SET Equipment_ID = Random.Equipment_ID
FROM Observation Obs
CROSS APPLY (
    SELECT TOP 1 Equipment_ID 
    FROM Equipment 
    WHERE Equipment_ID <> @GenericID -- Escolhe qualquer um MENOS o genérico
    -- TRUQUE: O CHECKSUM liga o random ao ID da linha, obrigando a variar sempre!
    ORDER BY CHECKSUM(NEWID(), Obs.Observation_ID) 
) Random
WHERE Obs.Equipment_ID = @GenericID OR Obs.Equipment_ID IN (6, 2);