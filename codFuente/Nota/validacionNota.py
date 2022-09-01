def validar_id(pk_nota: str) -> bool:
    return(len(pk_nota)<=3)

def validar_nota(nota: str) -> bool:
        nota = nota.strip()
        return(len(nota) > 0 and len(nota)<=3)

def validar_num_nota(num_nota: str) -> bool:
    if num_nota.isalpha:
        num_nota = num_nota.strip()
        return(len(num_nota)<=10)
