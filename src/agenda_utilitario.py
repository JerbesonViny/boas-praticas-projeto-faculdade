from .agenda_erros import (
    HorarioForaIntervaloPermitidoErro,
    ConsultaIntervaloDuracaoErro,
    ConsultaMultiploDuracaoErro,
    ConsultaTerminoForaExpedienteErro
)
from .constantes import MINUTOS_POR_HORA

AGENDAMENTO_HORA_MINIMA = 8
AGENDAMENTO_HORA_LIMITE = 18
CONSULTA_DURACAO_MINIMA_MINUTOS = 15
CONSULTA_DURACAO_MAXIMA_MINUTOS = 120
CONSULTA_MULTIPLO_DURACAO_MINUTOS = 15

def validar_hora_atendimento(hora_atendimento: int):
    """
    Valida se a hora de início está dentro do expediente (8 às 17).

    Args:
        hora_atendimento (int): Hora de início do atendimento.

    Raises:
        TypeError: Se a hora não for um número inteiro (ex.: '10' ou 8.5).
        HorarioForaIntervaloPermitidoErro: Se a hora for anterior às 8 ou
            igual ou posterior às 18.
    """
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
    """
    Valida se a duração está entre 15 e 120 minutos, em múltiplos de 15.

    Quando a duração viola as duas regras (ex.: 10 ou 125), o intervalo é
    verificado primeiro.

    Args:
        duracao_minutos (int): Duração da consulta em minutos.

    Raises:
        TypeError: Se a duração não for um número inteiro (ex.: '30' ou 45.0).
        ConsultaIntervaloDuracaoErro: Se a duração for menor que 15 ou maior
            que 120 minutos.
        ConsultaMultiploDuracaoErro: Se a duração não for múltipla de 15.
    """
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

def validar_termino_atendimento(hora_atendimento: int, duracao_minutos: int):
    """
    Valida se o atendimento termina até o fim do expediente (18h).

    Deve ser chamada depois de validar_hora_atendimento e validar_duracao,
    pois considera que a hora e a duração já são inteiros válidos.

    Args:
        hora_atendimento (int): Hora de início do atendimento.
        duracao_minutos (int): Duração da consulta em minutos.

    Raises:
        ConsultaTerminoForaExpedienteErro: Se o atendimento terminar depois
            das 18h (ex.: começar às 17h e durar 120 minutos).
    """
    termino_em_minutos = hora_atendimento * MINUTOS_POR_HORA + duracao_minutos

    if termino_em_minutos > AGENDAMENTO_HORA_LIMITE * MINUTOS_POR_HORA:
        raise ConsultaTerminoForaExpedienteErro(
            hora_atendimento=hora_atendimento,
            duracao_minutos=duracao_minutos,
            horario_fim=AGENDAMENTO_HORA_LIMITE
        )
