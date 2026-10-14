from datetime import datetime

from .constantes import FORMATO_DATA
from .utilitarios_erros import FormatoDataInvalidaErro

def validar_data(data: str):
    data_convertida = datetime.strptime(data, FORMATO_DATA)
    
    if data_convertida.strftime(FORMATO_DATA) != data:
        raise FormatoDataInvalidaErro(data)