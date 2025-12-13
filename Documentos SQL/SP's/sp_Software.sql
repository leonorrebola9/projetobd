USE projeto;
GO

-- 2. SP para Software
CREATE OR ALTER PROCEDURE SP_InserirSoftware
    @Computer VARCHAR(100)
AS
BEGIN
    SET NOCOUNT ON;
    DECLARE @NewID INT;

    -- 1. Verifica se o software/computador já existe pelo NOME
    SELECT @NewID = Software_ID FROM Software WHERE Computer = @Computer;

    -- 2. Se não existir, insere
    IF @NewID IS NULL
    BEGIN
        INSERT INTO Software (Computer)
        VALUES (@Computer);

        SET @NewID = SCOPE_IDENTITY();
    END
    -- Nota: Como esta tabela só tem o nome, não precisamos de "ELSE UPDATE"

    -- 3. Retorna o ID
    SELECT @NewID AS Software_ID;
END
GO