CREATE OR ALTER TRIGGER trg_AutoAlert_Simples
ON Orbital_Parameter
AFTER INSERT, UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    -- Declarar variáveis
    DECLARE @Asteroid_ID INT, @Orbital_ID INT;
    DECLARE @Novo_Dap DATETIME;
    DECLARE @Novo_Torino INT;
    DECLARE @Novo_Status VARCHAR(50);
    DECLARE @Nova_Prioridade VARCHAR(50);
    DECLARE @Nova_Descricao VARCHAR(255);
    
    -- Variáveis auxiliares para os cálculos
    DECLARE @moid FLOAT, @rms FLOAT, @e FLOAT, @i FLOAT;
    DECLARE @diametro FLOAT, @pha CHAR(1), @albedo FLOAT;

    -- Ler os dados da órbita e do asteroide
    SELECT 
        @Asteroid_ID = i.Asteroid_ID,
        @Orbital_ID = i.Orbital_ID,
        @moid = i.moid_ld,
        @rms = i.rms,
        @e = i.e,
        @i = i.i,
        @diametro = A.diameter,
        @pha = A.pha,
        @albedo = A.albedo
    FROM inserted i
    INNER JOIN Asteroid A ON i.Asteroid_ID = A.Asteroid_ID;

    -- Se não houver dados
    IF @Asteroid_ID IS NULL RETURN;
    
    -- Data Aproximação
    SET @Novo_Dap = DATEADD(day, @moid, GETDATE());
    
    -- Torino Scale
    SET @Novo_Torino = CASE 
        WHEN @diametro > 0.03 AND @moid < 1 THEN 4
        WHEN @diametro > 0.05 AND @moid < 5 AND @rms < 0.3 THEN 3
        WHEN @diametro > 0.1 AND @moid BETWEEN 5 AND 20 THEN 2
        WHEN @pha = 'Y' AND @diametro BETWEEN 0.05 AND 0.5 AND @moid BETWEEN 20 AND 100 THEN 1
        ELSE 0 
    END;

    -- Cor / Status
    SET @Novo_Status = CASE 
        WHEN @diametro > 0.03 AND @moid < 1 THEN 'Vermelho'
        WHEN @diametro > 0.05 AND @moid < 5 AND @rms < 0.3 THEN 'Laranja'
        WHEN @diametro > 0.1 AND @moid BETWEEN 5 AND 20 THEN 'Amarelo'
        WHEN @pha = 'Y' AND @diametro BETWEEN 0.05 AND 0.5 AND @moid BETWEEN 20 AND 100 THEN 'Verde'
        ELSE 'Sem Alerta'
    END;

    -- Prioridade
    SET @Nova_Prioridade = CASE 
        WHEN (@moid < 1 AND @diametro > 0.01) 
          OR (@pha = 'Y' AND @diametro > 0.1 AND @rms > 0.8 AND @moid < 20) THEN 'Alta'
        WHEN (@diametro > 0.5 AND @moid < 50)
          OR (@e > 0.05 OR @i > 2) THEN 'Media'
        WHEN (@albedo > 0.3 OR @e > 0.8 OR @i > 70) AND @diametro > 0.2 THEN 'Baixa'
        ELSE 'Normal'
    END;

    SET @Nova_Descricao = 'Alerta Auto (MOID: ' + CAST(CAST(@moid AS DECIMAL(10,2)) AS VARCHAR) + ')';

    -- Guarda a informação
    IF (@diametro > 0.03 AND @moid < 1) OR 
       (@diametro > 0.05 AND @moid < 5 AND @rms < 0.3) OR 
       (@diametro > 0.1 AND @moid BETWEEN 5 AND 20) OR 
       (@pha = 'Y') OR
       (@albedo > 0.3 OR @e > 0.8 OR @i > 70)
    BEGIN
       
        -- Verifica se já existe um alerta para este asteroide
        IF EXISTS (SELECT 1 FROM Alert WHERE Asteroid_ID = @Asteroid_ID)
        BEGIN
            -- Atualiza, caso exista
            UPDATE Alert
            SET 
                Orbital_ID = @Orbital_ID,
                dap = @Novo_Dap,
                torino = @Novo_Torino,
                status = @Novo_Status,
                Priority = @Nova_Prioridade,
                Description = @Nova_Descricao,
                Alert_Date = GETDATE()
            WHERE Asteroid_ID = @Asteroid_ID;
            
        END
        ELSE
        BEGIN
            -- Cria novo, caso exista
            INSERT INTO Alert (Asteroid_ID, Orbital_ID, dap, p, torino, status, Priority, Description, Alert_Date)
            VALUES (@Asteroid_ID, @Orbital_ID, @Novo_Dap, NULL, @Novo_Torino, @Novo_Status, @Nova_Prioridade, @Nova_Descricao, GETDATE());
            
        END
    END
END
GO