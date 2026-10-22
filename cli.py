from typing import Callable, Dict, NamedTuple

from src.agenda import Agenda
from src.agenda_erros import (
    AgendamentoNaoEncontradoErro,
    ConsultaIntervaloDuracaoErro,
    ConsultaMultiploDuracaoErro,
    HorarioForaIntervaloPermitidoErro,
    HorarioReservadoErro,
)
from src.apresentacao import formatar_agendamento
from src.utilitarios_erros import FormatoDataInvalidaErro


# A Agenda lança as exceções para o topo; aqui elas são capturadas apenas
# para mostrar a mensagem ao usuário sem encerrar o programa.
ERROS_EXIBIDOS = (
    AgendamentoNaoEncontradoErro,
    ConsultaIntervaloDuracaoErro,
    ConsultaMultiploDuracaoErro,
    FormatoDataInvalidaErro,
    HorarioForaIntervaloPermitidoErro,
    HorarioReservadoErro,
    ValueError,
    TypeError,
)


class Opcao(NamedTuple):
    descricao: str
    acao: Callable[[Agenda], None]


def ler_texto(rotulo: str) -> str:
    return input(f'{rotulo}: ')


def ler_inteiro(rotulo: str) -> int:
    return int(ler_texto(rotulo))


def marcar_atendimento(agenda: Agenda) -> None:
    nome_paciente = ler_texto('Paciente')

    agenda.adicionar(
        nome_paciente=nome_paciente,
        nome_doutor=ler_texto('Profissional'),
        data=ler_texto('Data (AAAA-MM-DD)'),
        hora_atendimento=ler_inteiro('Hora (8 a 17)'),
        duracao_minutos=ler_inteiro('Duracao (15 a 120 min, multiplo de 15)'),
    )

    print(f'Atendimento marcado para {nome_paciente}')


def remarcar_atendimento(agenda: Agenda) -> None:
    agenda.remarcar(
        nome_paciente=ler_texto('Paciente'),
        data=ler_texto('Data atual (AAAA-MM-DD)'),
        hora_atendimento=ler_inteiro('Hora atual'),
        nova_data=ler_texto('Nova data (AAAA-MM-DD)'),
        nova_hora_atendimento=ler_inteiro('Nova hora'),
    )

    print('Remarcado')


def listar_atendimentos(agenda: Agenda) -> None:
    for agendamento in agenda.listar_por_data(ler_texto('Data (AAAA-MM-DD)')):
        print(formatar_agendamento(agendamento))


OPCOES: Dict[str, Opcao] = {
    '1': Opcao('Marcar atendimento', marcar_atendimento),
    '2': Opcao('Remarcar atendimento', remarcar_atendimento),
    '3': Opcao('Listar atendimentos por data', listar_atendimentos),
}

OPCAO_SAIR = '0'


def exibir_menu() -> None:
    print('\n=== AgendaFacil ===')

    for numero, opcao in OPCOES.items():
        print(f'{numero} - {opcao.descricao}')

    print(f'{OPCAO_SAIR} - Sair')


def executar(agenda: Agenda) -> None:
    while True:
        exibir_menu()
        escolha = ler_texto('Opcao').strip()

        if escolha == OPCAO_SAIR:
            return

        opcao = OPCOES.get(escolha)

        if opcao is None:
            print(f'Opcao invalida: {escolha!r}')
            continue

        try:
            opcao.acao(agenda)
        except ERROS_EXIBIDOS as erro:
            print(f'Erro ({type(erro).__name__}): {erro}')


def main() -> None:
    try:
        executar(Agenda())
    except (EOFError, KeyboardInterrupt):
        print()


if __name__ == '__main__':
    main()
