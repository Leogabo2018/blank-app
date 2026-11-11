def registrar_usuario(identificacion, contrasena):
    return True

def validar_login(identificacion, contrasena):
    return True

def buscar_paciente(criterio):
    if criterio == "10234567" or criterio == "AT-9981":
        return {
            "id_registro": 1,
            "cama": "UCI-101",
            "nombre_paciente": "Carlos Mario Restrepo (Ficticio)",
            "num_atencion": "AT-9981",
            "edad": 62,
            "diagnostico": "J960 - Insuficiencia respiratoria aguda, Sepsis de origen urinario",
            "alergia_si_no": "Sí",
            "alergia_detalle": "Penicilina / Ampicilina",
            "aislamiento": "Contacto",
            "cant_periferico": 1,
            "cant_picc": 0,
            "cant_linea_media": 0,
            "cant_cvc": 1,
            "cant_linea_arterial": 0,
            "cant_alto_flujo": 0,
            "medico_tratante": "Dr. Alejandro Méndez (Intensivista)"
        }
    return None

def guardar_evaluacion_sbar(datos):
    return True
