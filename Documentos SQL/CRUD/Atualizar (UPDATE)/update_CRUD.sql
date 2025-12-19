-- Atualizar asteroide
CREATE OR ALTER PROCEDURE SP_AtualizarDadosAsteroid
    @Asteroid_ID INT,
    @NovoDiametro FLOAT,
    @NovoPerigo CHAR(1) -- 'Y' ou 'N'
AS
BEGIN
    UPDATE Asteroid
    SET 
        diameter = @NovoDiametro,
        pha = @NovoPerigo
    WHERE Asteroid_ID = @Asteroid_ID;
    
END
GO

-- Atualizar órbita
CREATE OR ALTER PROCEDURE SP_AtualizarOrbita
    @Orbital_ID INT,
    @moid_ld FLOAT,
    @e FLOAT,
    @a FLOAT,
    @q FLOAT,
    @i FLOAT,
    @rms FLOAT,
    @epoch FLOAT
AS
BEGIN
    UPDATE Orbital_Parameter
    SET 
        moid_ld = @moid_ld,
        e = @e,
        a = @a,
        q = @q,
        i = @i,
        rms = @rms,
        epoch = @epoch
    WHERE Orbital_ID = @Orbital_ID;

END
GO

-- Atualizar Alerta
CREATE OR ALTER PROCEDURE SP_AtualizarAlerta
    @Alert_ID INT,
    @NovoStatus VARCHAR(50),      -- 'Green', 'Red', etc
    @NovaPrioridade VARCHAR(50),
    @NovoTorino INT,
    @NovaProbabilidade FLOAT,
    @NovaDescricao VARCHAR(255)
AS
BEGIN
    UPDATE Alert
    SET 
        status = @NovoStatus,
        Priority = @NovaPrioridade,
        torino = @NovoTorino,
        p = @NovaProbabilidade,
        Description = @NovaDescricao,
        Alert_Date = GETDATE()
    WHERE Alert_ID = @Alert_ID;

END
GO

-- Atualizar Observação
CREATE OR ALTER PROCEDURE SP_AtualizarObservacao
    @Observation_ID INT,
    @NovoNumObs INT,
    @NovoArc FLOAT,
    @NovoEquipamentoID INT,
    @NovoAstronomoID INT 
AS
BEGIN
    UPDATE Observation
    SET 
        num_obs = @NovoNumObs,
        arc = @NovoArc,
        Equipment_ID = @NovoEquipamentoID,
        Astronomer_ID = @NovoAstronomoID
    WHERE Observation_ID = @Observation_ID;

END
GO

-- Atualizar Astrónomo
CREATE OR ALTER PROCEDURE SP_AtualizarAstronomo
    @Astronomer_ID INT,
    @NovoNome VARCHAR(100),
    @NovoCentroID INT
AS
BEGIN
    UPDATE Astronomer
    SET 
        name = @NovoNome,
        Center_ID = @NovoCentroID
    WHERE Astronomer_ID = @Astronomer_ID;

END
GO

-- Atualizar Equipamento
CREATE OR ALTER PROCEDURE SP_AtualizarEquipamento
    @Equipment_ID INT,
    @NovoNome VARCHAR(100),
    @NovoTipo VARCHAR(50),
    @NovoCentroID INT
AS
BEGIN
    UPDATE Equipment
    SET 
        name = @NovoNome,
        type = @NovoTipo,
        Center_ID = @NovoCentroID
    WHERE Equipment_ID = @Equipment_ID;

END
GO

-- Atualizar Software
CREATE OR ALTER PROCEDURE SP_AtualizarSoftware
    @Software_ID INT,
    @NovoNomePC VARCHAR(100)
AS
BEGIN
    UPDATE Software
    SET Computer = @NovoNomePC
    WHERE Software_ID = @Software_ID;
    
END
GO

-- Atualizar Centro de Observação
CREATE OR ALTER PROCEDURE SP_AtualizarCentro
    @Center_ID INT,
    @NovoNome VARCHAR(100),
    @NovaLat FLOAT,
    @NovaLong FLOAT,
    @NovaAlt FLOAT
AS
BEGIN
    UPDATE Observation_Center
    SET 
        name = @NovoNome,
        latitude = @NovaLat,
        longitude = @NovaLong,
        altitude = @NovaAlt
    WHERE Center_ID = @Center_ID;
    
END
GO