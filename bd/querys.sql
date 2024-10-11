--PARA CARGAR LA TABLA DE TURNOS
--SELECT Odontologos.Apellido_odontologo, Turnos.Prestacion FROM Odontologos
--JOIN Turnos ON Odontologos.Matricula = Turnos.Odontologo

--SELECT * FROM turnos WHERE fecha= '2024-10-10' ORDER BY hora
--SELECT Turnos.Hora, Turnos.Paciente, Odontologos.Apellido_odontologo, Turnos.Prestacion 
--FROM Odontologos JOIN Turnos ON Odontologos.Matricula = Turnos.Odontologo
--WHERE Turnos.Fecha= '2024-10-10' ORDER BY Turnos.Hora
--SELECT Matricula FROM odontologos WHERE Apellido_odontologo LIKE '%MA%'
SELECT DISTINCT nro, nro_diente, id_odonto, v, d, m, i,o, corona, extraccion FROM dientes inner join Odontogramas ON dientes.id_odonto=Odontogramas.id_odontograma
 WHERE Odontogramas.dni_paciente='25252525' AND dientes.id_odonto<='5'
UNION
SELECT * FROM dientes ORDER by nro DESC
--DELETE FROM Dientes WHERE id_odonto=3