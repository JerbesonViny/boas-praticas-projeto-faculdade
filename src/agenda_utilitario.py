from .agenda_erros import (
    HorarioForaIntervaloPermitidoErro,
    ConsultaIntervaloDuracaoErro,
    ConsultaMultiploDuracaoErro
)

AGENDAMENTO_HORA_MINIMA = 8
AGENDAMENTO_HORA_LIMITE = 18
CONSULTA_DURACAO_MINIMA_MINUTOS = 15
CONSULTA_DURACAO_MAXIMA_MINUTOS = 120
CONSULTA_MULTIPLO_DURACAO_MINUTOS = 15

def validar_hora_atendimento(hora_atendimento: int):
    if not isinstance(hora_atendimento, int):
        raise TypeError(
            f'Hora ({hora_atendimento!r}) deve ser um numero inteiro, '
            f'nao {type(hora_atendimento).__name__}.'
        )

    if hora_atendimento <AGENDAMENTO_HORA_MINIMA or hora_atendimento >= AGENDAMENTO_HORA_LIMITE:
        raise HorarioForaIntervaloPermitidoErro(
            hora_atendimento=hora_atendimento,
            horario_inicio=AGENDAMENTO_HORA_MINIMA,
            horario_fim=AGENDAMENTO_HORA_LIMITE - 1
        )

def validar_duracao(duracao_minutos: int):
    if not isinstance(duracao_minutos, int):
        raise TypeError(
            f'Duracao ({duracao_minutos!r}) deve ser um numero inteiro, '
            f'nao {type(duracao_minutos).__name__}.'
        )

    if duracao_minutos <CONSULTA_DURACAO_MINIMA_MINUTOS or duracao_minutos > CONSULTA_DURACAO_MAXIMA_MINUTOS:
        raise ConsultaIntervaloDuracaoErro(
            duracao_minutos=duracao_minutos,
            duracao_minima=CONSULTA_DURACAO_MINIMA_MINUTOS,
            duracao_maxima=CONSULTA_DURACAO_MAXIMA_MINUTOS
        )

    elif duracao_minutos % CONSULTA_MULTIPLO_DURACAO_MINUTOS != 0:
        raise ConsultaMultiploDuracaoErro(
            duracao_minutos=duracao_minutos,
            consulta_multiplo_duracao=CONSULTA_MULTIPLO_DURACAO_MINUTOS
        )
