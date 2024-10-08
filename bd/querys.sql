--PARA CARGAR LA TABLA DE TURNOS
--SELECT Odontologos.Apellido_odontologo, Turnos.Prestacion FROM Odontologos
--JOIN Turnos ON Odontologos.Matricula = Turnos.Odontologo

--SELECT * FROM turnos WHERE fecha= '2024-10-10' ORDER BY hora
--SELECT Turnos.Hora, Turnos.Paciente, Odontologos.Apellido_odontologo, Turnos.Prestacion 
--FROM Odontologos JOIN Turnos ON Odontologos.Matricula = Turnos.Odontologo
--WHERE Turnos.Fecha= '2024-10-10' ORDER BY Turnos.Hora
SELECT Matricula FROM odontologos WHERE Apellido_odontologo LIKE '%MA%'