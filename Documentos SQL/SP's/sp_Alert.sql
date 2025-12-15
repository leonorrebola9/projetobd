USE projeto;
GO

-- 6. SP para Alert (Atualizada com colunas reais)
CREATE OR ALTER PROCEDURE SP_InserirAlert
    @Priority VARCHAR(50),
    @torino INT,          -- CORRIGIDO: O nome na tabela é 'torino'
    @status VARCHAR(50),  -- Aumentei para 50 para garantir (era 20)
    @dap DATETIME,        -- Data da Aproximação
    @Asteroid_ID INT,
    @Orbital_ID INT,
    
    -- Novos campos detetados nas imagens:
    @p FLOAT = NULL,                 -- Coluna 'p' (probabilidade)
    @Description VARCHAR(255) = NULL, -- Coluna Description
    @Alert_Date DATETIME = NULL       -- Data de criação do alerta
AS
BEGIN
    SET NOCOUNT ON;
    DECLARE @NewID INT;

    -- Se a data do alerta não for fornecida, usamos a data de agora
    IF @Alert_Date IS NULL SET @Alert_Date = GETDATE();

    -- Verifica se já existe um alerta para este asteroide nesta data de aproximação (dap)
    SELECT @NewID = Alert_ID 
    FROM Alert 
    WHERE Asteroid_ID = @Asteroid_ID AND dap = @dap;

    IF @NewID IS NULL
    BEGIN
        -- INSERE (Com todas as colunas novas)
        INSERT INTO Alert (
            Priority, torino, status, dap, 
            p, Description, Alert_Date, 
            Asteroid_ID, Orbital_ID
        )
        VALUES (
            @Priority, @torino, @status, @dap, 
            @p, @Description, @Alert_Date, 
            @Asteroid_ID, @Orbital_ID
        );

        SET @NewID = SCOPE_IDENTITY();
    END
    ELSE
    BEGIN
        -- ATUALIZA (Garante que dados novos sobrepõem os antigos)
        UPDATE Alert 
        SET 
            Priority = @Priority, 
            torino = @torino, 
            status = @status, 
            p = @p,                       -- Atualiza p
            Description = @Description,   -- Atualiza descrição
            Orbital_ID = @Orbital_ID
            -- Nota: Não atualizamos Alert_Date para manter o registo de quando foi criado originalmente
        WHERE Alert_ID = @NewID;
    END

    SELECT @NewID AS Alert_ID;
END
GO