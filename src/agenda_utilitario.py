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

def validar_hora_atendimento(hora_atendimento: str):
    if hora_atendimento < AGENDAMENTO_HORA_MINIMA or hora_atendimento >= AGENDAMENTO_HORA_LIMITE:
        raise HorarioForaIntervaloPermitidoErro(AGENDAMENTO_HORA_MINIMA, AGENDAMENTO_HORA_LIMITE - 1)

def validar_duracao(duracao_minutos: int):
    if duracao_minutos < CONSULTA_DURACAO_MINIMA_MINUTOS or duracao_minutos > CONSULTA_DURACAO_MAXIMA_MINUTOS:
        raise ConsultaIntervaloDuracaoErro(
            duracao_minima=CONSULTA_DURACAO_MINIMA_MINUTOS,
            duracao_maxima=CONSULTA_DURACAO_MAXIMA_MINUTOS
        )

    elif duracao_minutos % CONSULTA_MULTIPLO_DURACAO_MINUTOS != 0:
        raise ConsultaMultiploDuracaoErro(
            CONSULTA_MULTIPLO_DURACAO_MINUTOS
        )
