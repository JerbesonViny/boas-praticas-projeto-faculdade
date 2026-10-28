import unittest

from src.agenda_erros import (
    AgendamentoNaoEncontradoErro,
    ConsultaIntervaloDuracaoErro,
    ConsultaMultiploDuracaoErro,
    ConsultaTerminoForaExpedienteErro,
    HorarioForaIntervaloPermitidoErro,
    HorarioReservadoErro,
)
from src.utilitarios_erros import FormatoDataInvalidaErro


class TestMensagensDeErro(unittest.TestCase):
    def test_horario_fora_intervalo_informa_valor_e_intervalo(self) -> None:
        erro = HorarioForaIntervaloPermitidoErro(
            hora_atendimento=20,
            horario_inicio=8,
            horario_fim=17,
        )

        self.assertEqual(
            str(erro),
            'Hora (20) fora do horario de atendimento: 08 as 17.'
        )

    def test_horario_fora_intervalo_aceita_hora_nao_inteira(self) -> None:
        # O valor recusado não usa :02d: uma hora como 20.5 não pode
        # quebrar a montagem da mensagem.
        erro = HorarioForaIntervaloPermitidoErro(
            hora_atendimento=20.5,
            horario_inicio=8,
            horario_fim=17,
        )

        self.assertEqual(
            str(erro),
            'Hora (20.5) fora do horario de atendimento: 08 as 17.'
        )

    def test_intervalo_duracao_informa_valor_minimo_e_maximo(self) -> None:
        erro = ConsultaIntervaloDuracaoErro(
            duracao_minutos=150,
            duracao_minima=15,
            duracao_maxima=120,
        )

        self.assertEqual(
            str(erro),
            'Duracao (150 minutos) invalida: '
            'uma consulta pode durar no minimo 15 minutos '
            'e no maximo 120 minutos.'
        )

    def test_multiplo_duracao_informa_valor_e_multiplo(self) -> None:
        erro = ConsultaMultiploDuracaoErro(
            duracao_minutos=50,
            consulta_multiplo_duracao=15,
        )

        self.assertEqual(
            str(erro),
            'Duracao (50 minutos) invalida: '
            'a duracao da consulta deve ser um multiplo de 15.'
        )

    def test_termino_fora_expediente_informa_inicio_duracao_e_termino(
        self,
    ) -> None:
        erro = ConsultaTerminoForaExpedienteErro(
            hora_atendimento=17,
            duracao_minutos=90,
            horario_fim=18,
        )

        self.assertEqual(
            str(erro),
            'Atendimento as 17 com 90 minutos terminaria as 18:30, '
            'depois do fim do expediente (18:00).'
        )

    def test_horario_reservado_informa_horario_e_profissional(self) -> None:
        erro = HorarioReservadoErro(
            data='2026-10-05',
            hora_atendimento=9,
            nome_doutor='Dr. Silva',
        )

        self.assertEqual(
            str(erro),
            'Horario indisponivel: Dr. Silva ja tem um atendimento '
            'em 2026-10-05 as 09.'
        )

    def test_agendamento_nao_encontrado_informa_paciente_e_horario(self) -> None:
        erro = AgendamentoNaoEncontradoErro(
            nome_paciente='Ana',
            data='2026-10-05',
            hora_atendimento=9,
        )

        self.assertEqual(
            str(erro),
            'Agendamento nao encontrado: paciente Ana em 2026-10-05 as 09.'
        )

    def test_formato_data_invalida_informa_valor_e_formato(self) -> None:
        erro = FormatoDataInvalidaErro('05/10/2026')

        self.assertEqual(
            str(erro),
            'Data (05/10/2026) em formato invalido. Formato aceito: %Y-%m-%d.'
        )


if __name__ == '__main__':
    unittest.main()
