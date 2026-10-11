from datetime import datetime
from typing import List, Optional


FORMATO_DATA = '%Y-%m-%d'

class HorarioForaIntervaloPermitidoErro(Exception):
    def __init__(self, horario_inicio: int, horario_fim: int):
        super().__init__(f'Horario de atendimento: {horario_inicio:02d} as {horario_fim:02d}')

class PisoDuracaoAtendimentoErro(Exception):
    def __init__(self):
        super().__init__('A duracao minima eh de 1 minuto.')

class HorarioReservadoErro(Exception):
    def __init__(self):
        super().__init__('Esse horario foi reservado para outro paciente.')

class AgendamentoNaoEncontradoErro(Exception):
    def __init__(self):
        super().__init__('Agendamento nao encontrado.')

class FormatoDataInvalidaErro(Exception):
    def __init__(self, data: str):
            super().__init__(f'Data ({data}) em formato invalido. Formato aceito: {FORMATO_DATA}.')

class AgendamentoStatus:
    marcado = 'MARCADO'
    remarcado = 'REMARCADO'

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

class Agenda:
    def __init__(self):
        self.__agendamentos: List[Agendamento] = []

    def __validar_hora_atendimento(self, hora_atendimento: str):
        if hora_atendimento < 8 or hora_atendimento >= 18:
            raise HorarioForaIntervaloPermitidoErro(8, 17)

    def __validar_duracao(self, duracao_minutos: int):
        if duracao_minutos <= 0:
            raise PisoDuracaoAtendimentoErro()

    def __validar_data(self, data: str):
        data_convertida = datetime.strptime(data, FORMATO_DATA)

        if data_convertida.strftime(FORMATO_DATA) != data:
            raise FormatoDataInvalidaErro(data)

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
        self.__validar_hora_atendimento(hora_atendimento)
        self.__validar_duracao(duracao_minutos)
        self.__validar_data(data)

        self.__validar_disponibilidade_horario(
            data,
            nome_doutor,
            hora_atendimento,
        )

        agendamento = Agendamento(
            nome_paciente,
            nome_doutor,
            data,
            hora_atendimento,
            duracao_minutos,
            status=AgendamentoStatus.marcado
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
        self.__validar_hora_atendimento(hora_atendimento)
        self.__validar_hora_atendimento(nova_hora_atendimento)
        self.__validar_data(data)
        self.__validar_data(nova_data)

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

        agendamento.data = nova_data
        agendamento.hora_atendimento = nova_hora_atendimento
        agendamento.status = AgendamentoStatus.remarcado

    def listar_por_data(self, data: str):
        self.__validar_data(data)

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