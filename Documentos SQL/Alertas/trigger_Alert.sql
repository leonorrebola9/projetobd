CREATE OR ALTER TRIGGER trg_AutoAlert
ON Orbital_Parameter
AFTER INSERT, UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO Alert (
        Asteroid_ID, 
        Orbital_ID,
        dap,        -- Data Aproximação
        p,          -- Probabilidade
        torino,     -- Nível (0-4)
        status,     -- Cor
        Priority,   -- Prioridade
        Description,
        Alert_Date
    )
    SELECT 
        i.Asteroid_ID,
        NULL,
        
        -- Estimativa simples da data (Hoje + Dias do MOID)
        DATEADD(day, i.moid_ld, GETDATE()), 
        NULL, -- p (Probabilidade)

        -- Classificação Torino
        CASE 
            WHEN A.diameter > 0.03 AND i.moid_ld < 1 THEN 4
            WHEN A.diameter > 0.05 AND i.moid_ld < 5 AND i.rms < 0.3 THEN 3
            WHEN A.diameter > 0.1 AND i.moid_ld BETWEEN 5 AND 20 THEN 2
            WHEN A.pha = 'Y' AND A.diameter BETWEEN 0.05 AND 0.5 AND i.moid_ld BETWEEN 20 AND 100 THEN 1
            ELSE 0 
        END,

        -- Cor
        CASE 
            WHEN A.diameter > 0.03 AND i.moid_ld < 1 THEN 'Vermelho'
            WHEN A.diameter > 0.05 AND i.moid_ld < 5 AND i.rms < 0.3 THEN 'Laranja'
            WHEN A.diameter > 0.1 AND i.moid_ld BETWEEN 5 AND 20 THEN 'Amarelo'
            WHEN A.pha = 'Y' AND A.diameter BETWEEN 0.05 AND 0.5 AND i.moid_ld BETWEEN 20 AND 100 THEN 'Verde'
            ELSE 'Sem Alerta'
        END,

        -- Prioridade
        CASE 
            WHEN (i.moid_ld < 1 AND A.diameter > 0.01) 
              OR (A.pha = 'Y' AND A.diameter > 0.1 AND i.rms > 0.8 AND i.moid_ld < 20) THEN 'Alta'
            WHEN (A.diameter > 0.5 AND i.moid_ld < 50)
              OR (i.e > 0.05 OR i.i > 2) THEN 'Media'
            WHEN (A.albedo > 0.3 OR i.e > 0.8 OR i.i > 70) AND A.diameter > 0.2 THEN 'Baixa'
            ELSE 'Normal'
        END,

        'Alerta Auto (MOID: ' + CAST(CAST(i.moid_ld AS DECIMAL(10,2)) AS VARCHAR) + ')',
        GETDATE()

    FROM inserted i
    INNER JOIN Asteroid A ON i.Asteroid_ID = A.Asteroid_ID
    -- Filtro: Só gera alerta se houver alguma condição relevante
    WHERE 
        (A.diameter > 0.03 AND i.moid_ld < 1) OR 
        (A.diameter > 0.05 AND i.moid_ld < 5 AND i.rms < 0.3) OR 
        (A.diameter > 0.1 AND i.moid_ld BETWEEN 5 AND 20) OR 
        (A.pha = 'Y') OR
        (A.albedo > 0.3 OR i.e > 0.8 OR i.i > 70);
END
GO