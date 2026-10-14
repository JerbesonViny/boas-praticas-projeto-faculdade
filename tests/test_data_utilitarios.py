import unittest

from src.data_utilitarios import FORMATO_DATA, validar_data
from src.utilitarios_erros import FormatoDataInvalidaErro
from tests.dados_teste import (
    DATAS_COM_TIPO_INVALIDO,
    DATAS_FORA_DO_PADRAO,
    DATAS_INEXISTENTES,
    DATAS_NAO_RECONHECIDAS,
)


class TestFormatoData(unittest.TestCase):
    def test_formato_eh_ano_mes_dia(self) -> None:
        self.assertEqual(FORMATO_DATA, '%Y-%m-%d')


class TestValidarData(unittest.TestCase):
    def test_aceita_datas_validas(self) -> None:
        for data in ['2026-10-05', '2026-01-01', '2026-12-31', '2028-02-29']:
            with self.subTest(data=data):
                validar_data(data)

    def test_rejeita_data_fora_do_padrao(self) -> None:
        for data in DATAS_FORA_DO_PADRAO:
            with self.subTest(data=data):
                with self.assertRaises(FormatoDataInvalidaErro):
                    validar_data(data)

    def test_rejeita_data_nao_reconhecida(self) -> None:
        for data in DATAS_NAO_RECONHECIDAS:
            with self.subTest(data=data):
                with self.assertRaises(ValueError):
                    validar_data(data)

    def test_rejeita_data_inexistente(self) -> None:
        for data in DATAS_INEXISTENTES:
            with self.subTest(data=data):
                with self.assertRaises(ValueError):
                    validar_data(data)

    def test_rejeita_data_que_nao_eh_texto(self) -> None:
        for data in DATAS_COM_TIPO_INVALIDO:
            with self.subTest(data=data):
                with self.assertRaises(TypeError):
                    validar_data(data)


if __name__ == '__main__':
    unittest.main()
