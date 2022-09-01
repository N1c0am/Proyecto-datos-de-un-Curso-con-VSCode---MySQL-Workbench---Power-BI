Create database Curso;

use Curso;

#drop table asignatura;

create table asignatura
( pk_asignatura int not null primary key auto_increment,
asig_nombre varchar(100) not null,
asig_descripcion varchar(30)
);

create table tipo_semestre
(pk_tipo_semestre int not null primary key,
descripcion varchar(30)
);

#drop table semestre;

create table semestre
(pk_semestre int not null,
pk_asignatura int not null,
pk_tipo_semestre int not null,
fecha date not null,
primary key (pk_semestre, pk_asignatura),
foreign key (pk_asignatura) references asignatura (pk_asignatura),
foreign key (pk_tipo_semestre) references tipo_semestre (pk_tipo_semestre)
);

#drop table alumno;

create table alumno
(pk_alumno varchar(10) not null,
pk_semestre int not null,
pk_asignatura int not null,
alu_nombre_alumno varchar(30) not null,
alu_apellido_alumno varchar(30) not null,
alu_direccion varchar(50) not null,
primary key (pk_alumno, pk_asignatura),
foreign key (pk_asignatura) references asignatura (pk_asignatura),
foreign key (pk_semestre) references semestre (pk_semestre)
);

#drop table nota;

create table nota
(pk_nota int not null,
pk_alumno varchar(10) not null,
pk_semestre int not null,
pk_asignatura int not null,
nota decimal(2,1) not null,
num_nota varchar(10),
primary key(pk_nota, pk_semestre),
foreign key (pk_alumno) references alumno (pk_alumno),
foreign key (pk_semestre) references alumno (pk_semestre),
foreign key (pk_asignatura) references asignatura (pk_asignatura)
);

#select * from asignatura;

insert into asignatura
values (1,'Algebra y Geometria', 'Matematicas');

insert into asignatura
values (2,'Gramatica y Ortografia', 'Lenguaje y Comunicacion');

insert into asignatura
values (3,'Learn English', 'English');


insert into tipo_semestre 
values (1, 'Primer semestre')

insert into tipo_semestre 
values (2, 'Segundo semestre')

insert into tipo_semestre 
values (3, 'Tercer semestre')


insert into asignatura
values (01, 'Algebra y Geometria', 'Matematicas')

insert into asignatura
values (02, 'Gramatica y Ortografia', 'Lenguaje y Comunicacion')

insert into asignatura
values (03, 'Learn English', 'English')


insert into semestre
values (1, 01, 1, '2022-08-01')

insert into semestre
values (1, 2, 1, '2022-08-01')

insert into semestre
values (1, 3, 1, '2022-08-01')

insert into semestre
values (2, 02, 2, '2022')

insert into semestre
values (3, 1, 1, '2022-08-01')


insert into alumno
values (22546531, 1, 1, 'Juan', 'Riquelme', 'Av Condores 364')

insert into alumno
values (22528531, 1, 2, 'Juan', 'Riquelme', 'Av Condores 364')

insert into alumno
values (22546531, 1, 3, 'Juan', 'Riquelme', 'Av Condores 364')

insert into alumno
values (22546531, 2, 2, 'Juan', 'Riquelme', 'Av Condores 364')

insert into alumno
values ('22936833-k', 1, 1, 'Carla', 'Saez', 'Av Leones 772')

insert into alumno
values ('22936833-k', 1, 2, 'Carla', 'Saez', 'Av Leones 772')

insert into alumno
values ('22936833-k', 1, 3, 'Carla', 'Saez', 'Av Leones 772')

insert into alumno
values (22936833, 2, 2, 'Carla', 'Sa�z', 'Av Leones 772')

insert into alumno
values (185436751, 1, 1, 'Carlos', 'Sa�z', 'Av Leones 772')


insert into nota
values (001, 22546531, 1, 1, 6, '1erS:1erA')

insert into nota
values (002, 22546531, 1, 1, 5.3, '1erS:1erA')

insert into nota
values (003, '22936833-k', 1, 1, 7, '1erS:1erA')

insert into nota
values (004, '22936833-k', 1, 1, 5, '1erS:1erA')

insert into nota
values (5, 22546531, 1, 1, 6.5, '1erS:1erA')

insert into nota
values (6, '22546531', 1, 2, 4, '1erS:2doA')

insert into nota
values (7, '22546531', 1, 2, 7, '1erS:2doA')

insert into nota
values (008, '22936833-k', 1, 2, 5, '2doS:1erA')

insert into nota
values (009, '22936833-k', 1, 2, 5.4, '2doS:1erA')

#insert into nota values (2,'22546531',1,2,5,'1erS:2doA')

delimiter @@
create procedure eliminar_asignatura (pkasignatura int)
begin
delete from asignatura where pk_asignatura = pkasignatura;
end@@

call eliminar_asignatura(3);

drop procedure actualizar_asignatura
delimiter @@
create procedure insertar_asignatura (pkasignatura int, asignombre varchar(100), asigdescripcion varchar(30))
begin
INSERT INTO asignatura (pk_asignatura, asig_nombre, asig_descripcion) VALUES (pkasignatura,asignombre,asigdescripcion);
end@@

call insertar_asignatura (6,'Historia de Chile','Historia')

drop procedure eliminar_semestre
delimiter @@
create procedure eliminar_semestre (pksemestre int)
begin
delete from semestre where pk_semestre = pksemestre;
end@@

call eliminar_semestre(1);

#drop procedure eliminar_alumno
delimiter @@
create procedure eliminar_alumno (pkalumno varchar(10))
begin
delete from alumno where pk_alumno = pkalumno;
end@@

call eliminar_alumno('19872678-0');


SELECT a.alu_nombre_alumno, a.alu_apellido_alumno,
CAST(AVG(n.nota) AS DECIMAL(3,2)) 'prom_calif'
FROM alumno a, nota n, semestre s, asignatura asig, tipo_semestre ts
WHERE ts.pk_tipo_semestre = s.pk_tipo_semestre and
asig.pk_asignatura = s.pk_asignatura and
asig.pk_asignatura = n.pk_asignatura and
s.pk_semestre = a.pk_semestre and
a.pk_alumno = n.pk_alumno
GROUP BY a.alu_nombre_alumno, a.alu_apellido_alumno
ORDER BY 3 desc;

CALL promedioNotasAlumno

delimiter @@
create procedure promedioNotasAlumno()
begin
SELECT a.alu_nombre_alumno, a.alu_apellido_alumno,
CAST(AVG(n.nota) AS DECIMAL(3,2)) 'prom_calif'
FROM alumno a, nota n, semestre s, asignatura asig, tipo_semestre ts
WHERE ts.pk_tipo_semestre = s.pk_tipo_semestre and
asig.pk_asignatura = s.pk_asignatura and
asig.pk_asignatura = n.pk_asignatura and
s.pk_semestre = a.pk_semestre and
a.pk_alumno = n.pk_alumno
GROUP BY a.alu_nombre_alumno, a.alu_apellido_alumno
ORDER BY 3 desc;
end@@

CALL promedioNotasAlumno;

delimiter @@
create procedure listadoNotasAlumnoAsignatura()
begin
SELECT a.alu_nombre_alumno, a.alu_apellido_alumno, n.nota, asig.asig_nombre
FROM alumno a, nota n, semestre s, asignatura asig, tipo_semestre ts
WHERE ts.pk_tipo_semestre = s.pk_tipo_semestre and
asig.pk_asignatura = s.pk_asignatura and
asig.pk_asignatura = n.pk_asignatura and
s.pk_semestre = a.pk_semestre and
a.pk_alumno = n.pk_alumno
ORDER BY 3 desc;
end@@

CALL listadoNotasAlumnoAsignatura;

delimiter @@
create procedure listadoNotasAlumno()
begin
SELECT a.alu_nombre_alumno, a.alu_apellido_alumno,n.nota
FROM alumno a, nota n, semestre s, asignatura asig, tipo_semestre ts
WHERE ts.pk_tipo_semestre = s.pk_tipo_semestre and
asig.pk_asignatura = s.pk_asignatura and
asig.pk_asignatura = n.pk_asignatura and
s.pk_semestre = a.pk_semestre and
a.pk_alumno = n.pk_alumno
ORDER BY 3 desc;
end@@

CALL listadoNotasAlumno;

#delete from nota where pk_nota=5;

commit;