CREATE OR ALTER VIEW vw_App_Completa AS
SELECT 
    -- Asteroide
    A.Asteroid_ID,
    A.full_name AS [full_name],
    A.diameter AS [diameter],
    A.diameter_sigma AS [diameter_sigma],
    A.H AS [H],
    A.albedo AS [albedo],
    A.pha AS [pha],
    A.neo AS [neo],
    A.epoch_cal AS [epoch_cal],

    -- Parâmetro orbital
    ISNULL(OP.moid_ld, 0) AS [moid_ld],
    ISNULL(OP.rms, 0) AS [rms],
    ISNULL(OP.e, 0) AS [e],
    ISNULL(OP.a, 0) AS [a],
    ISNULL(OP.q, 0) AS [q],
    ISNULL(OP.i, 0) AS [i],
    ISNULL(OP.M, 0) AS [M],
    OP.tp_cal AS [tp_cal],
    OP.epoch AS [epoch],

    -- Alertas
    ISNULL(AL.status, 'Sem Alerta') AS [status],
    ISNULL(AL.Priority, 'Nenhuma') AS [Priority],
    ISNULL(AL.torino, 0) AS [torino],
    AL.dap AS [dap],
    AL.Description AS [Description],

    -- Estatísticas
    COUNT(O.Observation_ID) AS [Observation_ID],
    SUM(O.num_obs) AS [num_obs],
    MAX(O.arc) AS [arc],

    -- Listas
    STRING_AGG(ISNULL(E.name, ''), '; ') AS [namee],
    STRING_AGG(ISNULL(S.Computer, ''), '; ') AS [Computer],
    STRING_AGG(ISNULL(AST.name, ''), '; ') AS [name],
    STRING_AGG(ISNULL(C.name, ''), '; ')   AS [namec]

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

select *
from INFORMATION_SCHEMA.VIEWS
where TABLE_NAME = 'vw_App_Completa';

select * from vw_App_Completa;