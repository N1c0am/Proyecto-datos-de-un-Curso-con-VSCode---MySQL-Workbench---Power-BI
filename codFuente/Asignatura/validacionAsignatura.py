def validar_id(pk_asignatura: str) -> bool:
    return(pk_asignatura.isnumeric() and len(pk_asignatura)<=2)

def validar_nombre(asig_nombre: str) -> bool:
    if asig_nombre.isalpha:
        asig_nombre = asig_nombre.strip()
        return(len(asig_nombre) > 0 and len(asig_nombre)<=100)

