import unittest

from src.agenda_erros import (
    AgendamentoNaoEncontradoErro,
    ConsultaIntervaloDuracaoErro,
    ConsultaMultiploDuracaoErro,
    HorarioForaIntervaloPermitidoErro,
    HorarioReservadoErro,
)
from src.utilitarios_erros import FormatoDataInvalidaErro


class TestMensagensDeErro(unittest.TestCase):
    def test_horario_fora_intervalo_informa_intervalo_permitido(self) -> None:
        erro = HorarioForaIntervaloPermitidoErro(8, 17)

        self.assertEqual(str(erro), 'Horario de atendimento: 08 as 17')

    def test_intervalo_duracao_informa_minimo_e_maximo(self) -> None:
        erro = ConsultaIntervaloDuracaoErro(
            duracao_minima=15,
            duracao_maxima=120,
        )

        self.assertEqual(
            str(erro),
            'Uma consulta pode durar no minimo 15 minutos '
            'e no maximo 120 minutos.'
        )

    def test_multiplo_duracao_informa_multiplo(self) -> None:
        erro = ConsultaMultiploDuracaoErro(15)

        self.assertEqual(
            str(erro),
            'A duracao da consulta deve ser um multiplo de 15.'
        )

    def test_horario_reservado_informa_conflito(self) -> None:
        erro = HorarioReservadoErro()

        self.assertEqual(
            str(erro),
            'Esse horario foi reservado para outro paciente.'
        )

    def test_agendamento_nao_encontrado_informa_ausencia(self) -> None:
        erro = AgendamentoNaoEncontradoErro()

        self.assertEqual(str(erro), 'Agendamento nao encontrado.')

    def test_formato_data_invalida_informa_valor_e_formato(self) -> None:
        erro = FormatoDataInvalidaErro('05/10/2026')

        self.assertEqual(
            str(erro),
            'Data (05/10/2026) em formato invalido. Formato aceito: %Y-%m-%d.'
        )


if __name__ == '__main__':
    unittest.main()
