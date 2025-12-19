-- Escolher de forma aleatória os centros para cada astrónomo
USE projeto;
GO

-- Usa o ID do astrónomo para os dados aleatórios
UPDATE Astronomer
SET Center_ID = (
    SELECT TOP 1 Center_ID 
    FROM Observation_Center 
    -- O CHECKSUM obriga a re-avaliar porque depende do ID de cada linha
    ORDER BY CHECKSUM(NEWID(), Astronomer.Astronomer_ID)
);

SELECT 
    A.name AS [Nome do Astronomo], 
    C.name AS [Trabalha no Centro]
FROM Astronomer A
INNER JOIN Observation_Center C ON A.Center_ID = C.Center_ID;



-- Escolher de forma aleatória os equipamentos para cada observação
USE projeto;
GO

-- Atualiza a tabela Observation
UPDATE Observation
SET Equipment_ID = (
    SELECT TOP 1 Equipment_ID 
    FROM Equipment
    -- O 'CHECKSUM' usa o ID da Observação para garantir que cada linha
    -- tem um sorteio diferente, evitando que fiquem todos iguais.
    ORDER BY CHECKSUM(NEWID(), Observation.Observation_ID)
);

-- Ver quantos asteroides ficaram em cada telescópio/equipamento
SELECT 
    E.name AS [Nome do Equipamento], 
    COUNT(*) AS [Qtd Observações]
FROM Observation O
JOIN Equipment E ON O.Equipment_ID = E.Equipment_ID
GROUP BY E.name
ORDER BY [Qtd Observações] DESC;