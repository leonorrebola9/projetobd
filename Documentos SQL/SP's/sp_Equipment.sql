USE projeto;
GO

-- 5. SP para Equipment
CREATE OR ALTER PROCEDURE SP_InserirEquipment
    @name VARCHAR(100),
    @type VARCHAR(50),
    @Center_ID INT
AS
BEGIN
    SET NOCOUNT ON;
    DECLARE @NewID INT;

    -- Verifica se este equipamento já existe NESTE centro específico
    SELECT @NewID = Equipment_ID 
    FROM Equipment 
    WHERE name = @name AND Center_ID = @Center_ID;

    IF @NewID IS NULL
    BEGIN
        INSERT INTO Equipment (name, type, Center_ID)
        VALUES (@name, @type, @Center_ID);

        SET @NewID = SCOPE_IDENTITY();
    END
    ELSE
    BEGIN
        -- Se já existe, atualiza o tipo caso tenha mudado
        UPDATE Equipment SET type = @type WHERE Equipment_ID = @NewID;
    END

    SELECT @NewID AS Equipment_ID;
END
GO

-- Para criar um equipamento para não dar erro
USE projeto;
GO

-- 1. Primeiro cria um Centro (porque o equipamento precisa dele)
EXEC SP_InserirObservationCenter 'Centro Padrao', 0.0, 0.0, 0.0;

-- 2. Agora cria o Equipamento (que vai ficar com o ID 1)
EXEC SP_InserirEquipment 'Telescopio Generico', 'Otico', 1;