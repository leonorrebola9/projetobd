-- 1. Limpa alertas antigos (se houver) para recalcular tudo de forma limpa
TRUNCATE TABLE Alert;

-- 2. Adiciona colunas que faltam
IF COL_LENGTH('Alert', 'Priority') IS NULL
    ALTER TABLE Alert ADD Priority VARCHAR(50);

IF COL_LENGTH('Alert', 'Description') IS NULL
    ALTER TABLE Alert ADD Description VARCHAR(255);

-- Adicionar a coluna Alert_Date (data de criação)
IF COL_LENGTH('Alert', 'Alert_Date') IS NULL
    ALTER TABLE Alert ADD Alert_Date DATETIME DEFAULT GETDATE();

-- Inserção de dados após trigger
INSERT INTO Alert (
    Asteroid_ID, Orbital_ID, dap, p, torino, status, Priority, Description, Alert_Date
)
SELECT 
    OP.Asteroid_ID,
    NULL, 
    DATEADD(day, OP.moid_ld, GETDATE()), 
    NULL, 

    -- Repetição da lógica para os dados existentes
    CASE 
        WHEN A.diameter > 0.03 AND OP.moid_ld < 1 THEN 4
        WHEN A.diameter > 0.05 AND OP.moid_ld < 5 AND OP.rms < 0.3 THEN 3
        WHEN A.diameter > 0.1 AND OP.moid_ld BETWEEN 5 AND 20 THEN 2
        WHEN A.pha = 'Y' AND A.diameter BETWEEN 0.05 AND 0.5 AND OP.moid_ld BETWEEN 20 AND 100 THEN 1
        ELSE 0 
    END,

    CASE 
        WHEN A.diameter > 0.03 AND OP.moid_ld < 1 THEN 'Vermelho'
        WHEN A.diameter > 0.05 AND OP.moid_ld < 5 AND OP.rms < 0.3 THEN 'Laranja'
        WHEN A.diameter > 0.1 AND OP.moid_ld BETWEEN 5 AND 20 THEN 'Amarelo'
        WHEN A.pha = 'Y' AND A.diameter BETWEEN 0.05 AND 0.5 AND OP.moid_ld BETWEEN 20 AND 100 THEN 'Verde'
        ELSE 'Sem Alerta'
    END,

    CASE 
        WHEN (OP.moid_ld < 1 AND A.diameter > 0.01) 
          OR (A.pha = 'Y' AND A.diameter > 0.1 AND OP.rms > 0.8 AND OP.moid_ld < 20) THEN 'Alta'
        WHEN (A.diameter > 0.5 AND OP.moid_ld < 50)
          OR (OP.e > 0.05 OR OP.i > 2) THEN 'Media'
        WHEN (A.albedo > 0.3 OR OP.e > 0.8 OR OP.i > 70) AND A.diameter > 0.2 THEN 'Baixa'
        ELSE 'Normal'
    END,

    'Analise Inicial (MOID: ' + CAST(CAST(OP.moid_ld AS DECIMAL(10,2)) AS VARCHAR) + ')',
    GETDATE()

FROM Orbital_Parameter OP
INNER JOIN Asteroid A ON OP.Asteroid_ID = A.Asteroid_ID
WHERE 
    (A.diameter > 0.03 AND OP.moid_ld < 1) OR 
    (A.diameter > 0.05 AND OP.moid_ld < 5 AND OP.rms < 0.3) OR 
    (A.diameter > 0.1 AND OP.moid_ld BETWEEN 5 AND 20) OR 
    (A.pha = 'Y') OR
    (A.albedo > 0.3 OR OP.e > 0.8 OR OP.i > 70);

-- Mostra um resumo do que foi encontrado
SELECT status AS [Cor], Priority AS [Prioridade], COUNT(*) AS [Qtd]
FROM Alert 
GROUP BY status, Priority
ORDER BY Qtd DESC;