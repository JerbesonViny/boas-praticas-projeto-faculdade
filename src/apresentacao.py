from .agendamento_entidade import Agendamento


def formatar_agendamento(agendamento: Agendamento) -> str:
    """
    Formata um agendamento para a listagem, no mesmo formato do código-base.

    Args:
        agendamento (Agendamento): Agendamento a ser formatado.

    Returns:
        str: Hora, paciente, profissional e status separados por espaço
            (ex.: '14 Carla Dra. Souza MARCADO').
    """
    return (
        f'{agendamento.hora_atendimento} '
        f'{agendamento.nome_paciente} '
        f'{agendamento.nome_doutor} '
        f'{agendamento.status}'
    )
