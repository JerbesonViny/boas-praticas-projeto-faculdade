import unittest
from typing import TypedDict

from src.agenda_erros import (
    ConsultaIntervaloDuracaoErro,
    ConsultaMultiploDuracaoErro,
    ConsultaTerminoForaExpedienteErro,
    HorarioForaIntervaloPermitidoErro,
)
from src.agendamento_entidade import Agendamento, AgendamentoStatus
from src.utilitarios_erros import FormatoDataInvalidaErro


class DadosAgendamentoEntidade(TypedDict, total=False):
    nome_paciente: str
    nome_doutor: str
    data: str
    hora_atendimento: int
    duracao_minutos: int
    status: str


AGENDAMENTO_ENTIDADE_PADRAO: DadosAgendamentoEntidade = {
    'nome_paciente': 'Ana',
    'nome_doutor': 'Dr. Silva',
    'data': '2026-10-05',
    'hora_atendimento': 9,
    'duracao_minutos': 30,
    'status': AgendamentoStatus.MARCADO,
}


def criar_agendamento(dados: DadosAgendamentoEntidade) -> Agendamento:
    return Agendamento(**{**AGENDAMENTO_ENTIDADE_PADRAO, **dados})


class TestAgendamentoStatus(unittest.TestCase):
    def test_valores_dos_status(self) -> None:
        self.assertEqual(AgendamentoStatus.MARCADO, 'MARCADO')
        self.assertEqual(AgendamentoStatus.REMARCADO, 'REMARCADO')


class TestCriarAgendamento(unittest.TestCase):
    def test_guarda_os_dados_informados(self) -> None:
        agendamento = criar_agendamento({})

        self.assertEqual(agendamento.nome_paciente, 'Ana')
        self.assertEqual(agendamento.nome_doutor, 'Dr. Silva')
        self.assertEqual(agendamento.data, '2026-10-05')
        self.assertEqual(agendamento.hora_atendimento, 9)
        self.assertEqual(agendamento.duracao_minutos, 30)
        self.assertEqual(agendamento.status, AgendamentoStatus.MARCADO)

    def test_rejeita_hora_fora_do_expediente(self) -> None:
        with self.assertRaises(HorarioForaIntervaloPermitidoErro):
            criar_agendamento({'hora_atendimento': 20})

    def test_rejeita_duracao_fora_do_intervalo(self) -> None:
        with self.assertRaises(ConsultaIntervaloDuracaoErro):
            criar_agendamento({'duracao_minutos': 0})

    def test_rejeita_atendimento_que_termina_depois_do_expediente(
        self,
    ) -> None:
        with self.assertRaises(ConsultaTerminoForaExpedienteErro):
            criar_agendamento({'hora_atendimento': 17, 'duracao_minutos': 120})

    def test_rejeita_duracao_que_nao_eh_multiplo(self) -> None:
        with self.assertRaises(ConsultaMultiploDuracaoErro):
            criar_agendamento({'duracao_minutos': 20})

    def test_rejeita_data_fora_do_padrao(self) -> None:
        with self.assertRaises(FormatoDataInvalidaErro):
            criar_agendamento({'data': '2026-10-5'})

    def test_rejeita_data_nao_reconhecida(self) -> None:
        with self.assertRaises(ValueError):
            criar_agendamento({'data': '05/10/2026'})

    def test_nao_eh_possivel_criar_agendamento_invalido(self) -> None:
        # Antes, a entidade aceitava qualquer valor sem passar pela barreira.
        with self.assertRaises(HorarioForaIntervaloPermitidoErro):
            Agendamento('X', 'Y', 'banana', 99, -1, 'QUALQUER')


class TestAtualizarData(unittest.TestCase):
    def test_altera_a_data(self) -> None:
        agendamento = criar_agendamento({})

        agendamento.atualizar_data('2026-10-06')

        self.assertEqual(agendamento.data, '2026-10-06')

    def test_data_invalida_mantem_a_data_original(self) -> None:
        agendamento = criar_agendamento({})

        with self.assertRaises(FormatoDataInvalidaErro):
            agendamento.atualizar_data('2026-10-6')

        self.assertEqual(agendamento.data, '2026-10-05')


class TestAtualizarHoraAtendimento(unittest.TestCase):
    def test_altera_a_hora(self) -> None:
        agendamento = criar_agendamento({})

        agendamento.atualizar_hora_atendimento(10)

        self.assertEqual(agendamento.hora_atendimento, 10)

    def test_aceita_ultima_hora_do_expediente(self) -> None:
        agendamento = criar_agendamento({})

        agendamento.atualizar_hora_atendimento(17)

        self.assertEqual(agendamento.hora_atendimento, 17)

    def test_hora_invalida_mantem_a_hora_original(self) -> None:
        agendamento = criar_agendamento({})

        with self.assertRaises(HorarioForaIntervaloPermitidoErro):
            agendamento.atualizar_hora_atendimento(20)

        self.assertEqual(agendamento.hora_atendimento, 9)

    def test_hora_que_estoura_o_expediente_mantem_a_hora_original(
        self,
    ) -> None:
        agendamento = criar_agendamento({'duracao_minutos': 120})

        with self.assertRaises(ConsultaTerminoForaExpedienteErro):
            agendamento.atualizar_hora_atendimento(17)

        self.assertEqual(agendamento.hora_atendimento, 9)


class TestStatusDoAgendamento(unittest.TestCase):
    def test_remarcar_muda_status_para_remarcado(self) -> None:
        agendamento = criar_agendamento({})

        agendamento.remarcar()

        self.assertEqual(agendamento.status, AgendamentoStatus.REMARCADO)

    def test_marcar_muda_status_para_marcado(self) -> None:
        agendamento = criar_agendamento({'status': AgendamentoStatus.REMARCADO})

        agendamento.marcar()

        self.assertEqual(agendamento.status, AgendamentoStatus.MARCADO)


if __name__ == '__main__':
    unittest.main()
