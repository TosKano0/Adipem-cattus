CREATE TABLE categoria (
    id_categoria INTEGER NOT NULL PRIMARY KEY,
    categoria TEXT NOT NULL
);

CREATE TABLE estado (
    id_estado INTEGER NOT NULL PRIMARY KEY,
    tipo_estado TEXT NOT NULL
);

CREATE TABLE historial_login (
    id_hislog INTEGER NOT NULL PRIMARY KEY,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    nombre_rol TEXT NOT NULL,
    email TEXT NOT NULL,
    fecha_log TEXT NOT NULL
);

CREATE TABLE historial_reporte (
    id_historial INTEGER NOT NULL PRIMARY KEY,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    fecha_cambio TEXT NOT NULL
);

CREATE TABLE Locacion (
    id_locacion INTEGER NOT NULL PRIMARY KEY,
    edificio TEXT NOT NULL,
    nro_piso INTEGER NOT NULL,
    sala_u_otros TEXT NOT NULL
);

CREATE TABLE prioridad (
    id_prioridad INTEGER NOT NULL PRIMARY KEY,
    nivel_prioridad TEXT NOT NULL
);

CREATE TABLE rol (
    id_rol INTEGER NOT NULL PRIMARY KEY,
    nombre_rol TEXT NOT NULL
);

CREATE TABLE usuario (
    id_usuario INTEGER NOT NULL,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    email TEXT NOT NULL,
    contraseña TEXT NOT NULL,
    edad INTEGER NOT NULL,
    genero TEXT NOT NULL,
    nombre_rol TEXT NOT NULL,
    rol_id_rol INTEGER NOT NULL,
    PRIMARY KEY (id_usuario, rol_id_rol),
    FOREIGN KEY (rol_id_rol) REFERENCES rol(id_rol)
);

CREATE TABLE Relation_3 (
    usuario_id_usuario INTEGER NOT NULL,
    usuario_rol_id_rol INTEGER NOT NULL,
    historial_login_id_hislog INTEGER NOT NULL,
    PRIMARY KEY (usuario_id_usuario, usuario_rol_id_rol, historial_login_id_hislog),
    FOREIGN KEY (historial_login_id_hislog) REFERENCES historial_login(id_hislog),
    FOREIGN KEY (usuario_id_usuario, usuario_rol_id_rol) REFERENCES usuario(id_usuario, rol_id_rol)
);

CREATE TABLE reporte (
    id_reporte INTEGER NOT NULL,
    categoria TEXT NOT NULL,
    titulo_reporte TEXT NOT NULL,
    descripcion TEXT NOT NULL,
    nombre_rol TEXT NOT NULL,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    edificio TEXT NOT NULL,
    nro_piso INTEGER NOT NULL,
    sala_u_otro TEXT NOT NULL,
    foto BLOB NOT NULL,
    nivel_prioridad TEXT NOT NULL,
    usuario_id_usuario INTEGER NOT NULL,
    usuario_rol_id_rol INTEGER NOT NULL,
    Locacion_id_locacion INTEGER NOT NULL,
    prioridad_id_prioridad INTEGER NOT NULL,
    categoria_id_categoria INTEGER NOT NULL,
    estado_id_estado INTEGER NOT NULL,
    historial_reporte_id_historial INTEGER NOT NULL,
    PRIMARY KEY (
        id_reporte,
        usuario_id_usuario,
        usuario_rol_id_rol,
        Locacion_id_locacion,
        prioridad_id_prioridad,
        categoria_id_categoria,
        estado_id_estado,
        historial_reporte_id_historial
    ),
    FOREIGN KEY (categoria_id_categoria) REFERENCES categoria(id_categoria),
    FOREIGN KEY (estado_id_estado) REFERENCES estado(id_estado),
    FOREIGN KEY (historial_reporte_id_historial) REFERENCES historial_reporte(id_historial),
    FOREIGN KEY (Locacion_id_locacion) REFERENCES Locacion(id_locacion),
    FOREIGN KEY (prioridad_id_prioridad) REFERENCES prioridad(id_prioridad),
    FOREIGN KEY (usuario_id_usuario, usuario_rol_id_rol) REFERENCES usuario(id_usuario, rol_id_rol)
);
