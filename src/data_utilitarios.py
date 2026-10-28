from datetime import datetime

from .constantes import FORMATO_DATA
from .utilitarios_erros import FormatoDataInvalidaErro

def validar_data(data: str):
    """
    Valida se a data existe e está estritamente no formato AAAA-MM-DD.

    Args:
        data (str): Data a ser validada.

    Raises:
        TypeError: Se a data não for uma string.
        ValueError: Se o texto não for reconhecido como data ou a data não
            existir (ex.: '05/10/2026', '2026-02-30').
        FormatoDataInvalidaErro: Se a data for reconhecida, mas estiver fora
            do padrão AAAA-MM-DD (ex.: '2026-1-5').
    """
    data_convertida = datetime.strptime(data, FORMATO_DATA)
    
    if data_convertida.strftime(FORMATO_DATA) != data:
        raise FormatoDataInvalidaErro(data)