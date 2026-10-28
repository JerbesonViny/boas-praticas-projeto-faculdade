from typing import List, Optional

from .agenda_erros import (
    AgendamentoNaoEncontradoErro,
    HorarioReservadoErro,
)
from .agenda_utilitario import (
    validar_hora_atendimento,
    validar_termino_atendimento,
)
from .data_utilitarios import (
    validar_data,
)
from .agendamento_entidade import (
    AgendamentoStatus,
    Agendamento
)
from .apresentacao import (
    formatar_agendamento,
)

class Agenda:
    """Agenda da clínica: guarda os agendamentos em memória e aplica as regras."""

    def __init__(self):
        self.__agendamentos: List[Agendamento] = []

    def __verificar_agendamento_por_paciente(
        self,
        data: str,
        hora_atendimento: int,
        nome_paciente: str,
        agendamento: Agendamento
    ):
        """
        Verifica se o agendamento informado corresponde à data, hora de
        atendimento e paciente informados.

        Args:
            data (str): Data no formato ANO-MES-DIA.
            hora_atendimento (int): Hora do início do atendimento.
            nome_paciente (str): Nome do paciente.
            agendamento (Agendamento): Agendamento a ser comparado.

        Returns:
            bool: True se data, hora de atendimento e paciente forem iguais
                aos do agendamento, False caso contrário.
        """
        return (
            agendamento.data == data and
            agendamento.hora_atendimento == hora_atendimento and
            agendamento.nome_paciente == nome_paciente
        )

    def __verificar_agendamento_por_doutor(
            self,
            data: str,
            hora_atendimento: int,
            nome_doutor: str,
            agendamento: Agendamento
        ):
            """
            Verifica se o agendamento informado corresponde à data, hora de
            atendimento e doutor informados.
        
            Args:
                data (str): Data no formato ANO-MES-DIA.
                hora_atendimento (int): Hora do início do atendimento.
                nome_doutor (str): Nome do doutor.
                agendamento (Agendamento): Agendamento a ser comparado.
        
            Returns:
                bool: True se data, hora de atendimento e doutor forem iguais
                    aos do agendamento, False caso contrário.
            """
            return (
                agendamento.data == data and
                agendamento.hora_atendimento == hora_atendimento and
                agendamento.nome_doutor == nome_doutor
            )

    def __buscar_agendamento(
        self,
        data: str,
        hora_atendimento: int,
        nome_doutor: Optional[str] = None,
        nome_paciente: Optional[str] = None
    ) -> Optional[Agendamento]:
        """
        Busca um agendamento pela data e hora de atendimento, combinadas
        com o nome do doutor ou com o nome do paciente.

        Se `nome_doutor` for informado, ele é usado primeiro. Se não for,
        a busca usa `nome_paciente`. Se nenhum dos dois for informado,
        nenhum agendamento é encontrado.

        Args:
            data (str): Data no formato ANO-MES-DIA.
            hora_atendimento (int): Hora de início do atendimento.
            nome_doutor (Optional[str], optional): Nome do profissional
                responsável pelo atendimento.
            nome_paciente (Optional[str], optional): Nome do paciente
                agendado.
        Returns:
            Optional[Agendamento]: O primeiro agendamento que corresponder
                aos critérios, ou None caso nenhum seja encontrado.
        """
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
        hora_atendimento: int,
    ):
        """
        Validar disponibilidade de horário para uma data, hora e profissional especifico.

        Args:
            data (str): Data no formato ANO-MES-DIA.
            nome_doutor (str): Nome do profissional.
            hora_atendimento (int): Hora ao qual o atendimento vai se iniciar.

        Raises:
            HorarioReservadoErro: Se o horário desejado já estiver reservado,
                este erro será lançado.
        """
        if self.__buscar_agendamento(
            data,
            hora_atendimento,
            nome_doutor,
        ):
            raise HorarioReservadoErro(
                data=data,
                hora_atendimento=hora_atendimento,
                nome_doutor=nome_doutor,
            )


    def adicionar(
        self, 
        nome_paciente: str,
        nome_doutor: str,
        data: str,
        hora_atendimento: int,
        duracao_minutos: int
    ) -> None:
        """
        Adiciona um novo agendamento com status MARCADO, caso os dados sejam
        válidos e o horário esteja livre para o profissional.

        Args:
            nome_paciente (str): Nome do paciente.
            nome_doutor (str): Nome do profissional responsável pelo atendimento.
            data (str): Data no formato ANO-MES-DIA.
            hora_atendimento (int): Hora de início do atendimento, entre 8 e 17.
            duracao_minutos (int): Duração da consulta em minutos, entre 15 e 120
                e múltipla de 15.

        Raises:
            HorarioForaIntervaloPermitidoErro: Se a hora de atendimento estiver
                fora do intervalo permitido (8 às 17).
            ConsultaIntervaloDuracaoErro: Se a duração for menor que 15 ou maior
                que 120 minutos.
            ConsultaMultiploDuracaoErro: Se a duração não for múltipla de 15.
            ConsultaTerminoForaExpedienteErro: Se o atendimento terminar
                depois das 18h.
            FormatoDataInvalidaErro: Se a data for reconhecida, mas estiver fora
                do padrão AAAA-MM-DD (ex.: '2026-1-5').
            ValueError: Se o texto não for reconhecido como data ou a data não
                existir (ex.: '05/10/2026', '2026-02-30').
            TypeError: Se a data não for uma string, ou se a hora de
                atendimento ou a duração não forem números inteiros.
            HorarioReservadoErro: Se o horário desejado já estiver reservado,
                este erro será lançado.
        """
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
        hora_atendimento: int,
        nova_data: str,
        nova_hora_atendimento: int
    ):  
        """Permite, caso a consulta informada exista, remarcar ela para outra data e/ou horário.

        Args:
            nome_paciente (str): Nome do paciente.
            data (str): Data no formato ANO-MES-DIA.
            hora_atendimento (int): Hora de início do atendimento.
            nova_data (str): Nova data desejada para o atendimento.
            nova_hora_atendimento (int): Novo horário desejado para o atendimento.

        Raises:
            AgendamentoNaoEncontradoErro: Caso a consulta a ser remarcada não exista, 
                este erro será lançado.
            HorarioForaIntervaloPermitidoErro: Caso o horário informado, seja o novo ou o antigo, 
                esteja fora do intervalo permitido, este erro será lançado.
            ConsultaTerminoForaExpedienteErro: Se, no novo horário, o
                atendimento terminar depois das 18h.
            FormatoDataInvalidaErro: Se a data for reconhecida, mas estiver fora
                do padrão AAAA-MM-DD (ex.: '2026-1-5').
            ValueError: Se o texto não for reconhecido como data ou a data não
                existir (ex.: '05/10/2026', '2026-02-30').
            TypeError: Se a data não for uma string, ou se a hora de
                atendimento não for um número inteiro.
            HorarioReservadoErro: Se o horário desejado já estiver reservado,
                este erro será lançado.
        """
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
            raise AgendamentoNaoEncontradoErro(
                nome_paciente=nome_paciente,
                data=data,
                hora_atendimento=hora_atendimento,
            )

        validar_termino_atendimento(
            hora_atendimento=nova_hora_atendimento,
            duracao_minutos=agendamento.duracao_minutos,
        )

        self.__validar_disponibilidade_horario(
            data=nova_data,
            hora_atendimento=nova_hora_atendimento,
            nome_doutor=agendamento.nome_doutor,
        )

        agendamento.atualizar_data(nova_data)
        agendamento.atualizar_hora_atendimento(nova_hora_atendimento)
        agendamento.remarcar()

    def listar_por_data(self, data: str) -> List[Agendamento]:
        """Busca os agendamentos de uma data, na ordem em que foram cadastrados.

        Args:
            data (str): Data no formato ANO-MES-DIA.

        Returns:
            List[Agendamento]: Agendamentos da data informada. A lista fica
                vazia se não houver nenhum.

        Raises:
            FormatoDataInvalidaErro: Se a data for reconhecida, mas estiver fora
                do padrão AAAA-MM-DD (ex.: '2026-1-5').
            ValueError: Se o texto não for reconhecido como data ou a data não
                existir (ex.: '05/10/2026', '2026-02-30').
            TypeError: Se a data não for uma string.
        """
        validar_data(data)

        return [
            agendamento
            for agendamento in self.__agendamentos
            if agendamento.data == data
        ]


if __name__ == '__main__':
    agenda = Agenda()

    agenda.adicionar(
        nome_paciente='Ana',
        nome_doutor='Dr. Silva',
        data='2026-10-05',
        hora_atendimento=9,
        duracao_minutos=30
    )
    print('Atendimento marcado para Ana')

    try:
        agenda.adicionar(
            nome_paciente='Bruno',
            nome_doutor='Dr. Silva',
            data='2026-10-05',
            hora_atendimento=9,
            duracao_minutos=30
        )
        print('Atendimento marcado para Bruno')
    except HorarioReservadoErro:
        print('Horario ocupado')

    agenda.adicionar(
        nome_paciente='Carla',
        nome_doutor='Dra. Souza',
        data='2026-10-05',
        hora_atendimento=14,
        duracao_minutos=60
    )
    print('Atendimento marcado para Carla')

    agenda.remarcar(
        nome_paciente='Ana',
        data='2026-10-05',
        hora_atendimento=9,
        nova_data='2026-10-06',
        nova_hora_atendimento=10
    )
    print('Remarcado')

    for agendamento in agenda.listar_por_data('2026-10-05'):
        print(formatar_agendamento(agendamento))
