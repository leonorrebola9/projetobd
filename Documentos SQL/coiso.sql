USE projeto;
GO

-- Adicionar a coluna Astronomer_ID na tabela de Observações
ALTER TABLE Observation
ADD Astronomer_ID INT;
GO

USE projeto;
GO

-- Atualiza todas as linhas da tabela Observation
UPDATE Observation
SET Astronomer_ID = (
    SELECT TOP 1 Astronomer_ID 
    FROM Astronomer 
    -- O CHECKSUM obriga o SQL a sortear um novo astrónomo para cada linha
    ORDER BY CHECKSUM(NEWID(), Observation.Observation_ID)
);

USE projeto;
GO

UPDATE Astronomer
SET Observation_ID = (
    SELECT TOP 1 Observation_ID 
    FROM Observation 
    -- O 'CHECKSUM' usa o ID do Astrónomo como "semente" para garantir
    -- que o sorteio é diferente para cada pessoa.
    ORDER BY CHECKSUM(NEWID(), Astronomer.Astronomer_ID)
);