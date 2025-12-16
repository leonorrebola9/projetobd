USE projeto;
GO

-- 1. APAGAR ASTEROIDE
-- Apagar um asteroide implica apagar TUDO o que se sabe sobre ele.
CREATE OR ALTER PROCEDURE SP_ApagarAsteroid
    @Asteroid_ID INT
AS
BEGIN
    -- 1. Apagar filhos diretos
    DELETE FROM Alert WHERE Asteroid_ID = @Asteroid_ID;
    DELETE FROM Orbital_Parameter WHERE Asteroid_ID = @Asteroid_ID;
    
    -- 2. Apagar Observações (são muitas!)
    DELETE FROM Observation WHERE Asteroid_ID = @Asteroid_ID;

    -- 3. Finalmente, apagar o pai
    DELETE FROM Asteroid WHERE Asteroid_ID = @Asteroid_ID;

END
GO

-- 2. APAGAR OBSERVAÇÃO (Simples)
CREATE OR ALTER PROCEDURE SP_ApagarObservacao
    @Observation_ID INT
AS
BEGIN
    DELETE FROM Observation WHERE Observation_ID = @Observation_ID;
END
GO

-- 3. APAGAR ASTRÓNOMO (Com Proteção de Histórico)
CREATE OR ALTER PROCEDURE SP_ApagarAstronomo
    @Astronomer_ID INT
AS
BEGIN
    -- Se este astrónomo fez observações, não queremos perder o registo delas.
    -- Vamos definir o autor dessas observações como NULL (ou podias pôr um ID "Desconhecido")
    
    IF EXISTS (SELECT 1 FROM Observation WHERE Astronomer_ID = @Astronomer_ID)
    BEGIN
        UPDATE Observation 
        SET Astronomer_ID = NULL 
        WHERE Astronomer_ID = @Astronomer_ID;
        
    END

    DELETE FROM Astronomer WHERE Astronomer_ID = @Astronomer_ID;
END
GO

-- 4. APAGAR EQUIPAMENTO (Proteção de Logística)
CREATE OR ALTER PROCEDURE SP_ApagarEquipamento
    @Equipment_ID INT
AS
BEGIN
    -- Se o equipamento foi usado, movemos as observações para o ID 1 (Genérico)
    IF EXISTS (SELECT 1 FROM Observation WHERE Equipment_ID = @Equipment_ID)
    BEGIN
        UPDATE Observation 
        SET Equipment_ID = 1 
        WHERE Equipment_ID = @Equipment_ID;
        
    END

    DELETE FROM Equipment WHERE Equipment_ID = @Equipment_ID;
END
GO

-- 5. APAGAR SOFTWARE (Proteção de Dados)
CREATE OR ALTER PROCEDURE SP_ApagarSoftware
    @Software_ID INT
AS
BEGIN
    -- Se o software foi usado, movemos para o ID 1 (Genérico)
    IF EXISTS (SELECT 1 FROM Observation WHERE Software_ID = @Software_ID)
    BEGIN
        UPDATE Observation 
        SET Software_ID = 1 
        WHERE Software_ID = @Software_ID;
        
    END

    DELETE FROM Software WHERE Software_ID = @Software_ID;
END
GO

-- 6. APAGAR CENTRO (Proteção Dupla: Equipamentos e Pessoas)
CREATE OR ALTER PROCEDURE SP_ApagarCentro
    @Center_ID INT
AS
BEGIN
    -- 1. Salvar os Equipamentos (Mover para Centro 1)
    UPDATE Equipment SET Center_ID = 1 WHERE Center_ID = @Center_ID;
    
    -- 2. Salvar os Astrónomos (Mover para Centro 1)
    UPDATE Astronomer SET Center_ID = 1 WHERE Center_ID = @Center_ID;

    -- 3. Apagar o Centro
    DELETE FROM Observation_Center WHERE Center_ID = @Center_ID;
    
END
GO

-- 7. APAGAR ALERTA
CREATE OR ALTER PROCEDURE SP_ApagarAlerta
    @Alert_ID INT
AS
BEGIN
    DELETE FROM Alert WHERE Alert_ID = @Alert_ID;
END
GO

-- 8. APAGAR ÓRBITA
CREATE OR ALTER PROCEDURE SP_ApagarOrbita
    @Orbital_ID INT
AS
BEGIN
    DELETE FROM Orbital_Parameter WHERE Orbital_ID = @Orbital_ID;
END
GO