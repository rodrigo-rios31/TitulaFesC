# backend/utils/seed.py
"""
Pobla la base de datos con datos iniciales de carreras, opciones de titulación
y sus requisitos. Ejecutar solo una vez o cuando la DB esté vacía.
"""
from sqlalchemy.orm import Session
from backend.database import Carrera, OpcionTitulacion, Requisito

SEED_DATA = [
    {
        "nombre": "Ingeniería Industrial",
        "clave": "II",
        "opciones": [
            {
                "nombre": "Tesis",
                "requisitos": [
                    {"nombre": "Constancia DGAE", "descripcion": "Documento de no adeudo con la DGAE.", "instrucciones": "Solicítala en ventanilla DGAE con tu credencial vigente. Debe tener sello y firma.", "orden": 1},
                    {"nombre": "No adeudo de Biblioteca", "descripcion": "Carta de no adeudo de libros.", "instrucciones": "Acude a biblioteca con tu credencial. El proceso tarda aprox. 1 día hábil.", "orden": 2},
                    {"nombre": "Fotografías", "descripcion": "3 fotos tamaño título en blanco y negro.", "instrucciones": "Deben ser en blanco y negro, fondo blanco, ropa formal, sin lentes. Tamaño 3.5 x 4.5 cm.", "orden": 3},
                    {"nombre": "Comprobante de pago de derechos", "descripcion": "Pago oficial de titulación.", "instrucciones": "Realiza el pago en la caja de la facultad o en banco con la referencia de titulación.", "orden": 4},
                    {"nombre": "Acta de nacimiento", "descripcion": "Copia certificada del acta de nacimiento.", "instrucciones": "Copia reciente (no mayor a 1 año). Puede ser digital del Registro Civil.", "orden": 5},
                    {"nombre": "CURP", "descripcion": "Copia del CURP.", "instrucciones": "Descarga la versión actualizada desde https://www.gob.mx/curp", "orden": 6},
                    {"nombre": "Certificado de Bachillerato", "descripcion": "Original o copia certificada.", "instrucciones": "Si es copia debe estar certificada por notario o institución de origen.", "orden": 7},
                    {"nombre": "Tesis impresa y digital", "descripcion": "Ejemplar impreso + CD con PDF de la tesis.", "instrucciones": "La tesis debe estar firmada por tu asesor en la portada. El CD debe estar etiquetado con tu nombre y título.", "orden": 8, "permite_archivo": True},
                    {"nombre": "Carta de no adeudo de Coordinación", "descripcion": "Firma de coordinador de carrera.", "instrucciones": "Solicita al coordinador de tu carrera con anticipación.", "orden": 9},
                ],
            },
            {
                "nombre": "Artículo de Investigación Publicado",
                "requisitos": [
                    {"nombre": "Constancia DGAE", "descripcion": "Documento de no adeudo con la DGAE.", "instrucciones": "Solicítala en ventanilla DGAE con tu credencial vigente.", "orden": 1},
                    {"nombre": "No adeudo de Biblioteca", "descripcion": "Carta de no adeudo de libros.", "instrucciones": "Acude a biblioteca con tu credencial.", "orden": 2},
                    {"nombre": "Fotografías", "descripcion": "3 fotos tamaño título en blanco y negro.", "instrucciones": "Deben ser en blanco y negro, fondo blanco, ropa formal, sin lentes.", "orden": 3},
                    {"nombre": "Comprobante de pago de derechos", "descripcion": "Pago oficial de titulación.", "instrucciones": "Realiza el pago en la caja de la facultad.", "orden": 4},
                    {"nombre": "Artículo publicado (PDF)", "descripcion": "PDF del artículo con ISSN de la revista.", "instrucciones": "Debe ser revista indexada. Incluye la carta de aceptación o constancia de publicación.", "orden": 5, "permite_archivo": True},
                    {"nombre": "Carta de participación del asesor", "descripcion": "Carta del asesor que avala tu participación.", "instrucciones": "Firmada y con sello del departamento.", "orden": 6},
                    {"nombre": "Acta de nacimiento", "descripcion": "Copia certificada.", "instrucciones": "No mayor a 1 año.", "orden": 7},
                    {"nombre": "CURP", "descripcion": "Copia del CURP.", "instrucciones": "Descarga actualizada desde gob.mx/curp.", "orden": 8},
                ],
            },
        ],
    },
    {
        "nombre": "Ingeniería en Computación",
        "clave": "IC",
        "opciones": [
            {
                "nombre": "Tesis",
                "requisitos": [
                    {"nombre": "Constancia DGAE", "descripcion": "Documento de no adeudo con la DGAE.", "instrucciones": "Solicítala en ventanilla DGAE con tu credencial vigente.", "orden": 1},
                    {"nombre": "No adeudo de Biblioteca", "descripcion": "Carta de no adeudo de libros.", "instrucciones": "Acude a biblioteca con tu credencial.", "orden": 2},
                    {"nombre": "Fotografías", "descripcion": "3 fotos tamaño título en blanco y negro.", "instrucciones": "Deben ser en blanco y negro, fondo blanco, ropa formal, sin lentes.", "orden": 3},
                    {"nombre": "Comprobante de pago de derechos", "descripcion": "Pago oficial de titulación.", "instrucciones": "Realiza el pago en la caja de la facultad.", "orden": 4},
                    {"nombre": "Acta de nacimiento", "descripcion": "Copia certificada.", "instrucciones": "No mayor a 1 año.", "orden": 5},
                    {"nombre": "CURP", "descripcion": "Copia del CURP.", "instrucciones": "Descarga actualizada desde gob.mx/curp.", "orden": 6},
                    {"nombre": "Tesis impresa y digital", "descripcion": "Ejemplar impreso + USB/CD con PDF.", "instrucciones": "La tesis debe estar firmada por tu asesor. Incluye código fuente en el USB si aplica.", "orden": 7, "permite_archivo": True},
                    {"nombre": "Repositorio de código (URL)", "descripcion": "URL del repositorio GitHub/GitLab del proyecto.", "instrucciones": "El repositorio debe ser público o compartido con el comité. Incluye README.", "orden": 8, "permite_archivo": False},
                ],
            },
            {
                "nombre": "Proyecto de Aplicación",
                "requisitos": [
                    {"nombre": "Constancia DGAE", "descripcion": "Documento de no adeudo con la DGAE.", "instrucciones": "Solicítala en ventanilla DGAE con tu credencial vigente.", "orden": 1},
                    {"nombre": "No adeudo de Biblioteca", "descripcion": "Carta de no adeudo de libros.", "instrucciones": "Acude a biblioteca con tu credencial.", "orden": 2},
                    {"nombre": "Fotografías", "descripcion": "3 fotos tamaño título en blanco y negro.", "instrucciones": "Deben ser en blanco y negro, fondo blanco, ropa formal, sin lentes.", "orden": 3},
                    {"nombre": "Comprobante de pago de derechos", "descripcion": "Pago oficial de titulación.", "instrucciones": "Realiza el pago en la caja de la facultad.", "orden": 4},
                    {"nombre": "Informe técnico del proyecto", "descripcion": "Documento técnico del sistema desarrollado.", "instrucciones": "Debe incluir: introducción, análisis, diseño, implementación, pruebas y conclusiones.", "orden": 5, "permite_archivo": True},
                    {"nombre": "Demo funcional o manual de usuario", "descripcion": "Demostración del sistema o manual detallado.", "instrucciones": "Puede ser un video demostrativo o documento PDF del manual.", "orden": 6, "permite_archivo": True},
                    {"nombre": "Acta de nacimiento", "descripcion": "Copia certificada.", "instrucciones": "No mayor a 1 año.", "orden": 7},
                    {"nombre": "CURP", "descripcion": "Copia del CURP.", "instrucciones": "Descarga actualizada desde gob.mx/curp.", "orden": 8},
                ],
            },
        ],
    },
    {
        "nombre": "Administración",
        "clave": "ADM",
        "opciones": [
            {
                "nombre": "Tesis",
                "requisitos": [
                    {"nombre": "Constancia DGAE", "descripcion": "Documento de no adeudo con la DGAE.", "instrucciones": "Solicítala en ventanilla DGAE con tu credencial vigente.", "orden": 1},
                    {"nombre": "No adeudo de Biblioteca", "descripcion": "Carta de no adeudo de libros.", "instrucciones": "Acude a biblioteca con tu credencial.", "orden": 2},
                    {"nombre": "Fotografías", "descripcion": "3 fotos tamaño título en blanco y negro.", "instrucciones": "Deben ser en blanco y negro, fondo blanco, ropa formal, sin lentes.", "orden": 3},
                    {"nombre": "Comprobante de pago de derechos", "descripcion": "Pago oficial de titulación.", "instrucciones": "Realiza el pago en la caja de la facultad.", "orden": 4},
                    {"nombre": "Acta de nacimiento", "descripcion": "Copia certificada.", "instrucciones": "No mayor a 1 año.", "orden": 5},
                    {"nombre": "CURP", "descripcion": "Copia del CURP.", "instrucciones": "Descarga actualizada desde gob.mx/curp.", "orden": 6},
                    {"nombre": "Tesis impresa y digital", "descripcion": "Ejemplar impreso + CD con PDF.", "instrucciones": "Firmada por asesor en portada. CD etiquetado con nombre y título.", "orden": 7, "permite_archivo": True},
                    {"nombre": "Carta de empresa (si aplica)", "descripcion": "Carta de la empresa donde se realizó el estudio.", "instrucciones": "Solo si tu tesis es caso de empresa real. Con membrete y firma del responsable.", "orden": 8, "obligatorio": False, "permite_archivo": True},
                ],
            },
        ],
    },
]


def run_seed(db: Session):
    if db.query(Carrera).count() > 0:
        print("⚠️  La base de datos ya tiene datos. Saltando seed.")
        return

    for carrera_data in SEED_DATA:
        carrera = Carrera(nombre=carrera_data["nombre"], clave=carrera_data["clave"])
        db.add(carrera)
        db.flush()

        for opcion_data in carrera_data["opciones"]:
            opcion = OpcionTitulacion(nombre=opcion_data["nombre"], carrera_id=carrera.id)
            db.add(opcion)
            db.flush()

            for i, req_data in enumerate(opcion_data["requisitos"]):
                req = Requisito(
                    nombre=req_data["nombre"],
                    descripcion=req_data.get("descripcion"),
                    instrucciones=req_data.get("instrucciones"),
                    obligatorio=req_data.get("obligatorio", True),
                    permite_archivo=req_data.get("permite_archivo", True),
                    opcion_id=opcion.id,
                    orden=req_data.get("orden", i),
                )
                db.add(req)

    db.commit()
    print("✅ Seed completado.")
