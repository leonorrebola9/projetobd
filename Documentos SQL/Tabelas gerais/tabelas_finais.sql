-- 1. Tabela OBSERVATION CENTER (Independente)
CREATE TABLE Observation_Center (
    Center_ID INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(100),
    latitude FLOAT,
    longitude FLOAT,
    altitude FLOAT
);

-- 2. Tabela SOFTWARE (Independente)
CREATE TABLE Software (
    Software_ID INT IDENTITY(1,1) PRIMARY KEY,
    Computer VARCHAR(100)
);

-- 3. Tabela ASTEROID (Independente - com os novos campos do diagrama)
CREATE TABLE Asteroid (
    Asteroid_ID INT IDENTITY(1,1) PRIMARY KEY,
    full_name VARCHAR(100),
    H FLOAT,
    albedo FLOAT,
    diameter FLOAT,
    diameter_sigma FLOAT, -- Novo campo do diagrama
    pha VARCHAR(5),       -- Pode ser 'Y'/'N' ou texto
    neo VARCHAR(5),
    epoch_cal FLOAT       -- Novo campo do diagrama
);

-- 4. Tabela EQUIPMENT (Depende de Observation_Center)
CREATE TABLE Equipment (
    Equipment_ID INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(100),
    type VARCHAR(50),
    Center_ID INT,
    FOREIGN KEY (Center_ID) REFERENCES Observation_Center(Center_ID)
);

-- 5. Tabela ORBITAL_PARAMETER (Depende de Asteroid)
-- Adicionei todos os 'sigmas' que aparecem no diagrama
CREATE TABLE Orbital_Parameter (
    Orbital_ID INT IDENTITY(1,1) PRIMARY KEY,
    Asteroid_ID INT,
    epoch FLOAT,
    e FLOAT,
    sigma_e FLOAT,      -- Novo
    a FLOAT,
    sigma_a FLOAT,      -- Novo
    q FLOAT,
    sigma_q FLOAT,      -- Novo
    i FLOAT,
    sigma_i FLOAT,      -- Novo
    M FLOAT,
    sigma_ma FLOAT,     -- Novo (assumo que seja sigma do M)
    moid_ld FLOAT,
    rms FLOAT,
    tp_cal FLOAT,
    sigma_tp FLOAT,     -- Novo
    FOREIGN KEY (Asteroid_ID) REFERENCES Asteroid(Asteroid_ID)
);

-- 6. Tabela ALERT (Depende de Asteroid e Orbital_Parameter)
CREATE TABLE Alert (
    Alert_ID INT IDENTITY(1,1) PRIMARY KEY,
    Asteroid_ID INT,
    Orbital_ID INT,     -- Ligação indicada pelo "Use" no diagrama
    dap DATE,           -- Date of Approach?
    p FLOAT,            -- Probabilidade?
    torino INT,         -- Escala de Torino
    status VARCHAR(50),
    FOREIGN KEY (Asteroid_ID) REFERENCES Asteroid(Asteroid_ID),
    FOREIGN KEY (Orbital_ID) REFERENCES Orbital_Parameter(Orbital_ID)
);

-- 7. Tabela OBSERVATION (Depende de Asteroid, Equipment, Software)
CREATE TABLE Observation (
    Observation_ID INT IDENTITY(1,1) PRIMARY KEY,
    Asteroid_ID INT,
    Equipment_ID INT,
    Software_ID INT,
    arc FLOAT,
    num_obs INT,        -- #Obs no diagrama
    FOREIGN KEY (Asteroid_ID) REFERENCES Asteroid(Asteroid_ID),
    FOREIGN KEY (Equipment_ID) REFERENCES Equipment(Equipment_ID),
    FOREIGN KEY (Software_ID) REFERENCES Software(Software_ID)
);

-- 8. Tabela ASTRONOMER (Depende de Observation e Center)
CREATE TABLE Astronomer (
    Astronomer_ID INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(100),
    Observation_ID INT, -- Relação "Made by"
    Center_ID INT,      -- Relação "Affiliated by"
    FOREIGN KEY (Observation_ID) REFERENCES Observation(Observation_ID),
    FOREIGN KEY (Center_ID) REFERENCES Observation_Center(Center_ID)
);