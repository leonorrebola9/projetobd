USE projeto;
GO

--- 1) INSERIR ASTEROIDES NOVOS
INSERT INTO Asteroid (full_name, neo, pha, diameter, H, albedo)
SELECT s.full_name, s.neo, s.pha, s.diameter, s.H, s.albedo
FROM Staging_Asteroid s
WHERE NOT EXISTS (
    SELECT 1 FROM Asteroid a WHERE a.full_name = s.full_name
);

--- 2) ATUALIZAR ASTEROIDES EXISTENTES
UPDATE a
SET 
    a.neo = s.neo,
    a.pha = s.pha,
    a.diameter = s.diameter,
    a.H = s.H,
    a.albedo = s.albedo
FROM Asteroid a
JOIN Staging_Asteroid s ON s.full_name = a.full_name;

--- 3) INSERIR SOFTWARE NOVO
INSERT INTO Software (Computer)
SELECT DISTINCT s.computer
FROM Staging_Software s
WHERE NOT EXISTS (
    SELECT 1 FROM Software sw WHERE sw.Computer = s.computer
);

--- 4) INSERIR PARÂMETROS ORBITAIS NOVOS
INSERT INTO Orbital_Parameter (Asteroid_ID, epoch, e, a, q, i, M, moid_ld, rms, tp_cal)
SELECT 
    a.Asteroid_ID,
    s.epoch,
    s.e,
    s.a,
    s.q,
    s.i,
    s.M,
    s.moid_ld,
    s.rms,
    0.0      -- valor por defeito porque não existe no dataset
FROM Staging_Orbit s
JOIN Asteroid a ON a.full_name = s.full_name
WHERE NOT EXISTS (
    SELECT 1 
    FROM Orbital_Parameter o 
    WHERE o.Asteroid_ID = a.Asteroid_ID
);

--- 5) ATUALIZAR PARÂMETROS EXISTENTES
UPDATE o
SET
    o.epoch = s.epoch,
    o.e = s.e,
    o.a = s.a,
    o.q = s.q,
    o.i = s.i,
    o.M = s.M,
    o.moid_ld = s.moid_ld,
    o.rms = s.rms,
    o.tp_cal = 0.0       -- mantém consistente
FROM Orbital_Parameter o
JOIN Asteroid a ON o.Asteroid_ID = a.Asteroid_ID
JOIN Staging_Orbit s ON s.full_name = a.full_name;

--- 6) INSERIR OBSERVAÇÕES NOVAS
INSERT INTO Observation (arc_days, num_obs, Asteroid_ID, Equipment_ID, Software_ID)
SELECT 
    s.arc_days,
    s.num_obs,
    a.Asteroid_ID,
    1,                  -- equipamento fixo
    sw.Software_ID
FROM Staging_Observation s
JOIN Asteroid a ON a.full_name = s.full_name
JOIN Software sw ON sw.Computer = s.computer
WHERE NOT EXISTS (
    SELECT 1 
    FROM Observation o
    WHERE o.Asteroid_ID = a.Asteroid_ID
      AND o.Software_ID = sw.Software_ID
      AND o.num_obs = s.num_obs
);