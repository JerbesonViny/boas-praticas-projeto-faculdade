class HorarioForaIntervaloPermitidoErro(Exception):
    def __init__(self, horario_inicio: int, horario_fim: int):
        super().__init__(f'Horario de atendimento: {horario_inicio:02d} as {horario_fim:02d}')

class ConsultaIntervaloDuracaoErro(Exception):
    def __init__(self, duracao_minima: int, duracao_maxima: int):
        super().__init__(
            f'Uma consulta pode durar no minimo {duracao_minima} minutos ' 
            f'e no maximo {duracao_maxima} minutos.'
        )

class ConsultaMultiploDuracaoErro(Exception):
    def __init__(self, consulta_multiplo_duracao):
            super().__init__(f'A duracao da consulta deve ser um multiplo de {consulta_multiplo_duracao}.')

class HorarioReservadoErro(Exception):
    def __init__(self):
        super().__init__('Esse horario foi reservado para outro paciente.')

class AgendamentoNaoEncontradoErro(Exception):
    def __init__(self):
        super().__init__('Agendamento nao encontrado.')
