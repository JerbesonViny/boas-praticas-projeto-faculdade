class HorarioForaIntervaloPermitidoErro(Exception):
    def __init__(self, hora_atendimento: int, horario_inicio: int, horario_fim: int):
        super().__init__(
            f'Hora ({hora_atendimento}) fora do horario de atendimento: '
            f'{horario_inicio:02d} as {horario_fim:02d}.'
        )

class ConsultaIntervaloDuracaoErro(Exception):
    def __init__(self, duracao_minutos: int, duracao_minima: int, duracao_maxima: int):
        super().__init__(
            f'Duracao ({duracao_minutos} minutos) invalida: '
            f'uma consulta pode durar no minimo {duracao_minima} minutos '
            f'e no maximo {duracao_maxima} minutos.'
        )

class ConsultaMultiploDuracaoErro(Exception):
    def __init__(self, duracao_minutos: int, consulta_multiplo_duracao: int):
        super().__init__(
            f'Duracao ({duracao_minutos} minutos) invalida: '
            f'a duracao da consulta deve ser um multiplo de {consulta_multiplo_duracao}.'
        )

class HorarioReservadoErro(Exception):
    def __init__(self, data: str, hora_atendimento: int, nome_doutor: str):
        super().__init__(
            f'Horario indisponivel: {nome_doutor} ja tem um atendimento '
            f'em {data} as {hora_atendimento:02d}.'
        )

class AgendamentoNaoEncontradoErro(Exception):
    def __init__(self, nome_paciente: str, data: str, hora_atendimento: int):
        super().__init__(
            f'Agendamento nao encontrado: paciente {nome_paciente} '
            f'em {data} as {hora_atendimento:02d}.'
        )
