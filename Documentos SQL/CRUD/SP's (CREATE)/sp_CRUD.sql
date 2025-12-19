-- Asteroid
CREATE OR ALTER PROCEDURE SP_InserirAsteroid
    @full_name VARCHAR(100), 
    @neo CHAR(1), 
    @pha CHAR(1), 
    @diameter FLOAT, 
    @H FLOAT, 
    @albedo FLOAT, 
    @diameter_sigma FLOAT = NULL, 
    @epoch_cal FLOAT = NULL
AS
BEGIN
    SET NOCOUNT ON;
    DECLARE @NewID INT;

    SELECT @NewID = Asteroid_ID FROM Asteroid WHERE full_name = @full_name;
    
    IF @NewID IS NULL
    BEGIN
        INSERT INTO Asteroid (full_name, neo, pha, diameter, H, albedo, diameter_sigma, epoch_cal)
        VALUES (@full_name, @neo, @pha, @diameter, @H, @albedo, @diameter_sigma, @epoch_cal);
        SET @NewID = SCOPE_IDENTITY();
    END
    ELSE
    BEGIN
        UPDATE Asteroid 
        SET diameter = @diameter, H = @H, albedo = @albedo, pha = @pha, neo = @neo, diameter_sigma = @diameter_sigma, epoch_cal = @epoch_cal 
        WHERE Asteroid_ID = @NewID;
    END
    SELECT @NewID AS Asteroid_ID;
END
GO

-- Parâmetro Orbital
CREATE OR ALTER PROCEDURE SP_InserirOrbitalParameter
    @Asteroid_ID INT, @epoch FLOAT, @e FLOAT, @sigma_e FLOAT = NULL, @a FLOAT, @sigma_a FLOAT = NULL, 
    @q FLOAT, @sigma_q FLOAT = NULL, @i FLOAT, @sigma_i FLOAT = NULL, @M FLOAT, @sigma_ma FLOAT = NULL, 
    @moid_ld FLOAT, @rms FLOAT, @tp_cal FLOAT, @sigma_tp FLOAT = NULL
AS
BEGIN
    SET NOCOUNT ON;
    IF EXISTS (SELECT 1 FROM Orbital_Parameter WHERE Asteroid_ID = @Asteroid_ID)
    BEGIN
        UPDATE Orbital_Parameter 
        SET epoch = @epoch, e = @e, sigma_e = @sigma_e, a = @a, sigma_a = @sigma_a, q = @q, sigma_q = @sigma_q, i = @i, sigma_i = @sigma_i, M = @M, sigma_ma = @sigma_ma, moid_ld = @moid_ld, rms = @rms, tp_cal = @tp_cal, sigma_tp = @sigma_tp 
        WHERE Asteroid_ID = @Asteroid_ID;
        
        SELECT Orbital_ID FROM Orbital_Parameter WHERE Asteroid_ID = @Asteroid_ID;
    END
    ELSE
    BEGIN
        INSERT INTO Orbital_Parameter (Asteroid_ID, epoch, e, sigma_e, a, sigma_a, q, sigma_q, i, sigma_i, M, sigma_ma, moid_ld, rms, tp_cal, sigma_tp)
        VALUES (@Asteroid_ID, @epoch, @e, @sigma_e, @a, @sigma_a, @q, @sigma_q, @i, @sigma_i, @M, @sigma_ma, @moid_ld, @rms, @tp_cal, @sigma_tp);
        SELECT SCOPE_IDENTITY() AS Orbital_ID;
    END
END
GO

-- Alerta
CREATE OR ALTER PROCEDURE SP_InserirAlert
    @Priority VARCHAR(50), @torino INT, @status VARCHAR(50), @dap DATETIME, @Asteroid_ID INT, @Orbital_ID INT, 
    @p FLOAT = NULL, @Description VARCHAR(255) = NULL, @Alert_Date DATETIME = NULL
AS
BEGIN
    SET NOCOUNT ON;
    DECLARE @NewID INT;
    
    IF @Alert_Date IS NULL SET @Alert_Date = GETDATE();
    
    SELECT @NewID = Alert_ID FROM Alert WHERE Asteroid_ID = @Asteroid_ID AND dap = @dap;

    IF @NewID IS NULL
    BEGIN
        INSERT INTO Alert (Priority, torino, status, dap, p, Description, Alert_Date, Asteroid_ID, Orbital_ID)
        VALUES (@Priority, @torino, @status, @dap, @p, @Description, @Alert_Date, @Asteroid_ID, @Orbital_ID);
        SET @NewID = SCOPE_IDENTITY();
    END
    ELSE
    BEGIN
        UPDATE Alert 
        SET Priority = @Priority, torino = @torino, status = @status, p = @p, Description = @Description, Orbital_ID = @Orbital_ID 
        WHERE Alert_ID = @NewID;
    END
    SELECT @NewID AS Alert_ID;
END
GO

-- Software
CREATE OR ALTER PROCEDURE SP_InserirSoftware 
    @Computer VARCHAR(100) 
AS 
BEGIN 
    SET NOCOUNT ON; 
    DECLARE @ID INT; 
    
    SELECT @ID = Software_ID FROM Software WHERE Computer = @Computer; 
    
    IF @ID IS NULL 
    BEGIN 
        INSERT INTO Software (Computer) VALUES (@Computer); 
        SET @ID = SCOPE_IDENTITY(); 
    END 
    
    SELECT @ID AS Software_ID; 
END 
GO

-- Centro de Observação
CREATE OR ALTER PROCEDURE SP_InserirObservationCenter 
    @name VARCHAR(100), 
    @latitude FLOAT, 
    @longitude FLOAT, 
    @altitude FLOAT 
AS 
BEGIN 
    SET NOCOUNT ON; 
    DECLARE @ID INT; 
    
    SELECT @ID = Center_ID FROM Observation_Center WHERE name = @name; 
    
    IF @ID IS NULL 
    BEGIN 
        INSERT INTO Observation_Center (name, latitude, longitude, altitude) VALUES (@name, @latitude, @longitude, @altitude); 
        SET @ID = SCOPE_IDENTITY(); 
    END 
    ELSE 
    BEGIN 
        UPDATE Observation_Center SET latitude = @latitude, longitude = @longitude, altitude = @altitude WHERE Center_ID = @ID; 
    END 
    
    SELECT @ID AS Center_ID; 
END 
GO

-- Equipamentos
CREATE OR ALTER PROCEDURE SP_InserirEquipment 
    @name VARCHAR(100), 
    @type VARCHAR(50), 
    @Center_ID INT 
AS 
BEGIN 
    SET NOCOUNT ON; 
    DECLARE @ID INT; 
    
    SELECT @ID = Equipment_ID FROM Equipment WHERE name = @name AND Center_ID = @Center_ID; 
    
    IF @ID IS NULL 
    BEGIN 
        INSERT INTO Equipment (name, type, Center_ID) VALUES (@name, @type, @Center_ID); 
        SET @ID = SCOPE_IDENTITY(); 
    END 
    ELSE 
    BEGIN 
        UPDATE Equipment SET type = @type WHERE Equipment_ID = @ID; 
    END 
    
    SELECT @ID AS Equipment_ID; 
END 
GO

-- Astrónomo
CREATE OR ALTER PROCEDURE SP_InserirAstronomer
    @name VARCHAR(100),
    @Center_ID INT
AS
BEGIN
    SET NOCOUNT ON;
    DECLARE @NewID INT;
    
    SELECT @NewID = Astronomer_ID FROM Astronomer WHERE name = @name;
    
    IF @NewID IS NULL
    BEGIN
        INSERT INTO Astronomer (name, Center_ID) VALUES (@name, @Center_ID);
        SET @NewID = SCOPE_IDENTITY();
    END
    ELSE
    BEGIN
        UPDATE Astronomer SET Center_ID = @Center_ID WHERE Astronomer_ID = @NewID;
    END
    SELECT @NewID AS Astronomer_ID;
END
GO

-- Observação
CREATE OR ALTER PROCEDURE SP_InserirObservation
    @arc FLOAT, 
    @num_obs INT, 
    @Asteroid_ID INT, 
    @Equipment_ID INT, 
    @Software_ID INT,
    @Astronomer_ID INT
AS
BEGIN
    SET NOCOUNT ON;
    DECLARE @NewID INT;
    
    SELECT @NewID = Observation_ID FROM Observation 
    WHERE Asteroid_ID = @Asteroid_ID AND Equipment_ID = @Equipment_ID AND Software_ID = @Software_ID 
      AND num_obs = @num_obs AND Astronomer_ID = @Astronomer_ID;

    IF @NewID IS NULL
    BEGIN
        INSERT INTO Observation (arc, num_obs, Asteroid_ID, Equipment_ID, Software_ID, Astronomer_ID)
        VALUES (@arc, @num_obs, @Asteroid_ID, @Equipment_ID, @Software_ID, @Astronomer_ID);
        SET @NewID = SCOPE_IDENTITY();
    END
    SELECT @NewID AS Observation_ID;
END
GO