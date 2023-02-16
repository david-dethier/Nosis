SELECT 
    consultas.CUIT_Consultado,
    COUNT(CUIT_Consultado) AS 'Consultas_Ultimos_30d'
FROM
    consultas
        INNER JOIN
    empresas ON empresas.IdEmpresa = consultas.IdEmpresa
        INNER JOIN
    tipo_consultas ON tipo_consultas.IdTipoConsulta = consultas.IdTipoConsulta
        INNER JOIN
    bancos ON bancos.CUIT_Bancos = empresas.CUIT_Empresa
WHERE
    CUIT_Consultado = '30-88999243-5'
        AND consultas.FechaHora >= DATE_SUB(NOW(), INTERVAL 30 DAY)
        AND tipo_consultas.DescripcionTipoConsulta IN ('Nosis Manager' , 'Nosis VID')
GROUP BY consultas.CUIT_Consultado
;