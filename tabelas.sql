CREATE TABLE Observation_Center
(
  Center_ID INT IDENTITY(1,1) NOT NULL,
  name VARCHAR(100) NOT NULL,    
  latitude FLOAT NOT NULL,       
  longitude FLOAT NOT NULL,      
  altitude FLOAT NOT NULL,       
  PRIMARY KEY (Center_ID)
);

CREATE TABLE Software
(
  Software_ID INT IDENTITY(1,1) NOT NULL,
  Computer VARCHAR(100) NOT NULL, 
  PRIMARY KEY (Software_ID)
);

CREATE TABLE Asteroid
(
  Asteroid_ID INT IDENTITY(1,1) NOT NULL,   
  full_name VARCHAR(100) NULL,   
  neo CHAR(1) NULL,              
  pha CHAR(1) NULL,              
  diameter FLOAT NULL,           
  H FLOAT NULL,                  
  albedo FLOAT NULL,             
  PRIMARY KEY (Asteroid_ID)
);

CREATE TABLE Orbital_Parameter
(
  Orbital_ID INT IDENTITY(1,1) NOT NULL,
  epoch FLOAT NOT NULL,          
  e FLOAT NOT NULL,              
  a FLOAT NOT NULL,              
  q FLOAT NOT NULL,              
  i FLOAT NOT NULL,              
  M FLOAT NOT NULL,              
  moid_ld FLOAT NOT NULL,        
  rms FLOAT NOT NULL,            
  tp_cal FLOAT NOT NULL,         
  Asteroid_ID INT NOT NULL,
  PRIMARY KEY (Orbital_ID),
  FOREIGN KEY (Asteroid_ID) REFERENCES Asteroid(Asteroid_ID)
);

CREATE TABLE Equipment
(
  Equipment_ID INT IDENTITY(1,1) NOT NULL,
  name VARCHAR(100) NULL,        
  type VARCHAR(50) NOT NULL,     
  Center_ID INT NOT NULL,
  PRIMARY KEY (Equipment_ID),
  FOREIGN KEY (Center_ID) REFERENCES Observation_Center(Center_ID)
);

CREATE TABLE Alert
(
  Alert_ID INT IDENTITY(1,1) NOT NULL,
  priority VARCHAR(50) NOT NULL, 
  torino_scale INT NOT NULL,     
  status VARCHAR(20) NOT NULL,   
  dap DATE NOT NULL,             
  Asteroid_ID INT NOT NULL,
  Orbital_ID INT NOT NULL,       
  PRIMARY KEY (Alert_ID),
  FOREIGN KEY (Asteroid_ID) REFERENCES Asteroid(Asteroid_ID),
  FOREIGN KEY (Orbital_ID) REFERENCES Orbital_Parameter(Orbital_ID)
);

CREATE TABLE Observation
(
  Observation_ID INT IDENTITY(1,1) NOT NULL,
  arc_days FLOAT NULL,           
  num_obs INT NOT NULL,          
  Asteroid_ID INT NOT NULL,
  Equipment_ID INT NOT NULL,
  Software_ID INT NOT NULL,
  PRIMARY KEY (Observation_ID),
  FOREIGN KEY (Asteroid_ID) REFERENCES Asteroid(Asteroid_ID),
  FOREIGN KEY (Equipment_ID) REFERENCES Equipment(Equipment_ID),
  FOREIGN KEY (Software_ID) REFERENCES Software(Software_ID)
);

CREATE TABLE Astronomer
(
  Astronomer_ID INT IDENTITY(1,1) NOT NULL,
  name VARCHAR(100) NOT NULL,    
  Observation_ID INT NOT NULL,   
  Center_ID INT NOT NULL,        
  PRIMARY KEY (Astronomer_ID),
  FOREIGN KEY (Observation_ID) REFERENCES Observation(Observation_ID),
  FOREIGN KEY (Center_ID) REFERENCES Observation_Center(Center_ID)
);