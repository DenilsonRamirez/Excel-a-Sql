import pandas as pd
from datetime import datetime

# Leer archivos Excel
estudiantes_df = pd.read_excel('archivo.xlsx', sheet_name='Estudiantes')
catedraticos_df = pd.read_excel('archivo.xlsx', sheet_name='Catedráticos')
cursos_df = pd.read_excel('archivo.xlsx', sheet_name='Cursos')

# Abrir archivo SQL para escribir
with open('insertar_datos.sql', 'w', encoding='utf-8') as f:
    # Escribir encabezado
    f.write("-- Script generado automáticamente para insertar datos\n\n")

    # Insertar estudiantes
    f.write("-- Insertar estudiantes\n")
    for _, row in estudiantes_df.iterrows():
        f.write(f"INSERT INTO estudiantes (nombreEst, apellidoEst, codigoEst) VALUES ('{row['Nombres']}', '{row['Apellidos']}', '{row['Código Personal']}');\n")
    f.write("\n")

    # Insertar catedráticos (users)
    f.write("-- Insertar catedráticos\n")
    for _, row in catedraticos_df.iterrows():
        email = f"{row['Nombre'].lower().replace(' ', '.')}@ejemplo.com"
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"INSERT INTO users (name, email, password, created_at, updated_at) VALUES ('{row['Nombre']}', '{email}', 'placeholder', '{now}', '{now}');\n")
    f.write("\n")

    # Insertar cursos
    f.write("-- Insertar cursos\n")
    for _, row in cursos_df.iterrows():
        secciones = [sec.strip() for sec in row['Seccion'].split(',')]
        for seccion in secciones:
            nombre_curso = f"{row['Nombre Curso']} - Sección {seccion}"
            f.write(f"INSERT INTO cursos (nombreCurso, anio, Catedratico, Carrera, Grado) VALUES ('{nombre_curso}', 2024, {row['Catedrático ID']}, '{row['Carrera']}', '{row['Grado']}');\n")
    f.write("\n")

    # Asignar estudiantes a cursos
    f.write("-- Asignar estudiantes a cursos\n")
    for _, estudiante in estudiantes_df.iterrows():
        grado = estudiante['Grado']
        seccion = estudiante['Seccion']
        carrera = estudiante['Carrera']
        cursos_estudiante = cursos_df[(cursos_df['Grado'] == grado) & (cursos_df['Carrera'] == carrera)]
        for _, curso in cursos_estudiante.iterrows():
            if seccion in [sec.strip() for sec in curso['Seccion'].split(',')]:
                nombre_curso = f"{curso['Nombre Curso']} - Sección {seccion}"
                f.write(f"INSERT INTO estudiantesporcurso (estudiante, curso) VALUES ((SELECT idEstudiante FROM estudiantes WHERE codigoEst = '{estudiante['Código Personal']}'), (SELECT idCurso FROM cursos WHERE nombreCurso = '{nombre_curso}' AND Grado = '{grado}' AND Carrera = '{carrera}'));\n")

print("Archivo SQL generado: insertar_datos.sql")