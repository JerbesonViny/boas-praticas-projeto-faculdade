"""Programa de demonstração do AgendaFácil.

Reproduz o cenário do código-base: as mensagens ao usuário ficam aqui, e a
Agenda apenas aplica as regras e lança exceções.
"""

from src.agenda import Agenda
from src.agenda_erros import HorarioReservadoErro
from src.apresentacao import formatar_agendamento

agenda = Agenda()


def marcar(
    nome_paciente: str,
    nome_doutor: str,
    data: str,
    hora_atendimento: int,
    duracao_minutos: int,
) -> None:
    """
    Marca um atendimento e informa se o horário já estava ocupado.

    Args:
        nome_paciente (str): Nome do paciente.
        nome_doutor (str): Nome do profissional responsável pelo atendimento.
        data (str): Data no formato ANO-MES-DIA.
        hora_atendimento (int): Hora de início do atendimento.
        duracao_minutos (int): Duração da consulta em minutos.
    """
    try:
        agenda.adicionar(
            nome_paciente=nome_paciente,
            nome_doutor=nome_doutor,
            data=data,
            hora_atendimento=hora_atendimento,
            duracao_minutos=duracao_minutos,
        )
        print('Atendimento marcado para', nome_paciente)
    except HorarioReservadoErro:
        print('Horario ocupado')


def remarcar(
    nome_paciente: str,
    data: str,
    hora_atendimento: int,
    nova_data: str,
    nova_hora_atendimento: int,
) -> None:
    """
    Remarca um atendimento e informa se o novo horário já estava ocupado.

    Args:
        nome_paciente (str): Nome do paciente.
        data (str): Data atual do atendimento, no formato ANO-MES-DIA.
        hora_atendimento (int): Hora atual de início do atendimento.
        nova_data (str): Nova data desejada para o atendimento.
        nova_hora_atendimento (int): Novo horário desejado para o atendimento.
    """
    try:
        agenda.remarcar(
            nome_paciente=nome_paciente,
            data=data,
            hora_atendimento=hora_atendimento,
            nova_data=nova_data,
            nova_hora_atendimento=nova_hora_atendimento,
        )
        print('Remarcado')
    except HorarioReservadoErro:
        print('Horario ocupado')


def listar(data: str) -> None:
    """
    Exibe os atendimentos de uma data, um por linha.

    Args:
        data (str): Data no formato ANO-MES-DIA.
    """
    for agendamento in agenda.listar_por_data(data):
        print(formatar_agendamento(agendamento))


if __name__ == '__main__':
    marcar(nome_paciente='Ana', nome_doutor='Dr. Silva', data='2026-10-05', hora_atendimento=9, duracao_minutos=30)
    marcar(nome_paciente='Bruno', nome_doutor='Dr. Silva', data='2026-10-05', hora_atendimento=9, duracao_minutos=30)
    marcar(nome_paciente='Carla', nome_doutor='Dra. Souza', data='2026-10-05', hora_atendimento=14, duracao_minutos=60)
    remarcar(nome_paciente='Ana', data='2026-10-05', hora_atendimento=9, nova_data='2026-10-06', nova_hora_atendimento=10)
    listar(data='2026-10-05')
