from .agenda_utilitario import (
    validar_duracao,
    validar_hora_atendimento
)

from .data_utilitarios import (
    validar_data
)

class AgendamentoStatus:
    MARCADO = 'MARCADO'
    REMARCADO = 'REMARCADO'

class Agendamento:
    def __init__(
        self,
        nome_paciente: str,
        nome_doutor: str,
        data: str,
        hora_atendimento: int,
        duracao_minutos: int,
        status: str,
    ):
        self.nome_paciente = nome_paciente
        self.nome_doutor = nome_doutor
        self.data = data
        self.hora_atendimento = hora_atendimento
        self.duracao_minutos = duracao_minutos
        self.status = status

        self.se_validar()

    def se_validar(self):
        validar_hora_atendimento(self.hora_atendimento)
        validar_duracao(self.duracao_minutos)
        validar_data(self.data)

    def atualizar_data(self, nova_data: str):
        validar_data(nova_data)

        self.data = nova_data
        self.se_validar()

    def atualizar_hora_atendimento(self, nova_hora_atendimento: str): 
        validar_hora_atendimento(nova_hora_atendimento)
        
        self.hora_atendimento = nova_hora_atendimento
        self.se_validar()

    def marcar(self):
        self.status = AgendamentoStatus.MARCADO

    def remarcar(self):
        self.status = AgendamentoStatus.REMARCADO