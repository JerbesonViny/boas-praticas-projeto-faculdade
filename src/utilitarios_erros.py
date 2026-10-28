from .constantes import FORMATO_DATA

class FormatoDataInvalidaErro(Exception):
    """Lançada quando a data é reconhecida, mas não está no formato AAAA-MM-DD."""

    def __init__(self, data: str):
        super().__init__(
            f'Data ({data}) em formato invalido. Formato aceito: {FORMATO_DATA}.'
        )