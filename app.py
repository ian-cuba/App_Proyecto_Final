import sqlite3
import datetime
from flask import Flask,  jsonify, request, render_template
from flask_cors import CORS

DATABASE = 'clinica.db'
#DATABASE = '/home/ianluisnoa/mysite/clinica.db'

conn = sqlite3.connect(DATABASE, check_same_thread=False)
cursor = conn.cursor()

# -------------------------------------------------------------------
# Definimos la clase "Turno"
# -------------------------------------------------------------------
class Turno:
    def __init__(self, id_t, fecha, hora, especialidad, profesional):
        self.id_turno = id_t
        self.fecha = fecha
        self.hora = hora
        self.especialidad = especialidad
        self.profesional = profesional
        #self.usuario = usuario

    def modificar(self, fecha, hora):
        self.fecha = fecha
        self.hora = hora

# -------------------------------------------------------------------
# Definimos la clase "Turnero"
# -------------------------------------------------------------------
class Turnero:
    def __init__(self):
        self.conexion = conn
        self.cursor = self.conexion.cursor()

    def agregar_turno(self, fecha, hora, especialidad, profesional):
        turno_existente = self.consultar_turno(fecha, hora)
        if turno_existente:
            return jsonify({'message': 'Ya existe un turno reservado en esa fecha y hora.'}), 400
        
        self.cursor.execute("INSERT INTO Turnos (fecha, hora, id_especialidad, id_profesional) VALUES (?, ?, ?, ?)", (fecha, hora, especialidad, profesional))
        self.conexion.commit()
        return jsonify({'message': 'Turno agregado exitosamente.'}), 200

    def consultar_turno(self, fecha, hora):
        self.cursor.execute("SELECT fecha, hora, id_especialidad, id_profesional FROM Turnos WHERE fecha = ? AND hora = ?", (fecha,hora))
        row = self.cursor.fetchone()
        if row:
            fecha, hora, especialidad, profesional = row
            return Turno(fecha, hora, especialidad, profesional)
        return None
    
    def consultar_turno_profesional(self,id_t, especialidad, profesional):
        self.cursor.execute("SELECT id_turno, fecha, hora, id_especialidad, id_profesional FROM Turnos WHERE id_turno = ? AND id_especialidad = ? AND id_profesional = ?", (id_t, especialidad, profesional))
        row = self.cursor.fetchone()
        if row:
            id_t, fecha, hora, especialidad, profesional = row
            return Turno(id_t, fecha, hora, especialidad, profesional)
        return None

    def modificar_turno(self,id_t, especialidad, profesional, nueva_fecha, nueva_hora):
        turno = self.consultar_turno_profesional(id_t,especialidad, profesional)
        if turno:
            turno.modificar(nueva_fecha, nueva_hora)
            self.cursor.execute("UPDATE Turnos SET fecha = ?, hora = ? WHERE id_turno = ? AND id_especialidad = ? AND id_profesional = ?",
                                (nueva_fecha, nueva_hora, id_t, especialidad, profesional))
            self.conexion.commit()
            return jsonify({'message': 'Turno modificado exitosamente.'}), 200
        return jsonify({'message': 'Turno no encontrado.'}), 404


    def listar_turnos(self):
        print("-" * 30)
        # self.cursor.execute("SELECT t.fecha, t.hora, e.nombre, p.rol, p.apellido, p.nombre, u.apellido, u.nombre, p.consultorio FROM Turnos AS t,Especialidades AS e, Profesionales AS p, Usuarios AS u WHERE t.id_usuario = u.id_usuario AND t.id_profesional = p.id_profesional AND t.id_especialidad = e.id_especialidad")
        self.cursor.execute("SELECT t.id_turno, t.fecha, t.hora, t.id_especialidad, t.id_profesional, e.nombre, p.rol, p.apellido, p.nombre, p.consultorio FROM Turnos AS t,Especialidades AS e, Profesionales AS p WHERE t.id_profesional = p.id_profesional AND t.id_especialidad = e.id_especialidad")
        rows = self.cursor.fetchall()
        turnos = []
        for row in rows:
            id_t, fecha, hora, id_e, id_p, especialidad, rolP, apellidoP, nombreP, consultorio = row
            turno = {'id_t': id_t, 'fecha': fecha, 'hora': hora, 'id_e': id_e, 'id_p':id_p, 'especialidad': especialidad, 'profesional': rolP + ' ' + nombreP + ' ' + apellidoP, 'consultorio': consultorio}
            turnos.append(turno)
        return jsonify(turnos), 200
    '''
    def eliminar_turno(self, fecha, hora):
        self.cursor.execute("DELETE FROM Turnos WHERE fecha = ? AND hora = ?", (fecha,hora))
        if self.cursor.rowcount > 0:
            self.conexion.commit()
            return jsonify({'message': 'Turno eliminado exitosamente.'}), 200
        return jsonify({'message': 'Turno no encontrado.'}), 404'''
    
    def eliminar_turno(self, fecha, hora):
        # Obtener la fecha y hora actual
        fecha_actual = datetime.date.today()
        hora_actual = datetime.datetime.now().time()

        # Convertir la fecha y hora del turno a objetos datetime
        fecha_turno = datetime.datetime.strptime(fecha, "%Y-%m-%d").date()
        hora_turno = datetime.datetime.strptime(hora, "%H:%M").time()

        # Calcular la diferencia de tiempo entre el turno y la fecha/hora actual
        tiempo_restante = datetime.datetime.combine(fecha_turno, hora_turno) - datetime.datetime.combine(fecha_actual, hora_actual)

        # Verificar si hay al menos 48 horas de anticipación
        if tiempo_restante.total_seconds() >= 48 * 60 * 60:
            self.cursor.execute("DELETE FROM Turnos WHERE fecha = ? AND hora = ?", (fecha, hora))
            if self.cursor.rowcount > 0:
                self.conexion.commit()
                return jsonify({'message': 'Turno eliminado exitosamente.'}), 200
            else:
                return jsonify({'message': 'Turno no encontrado.'}), 404
        else:
            return jsonify({'message': 'No se puede eliminar el turno con menos de 48 horas de anticipación.'}), 404
    
'''
# -------------------------------------------------------------------
# Definimos la clase "Usuario"
# -------------------------------------------------------------------
class Usuario:
    def __init__(self, id_usuario, apellido, nombre, dni, fecha_nacimiento, telefono, email, obra_social, obra_social_nombre, obra_social_numero, provincia, municipio, localidad, direccion, codigo_postal, contraseña):
        self.id_usuario = id_usuario
        self.apellido = apellido
        self.nombre = nombre
        self.dni = dni
        self.fecha_nacimiento = fecha_nacimiento
        self.telefono = telefono
        self.email = email
        self.obra_social = obra_social
        self.obra_social_nombre = obra_social_nombre
        self.obra_social_numero = obra_social_numero
        self.provincia = provincia
        self.municipio = municipio
        self.localidad = localidad
        self.direccion = direccion
        self.codigo_postal = codigo_postal
        self.contraseña = contraseña

    def modificar(self, nuevo_apellido, nuevo_nombre, nuevo_dni, nueva_fecha_nacimiento, nuevo_telefono, nuevo_email, nueva_obra_social, nuevo_obra_social_nombre, nuevo_obra_social_numero, nueva_provincia, nuevo_municipio, nueva_localidad, nueva_direccion, nuevo_codigo_postal, nueva_contraseña):
        self.apellido = nuevo_apellido
        self.nombre = nuevo_nombre
        self.dni = nuevo_dni
        self.fecha_nacimiento = nueva_fecha_nacimiento
        self.telefono = nuevo_telefono
        self.email = nuevo_email
        self.obra_social = nueva_obra_social
        self.obra_social_nombre = nuevo_obra_social_nombre
        self.obra_social_numero = nuevo_obra_social_numero
        self.provincia = nueva_provincia
        self.municipio = nuevo_municipio
        self.localidad = nueva_localidad
        self.direccion = nueva_direccion
        self.codigo_postal = nuevo_codigo_postal
        self.contraseña = nueva_contraseña

# -------------------------------------------------------------------
# Definimos la clase "Usuarios"
# -------------------------------------------------------------------
class Usuarios:
    def __init__(self):
        self.conexion = conn
        self.cursor = self.conexion.cursor()

    def agregar_usuario(self, apellido, nombre, dni, fecha_nacimiento, telefono, email, obra_social, obra_social_nombre, obra_social_numero, provincia, municipio, localidad, direccion, codigo_postal, contraseña):
        usuario_existente = self.consultar_usuario(email)
        if usuario_existente:
            print("Ya existe un usuario con ese email.")
            return False
        self.cursor.execute("INSERT INTO Usuarios (apellido, nombre, dni, fecha_nacimiento, telefono, email, obra_social, obra_social_nombre, obra_social_numero, provincia, municipio, localidad, direccion, codigo_postal, pass) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (apellido, nombre, dni, fecha_nacimiento, telefono, email, obra_social, obra_social_nombre, obra_social_numero, provincia, municipio, localidad, direccion, codigo_postal, contraseña))
        self.conexion.commit()
        print("Usuario añadido correctamente.")
        return True

    def consultar_usuario(self, email):
        self.cursor.execute("SELECT * FROM Usuarios WHERE email = ?", (email,))
        row = self.cursor.fetchone()
        if row:
            id_usuario, apellido, nombre, dni, fecha_nacimiento, telefono, email, obra_social, obra_social_nombre, obra_social_numero, provincia, municipio, localidad, direccion, codigo_postal, contraseña = row
            return Usuario(id_usuario, apellido, nombre, dni, fecha_nacimiento, telefono, email, obra_social, obra_social_nombre, obra_social_numero, provincia, municipio, localidad, direccion, codigo_postal, contraseña)
        return False

    def modificar_usuario(self, email, nuevo_apellido, nuevo_nombre, nuevo_dni, nueva_fecha_nacimiento, nuevo_telefono, nuevo_email, nueva_obra_social, nuevo_obra_social_nombre, nuevo_obra_social_numero, nueva_provincia, nuevo_municipio, nueva_localidad, nueva_direccion, nuevo_codigo_postal, nueva_contraseña):
        usuario = self.consultar_usuario(email)
        if usuario:
            usuario.modificar(nuevo_apellido, nuevo_nombre, nuevo_dni, nueva_fecha_nacimiento, nuevo_telefono, nuevo_email, nueva_obra_social, nuevo_obra_social_nombre, nuevo_obra_social_numero, nueva_provincia, nuevo_municipio, nueva_localidad, nueva_direccion, nuevo_codigo_postal, nueva_contraseña)
            self.cursor.execute("UPDATE Usuarios SET apellido = ?, nombre = ?, dni = ?, fecha_nacimiento = ?, telefono = ?, email = ?, obra_social = ?, obra_social_nombre = ?, obra_social_numero = ?, provincia = ?, municipio = ?, localidad = ?, direccion = ?, codigo_postal = ?, pass = ? WHERE email = ?",
                    (nuevo_apellido, nuevo_nombre, nuevo_dni, nueva_fecha_nacimiento, nuevo_telefono, nuevo_email, nueva_obra_social, nuevo_obra_social_nombre, nuevo_obra_social_numero, nueva_provincia, nuevo_municipio, nueva_localidad, nueva_direccion, nuevo_codigo_postal, nueva_contraseña, email))
            self.conexion.commit()
            print("Usuario modificado exitosamente.")
        else:
            print("No se pudo modificar el usuario. El usuario no fue encontrado.")

    def eliminar_usuario(self, email):
        self.cursor.execute("DELETE FROM Turnos WHERE email = ?", (email,))
        if self.cursor.rowcount > 0:
            self.conexion.commit()
            return jsonify({'message': 'Usuario eliminado exitosamente.'}), 200
        return jsonify({'message': 'Usuario no encontrado.'}), 404
'''

# -------------------------------------------------------------------
# Función para listar especialidades
# -------------------------------------------------------------------
def listar_especialidades():
    especialidades = []
    cursor.execute("SELECT id_especialidad, nombre, ruta_img, descripcion FROM Especialidades")
    rows = cursor.fetchall()
    for row in rows:
        id_e, nombre, ruta_img, descripcion = row
        especialidad = {'id': id_e, 'ruta_imagen': ruta_img, 'nombre': nombre, 'descripcion': descripcion}
        especialidades.append(especialidad)
    return jsonify(especialidades), 200

# Para listar solo los nombre para el submenú
def listar_nombre_especialidades():
    especialidades = []
    cursor.execute("SELECT id_especialidad, nombre FROM Especialidades")
    rows = cursor.fetchall()
    for row in rows:
        id_e, nombre = row
        especialidad = {'id': id_e, 'nombre': nombre}
        especialidades.append(especialidad)
    return jsonify(especialidades), 200

# -------------------------------------------------------------------
# Función para listar profesionales
# -------------------------------------------------------------------
def listar_profesionales():
    profesionales = []
    cursor.execute("SELECT rol, nombre, apellido, descripcion, ruta_img FROM Profesionales")
    rows = cursor.fetchall()
    for row in rows:
        rol, nombre, apellido, descripcion, ruta_img = row
        profesional = {'ruta_imagen': ruta_img, 'nombre': rol + ' ' + nombre + ' ' + apellido, 'descripcion': descripcion}
        profesionales.append(profesional)
    return jsonify(profesionales), 200


# -------------------------------------------------------------------
# Configuración y rutas de la API Flask
# -------------------------------------------------------------------

#app = Flask(__name__, template_folder='https://centrosaludintegral.netlify.app/')
app = Flask(__name__)
CORS(app)

#usuarios = Usuarios()   # Instanciamos los usuarios
turnero = Turnero()     # Instanciamos un turnero

# Ruta para obtener la lista de nombres de especialidades para el submenu
@app.route('/submenu', methods=['GET'])
def obtener_nombre_especialidades():
    return listar_nombre_especialidades()

# Ruta para obtener la lista de especialidades
@app.route('/services', methods=['GET'])
def obtener_especialidades():
    return listar_especialidades()

# Ruta para obtener la lista de profesionales
@app.route('/professionals', methods=['GET'])
def obtener_profesionales():
    return listar_profesionales()

# Ruta para obtener la lista de turnos del turnero
@app.route('/turns', methods=['GET'])
def obtener_turnos():
    return turnero.listar_turnos()

# Ruta para agregar un turno al turnero
@app.route('/new_turn', methods=['POST'])
def agregar_turno():
    fecha = request.json.get('fecha')
    hora = request.json.get('hora')
    especialidad = request.json.get('especialidad')
    profesional = request.json.get('profesional')
    # usuario = request.json.get('usuario')
    return turnero.agregar_turno(fecha, hora, especialidad, profesional)

# Ruta para obtener los datos de un turno según su especialidad y profesional
@app.route('/turns/<int:id_t>&<int:especialidad>&<int:profesional>', methods=['GET'])
def obtener_turno(id_t,especialidad,profesional):
    turno = turnero.consultar_turno_profesional(id_t,especialidad,profesional)
    if turno:
        return jsonify({
            'id_t': turno.id_turno,
            'fecha': turno.fecha,
            'hora': turno.hora,
            'especialidad': turno.especialidad,
            'profesional': turno.profesional
        }), 200
    return jsonify({'message': 'Turno no encontrado.'}), 404

# Ruta para modificar un turno del turnero
@app.route('/turns/<int:id_t>&<int:especialidad>&<int:profesional>', methods=['PUT'])
def modificar_turno(id_t,especialidad, profesional):
    nueva_fecha = request.json.get('fecha')
    nueva_hora = request.json.get('hora')
    return turnero.modificar_turno(id_t,especialidad, profesional, nueva_fecha, nueva_hora)

# Ruta para eliminar un turno del turnero
@app.route('/turns/<string:fecha>&<string:hora>', methods=['DELETE'])
def eliminar_turno(fecha, hora):
    return turnero.eliminar_turno(fecha, hora)

# Ruta para devolver las especialidades para el select de nuevo turno
@app.route('/new_turn', methods=['GET'])
def get_especialidades():
    cursor.execute("SELECT * FROM Especialidades")
    rows = cursor.fetchall()
    especialidades = [{'id_especialidad': row[0], 'nombre': row[1]} for row in rows]
    return jsonify(especialidades)

# Ruta para devolver las especialidades para el select de nuevo turno
@app.route('/update_turn', methods=['GET'])
def get_professionals():
    cursor.execute("SELECT * FROM Profesionales")
    rows = cursor.fetchall()
    profesionales = [{'id_profesional': row[0], 'rol': row[1], 'apellido': row[2], 'nombre': row[3]} for row in rows]
    return jsonify(profesionales)

# Ruta para devolver profesionales dado una especialidad para el select de nuevo turno
@app.route('/new_turn/<int:id_especialidad>', methods=['GET'])
def get_profesionales(id_especialidad):
    cursor.execute("SELECT * FROM Profesionales WHERE id_especialidad = ?", (id_especialidad,))
    rows = cursor.fetchall()
    profesionales = [{'id_profesional': row[0], 'rol': row[1], 'apellido': row[2], 'nombre': row[3]} for row in rows]
    return jsonify(profesionales)

# Rutas para renderizar cada página y redirigir a 404 en caso de que no se ninguna de estas URL
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/new_turn')
def new_turn():
    return render_template('new_turn.html')

@app.route('/professionals')
def professionals():
    return render_template('professionals.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/recovery')
def recovery():
    return render_template('recovery.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/turns')
def turns():
    return render_template('turns.html')

@app.route('/update_turn')
def update_turn():
    return render_template('update_turn.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

# Finalmente, si estamos ejecutando este archivo, lanzamos app.
if __name__ == '__main__':
    app.run()