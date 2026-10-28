from .constantes import MINUTOS_POR_HORA

class HorarioForaIntervaloPermitidoErro(Exception):
    """Lançada quando a hora de início está fora do expediente (8 às 17)."""

    def __init__(self, hora_atendimento: int, horario_inicio: int, horario_fim: int):
        super().__init__(
            f'Hora ({hora_atendimento}) fora do horario de atendimento: '
            f'{horario_inicio:02d} as {horario_fim:02d}.'
        )

class ConsultaIntervaloDuracaoErro(Exception):
    """Lançada quando a duração é menor que 15 ou maior que 120 minutos."""

    def __init__(self, duracao_minutos: int, duracao_minima: int, duracao_maxima: int):
        super().__init__(
            f'Duracao ({duracao_minutos} minutos) invalida: '
            f'uma consulta pode durar no minimo {duracao_minima} minutos '
            f'e no maximo {duracao_maxima} minutos.'
        )

class ConsultaMultiploDuracaoErro(Exception):
    """Lançada quando a duração não é múltipla de 15 minutos."""

    def __init__(self, duracao_minutos: int, consulta_multiplo_duracao: int):
        super().__init__(
            f'Duracao ({duracao_minutos} minutos) invalida: '
            f'a duracao da consulta deve ser um multiplo de {consulta_multiplo_duracao}.'
        )

class ConsultaTerminoForaExpedienteErro(Exception):
    """Lançada quando o atendimento termina depois das 18h."""

    def __init__(self, hora_atendimento: int, duracao_minutos: int, horario_fim: int):
        hora_termino, minuto_termino = divmod(
            hora_atendimento * MINUTOS_POR_HORA + duracao_minutos,
            MINUTOS_POR_HORA,
        )

        super().__init__(
            f'Atendimento as {hora_atendimento:02d} com {duracao_minutos} minutos '
            f'terminaria as {hora_termino:02d}:{minuto_termino:02d}, '
            f'depois do fim do expediente ({horario_fim:02d}:00).'
        )

class HorarioReservadoErro(Exception):
    """Lançada quando o profissional já tem um atendimento na data e hora."""

    def __init__(self, data: str, hora_atendimento: int, nome_doutor: str):
        super().__init__(
            f'Horario indisponivel: {nome_doutor} ja tem um atendimento '
            f'em {data} as {hora_atendimento:02d}.'
        )

class AgendamentoNaoEncontradoErro(Exception):
    """Lançada quando não existe o agendamento informado para remarcar."""

    def __init__(self, nome_paciente: str, data: str, hora_atendimento: int):
        super().__init__(
            f'Agendamento nao encontrado: paciente {nome_paciente} '
            f'em {data} as {hora_atendimento:02d}.'
        )
