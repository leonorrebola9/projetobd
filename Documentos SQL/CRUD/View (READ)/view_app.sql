CREATE OR ALTER VIEW vw_App_Completa AS
SELECT 
    -- Asteroide
    A.Asteroid_ID,
    A.full_name AS [Nome],
    A.diameter AS [Diametro],
    A.diameter_sigma AS [Incerteza],
    A.H AS [H],
    A.albedo AS [Albedo],
    A.pha AS [PHA],
    A.neo AS [NEO],
    A.epoch_cal,

    -- Parâmetro orbital
    ISNULL(OP.moid_ld, 0) AS [Distancia_Minima_Terra],
    ISNULL(OP.rms, 0) AS [RMS],
    ISNULL(OP.e, 0) AS [Excentricidade],
    ISNULL(OP.a, 0) AS [Eixo_Semimaior],
    ISNULL(OP.q, 0) AS [Perielio],
    ISNULL(OP.i, 0) AS [Inclinacao],
    ISNULL(OP.M, 0) AS [Anomalia_Media],
    OP.tp_cal,
    OP.epoch AS [Epoch_Orbital],

    -- Alertas
    ISNULL(AL.status, 'Sem Alerta') AS [Status_Alerta],
    ISNULL(AL.Priority, 'Nenhuma') AS [Prioridade_Alerta],
    ISNULL(AL.torino, 0) AS [Escala_Torino],
    AL.dap AS [Data_Aproximacao],
    AL.Description AS [Descricao_Risco],

    -- Estatísticas
    COUNT(O.Observation_ID) AS [Total_Sessoes],
    SUM(O.num_obs) AS [Total_Imagens],
    MAX(O.arc) AS [Maior_Arco_Dias],

    -- Listas
    STRING_AGG(ISNULL(E.name, ''), '; ') AS [Lista_Equipamentos],
    STRING_AGG(ISNULL(S.Computer, ''), '; ') AS [Lista_Softwares],
    STRING_AGG(ISNULL(AST.name, ''), '; ') AS [Equipa_Astronomos],
    STRING_AGG(ISNULL(C.name, ''), '; ')   AS [Centros_Observacao]

FROM Asteroid A
LEFT JOIN Orbital_Parameter OP ON A.Asteroid_ID = OP.Asteroid_ID
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

select * from vw_App_Completa WHERE Nome = 'Conae';