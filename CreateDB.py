import sqlite3

DATABASE = 'clinica.db'


conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

# Creación de tablas

query1 = '''
CREATE TABLE IF NOT EXISTS Especialidades (
    id_especialidad INTEGER NOT NULL PRIMARY KEY,
    nombre TEXT NOT NULL,
    ruta_img TEXT NOT NULL,
    descripcion TEXT NOT NULL
)
'''
query2 = '''
CREATE TABLE IF NOT EXISTS Profesionales (
    id_profesional INTEGER NOT NULL PRIMARY KEY,
    rol TEXT NOT NULL,
    apellido TEXT NOT NULL,
    nombre TEXT NOT NULL,
    ruta_img TEXT NOT NULL,
    descripcion TEXT,
    id_especialidad INTEGER NOT NULL,
    consultorio INTEGER NOT NULL,
    FOREIGN KEY(id_especialidad)REFERENCES Especialidades(id_especialidad)
)
'''
query3 = '''
create table if not exists Turnos (
        id_turno integer not null primary key,
        fecha text not null,
        hora text not null,
        id_especialidad integer not null,
        id_profesional integer not null,
        id_usuario integer,
        FOREIGN KEY(id_especialidad)REFERENCES Especialidades(id_especialidad),
        FOREIGN KEY(id_profesional)REFERENCES Profesionales(id_profesional)
)
'''
query4 = '''
CREATE TABLE IF NOT EXISTS Usuarios (
        id_usuario INTEGER NOT NULL PRIMARY KEY,
        apellido TEXT NOT NULL,
        nombre TEXT NOT NULL,
        dni TEXT NOT NULL,
        fecha_nacimiento TEXT NOT NULL,
        telefono TEXT,
        email TEXT NOT NULL,
        obra_social INTEGER,
        obra_social_nombre TEXT,
        obra_social_numero TEXT,
        provincia TEXT NOT NULL,
        municipio TEXT NOT NULL,
        localidad TEXT NOT NULL,
        direccion TEXT NOT NULL,
        codigo_postal INTEGER,
        pass TEXT NOT NULL
)    
'''

cursor.execute(query1)
cursor.execute(query2)
cursor.execute(query3)
cursor.execute(query4)

# Inserción de datos
# Insertar datos en Especialidades
datos_Especialidades = [
    (1, 'Clinica Medica', 'img/imgServices/clinicaGeneral.webp', 'La Clinica Medica es la especialidad que se dedica a la atencion integral del adulto enfermo, enfocada en la prevencion, el diagnostico y el tratamiento no quirurgico de las enfermedades que afectan distintos organos y sistemas, trabaja en forma integrada'),
    (2, 'Pediatria', 'img/imgServices/pediatria.webp', 'Sabemos que lo mas importante es que nuestros niños y niñas esten bien siempre. Por eso garantizamos la atencion pediatrica los 365 dias, un servicio unico en la ciudad. Somos un equipo de profesionales comprometidos con la salud de la infancia y la comun'),
    (3, 'Cardiologia', 'img/imgServices/cardiologia.webp', 'La Cardiologia es la rama de la medicina que se ocupa del estudio, diagnostico y tratamiento de enfermedades del corazon y de las enfermedades cardiocirculatorias. Nuestros profesionales brindan una atencion integral al paciente, evaluandolo en asociacion'),
    (4, 'Odontologia', 'img/imgServices/odontologia.webp', 'En nuestra clinica nos esforzamos por brindar atencion dental de alta calidad a nuestros pacientes. Nuestro equipo de profesionales altamente capacitados esta comprometido con la excelencia en todos los aspectos de la atencion dental, desde la prevencion '),
    (5, 'Ginecologia', 'img/imgServices/ginecologia.webp', 'Actualmente brinda atencion en todo lo relacionado a salud femenina, adolescencia, control reproductivo, climaterio y menopausia, uroginecologia, patologias benignas y oncologicas de la mama, utero, ovarios y cuello uterino, videocolposcopias y una serie '),
    (6, 'Nutricion', 'img/imgServices/nutricionista.webp', 'Tenemos como objetivo acompanar procesos, desde el respeto y empatia con el otro, poder brindar educacion en alimentacion para todas las edades con el fin de promover la salud integral. Hacemos un abordaje de nutricion individual y/o familiar. Nos dedicam'),
    (7, 'Psicologia', 'img/imgServices/psicologia.webp', 'La mente es altamente compleja y las afecciones relacionadas con ella pueden ser dificiles de tratar. Los procesos de pensamiento, las emociones, los recuerdos, los suenos, las percepciones, etc., no se pueden ver fisicamente, como una erupcion cutanea o ')
]
cursor.executemany('INSERT INTO Especialidades VALUES (?, ?, ?, ?)', datos_Especialidades)

# Insertar datos en tabla2
datos_Profesionales = [
    (19, 'Dra.', 'Miller', 'Maria', 'img/proffesionals/dra6.webp', 'Medica clinica con experiencia en atencion primaria y cuidado de pacientes hospitalizados.', 1, 1),
    (20, 'Dr.', 'Williams', 'Luis', 'img/proffesionals/dc1.webp', 'Pediatra altamente capacitado y dedicado a brindar atencion medica de calidad a los ninos y adolescentes.', 2, 3),
    (21, 'Dra.', 'Evans', 'Juliana', 'img/proffesionals/dra1.webp', 'Cardiologa con experiencia en diagnostico y tratamiento de enfermedades cardiovasculares, que brinda atencion medica personalizada y de calidad a sus pacientes.', 3, 2),
    (22, 'Dra.', 'Adams', 'Ana', 'img/proffesionals/dra2.webp', 'Pediatra con experiencia en el cuidado de ninos, incluyendo la atencion de enfermedades y problemas de desarrollo.', 2, 1),
    (23, 'Dr.', 'Moore', 'Carlos', 'img/proffesionals/dc2.webp', 'Ginecologo experimentado en el diagnostico y tratamiento de enfermedades y condiciones ginecologicas, brindando atencion medica integral y personalizada a sus pacientes.', 5, 1),
    (24, 'Dra.', 'Taylor', 'Juana', 'img/proffesionals/dra4.webp', 'Psiquiatra con amplia experiencia en el tratamiento de trastornos mentales y emocionales, incluyendo ansiedad, depresion y trastornos del estado de animo.', 7, 2),
    (25, 'Dra.', 'Collins', 'Monica', 'img/proffesionals/dra3.webp', 'Nutricionista especializada en mejorar la salud de sus pacientes con cambios personalizados en la alimentacion y estilo de vida.', 6, 4),
    (26, 'Dr.', 'Wilson', 'Juan', 'img/proffesionals/dc3.webp', 'Odontologo especializado en prevencion, tratamiento y procedimientos dentales cosmeticos para mejorar la salud y estetica oral de sus pacientes.', 4, 3),
    (27, 'Dra.', 'McAllister', 'Ana', 'img/proffesionals/dra5.webp', 'Medica clinica comprometida con el bienestar de sus pacientes y en ofrecer una atencion medica integral y personalizada.', 1, 3)
]
cursor.executemany('INSERT INTO Profesionales VALUES (?, ?, ?, ?, ?, ?, ?, ?)', datos_Profesionales)

conn.commit()
conn.close()





