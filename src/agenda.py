from typing import List, Optional

from .agenda_erros import (
    AgendamentoNaoEncontradoErro,
    HorarioReservadoErro,
)
from .agenda_utilitario import (
    validar_hora_atendimento,
)
from .data_utilitarios import (
    validar_data,
)
from .agendamento_entidade import (
    AgendamentoStatus,
    Agendamento
)

class Agenda:
    def __init__(self):
        self.__agendamentos: List[Agendamento] = []

    def __verificar_agendamento_por_paciente(
        self,
        data: str,
        hora_atendimento: str,
        nome_paciente: str,
        agendamento: Agendamento
    ):
        return (
            agendamento.data == data and
            agendamento.hora_atendimento == hora_atendimento and
            agendamento.nome_paciente == nome_paciente
        )

    def __verificar_agendamento_por_doutor(
            self,
            data: str,
            hora_atendimento: str,
            nome_doutor: str,
            agendamento: Agendamento
        ):
            return (
                agendamento.data == data and
                agendamento.hora_atendimento == hora_atendimento and
                agendamento.nome_doutor == nome_doutor
            )

    def __buscar_agendamento(
        self,
        data: str,
        hora_atendimento: str,
        nome_doutor: Optional[str] = None,
        nome_paciente: Optional[str] = None
    ) -> Optional[Agendamento]:
        for agendamento in self.__agendamentos:
                
            if nome_doutor and self.__verificar_agendamento_por_doutor(
                data,
                hora_atendimento,
                nome_doutor,
                agendamento,
            ):
                return agendamento

            elif nome_paciente and self.__verificar_agendamento_por_paciente(
                data,
                hora_atendimento,
                nome_paciente,
                agendamento,
            ):
                return agendamento


    def __validar_disponibilidade_horario(
        self,
        data: str,
        nome_doutor: str,
        hora_atendimento: str,
    ):
        if self.__buscar_agendamento(
            data,
            hora_atendimento,
            nome_doutor,
        ):
            raise HorarioReservadoErro()


    def adicionar(
        self, 
        nome_paciente: str,
        nome_doutor: str,
        data: str,
        hora_atendimento: int,
        duracao_minutos: int
    ) -> None:
        agendamento = Agendamento(
            nome_paciente,
            nome_doutor,
            data,
            hora_atendimento,
            duracao_minutos,
            status=AgendamentoStatus.MARCADO
        )

        self.__validar_disponibilidade_horario(
            data,
            nome_doutor,
            hora_atendimento,
        )

        self.__agendamentos.append(agendamento)
        
    def remarcar(
        self,
        nome_paciente: str,
        data: str,
        hora_atendimento: str,
        nova_data: str,
        nova_hora_atendimento: str
    ):  
        validar_hora_atendimento(hora_atendimento)
        validar_hora_atendimento(nova_hora_atendimento)
        validar_data(data)
        validar_data(nova_data)

        agendamento: Optional[Agendamento] = self.__buscar_agendamento(
            data,
            hora_atendimento,
            nome_paciente=nome_paciente,
        )

        if not agendamento:
            raise AgendamentoNaoEncontradoErro()

        self.__validar_disponibilidade_horario(
            data=nova_data,
            hora_atendimento=nova_hora_atendimento,
            nome_doutor=agendamento.nome_doutor,
        )

        agendamento.atualizar_data(nova_data)
        agendamento.atualizar_hora_atendimento(nova_hora_atendimento)
        agendamento.remarcar()

    def listar_por_data(self, data: str):
        validar_data(data)

        for agendamento in self.__agendamentos:

            if agendamento.data == data:
                print(
                    f'Data: {agendamento.data}; '
                    f'Paciente: {agendamento.nome_paciente}; '
                    f'Profissional: {agendamento.nome_doutor}; '
                    f'Status: {agendamento.status}'
                )


if __name__ == '__main__':
    agenda = Agenda()

    agenda.adicionar(
        nome_paciente='Jerbeson',
        nome_doutor='Testerson',
        data='2026-01-01',
        hora_atendimento=18,
        duracao_minutos=30
    )