USE projeto;
GO

-- ===========================
--  STAGING TABLES (TEMPORÁRIAS)
-- ===========================

IF OBJECT_ID('Staging_Asteroid', 'U') IS NOT NULL DROP TABLE Staging_Asteroid;
CREATE TABLE Staging_Asteroid (
    full_name VARCHAR(100),
    neo BIT,
    pha BIT,
    diameter FLOAT,
    H FLOAT,
    albedo FLOAT
);
GO

IF OBJECT_ID('Staging_Orbit', 'U') IS NOT NULL DROP TABLE Staging_Orbit;
CREATE TABLE Staging_Orbit (
    full_name VARCHAR(100),
    epoch FLOAT,
    e FLOAT,
    a FLOAT,
    q FLOAT,
    i FLOAT,
    M FLOAT,
    moid_ld FLOAT,
    rms FLOAT
);
GO

IF OBJECT_ID('Staging_Software', 'U') IS NOT NULL DROP TABLE Staging_Software;
CREATE TABLE Staging_Software (
    computer VARCHAR(100)
);
GO

IF OBJECT_ID('Staging_Observation', 'U') IS NOT NULL DROP TABLE Staging_Observation;
CREATE TABLE Staging_Observation (
    full_name VARCHAR(100),
    arc_days FLOAT,
    num_obs INT,
    computer VARCHAR(100)
);
GO
