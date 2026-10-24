# Anotações — mapeamento da refatoração para o relatório

## Estado atual (`src/`)

### Estrutura dos módulos

| Arquivo | Responsabilidade |
|---|---|
| `src/agenda.py` | `Agenda`: guarda os agendamentos e coordena os casos de uso (`adicionar`, `remarcar`, `listar_por_data`); verifica conflito e existência |
| `src/agendamento_entidade.py` | `Agendamento` (se valida ao ser criado e ao ser alterado) e `AgendamentoStatus` (`MARCADO`, `REMARCADO`) |
| `src/agenda_utilitario.py` | Regras de negócio de hora e duração (`validar_hora_atendimento`, `validar_duracao`) e suas constantes |
| `src/data_utilitarios.py` | Regra de data (`validar_data`) |
| `src/constantes.py` | `FORMATO_DATA` — módulo próprio para evitar import circular entre `data_utilitarios` e `utilitarios_erros` |
| `src/agenda_erros.py` | Exceções de agenda e duração |
| `src/utilitarios_erros.py` | `FormatoDataInvalidaErro` |

Imports internos são **relativos** (`from .agenda_erros import ...`): o código roda como pacote (`python3 -m src.agenda`, `python3 -m unittest`, `python3 cli.py`).

Até agora, o trabalho mistura duas etapas do enunciado — e isso define onde cada coisa entra no relatório.

### Etapa 2 — Refatoração (não muda comportamento) → Seção 2 do relatório

| O que foi feito | Exigência do enunciado atendida |
|---|---|
| Classe `Agendamento` com campos nomeados | "o atendimento deve virar um tipo com campos nomeados" (fim de `a[2]`, `a[3]`) |
| `add`/`rem`/`lst`/`p`/`pr`/`h`/`dur` → `adicionar`/`remarcar`/`listar_por_data`/`nome_paciente`/`nome_doutor`/... | Nomes seguem PEP 8 |
| Campo `status` em `Agendamento` + classe `AgendamentoStatus` (`MARCADO`, `REMARCADO`) | Fim da string mágica `"MARCADO"` em `a[5]` |
| Conflito verificado só em `__validar_disponibilidade_horario`, usado por `adicionar` **e** `remarcar` | "a verificação de conflito deve existir em um único lugar" (no código-base, o laço de conflito estava duplicado em `add` e `rem`) |
| Busca centralizada em `__buscar_agendamento` (por doutor ou por paciente) | Elimina laços duplicados |
| Regras de negócio em módulos próprios (`agenda_utilitario`, `data_utilitarios`), separadas da `Agenda` | "quem valida não agenda" |
| Exceções em módulos próprios (`agenda_erros`, `utilitarios_erros`) | Organização |
| Lista global `ag` → `self.__agendamentos` por instância (em `__init__`) | Organização: elimina estado global compartilhado |
| Constantes: `AGENDAMENTO_HORA_MINIMA = 8`, `AGENDAMENTO_HORA_LIMITE = 18`, `CONSULTA_DURACAO_MINIMA_MINUTOS = 15`, `CONSULTA_DURACAO_MAXIMA_MINUTOS = 120`, `CONSULTA_MULTIPLO_DURACAO_MINUTOS = 15`, `FORMATO_DATA` | "nenhum valor fixo com significado de negócio solto" |
| `if __name__ == '__main__'` | Organização |

### Etapa 4 — Programação defensiva (muda comportamento) → Seções 2 e 4

| O que foi feito | Exigência do enunciado atendida |
|---|---|
| Exceções próprias: `HorarioForaIntervaloPermitidoErro`, `ConsultaIntervaloDuracaoErro`, `ConsultaMultiploDuracaoErro`, `HorarioReservadoErro`, `AgendamentoNaoEncontradoErro`, `FormatoDataInvalidaErro` | "exceção específica (`ValueError` ou própria herdando de `Exception`)" |
| Remoção do `try/except: pass` | "nenhum bloco de captura vazio ou genérico" |
| Horário fora do expediente e duração inválida lançam exceção | "nenhuma operação pode falhar em silêncio" |
| Regra de duração completa: 15 a 120 minutos, em múltiplos de 15 | Regra de negócio "Duração" (o código-base só exigia `dur > 0`) |
| `remarcar` de agendamento inexistente lança `AgendamentoNaoEncontradoErro` | "nenhuma operação pode falhar em silêncio" (o `rem` não fazia nada) |
| `remarcar` valida expediente e data, da original e da nova | Cláusulas de guarda em toda função pública |
| Validação de data em `adicionar` (via `Agendamento`), `remarcar` e `listar_por_data` | Regra de negócio "Data — formato AAAA-MM-DD" |
| `Agendamento` se valida no construtor e em `atualizar_data`/`atualizar_hora_atendimento` — é impossível existir um agendamento inválido | "pré-condições verificadas com cláusulas de guarda" (fecha a "porta escondida" da entidade) |
| Todas as exceções próprias incluem na mensagem o valor que causou o erro (hora, duração, data, horário reservado, agendamento buscado) | "mensagem que diz qual valor causou o problema" |

### Apoio — CLI para teste manual (`cli.py`)

- Menu numerado (1 marcar, 2 remarcar, 3 listar, 0 sair) com `input` para cada entrada.
- A `Agenda` lança as exceções para o topo; a CLI captura **uma tupla explícita** (as seis exceções próprias + `ValueError` + `TypeError`) só para exibir `Erro (Tipo): mensagem` e continuar. Sem `except Exception` — respeita "nenhum bloco de captura genérico".
- `EOFError`/`KeyboardInterrupt` (Ctrl+D / Ctrl+C) encerram sem traceback.
- A data digitada não passa por `.strip()`, para permitir testar entradas como `' 2026-10-05'`.
- O cenário do código-base (Ana, Bruno, Carla, remarcar, listar) funciona pela CLI.

### Seção 3 — Decisões de projeto

- **Exceções próprias** em vez de `ValueError` / `print`.
- **Duas exceções para a duração** (`ConsultaIntervaloDuracaoErro` e `ConsultaMultiploDuracaoErro`) em vez de uma: cada uma diz exatamente qual regra foi violada. Quando a duração viola as duas (ex.: 10 ou 125), o **intervalo** é verificado primeiro.
- **Nome `AGENDAMENTO_HORA_LIMITE` (e não `..._MAXIMA`)**: a comparação é `>=`, então 18h já é recusado. "Máxima" daria a entender que 18h é permitido. A mensagem de erro recebe `AGENDAMENTO_HORA_LIMITE - 1` para continuar mostrando "08 as 17" — a última hora em que um atendimento pode **começar**.
- **Nome `CONSULTA_MULTIPLO_DURACAO_MINUTOS` separado de `CONSULTA_DURACAO_MINIMA_MINUTOS`**, mesmo com o mesmo valor (15): são conceitos diferentes. Se a duração mínima passar a 30, o passo de 15 em 15 não deve mudar junto.
- **`FORMATO_DATA` em `constantes.py`**: `data_utilitarios` precisa de `FormatoDataInvalidaErro` e `utilitarios_erros` precisa de `FORMATO_DATA`. Com a constante dentro de um deles, os dois se importavam mutuamente (import circular → `ImportError`). Com um terceiro módulo, as dependências vão num sentido só.
- **Validação de data por "ida e volta"** (`strptime` → `strftime` → comparar com a entrada):
  - `datetime.strptime` sozinho aceita `2026-1-5` (sem zero à esquerda) e dígitos Unicode (`２０２６-10-05`).
  - `date.fromisoformat` sozinho (Python ≥ 3.11) aceita outros formatos ISO, como `20261005`.
  - Regex + `fromisoformat` também funcionaria, mas exige cuidado (`[0-9]` em vez de `\d`, `fullmatch` em vez de `match`). A ida e volta resolve com uma ferramenta só.
- **O `ValueError` do `strptime` sobe sem conversão (decisão consciente).** Consequência: uma data inválida pode gerar **duas exceções diferentes**, dependendo de quem a recusa:

  | Entrada | Quem recusa | Exceção |
  |---|---|---|
  | `2026-1-5`, `2026-10-5`, `２０２６-10-05` | comparação após `strftime` | `FormatoDataInvalidaErro` |
  | `05/10/2026`, `20261005`, `''`, espaços, `T10:00` | `strptime` | `ValueError` |
  | `2026-02-30`, `2026-13-01` (data inexistente) | `strptime` | `ValueError` (`day is out of range for month`) |

  Justificar o porquê no relatório. Alternativa a citar: fazer `FormatoDataInvalidaErro` herdar de `ValueError`, para que `except ValueError` capture os dois casos com um único tipo.
- **Tipo errado (`None`, `int`, `bytes`) gera `TypeError`** vindo do próprio `strptime` — segue a convenção do Python: `TypeError` para tipo errado, `ValueError` para valor errado.
- **`remarcar` valida também a hora original.** Remarcar "das 20h" lança `HorarioForaIntervaloPermitidoErro` em vez de `AgendamentoNaoEncontradoErro`. Não é bug (nunca existe agendamento nesse horário), mas a mensagem pode confundir — decidir se mantém e justificar.
- **Status `REMARCADO` (decidir e justificar).** No código-base, `rem` não mexia no status — o atendimento remarcado continuava `MARCADO`. Agora `remarcar` muda para `REMARCADO`. O enunciado diz que "não há funcionalidade nova a implementar", então: ou justificar a escolha aqui (e registrar na Seção 4), ou voltar a manter `MARCADO`.
- **A entidade `Agendamento` se valida sozinha.** Antes, `Agendamento('X', 'Y', 'banana', 99, -1, 'QUALQUER')` criava um objeto inválido sem passar por nenhuma guarda, porque as validações moravam na `Agenda` — toda classe pública é uma porta de entrada. Alternativa descartada: tratar `Agendamento` como interno (só a `Agenda` cria), que dependeria de disciplina de quem usa. Com a validação no construtor e nos métodos `atualizar_*`, é impossível existir um agendamento inválido.
- **Onde fica a barreira de validação: na entrada das classes e métodos públicos.**
  - `Agendamento` (construtor e `atualizar_*`), `Agenda.remarcar` e `Agenda.listar_por_data` são a **fronteira de confiança**: recebem dados de fora (CLI, testes, outros módulos) e tratam tudo como hostil.
  - A validação fica **dentro** do código chamado, não em quem o chama (ex.: a CLI). Se ficasse fora, todo chamador teria que lembrar de validar, e bastaria um esquecer para dado inválido entrar.
  - Os validadores (`validar_hora_atendimento`, `validar_duracao`, `validar_data`) **são** a barreira — estão em módulos separados só por organização. Já `__buscar_agendamento` e `__verificar_agendamento_*` ficam **atrás** dela: recebem dados já validados e não revalidam.
  - Chamar os validadores de dentro de `adicionar`/`remarcar` **não** quebra o SRP: a regra mora no validador; o método só coordena o caso de uso ("garantir pré-condições, depois guardar"). Uma mudança no expediente altera `agenda_utilitario.py`, não a `Agenda`.
- **Quando validar: antes de qualquer efeito colateral (tudo ou nada).** O `Agendamento` é criado (e validado) antes do `append`; em `remarcar`, tudo é validado antes de alterar `data`/`hora_atendimento`/`status`. Se uma guarda falha, nada foi alterado — a agenda nunca fica meio modificada.
- **Ordem das guardas: entrada primeiro, estado depois.** Tipo/formato/faixa (baratas, sem consultar a agenda) antes de conflito/existência (consultam a lista). Ex.: data `2026-10-5` num horário ocupado gera `FormatoDataInvalidaErro`, não `HorarioReservadoErro`.
- **`raise` para validação, nunca `assert`.**
  - Critério: *quem pode causar a falha?* Quem chama (entrada ruim, estado inesperado) → `raise` com exceção específica. Só um bug no próprio código → `assert`.
  - `assert` é removido com `python -O` (`__debug__ = False`). Validar entrada com `assert` faria o sistema voltar a aceitar 20h, duração negativa e qualquer data em modo otimizado — falha silenciosa, exatamente o que a Etapa 4 proíbe. Além disso, `AssertionError` não é uma exceção específica.
  - Uso possível de `assert` (opcional, não implementado): registrar **invariantes** no núcleo, ex. no início de `__buscar_agendamento`, uma vez antes do laço:
    ```python
    assert data_no_formato(data), f'Data nao validada pela barreira: {data!r}'
    ```
    com um predicado `data_no_formato(data) -> bool` (não dá para usar `assert validar_data(data)`: o validador retorna `None` e o assert falharia sempre). Custo: duplica a lógica da ida e volta. Ganho: avisa se algum caminho novo chamar o núcleo sem passar pela barreira.
  - A suíte passa igual com `python3 -O -m unittest` — nenhum teste depende de `assert` (os `self.assert*` do `unittest` são métodos, não o comando `assert`).
- **Testes com `unittest`** — 114 testes, um arquivo por módulo, cobrindo expediente, duração, data, conflito, remarcação, listagem, status, entidade, barreira de validação, isolamento entre instâncias e mensagens de erro. Usam `subTest` para listar cada valor inválido separadamente. Garantem que a refatoração não mudou o caminho feliz e documentam cada mudança intencional.

  | Arquivo | Cobre |
  |---|---|
  | `tests/test_agenda.py` | Casos de uso da `Agenda` + barreira (`TestBarreiraTudoOuNada`, `TestBarreiraOrdem`, `TestBarreiraTipos`) + listagem |
  | `tests/test_agendamento_entidade.py` | Validação no construtor, `atualizar_*` (valor inválido mantém o original), `marcar`/`remarcar`, `AgendamentoStatus` |
  | `tests/test_agenda_utilitario.py` | Constantes de negócio; todas as horas 8–17; todos os múltiplos de 15 entre 15 e 120; precedência intervalo × múltiplo |
  | `tests/test_data_utilitarios.py` | `validar_data` e `FORMATO_DATA` |
  | `tests/test_erros.py` | Mensagens das seis exceções |
  | `tests/test_apresentacao.py` | Formato de `formatar_agendamento` e saída do programa de demonstração idêntica à do código-base |
  | `tests/dados_teste.py` | Listas de datas inválidas compartilhadas |

  - ~~Quatro testes marcados com `@unittest.expectedFailure` documentavam os furos de tipo (hora `8.5` e duração `45.0` aceitas).~~ Corrigidos: os decoradores foram removidos e os testes passam.
  - Os testes de `listar_por_data` verificam a lista retornada (e que nada é impresso). O helper `_listar` monta o texto com `formatar_agendamento` para os testes que usam `assertIn`.
  - Como `'MARCADO'` está contido em `'REMARCADO'`, os testes de status também verificam que `REMARCADO` **não** aparece quando não deveria.

### Linhas para a Seção 4 (Mudanças de comportamento)

| Entrada ou situação | O que acontecia antes | O que acontece agora |
|---|---|---|
| Atendimento às 18h ou mais (ex.: 20h) ou antes das 8h | Nada — os `if` falhavam e a função saía sem marcar e sem avisar | Lança `HorarioForaIntervaloPermitidoErro` |
| Duração ≤ 0 | Nada — `if dur > 0` falhava em silêncio | Lança `ConsultaIntervaloDuracaoErro` |
| Duração entre 1 e 14 ou acima de 120 minutos | Aceita | Lança `ConsultaIntervaloDuracaoErro` (regra nova) |
| Duração que não é múltiplo de 15 (ex.: 20, 50) | Aceita | Lança `ConsultaMultiploDuracaoErro` (regra nova) |
| Mesmo profissional, data e hora já ocupados | Imprimia `Horario ocupado` | Lança `HorarioReservadoErro` (o demo deve capturar e imprimir `Horario ocupado` — ver pendências) |
| Data fora do padrão (`2026-1-5`) ao marcar ou remarcar | Aceita — qualquer valor era gravado como data | Lança `FormatoDataInvalidaErro` |
| Data não reconhecida ou inexistente (`05/10/2026`, `2026-02-30`) ao marcar ou remarcar | Aceita | Lança `ValueError` (vindo do `strptime`) |
| Data que não é texto (`None`, `20261005` como `int`) | Aceita | Lança `TypeError` (vindo do `strptime`) |
| Remarcar para fora do expediente (ex.: 20h) | Remarcava normalmente — `rem` não validava a hora | Lança `HorarioForaIntervaloPermitidoErro` |
| Remarcar atendimento que não existe | Nada — o laço não encontrava e a função saía em silêncio | Lança `AgendamentoNaoEncontradoErro` |
| Status após remarcar | Continuava `MARCADO` | Passa a `REMARCADO` (se a decisão for mantida — ver Seção 3) |
| Listar com data inválida (`2026-1-5`, `05/10/2026`, `None`) | Aceita — `lst` só comparava e não imprimia nada | Lança `FormatoDataInvalidaErro`, `ValueError` ou `TypeError`, como em `adicionar` |

## Pendências em relação ao enunciado

### Etapa 2

- [x] **Programa de demonstração idêntico ao código-base.** A "regra de ouro" exige a mesma saída:

  ```
  Atendimento marcado para Ana
  Horario ocupado
  Atendimento marcado para Carla
  Remarcado
  14 Carla Dra. Souza MARCADO
  ```

  Feito: o `__main__` de `src/agenda.py` repete as cinco chamadas do código-base (`python3 -m src.agenda`), e `tests/test_apresentacao.py` compara a saída com a do código-base, caractere a caractere.

- [x] ~~Caso do Bruno~~ — feito: o `__main__` captura só `HorarioReservadoErro` e imprime `Horario ocupado`.
- [x] ~~Recriar `rem` (remarcar)~~ — feito como `remarcar`, reusando `__validar_disponibilidade_horario`.
- [x] ~~Recriar `lst` (listar)~~ — feito como `listar_por_data`.
- [x] ~~Status do atendimento~~ — feito: campo `status` + `AgendamentoStatus`.
- [x] ~~Valores fixos soltos~~ — feito: constantes de expediente, duração e formato de data.
- [x] ~~Formato da listagem~~ — feito: `formatar_agendamento` gera `hora paciente profissional status` (`14 Carla Dra. Souza MARCADO`), usado pelo `__main__` e pela CLI.
- [x] ~~Impressão fora da lógica~~ — feito: `listar_por_data` **retorna** `List[Agendamento]`; quem imprime é o `__main__` e a CLI, usando `formatar_agendamento` (`src/apresentacao.py`).
- [x] ~~**Tipo errado:** `hora_atendimento`/`nova_hora_atendimento` estão anotados como `str` em `src/agenda.py` (vários métodos), em `Agendamento.atualizar_hora_atendimento` e em `validar_hora_atendimento`; deve ser `int`.~~ — feito.

### Etapa 3

- [ ] Docstrings estilo Google (Args, Returns, Raises) em toda função pública. O `Raises` lista também as exceções propagadas pelas funções chamadas (ex.: `adicionar` lista as de `Agendamento`).
  - [x] ~~`src/agenda.py`~~ — todos os métodos da `Agenda`, inclusive os privados.
    - [x] ~~Corrigir o `Returns` de `__verificar_agendamento_por_doutor`: diz "paciente", deveria ser "doutor".~~ — feito.
    - [x] ~~Ao corrigir o tipo da hora para `int` (Etapa 2), atualizar os `(str)` das docstrings.~~ — feito.
    - [x] ~~Se `listar_por_data` passar a retornar a lista (Etapa 2), trocar "Exibe no terminal" por um `Returns`~~ — feito.
    - As docstrings de `adicionar` e do construtor de `Agendamento` citam os limites (8 a 17, 15 a 120, múltiplo de 15): se as constantes mudarem, atualizar as duas.
  - [ ] `src/agendamento_entidade.py` — construtor, `marcar` e `remarcar` feitos; falta o `Raises` de `se_validar`, `atualizar_data` e `atualizar_hora_atendimento`.
  - [ ] `src/agenda_utilitario.py` — `validar_hora_atendimento`, `validar_duracao`.
  - [ ] `src/data_utilitarios.py` — `validar_data`.
  - [ ] `cli.py`.
- [ ] Pelo menos um comentário de decisão. Candidatos:
  - por que a data é validada por ida e volta (`strptime` + `strftime`);
  - por que o `ValueError` do `strptime` sobe sem conversão;
  - por que a mensagem de expediente usa `AGENDAMENTO_HORA_LIMITE - 1`;
  - por que `FORMATO_DATA` mora em `constantes.py`.
- [ ] README com instruções de execução e de geração de documentação.
- [ ] Gerar documentação com `pdoc` ou `sphinx-apidoc`.

### Etapa 4

- [x] ~~**Mensagens de erro devem dizer qual valor causou o problema.**~~ — feito nas cinco exceções restantes, com `tests/test_erros.py` atualizado. Padrão: valor recusado entre parênteses, depois a regra (como em `FormatoDataInvalidaErro`).
  - O valor recusado usa `{}` e não `:02d`: uma hora `20.5` faria o `:02d` lançar `ValueError` dentro do construtor da exceção. Hoje `validar_hora_atendimento` já barra o tipo antes, mas a exceção continua segura se for criada diretamente. Os limites (constantes) continuam com `:02d`.
  - `HorarioReservadoErro` deixou de dizer "para outro paciente": remarcar a Ana para o horário em que ela já está encontra o próprio agendamento dela, e a frase seria falsa. Agora o profissional é o sujeito da frase (`Horario indisponivel: Dr. Silva ja tem um atendimento em 2026-10-05 as 09.`): uma versão anterior, "ja reservado para Dr. Silva", dava a entender que o doutor é quem tinha reservado.
- **Mensagem de `FormatoDataInvalidaErro`** mostra `%Y-%m-%d` (o próprio `FORMATO_DATA`) — **decisão: manter de propósito**, não trocar por `AAAA-MM-DD`.
- [x] ~~Regra de duração: 15 a 120 minutos, múltiplos de 15~~ — feito (`validar_duracao` + duas exceções).
- [x] ~~Regra de data: validar formato `AAAA-MM-DD`~~ — feito (ver Seção 3 para a decisão sobre as exceções).
- [x] ~~Guardas no início de `remarcar` e `listar_por_data`~~ — feito.
- [x] ~~Porta de entrada escondida — `Agendamento`~~ — feito: a entidade se valida no construtor e em `atualizar_*` (ver Seção 3).
- [x] ~~**Furo de tipo na barreira:** hora `8.5` e duração `45.0` eram aceitas (a guarda verificava a faixa, não o tipo), e hora `'10'` só era recusada por acaso (`TypeError` da comparação `str < int`).~~ — feito: `isinstance(valor, int)` no início de `validar_hora_atendimento` e `validar_duracao`, lançando `TypeError` com o valor e o tipo recebido (ex.: `Hora ('10') deve ser um numero inteiro, nao str.`).
  - O tipo é verificado **antes** da faixa: `20.5` e `30.5` agora dão `TypeError`, não mais `HorarioForaIntervaloPermitidoErro` / `ConsultaMultiploDuracaoErro` (o teste de `30.5` foi ajustado).
  - `TypeError` (e não exceção própria) segue a mesma convenção da data: tipo errado → `TypeError`, valor errado → exceção da regra.
  - `bool` é subclasse de `int` em Python, então `True`/`False` passam pelo `isinstance`; na prática são barrados pela faixa (viram 1/0). Mantido assim por simplicidade.
  - O `Raises` de `adicionar`, `remarcar` e do construtor de `Agendamento` passou a citar o `TypeError` de hora/duração.

## Ordem sugerida

**Prazo: 25/10/2026, 23h59** (atraso: −1,0 por dia). Entregáveis: código, `README.md`, relatório e `docs/` (ou o comando que gera, no README).

1. ~~Concluir a **Etapa 2**: programa de demonstração com a saída idêntica, formato da listagem e separar impressão da lógica.~~ Feito, inclusive o tipo da hora (`str` → `int`).
2. Completar a **Etapa 4**: mensagens com o valor e furo de tipo.
3. **Etapa 3** por último, documentando o código já estável.

Assim fica fácil provar que o caminho feliz não mudou (evita a penalidade de −1,0) e a Seção 4 do relatório fica limpa, com cada mudança intencional registrada.
