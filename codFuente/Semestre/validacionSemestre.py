from time import *
from datetime import *

def validar_id(pk_semestre: str) -> bool:
    return(pk_semestre.isnumeric() and len(pk_semestre)<=2)

#def validar_fecha(fecha: datetime) -> bool:
 #       fecha = datetime.date("%y/%m/%d")
   #     return(fecha)

