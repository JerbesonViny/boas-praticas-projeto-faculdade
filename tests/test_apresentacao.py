import subprocess
import sys
import unittest
from pathlib import Path

from src.agendamento_entidade import Agendamento, AgendamentoStatus
from src.apresentacao import formatar_agendamento


RAIZ_DO_PROJETO = Path(__file__).resolve().parent.parent

SAIDA_DO_CODIGO_BASE = (
    'Atendimento marcado para Ana\n'
    'Horario ocupado\n'
    'Atendimento marcado para Carla\n'
    'Remarcado\n'
    '14 Carla Dra. Souza MARCADO\n'
)


class TestFormatarAgendamento(unittest.TestCase):
    def test_formato_do_codigo_base(self) -> None:
        agendamento = Agendamento(
            nome_paciente='Carla',
            nome_doutor='Dra. Souza',
            data='2026-10-05',
            hora_atendimento=14,
            duracao_minutos=60,
            status=AgendamentoStatus.MARCADO,
        )

        self.assertEqual(
            formatar_agendamento(agendamento),
            '14 Carla Dra. Souza MARCADO',
        )

    def test_mostra_status_remarcado(self) -> None:
        agendamento = Agendamento(
            nome_paciente='Ana',
            nome_doutor='Dr. Silva',
            data='2026-10-06',
            hora_atendimento=10,
            duracao_minutos=30,
            status=AgendamentoStatus.REMARCADO,
        )

        self.assertEqual(
            formatar_agendamento(agendamento),
            '10 Ana Dr. Silva REMARCADO',
        )


class TestProgramaDeDemonstracao(unittest.TestCase):
    def test_saida_identica_ao_codigo_base(self) -> None:
        resultado = subprocess.run(
            [sys.executable, '-m', 'src.agenda'],
            cwd=RAIZ_DO_PROJETO,
            capture_output=True,
            text=True,
        )

        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        self.assertEqual(resultado.stdout, SAIDA_DO_CODIGO_BASE)


if __name__ == '__main__':
    unittest.main()
