import io
import unittest
from contextlib import redirect_stdout
from typing import TypedDict

from src.agenda import Agenda
from src.agenda_erros import (
    AgendamentoNaoEncontradoErro,
    ConsultaIntervaloDuracaoErro,
    ConsultaMultiploDuracaoErro,
    HorarioForaIntervaloPermitidoErro,
    HorarioReservadoErro,
)
from src.agendamento_entidade import Agendamento, AgendamentoStatus
from src.apresentacao import formatar_agendamento
from src.utilitarios_erros import FormatoDataInvalidaErro
from tests.dados_teste import (
    DATAS_COM_TIPO_INVALIDO,
    DATAS_FORA_DO_PADRAO,
    DATAS_INEXISTENTES,
    DATAS_NAO_RECONHECIDAS,
)


class DadosAgendamento(TypedDict, total=False):
    nome_paciente: str
    nome_doutor: str
    data: str
    hora_atendimento: int
    duracao_minutos: int


AGENDAMENTO_PADRAO: DadosAgendamento = {
    'nome_paciente': 'Ana',
    'nome_doutor': 'Dr. Silva',
    'data': '2026-10-05',
    'hora_atendimento': 9,
    'duracao_minutos': 30,
}


class DadosRemarcacao(TypedDict, total=False):
    nome_paciente: str
    data: str
    hora_atendimento: int
    nova_data: str
    nova_hora_atendimento: int


REMARCACAO_PADRAO: DadosRemarcacao = {
    'nome_paciente': 'Ana',
    'data': '2026-10-05',
    'hora_atendimento': 9,
    'nova_data': '2026-10-05',
    'nova_hora_atendimento': 10,
}


class AgendaTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.agenda = Agenda()

    def _adicionar(self, dados: DadosAgendamento) -> None:
        self.agenda.adicionar(**{**AGENDAMENTO_PADRAO, **dados})

    def _remarcar(self, dados: DadosRemarcacao) -> None:
        self.agenda.remarcar(**{**REMARCACAO_PADRAO, **dados})

    def _listar(self, data: str) -> str:
        return ''.join(
            f'{formatar_agendamento(agendamento)}\n'
            for agendamento in self.agenda.listar_por_data(data)
        )


class TestAdicionarHorario(AgendaTestCase):
    def test_aceita_primeiro_horario_do_expediente(self) -> None:
        self._adicionar({'hora_atendimento': 8})

    def test_aceita_ultimo_horario_do_expediente(self) -> None:
        self._adicionar({'hora_atendimento': 17})

    def test_rejeita_horario_antes_do_expediente(self) -> None:
        with self.assertRaises(HorarioForaIntervaloPermitidoErro):
            self._adicionar({'hora_atendimento': 7})

    def test_rejeita_horario_apos_o_expediente(self) -> None:
        with self.assertRaises(HorarioForaIntervaloPermitidoErro):
            self._adicionar({'hora_atendimento': 18})


class TestAdicionarDuracao(AgendaTestCase):
    def test_aceita_duracao_minima(self) -> None:
        self._adicionar({'duracao_minutos': 15})

    def test_aceita_duracao_maxima(self) -> None:
        self._adicionar({'duracao_minutos': 120})

    def test_rejeita_duracao_abaixo_do_minimo(self) -> None:
        for duracao in [-10, 0, 14]:
            with self.subTest(duracao=duracao):
                with self.assertRaises(ConsultaIntervaloDuracaoErro):
                    self._adicionar({'duracao_minutos': duracao})

    def test_rejeita_duracao_acima_do_maximo(self) -> None:
        with self.assertRaises(ConsultaIntervaloDuracaoErro):
            self._adicionar({'duracao_minutos': 135})

    def test_rejeita_duracao_que_nao_eh_multiplo_de_15(self) -> None:
        with self.assertRaises(ConsultaMultiploDuracaoErro):
            self._adicionar({'duracao_minutos': 20})


class TestAdicionarData(AgendaTestCase):
    def test_aceita_data_valida(self) -> None:
        self._adicionar({'data': '2026-10-05'})

    def test_aceita_29_de_fevereiro_em_ano_bissexto(self) -> None:
        self._adicionar({'data': '2028-02-29'})

    def test_rejeita_data_fora_do_padrao(self) -> None:
        for data in DATAS_FORA_DO_PADRAO:
            with self.subTest(data=data):
                with self.assertRaises(FormatoDataInvalidaErro):
                    self._adicionar({'data': data})

    def test_rejeita_data_nao_reconhecida(self) -> None:
        for data in DATAS_NAO_RECONHECIDAS:
            with self.subTest(data=data):
                with self.assertRaises(ValueError):
                    self._adicionar({'data': data})

    def test_rejeita_data_inexistente(self) -> None:
        for data in DATAS_INEXISTENTES:
            with self.subTest(data=data):
                with self.assertRaises(ValueError):
                    self._adicionar({'data': data})

    def test_rejeita_data_que_nao_eh_texto(self) -> None:
        for data in DATAS_COM_TIPO_INVALIDO:
            with self.subTest(data=data):
                with self.assertRaises(TypeError):
                    self._adicionar({'data': data})

    def test_agendamento_rejeitado_por_data_nao_ocupa_horario(self) -> None:
        with self.assertRaises(FormatoDataInvalidaErro):
            self._adicionar({'data': '2026-10-5'})

        self._adicionar({'data': '2026-10-05'})


class TestAdicionarDisponibilidade(AgendaTestCase):
    def test_rejeita_mesmo_doutor_data_e_hora(self) -> None:
        self._adicionar({'nome_paciente': 'Ana'})

        with self.assertRaises(HorarioReservadoErro):
            self._adicionar({'nome_paciente': 'Bruno'})

    def test_aceita_mesmo_horario_com_outro_doutor(self) -> None:
        self._adicionar({'nome_doutor': 'Dr. Silva'})
        self._adicionar({'nome_doutor': 'Dra. Souza'})

    def test_aceita_mesmo_horario_em_outra_data(self) -> None:
        self._adicionar({'data': '2026-10-05'})
        self._adicionar({'data': '2026-10-06'})

    def test_aceita_outro_horario_no_mesmo_dia(self) -> None:
        self._adicionar({'hora_atendimento': 9})
        self._adicionar({'hora_atendimento': 10})

    def test_agendamento_rejeitado_nao_ocupa_horario(self) -> None:
        with self.assertRaises(ConsultaIntervaloDuracaoErro):
            self._adicionar({'duracao_minutos': 0})

        self._adicionar({'duracao_minutos': 30})

    def test_agendas_distintas_nao_compartilham_agendamentos(self) -> None:
        self._adicionar({})

        outra_agenda = Agenda()
        outra_agenda.adicionar(**AGENDAMENTO_PADRAO)


class TestRemarcar(AgendaTestCase):
    def setUp(self) -> None:
        super().setUp()
        self._adicionar({'nome_paciente': 'Ana', 'hora_atendimento': 9})

    def test_libera_horario_antigo(self) -> None:
        self._remarcar({'nova_hora_atendimento': 10})

        self._adicionar({'nome_paciente': 'Bruno', 'hora_atendimento': 9})

    def test_ocupa_novo_horario(self) -> None:
        self._remarcar({'nova_hora_atendimento': 10})

        with self.assertRaises(HorarioReservadoErro):
            self._adicionar({'nome_paciente': 'Bruno', 'hora_atendimento': 10})

    def test_ocupa_nova_data(self) -> None:
        self._remarcar({'nova_data': '2026-10-06', 'nova_hora_atendimento': 10})

        with self.assertRaises(HorarioReservadoErro):
            self._adicionar({
                'nome_paciente': 'Bruno',
                'data': '2026-10-06',
                'hora_atendimento': 10,
            })

    def test_agendamento_remarcado_pode_ser_remarcado_de_novo(self) -> None:
        self._remarcar({'nova_hora_atendimento': 10})

        self._remarcar({'hora_atendimento': 10, 'nova_hora_atendimento': 11})

    def test_rejeita_horario_ocupado_do_mesmo_doutor(self) -> None:
        self._adicionar({'nome_paciente': 'Bruno', 'hora_atendimento': 10})

        with self.assertRaises(HorarioReservadoErro):
            self._remarcar({'nova_hora_atendimento': 10})

    def test_aceita_horario_ocupado_por_outro_doutor(self) -> None:
        self._adicionar({
            'nome_paciente': 'Bruno',
            'nome_doutor': 'Dra. Souza',
            'hora_atendimento': 10,
        })

        self._remarcar({'nova_hora_atendimento': 10})

    def test_remarcacao_rejeitada_mantem_horario_original(self) -> None:
        self._adicionar({'nome_paciente': 'Bruno', 'hora_atendimento': 10})

        with self.assertRaises(HorarioReservadoErro):
            self._remarcar({'nova_hora_atendimento': 10})

        with self.assertRaises(HorarioReservadoErro):
            self._adicionar({'nome_paciente': 'Carla', 'hora_atendimento': 9})

    def test_rejeita_paciente_sem_agendamento(self) -> None:
        with self.assertRaises(AgendamentoNaoEncontradoErro):
            self._remarcar({'nome_paciente': 'Zeca'})

    def test_rejeita_horario_original_errado(self) -> None:
        with self.assertRaises(AgendamentoNaoEncontradoErro):
            self._remarcar({'hora_atendimento': 15})

    def test_rejeita_data_original_errada(self) -> None:
        with self.assertRaises(AgendamentoNaoEncontradoErro):
            self._remarcar({'data': '2026-10-07'})

    def test_cenario_do_programa_de_demonstracao(self) -> None:
        self._remarcar({'nova_data': '2026-10-06', 'nova_hora_atendimento': 10})

        self._adicionar({'nome_paciente': 'Bruno', 'hora_atendimento': 9})

    def test_rejeita_nova_hora_antes_do_expediente(self) -> None:
        with self.assertRaises(HorarioForaIntervaloPermitidoErro):
            self._remarcar({'nova_hora_atendimento': 7})

    def test_rejeita_nova_hora_apos_o_expediente(self) -> None:
        with self.assertRaises(HorarioForaIntervaloPermitidoErro):
            self._remarcar({'nova_hora_atendimento': 20})

    def test_rejeita_nova_data_fora_do_padrao(self) -> None:
        for nova_data in DATAS_FORA_DO_PADRAO:
            with self.subTest(nova_data=nova_data):
                with self.assertRaises(FormatoDataInvalidaErro):
                    self._remarcar({'nova_data': nova_data})

    def test_rejeita_nova_data_nao_reconhecida_ou_inexistente(self) -> None:
        for nova_data in DATAS_NAO_RECONHECIDAS + DATAS_INEXISTENTES:
            with self.subTest(nova_data=nova_data):
                with self.assertRaises(ValueError):
                    self._remarcar({'nova_data': nova_data})

    def test_rejeita_data_original_fora_do_padrao(self) -> None:
        with self.assertRaises(FormatoDataInvalidaErro):
            self._remarcar({'data': '2026-10-5'})

    def test_rejeita_data_original_nao_reconhecida(self) -> None:
        with self.assertRaises(ValueError):
            self._remarcar({'data': '05/10/2026'})

    def test_rejeita_nova_data_que_nao_eh_texto(self) -> None:
        for nova_data in DATAS_COM_TIPO_INVALIDO:
            with self.subTest(nova_data=nova_data):
                with self.assertRaises(TypeError):
                    self._remarcar({'nova_data': nova_data})

    def test_remarcacao_com_entrada_invalida_mantem_horario_original(
        self,
    ) -> None:
        with self.assertRaises(HorarioForaIntervaloPermitidoErro):
            self._remarcar({'nova_hora_atendimento': 20})

        with self.assertRaises(FormatoDataInvalidaErro):
            self._remarcar({'nova_data': '2026-10-6'})

        with self.assertRaises(HorarioReservadoErro):
            self._adicionar({'nome_paciente': 'Bruno', 'hora_atendimento': 9})


class TestBarreiraTudoOuNada(AgendaTestCase):
    """Uma operacao rejeitada nao pode deixar a agenda meio alterada."""

    def test_adicionar_rejeitado_por_hora_nao_ocupa_horario(self) -> None:
        with self.assertRaises(HorarioForaIntervaloPermitidoErro):
            self._adicionar({'hora_atendimento': 20})

        self.assertEqual(self._listar('2026-10-05'), '')

    def test_adicionar_rejeitado_por_conflito_nao_adiciona(self) -> None:
        self._adicionar({'nome_paciente': 'Ana'})

        with self.assertRaises(HorarioReservadoErro):
            self._adicionar({'nome_paciente': 'Bruno'})

        self.assertNotIn('Bruno', self._listar('2026-10-05'))

    def test_remarcar_rejeitado_mantem_status_marcado(self) -> None:
        self._adicionar({})

        with self.assertRaises(HorarioForaIntervaloPermitidoErro):
            self._remarcar({'nova_hora_atendimento': 20})

        saida = self._listar('2026-10-05')

        self.assertIn(AgendamentoStatus.MARCADO, saida)
        self.assertNotIn(AgendamentoStatus.REMARCADO, saida)

    def test_remarcar_rejeitado_por_nova_data_mantem_data_original(
        self,
    ) -> None:
        self._adicionar({'nome_paciente': 'Ana'})

        with self.assertRaises(ValueError):
            self._remarcar({'nova_data': '06/10/2026'})

        self.assertIn('Ana', self._listar('2026-10-05'))


class TestBarreiraOrdem(AgendaTestCase):
    """Validacoes da entrada vem antes das que consultam o estado."""

    def test_data_invalida_eh_detectada_antes_do_conflito(self) -> None:
        self._adicionar({})

        with self.assertRaises(FormatoDataInvalidaErro):
            self._adicionar({'nome_paciente': 'Bruno', 'data': '2026-10-5'})

    def test_hora_invalida_eh_detectada_antes_da_busca(self) -> None:
        with self.assertRaises(HorarioForaIntervaloPermitidoErro):
            self._remarcar({'nome_paciente': 'Zeca', 'nova_hora_atendimento': 20})

    def test_nova_data_invalida_eh_detectada_antes_da_busca(self) -> None:
        with self.assertRaises(FormatoDataInvalidaErro):
            self._remarcar({'nome_paciente': 'Zeca', 'nova_data': '2026-10-6'})


class TestBarreiraTipos(AgendaTestCase):
    def test_rejeita_hora_como_texto(self) -> None:
        with self.assertRaises(TypeError):
            self._adicionar({'hora_atendimento': '10'})

    def test_rejeita_duracao_como_texto(self) -> None:
        with self.assertRaises(TypeError):
            self._adicionar({'duracao_minutos': '30'})

    @unittest.expectedFailure
    def test_rejeita_hora_fracionada(self) -> None:
        # Furo conhecido: a barreira verifica a faixa, mas nao o tipo.
        with self.assertRaises(TypeError):
            self._adicionar({'hora_atendimento': 8.5})

    @unittest.expectedFailure
    def test_rejeita_duracao_fracionada(self) -> None:
        # Furo conhecido: 45.0 passa porque 45.0 % 15 == 0.
        with self.assertRaises(TypeError):
            self._adicionar({'duracao_minutos': 45.0})


class TestListarPorData(AgendaTestCase):
    def test_agenda_vazia_retorna_lista_vazia(self) -> None:
        self.assertEqual(self.agenda.listar_por_data('2026-10-05'), [])

    def test_data_sem_agendamentos_retorna_lista_vazia(self) -> None:
        self._adicionar({'data': '2026-10-05'})

        self.assertEqual(self.agenda.listar_por_data('2026-10-06'), [])

    def test_retorna_agendamentos(self) -> None:
        self._adicionar({'nome_paciente': 'Ana'})

        agendamentos = self.agenda.listar_por_data('2026-10-05')

        self.assertEqual(len(agendamentos), 1)
        self.assertIsInstance(agendamentos[0], Agendamento)
        self.assertEqual(agendamentos[0].nome_paciente, 'Ana')

    def test_nao_imprime_nada(self) -> None:
        self._adicionar({})
        saida = io.StringIO()

        with redirect_stdout(saida):
            self.agenda.listar_por_data('2026-10-05')

        self.assertEqual(saida.getvalue(), '')

    def test_lista_paciente_e_profissional_da_data(self) -> None:
        self._adicionar({'nome_paciente': 'Ana', 'nome_doutor': 'Dr. Silva'})

        saida = self._listar('2026-10-05')

        self.assertIn('Ana', saida)
        self.assertIn('Dr. Silva', saida)

    def test_lista_apenas_agendamentos_da_data(self) -> None:
        self._adicionar({'nome_paciente': 'Ana', 'data': '2026-10-05'})
        self._adicionar({'nome_paciente': 'Bruno', 'data': '2026-10-06'})

        saida = self._listar('2026-10-05')

        self.assertIn('Ana', saida)
        self.assertNotIn('Bruno', saida)

    def test_lista_na_ordem_de_cadastro(self) -> None:
        self._adicionar({'nome_paciente': 'Carla', 'hora_atendimento': 14})
        self._adicionar({'nome_paciente': 'Ana', 'hora_atendimento': 9})

        saida = self._listar('2026-10-05')

        self.assertLess(saida.index('Carla'), saida.index('Ana'))

    def test_agendamento_novo_aparece_como_marcado(self) -> None:
        self._adicionar({})

        saida = self._listar('2026-10-05')

        self.assertIn(AgendamentoStatus.MARCADO, saida)
        self.assertNotIn(AgendamentoStatus.REMARCADO, saida)

    def test_agendamento_remarcado_aparece_na_nova_data(self) -> None:
        self._adicionar({'nome_paciente': 'Ana'})
        self._remarcar({'nova_data': '2026-10-06', 'nova_hora_atendimento': 10})

        self.assertNotIn('Ana', self._listar('2026-10-05'))
        self.assertIn('Ana', self._listar('2026-10-06'))

    def test_agendamento_remarcado_aparece_como_remarcado(self) -> None:
        self._adicionar({})
        self._remarcar({'nova_hora_atendimento': 10})

        self.assertIn(AgendamentoStatus.REMARCADO, self._listar('2026-10-05'))

    def test_cenario_do_programa_de_demonstracao(self) -> None:
        self._adicionar({'nome_paciente': 'Ana', 'hora_atendimento': 9})
        with self.assertRaises(HorarioReservadoErro):
            self._adicionar({'nome_paciente': 'Bruno', 'hora_atendimento': 9})
        self._adicionar({
            'nome_paciente': 'Carla',
            'nome_doutor': 'Dra. Souza',
            'hora_atendimento': 14,
            'duracao_minutos': 60,
        })
        self._remarcar({'nova_data': '2026-10-06', 'nova_hora_atendimento': 10})

        saida = self._listar('2026-10-05')

        self.assertIn('Carla', saida)
        self.assertIn('Dra. Souza', saida)
        self.assertIn(AgendamentoStatus.MARCADO, saida)
        self.assertNotIn(AgendamentoStatus.REMARCADO, saida)
        self.assertNotIn('Ana', saida)
        self.assertNotIn('Bruno', saida)

    def test_rejeita_data_fora_do_padrao(self) -> None:
        for data in DATAS_FORA_DO_PADRAO:
            with self.subTest(data=data):
                with self.assertRaises(FormatoDataInvalidaErro):
                    self._listar(data)

    def test_rejeita_data_nao_reconhecida_ou_inexistente(self) -> None:
        for data in DATAS_NAO_RECONHECIDAS + DATAS_INEXISTENTES:
            with self.subTest(data=data):
                with self.assertRaises(ValueError):
                    self._listar(data)

    def test_rejeita_data_que_nao_eh_texto(self) -> None:
        for data in DATAS_COM_TIPO_INVALIDO:
            with self.subTest(data=data):
                with self.assertRaises(TypeError):
                    self._listar(data)


if __name__ == '__main__':
    unittest.main()
