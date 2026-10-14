from .constantes import FORMATO_DATA

class FormatoDataInvalidaErro(Exception):
    def __init__(self, data: str):
        super().__init__(
            f'Data ({data}) em formato invalido. Formato aceito: {FORMATO_DATA}.'
        )