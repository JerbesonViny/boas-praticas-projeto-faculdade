from .agenda_utilitario import (
    validar_duracao,
    validar_hora_atendimento,
    validar_termino_atendimento
)

from .data_utilitarios import (
    validar_data
)

class AgendamentoStatus:
    """Valores possíveis para o status de um agendamento."""

    MARCADO = 'MARCADO'
    REMARCADO = 'REMARCADO'

class Agendamento:
    """Atendimento de um paciente com um profissional, sempre em estado válido."""

    def __init__(
        self,
        nome_paciente: str,
        nome_doutor: str,
        data: str,
        hora_atendimento: int,
        duracao_minutos: int,
        status: str,
    ):
        """
        Cria um agendamento e valida seus dados.

        Args:
            nome_paciente (str): Nome do paciente.
            nome_doutor (str): Nome do profissional responsável pelo atendimento.
            data (str): Data no formato ANO-MES-DIA.
            hora_atendimento (int): Hora de início do atendimento, entre 8 e 17.
            duracao_minutos (int): Duração da consulta em minutos, entre 15 e 120
                e múltipla de 15.
            status (str): Status do agendamento (um dos valores de
                AgendamentoStatus).

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
        """
        self.nome_paciente = nome_paciente
        self.nome_doutor = nome_doutor
        self.data = data
        self.hora_atendimento = hora_atendimento
        self.duracao_minutos = duracao_minutos
        self.status = status

        self.se_validar()

    def se_validar(self):
        """Validar todos os campos.

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
        """
        validar_hora_atendimento(self.hora_atendimento)
        validar_duracao(self.duracao_minutos)
        validar_termino_atendimento(
            hora_atendimento=self.hora_atendimento,
            duracao_minutos=self.duracao_minutos,
        )
        validar_data(self.data)

    def atualizar_data(self, nova_data: str):
        """Atualizar a data a qual o atendimento ocorrerá.

        Args:
            nova_data (str): Data no formato ANO-MES-DIA.

        Raises:
            FormatoDataInvalidaErro: Se a data for reconhecida, mas estiver fora
                do padrão AAAA-MM-DD (ex.: '2026-1-5').
            ValueError: Se o texto não for reconhecido como data ou a data não
                existir (ex.: '05/10/2026', '2026-02-30').
            TypeError: Se a data não for uma string.
        """
        validar_data(nova_data)

        self.data = nova_data
        self.se_validar()

    def atualizar_hora_atendimento(self, nova_hora_atendimento: int):
        """Modifica a hora de início do atendimento.

        Args:
            nova_hora_atendimento (int): Hora desejada para iniciar o atendimento.

        Raises:
            HorarioForaIntervaloPermitidoErro: Se a hora de atendimento estiver
                fora do intervalo permitido (8 às 17).
            ConsultaTerminoForaExpedienteErro: Se o atendimento terminar
                depois das 18h.
            TypeError: Se a hora de atendimento não for um número inteiro.
        """
        validar_hora_atendimento(nova_hora_atendimento)
        validar_termino_atendimento(
            hora_atendimento=nova_hora_atendimento,
            duracao_minutos=self.duracao_minutos,
        )
        
        self.hora_atendimento = nova_hora_atendimento
        self.se_validar()

    def marcar(self):
        """Define o status do agendamento como sendo MARCADO."""
        self.status = AgendamentoStatus.MARCADO

    def remarcar(self):
        """Define o status do agendamento como sendo REMARCADO."""
        self.status = AgendamentoStatus.REMARCADO