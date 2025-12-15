USE projeto;
GO

-- Tabela temporária apenas para listar os nomes
DECLARE @AstronomosVivos TABLE (Nome VARCHAR(100));

INSERT INTO @AstronomosVivos (Nome) VALUES 
('Neil deGrasse Tyson'),   -- Divulgador científico e Astrofísico (Hayden Planetarium)
('Jocelyn Bell Burnell'),  -- Descobriu os Pulsares (ainda ativa)
('Kip Thorne'),            -- Nobel da Física (Ondas Gravitacionais / Interstellar)
('Andrea Ghez'),           -- Nobel da Física (Buraco Negro no centro da Via Láctea)
('Michel Mayor'),          -- Nobel da Física (Primeiro Exoplaneta)
('Didier Queloz'),         -- Nobel da Física (Primeiro Exoplaneta)
('Sara Seager'),           -- Especialista em atmosferas de exoplanetas
('Alan Stern'),            -- Líder da missão New Horizons (Plutão)
('Carolyn Porco'),         -- Líder da equipa de imagem da sonda Cassini (Saturno)
('Jill Tarter'),           -- A inspiração para o filme "Contact" (SETI)
('Brian May'),             -- Astrofísico e guitarrista dos Queen
('Jane Luu'),              -- Co-descobridora da Cintura de Kuiper
('Mike Brown'),            -- O homem que "matou" Plutão (descobriu Eris)
('Reinhard Genzel'),       -- Nobel da Física (Buraco Negro Sagitário A*)
('Sheperd Doeleman');      -- Diretor do Event Horizon Telescope (Foto do Buraco Negro)

-- Inserir na tabela real
-- NOTA: Este script precisa que já tenhas dados nas tabelas Observation e Center
INSERT INTO Astronomer (name, Observation_ID, Center_ID)
SELECT 
    A.Nome,
    -- Escolhe uma Observação aleatória que JÁ EXISTA
    (SELECT TOP 1 Observation_ID FROM Observation ORDER BY NEWID()),
    
    -- Escolhe um Centro aleatório que JÁ EXISTA
    -- (Confirma se a tua tabela se chama 'Center' ou 'Research_Center')
    (SELECT TOP 1 Center_ID FROM Observation_Center ORDER BY NEWID()) 
FROM @AstronomosVivos A;