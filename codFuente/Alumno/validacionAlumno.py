def validar_id(pk_alumno: str) -> bool:
    return(len(pk_alumno)==10)

def validar_nombre(alu_nombre_alumno: str) -> bool:
    if alu_nombre_alumno.isalpha:
        alu_nombre_alumno = alu_nombre_alumno.strip()
        return(len(alu_nombre_alumno) > 0 and len(alu_nombre_alumno)<=30)

def validar_apellido(alu_apellido_alumno: str) -> bool:
    if alu_apellido_alumno.isalpha:
        alu_apellido_alumno = alu_apellido_alumno.strip()
        return(len(alu_apellido_alumno) > 0 and len(alu_apellido_alumno)<=30)

def validar_direccion(alu_direccion: str) -> bool:
    if alu_direccion.isalpha:
        alu_direccion = alu_direccion.strip()
        return(len(alu_direccion) > 0 and len(alu_direccion)<=30)
