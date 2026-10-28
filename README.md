# AgendaFácil

Sistema de agendamento de atendimentos de uma clínica, refatorado a partir do
código-base do Projeto da Unidade 1 de DIM0501 — Boas Práticas de Programação
(DIMAp/UFRN).

O sistema permite marcar, remarcar e listar atendimentos por data, validando:

- horário de início entre 8h e 17h, terminando até as 18h;
- duração entre 15 e 120 minutos, em múltiplos de 15;
- data no formato `AAAA-MM-DD`;
- conflito de horário do mesmo profissional.

Cada regra violada lança uma exceção específica.

## Requisitos

- Python 3.10 ou superior

## Como executar

Programa de demonstração (os dois comandos imprimem a mesma saída):

```bash
python3 cli.py
python3 -m src.agenda
```

Testes:

```bash
python3 -m unittest
```

## Documentação da API

A documentação gerada fica em `docs/` (abra `docs/index.html` no navegador).
Para gerá-la novamente:

```bash
python3 -m venv .venv
.venv/bin/pip install pdoc
.venv/bin/pdoc src -o docs
```

## Estrutura

```
src/
  agenda.py               # Agenda: adicionar, remarcar e listar_por_data
  agendamento_entidade.py # Agendamento e AgendamentoStatus
  agenda_utilitario.py    # validação de hora e duração
  data_utilitarios.py     # validação de data
  agenda_erros.py         # exceções das regras de agendamento
  utilitarios_erros.py    # exceção de formato de data
  apresentacao.py         # formatação de um agendamento para exibição
  constantes.py           # formato de data
tests/                    # testes unitários
docs/                     # documentação da API (pdoc)
```

## Autores

- Francisco Edson da Costa Filho
- Jerbeson Vinycius Sousa Rodrigues
