-- Ver quantos asteroides conseguem ser ligados
SELECT 
    COUNT(DISTINCT A.Asteroid_ID) as Asteroides_Encontrados,
    COUNT_BIG(DISTINCT CAST(M.Nome1 AS VARCHAR(MAX))) as Nomes_MPCORB
FROM dbo.MPCORB AS M
INNER JOIN Asteroid AS A 
    ON REPLACE(REPLACE(REPLACE(
        ISNULL(CAST(M.Nome1 AS VARCHAR(MAX)), '') + 
        ISNULL(CAST(M.Nome2 AS VARCHAR(MAX)), ''), 
        ' ', ''), '(', ''), ')', '') 
       = 
       REPLACE(REPLACE(REPLACE(A.full_name, ' ', ''), '(', ''), ')', '');

USE projeto;
GO

-- PARTE 1: Inserir observações reais do MPCORB
INSERT INTO Observation (Asteroid_ID, Equipment_ID, Software_ID, arc, num_obs)
SELECT DISTINCT
    A.Asteroid_ID,
    -- Distribuição cíclica pelos 6 equipamentos
    (CASE (ROW_NUMBER() OVER (ORDER BY NEWID())) % 6
        WHEN 0 THEN 1
        WHEN 1 THEN 2
        WHEN 2 THEN 3
        WHEN 3 THEN 4
        WHEN 4 THEN 5
        ELSE 6
    END) as Equipment_ID,
    ISNULL(S.Software_ID, (SELECT TOP 1 Software_ID FROM Software)) as Software_ID,
    TRY_CAST(CAST(M.Arc AS VARCHAR(50)) AS FLOAT) as arc,
    TRY_CAST(CAST(M.Obs AS VARCHAR(50)) AS INT) as num_obs
FROM dbo.MPCORB AS M
INNER JOIN Asteroid AS A 
    ON REPLACE(REPLACE(REPLACE(
        ISNULL(CAST(M.Nome1 AS VARCHAR(MAX)), '') + 
        ISNULL(CAST(M.Nome2 AS VARCHAR(MAX)), ''), 
        ' ', ''), '(', ''), ')', '') 
       = 
       REPLACE(REPLACE(REPLACE(A.full_name, ' ', ''), '(', ''), ')', '')
LEFT JOIN Software AS S 
    ON CAST(M.Computer AS VARCHAR(MAX)) = S.Computer
WHERE TRY_CAST(CAST(M.Arc AS VARCHAR(50)) AS FLOAT) BETWEEN 0.1 AND 100
AND TRY_CAST(CAST(M.Obs AS VARCHAR(50)) AS INT) BETWEEN 1 AND 10000;

-- PARTE 2: Verificar quantas inseriu
DECLARE @ObservacoesReais INT = @@ROWCOUNT;

-- PARTE 3: Completar com observações simuladas (mínimo 30 no total)
DECLARE @TotalDesejado INT = 30;
DECLARE @AInserir INT = @TotalDesejado - @ObservacoesReais;

IF @AInserir > 0
BEGIN
    -- Sequência cíclica de equipamentos 1-6
    WITH Numeros AS (
        SELECT 1 as n UNION SELECT 2 UNION SELECT 3 UNION 
        SELECT 4 UNION SELECT 5 UNION SELECT 6
    ),
    Sequencia AS (
        SELECT TOP (@AInserir)
            ROW_NUMBER() OVER (ORDER BY NEWID()) as seq,
            (CASE (ROW_NUMBER() OVER (ORDER BY NEWID()) - 1) % 6
                WHEN 0 THEN 1
                WHEN 1 THEN 2
                WHEN 2 THEN 3
                WHEN 3 THEN 4
                WHEN 4 THEN 5
                ELSE 6
            END) as Equipment_ID
        FROM Numeros n1
        CROSS JOIN Numeros n2
        CROSS JOIN Numeros n3
    )
    INSERT INTO Observation (Asteroid_ID, Equipment_ID, Software_ID, arc, num_obs)
    SELECT 
        (SELECT TOP 1 Asteroid_ID FROM Asteroid 
         WHERE (pha = 'Y' OR neo = 'Y') 
         ORDER BY NEWID()) as Asteroid_ID,
        S.Equipment_ID,
        CASE WHEN ABS(CHECKSUM(NEWID())) % 3 > 0  -- 66% com software
            THEN (SELECT TOP 1 Software_ID FROM Software ORDER BY NEWID())
            ELSE NULL 
        END as Software_ID,
        ROUND(0.5 + (RAND(CHECKSUM(NEWID())) * 20), 2) as arc, -- 0.5-20.5 anos
        5 + (ABS(CHECKSUM(NEWID())) % 500) as num_obs -- 5-505 observações
    FROM Sequencia S;
END

-- PARTE 4: Verificar distribuição
SELECT 'Distribuição final' as Info;

SELECT 
    E.Equipment_ID,
    E.name as Equipamento,
    COUNT(O.Observation_ID) as Num_Observacoes,
    CAST(COUNT(O.Observation_ID) * 100.0 / NULLIF((SELECT COUNT(*) FROM Observation), 0) AS DECIMAL(5,2)) as Percentagem
FROM Equipment E
LEFT JOIN Observation O ON E.Equipment_ID = O.Equipment_ID
GROUP BY E.Equipment_ID, E.name
ORDER BY E.Equipment_ID;