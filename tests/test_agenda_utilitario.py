import unittest

from src.agenda_erros import (
    ConsultaIntervaloDuracaoErro,
    ConsultaMultiploDuracaoErro,
    ConsultaTerminoForaExpedienteErro,
    HorarioForaIntervaloPermitidoErro,
)
from src.agenda_utilitario import (
    AGENDAMENTO_HORA_LIMITE,
    AGENDAMENTO_HORA_MINIMA,
    CONSULTA_DURACAO_MAXIMA_MINUTOS,
    CONSULTA_DURACAO_MINIMA_MINUTOS,
    CONSULTA_MULTIPLO_DURACAO_MINUTOS,
    validar_duracao,
    validar_hora_atendimento,
    validar_termino_atendimento,
)


class TestConstantesDeNegocio(unittest.TestCase):
    def test_expediente(self) -> None:
        self.assertEqual(AGENDAMENTO_HORA_MINIMA, 8)
        self.assertEqual(AGENDAMENTO_HORA_LIMITE, 18)

    def test_duracao(self) -> None:
        self.assertEqual(CONSULTA_DURACAO_MINIMA_MINUTOS, 15)
        self.assertEqual(CONSULTA_DURACAO_MAXIMA_MINUTOS, 120)
        self.assertEqual(CONSULTA_MULTIPLO_DURACAO_MINUTOS, 15)


class TestValidarHoraAtendimento(unittest.TestCase):
    def test_aceita_todas_as_horas_do_expediente(self) -> None:
        for hora in range(8, 18):
            with self.subTest(hora=hora):
                validar_hora_atendimento(hora)

    def test_rejeita_horas_fora_do_expediente(self) -> None:
        for hora in [-1, 0, 7, 18, 20, 24]:
            with self.subTest(hora=hora):
                with self.assertRaises(HorarioForaIntervaloPermitidoErro):
                    validar_hora_atendimento(hora)

    def test_rejeita_hora_como_texto(self) -> None:
        with self.assertRaises(TypeError):
            validar_hora_atendimento('10')

    def test_rejeita_hora_fracionada(self) -> None:
        for hora in [8.5, 10.0]:
            with self.subTest(hora=hora):
                with self.assertRaises(TypeError):
                    validar_hora_atendimento(hora)

    def test_tipo_eh_verificado_antes_do_expediente(self) -> None:
        # 20.5 viola as duas regras; o tipo tem prioridade.
        with self.assertRaises(TypeError):
            validar_hora_atendimento(20.5)

    def test_mensagem_de_tipo_informa_valor_e_tipo(self) -> None:
        with self.assertRaises(TypeError) as contexto:
            validar_hora_atendimento('10')

        self.assertEqual(
            str(contexto.exception),
            "Hora ('10') deve ser um numero inteiro, nao str."
        )


class TestValidarDuracao(unittest.TestCase):
    def test_aceita_todos_os_multiplos_de_15_entre_15_e_120(self) -> None:
        for duracao in range(15, 121, 15):
            with self.subTest(duracao=duracao):
                validar_duracao(duracao)

    def test_rejeita_duracao_fora_do_intervalo(self) -> None:
        for duracao in [-15, 0, 14, 121, 135, 150]:
            with self.subTest(duracao=duracao):
                with self.assertRaises(ConsultaIntervaloDuracaoErro):
                    validar_duracao(duracao)

    def test_rejeita_duracao_que_nao_eh_multiplo_de_15(self) -> None:
        for duracao in [16, 20, 25, 50, 100, 119]:
            with self.subTest(duracao=duracao):
                with self.assertRaises(ConsultaMultiploDuracaoErro):
                    validar_duracao(duracao)

    def test_intervalo_eh_verificado_antes_do_multiplo(self) -> None:
        # 10 e 125 violam as duas regras; o intervalo tem prioridade.
        for duracao in [10, 125]:
            with self.subTest(duracao=duracao):
                with self.assertRaises(ConsultaIntervaloDuracaoErro):
                    validar_duracao(duracao)

    def test_rejeita_duracao_fracionada_fora_do_multiplo(self) -> None:
        # 30.5 viola o tipo e o multiplo; o tipo tem prioridade.
        with self.assertRaises(TypeError):
            validar_duracao(30.5)

    def test_rejeita_duracao_como_texto(self) -> None:
        with self.assertRaises(TypeError):
            validar_duracao('30')

    def test_rejeita_duracao_fracionada_multipla_de_15(self) -> None:
        # 45.0 % 15 == 0: sem a verificacao de tipo, passaria.
        with self.assertRaises(TypeError):
            validar_duracao(45.0)

    def test_mensagem_de_tipo_informa_valor_e_tipo(self) -> None:
        with self.assertRaises(TypeError) as contexto:
            validar_duracao(45.0)

        self.assertEqual(
            str(contexto.exception),
            'Duracao (45.0) deve ser um numero inteiro, nao float.'
        )


class TestValidarTerminoAtendimento(unittest.TestCase):
    def test_aceita_atendimento_que_termina_exatamente_as_18h(self) -> None:
        for hora, duracao in [(17, 60), (16, 120), (17, 15), (8, 120)]:
            with self.subTest(hora=hora, duracao=duracao):
                validar_termino_atendimento(
                    hora_atendimento=hora,
                    duracao_minutos=duracao,
                )

    def test_rejeita_atendimento_que_termina_depois_das_18h(self) -> None:
        for hora, duracao in [(17, 75), (17, 120), (16, 135), (17, 90)]:
            with self.subTest(hora=hora, duracao=duracao):
                with self.assertRaises(ConsultaTerminoForaExpedienteErro):
                    validar_termino_atendimento(
                        hora_atendimento=hora,
                        duracao_minutos=duracao,
                    )


if __name__ == '__main__':
    unittest.main()
