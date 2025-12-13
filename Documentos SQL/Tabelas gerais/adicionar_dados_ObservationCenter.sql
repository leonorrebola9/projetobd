-- Valores para a tabela Observation_Center
-- Criar Centro Padrão
INSERT INTO Observation_Center (name, latitude, longitude, altitude)
VALUES ('Minor Planet Center (General)', 0.0, 0.0, 0.0);
-- Guardar o ID
DECLARE @CenterID INT = SCOPE_IDENTITY();
-- Criar Equipamento Padrão
INSERT INTO Equipment (name, type, Center_ID)
VALUES ('Generic Telescope', 'Optical', @CenterID);