USE projeto;
GO

CREATE OR ALTER VIEW vw_App_Completa AS
SELECT 
    -- 1. IDENTIDADE
    A.full_name AS [Nome],
    A.diameter AS [Diametro],
    A.diameter_sigma AS [Incerteza_Diametro],
    A.H AS [Magnitude],
    A.albedo AS [Albedo],
    A.pha AS [PHA],
    A.neo AS [NEO],
    A.epoch_cal,

    -- 2. ORBITAL
    OP.moid_ld AS [Distancia_Minima_Terra],
    OP.rms AS [RMS],
    OP.e AS [Excentricidade],
    OP.a AS [Eixo_Semimaior],
    OP.q AS [Perielio],
    OP.i AS [Inclinacao],
    OP.M AS [Anomalia_Media],
    OP.tp_cal,
    OP.epoch AS [Epoch],

    -- 3. ALERTA
    ISNULL(AL.status, 'Sem Alerta') AS [Status_Alerta],
    ISNULL(AL.Priority, 'Nenhuma') AS [Prioridade_Alerta],
    AL.torino AS [Escala_Torino],
    AL.dap AS [Data_Aproximacao],
    AL.Description AS [Descricao_Risco],

    -- 4. ESTATÍSTICAS
    COUNT(O.Observation_ID) AS [Total_Sessoes],
    SUM(O.num_obs) AS [Total_Imagens],
    MAX(O.arc) AS [Maior_Arco_Dias],

    -- 5. LISTAS
    STRING_AGG(ISNULL(E.name, ''), '; ') AS [Lista_Equipamentos],
    STRING_AGG(ISNULL(S.Computer, ''), '; ') AS [Lista_Softwares],
    
    -- LIGAÇÃO CORRIGIDA (Usa a nova lógica se tiveres criado a coluna Astronomer_ID na Observation)
    STRING_AGG(ISNULL(AST.name, ''), '; ') AS [Equipa_Astronomos],
    STRING_AGG(ISNULL(C.name, ''), '; ')   AS [Centros_Observacao]

FROM Asteroid A
INNER JOIN Orbital_Parameter OP ON A.Asteroid_ID = OP.Asteroid_ID
LEFT JOIN Alert AL ON A.Asteroid_ID = AL.Asteroid_ID
LEFT JOIN Observation O ON A.Asteroid_ID = O.Asteroid_ID
LEFT JOIN Equipment E ON O.Equipment_ID = E.Equipment_ID
LEFT JOIN Software S ON O.Software_ID = S.Software_ID
LEFT JOIN Astronomer AST ON O.Astronomer_ID = AST.Astronomer_ID
LEFT JOIN Observation_Center C ON AST.Center_ID = C.Center_ID

GROUP BY 
    A.Asteroid_ID, A.full_name, A.diameter, A.diameter_sigma, A.H, A.albedo, A.pha, A.neo, A.epoch_cal,
    OP.Orbital_ID, OP.moid_ld, OP.rms, OP.e, OP.a, OP.q, OP.i, OP.M, OP.tp_cal, OP.epoch,
    AL.status, AL.Priority, AL.torino, AL.dap, AL.Description;
GO


select * from vw_App_Completa;