# Anotações — mapeamento da refatoração para o relatório

## Estado atual (`src/agenda.py`)

Até agora, o trabalho mistura duas etapas do enunciado — e isso define onde cada coisa entra no relatório.

### Etapa 2 — Refatoração (não muda comportamento) → Seção 2 do relatório

| O que foi feito | Exigência do enunciado atendida |
|---|---|
| Classe `Agendamento` com campos nomeados | "o atendimento deve virar um tipo com campos nomeados" (fim de `a[2]`, `a[3]`) |
| `add`/`rem`/`lst`/`p`/`pr`/`h`/`dur` → `adicionar`/`remarcar`/`listar_por_data`/`nome_paciente`/`nome_doutor`/... | Nomes seguem PEP 8 |
| Campo `status` em `Agendamento` + classe `AgendamentoStatus` (`marcado`, `remarcado`) | Fim da string mágica `"MARCADO"` em `a[5]` |
| Conflito verificado só em `__validar_disponibilidade_horario`, usado por `adicionar` **e** `remarcar` | "a verificação de conflito deve existir em um único lugar" (no código-base, o laço de conflito estava duplicado em `add` e `rem`) |
| Busca centralizada em `__buscar_agendamento` (por doutor ou por paciente) | Elimina laços duplicados |
| Validações em métodos privados separados de `adicionar` / `remarcar` | "quem valida não agenda" |
| Lista global `ag` → `self.__agendamentos` por instância (em `__init__`) | Organização: elimina estado global compartilhado |
| Constante `FORMATO_DATA = '%Y-%m-%d'` | "nenhum valor fixo com significado de negócio solto" (parcial — ver pendências) |
| `if __name__ == '__main__'` | Organização |

### Etapa 4 — Programação defensiva (muda comportamento) → Seções 2 e 4

| O que foi feito | Exigência do enunciado atendida |
|---|---|
| Exceções próprias: `HorarioForaIntervaloPermitidoErro`, `PisoDuracaoAtendimentoErro`, `HorarioReservadoErro`, `AgendamentoNaoEncontradoErro`, `FormatoDataInvalidaErro` | "exceção específica (`ValueError` ou própria herdando de `Exception`)" |
| Remoção do `try/except: pass` | "nenhum bloco de captura vazio ou genérico" |
| Horário fora do expediente e duração ≤ 0 lançam exceção | "nenhuma operação pode falhar em silêncio" |
| `remarcar` de agendamento inexistente lança `AgendamentoNaoEncontradoErro` | "nenhuma operação pode falhar em silêncio" (o `rem` não fazia nada) |
| `remarcar` valida expediente da hora original e da nova | Cláusulas de guarda em toda função pública |
| Validação de data (`adicionar`: `data`; `remarcar`: `data` e `nova_data`; `listar_por_data`: `data`) | Regra de negócio "Data — formato AAAA-MM-DD" |
| Validações no início de `adicionar`, `remarcar` e `listar_por_data` | "pré-condições verificadas com cláusulas de guarda" |
| `FormatoDataInvalidaErro` inclui a data rejeitada na mensagem | "mensagem que diz qual valor causou o problema" (só esta, por enquanto) |

### Apoio — CLI para teste manual (`cli.py`)

- Menu numerado (1 marcar, 2 remarcar, 3 listar, 0 sair) com `input` para cada entrada.
- A `Agenda` lança as exceções para o topo; a CLI captura **uma tupla explícita** (as cinco exceções próprias + `ValueError` + `TypeError`) só para exibir `Erro (Tipo): mensagem` e continuar. Sem `except Exception` — respeita "nenhum bloco de captura genérico".
- `EOFError`/`KeyboardInterrupt` (Ctrl+D / Ctrl+C) encerram sem traceback.
- A data digitada não passa por `.strip()`, para permitir testar entradas como `' 2026-10-05'`.

### Seção 3 — Decisões de projeto

- **Exceções próprias** em vez de `ValueError` / `print`.
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
- **Onde fica a barreira de validação: na entrada dos métodos públicos.**
  - `adicionar`, `remarcar` e `listar_por_data` são a **fronteira de confiança**: recebem dados de fora (CLI, testes, outros módulos) e tratam tudo como hostil.
  - A validação fica **dentro** do método público, não em quem o chama (ex.: a CLI). Se ficasse fora, todo chamador teria que lembrar de validar, e bastaria um esquecer para dado inválido entrar. O método se protege sozinho.
  - Os `__validar_*` são privados só por organização (uma responsabilidade cada) — eles **são** a barreira. Já `__buscar_agendamento` e `__verificar_agendamento_*` ficam **atrás** dela: recebem dados já validados e não revalidam.
- **Quando validar: antes de qualquer efeito colateral (tudo ou nada).** Todas as guardas rodam antes do `append` (em `adicionar`) e antes de alterar `data`/`hora_atendimento`/`status` (em `remarcar`). Se uma falha, nada foi alterado — a agenda nunca fica meio modificada.
- **Ordem das guardas: entrada primeiro, estado depois.** Tipo/formato/faixa (baratas, sem consultar a agenda) antes de conflito/existência (consultam a lista). Ex.: data `2026-10-5` num horário ocupado gera `FormatoDataInvalidaErro`, não `HorarioReservadoErro`.
- **`raise` para validação, nunca `assert`.**
  - Critério: *quem pode causar a falha?* Quem chama (entrada ruim, estado inesperado) → `raise` com exceção específica. Só um bug no próprio código → `assert`.
  - `assert` é removido com `python -O` (`__debug__ = False`). Validar entrada com `assert` faria o sistema voltar a aceitar 20h, duração negativa e qualquer data em modo otimizado — falha silenciosa, exatamente o que a Etapa 4 proíbe. Além disso, `AssertionError` não é uma exceção específica.
  - Uso possível de `assert` (opcional, não implementado): registrar **invariantes** no núcleo, ex. no início de `__buscar_agendamento`, uma vez antes do laço:
    ```python
    assert self.__data_no_formato(data), f'Data nao validada pela barreira: {data!r}'
    ```
    com um predicado `__data_no_formato(data) -> bool` (não dá para usar `assert self.__validar_data(data)`: o validador retorna `None` e o assert falharia sempre). Custo: duplica a lógica da ida e volta. Ganho: na reestruturação em vários arquivos, avisa se algum caminho novo chamar o núcleo sem passar pela barreira.
  - A suíte passa igual com `python3 -O -m unittest` — nenhum teste depende de `assert` (os `self.assert*` do `unittest` são métodos, não o comando `assert`).
- **Testes com `unittest`** — 68 testes em `tests/test_agenda.py` cobrindo expediente, duração, data, conflito, remarcação, listagem, status, barreira de validação, isolamento entre instâncias e mensagens de erro. Usam `subTest` para listar cada data inválida separadamente. Garantem que a refatoração não mudou o caminho feliz e documentam cada mudança intencional.
  - `TestBarreiraTudoOuNada`: operação rejeitada não deixa a agenda alterada (nem status).
  - `TestBarreiraOrdem`: validações de entrada são detectadas antes das de estado.
  - `TestBarreiraTipos`: dois testes marcados com `@unittest.expectedFailure` documentam os furos conhecidos (hora `8.5` e duração `30.5` aceitas). Quando forem corrigidos, o `unittest` acusa *unexpected success* — sinal para remover o decorador.
  - Os testes de `listar_por_data` capturam a saída (`redirect_stdout`) e verificam só se cada informação aparece (`assertIn`), sem fixar o texto exato — o formato ainda vai mudar (ver pendências).
  - Como `'MARCADO'` está contido em `'REMARCADO'`, os testes de status também verificam que `REMARCADO` **não** aparece quando não deveria.

### Linhas para a Seção 4 (Mudanças de comportamento)

| Entrada ou situação | O que acontecia antes | O que acontece agora |
|---|---|---|
| Atendimento às 18h ou mais (ex.: 20h) ou antes das 8h | Nada — os `if` falhavam e a função saía sem marcar e sem avisar | Lança `HorarioForaIntervaloPermitidoErro` |
| Duração ≤ 0 | Nada — `if dur > 0` falhava em silêncio | Lança `PisoDuracaoAtendimentoErro` |
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

- [ ] **Programa de demonstração idêntico ao código-base.** A "regra de ouro" exige a mesma saída de hoje:

  ```
  Atendimento marcado para Ana
  Horario ocupado
  Atendimento marcado para Carla
  Remarcado
  14 Carla Dra. Souza MARCADO
  ```

  O `__main__` de `src/agenda.py` deve repetir as cinco chamadas do código-base (Ana, Bruno, Carla, `rem`, `lst`). Hoje ele chama `adicionar` às 18h e termina com exceção.

- [ ] **Caso do Bruno:** `adicionar` agora lança `HorarioReservadoErro` em vez de imprimir. O demo precisa capturar a exceção e imprimir `Horario ocupado`, senão a saída muda.
- [x] ~~Recriar `rem` (remarcar)~~ — feito como `remarcar`, reusando `__validar_disponibilidade_horario`.
- [x] ~~Recriar `lst` (listar)~~ — feito como `listar_por_data`.
- [x] ~~Status do atendimento~~ — feito: campo `status` + `AgendamentoStatus`.
- [ ] **Formato da listagem quebra a regra de ouro.** O `lst` do código-base imprime uma linha por atendimento: `hora paciente profissional status` → `14 Carla Dra. Souza MARCADO`. O `listar_por_data` imprime várias linhas, **sem a hora**, e com os espaços de indentação do código dentro do texto (efeito da f-string com aspas triplas):

  ```
  Data: 2026-10-05;
                      Paciente: Carla;
                      Profissional: Dra. Souza;
                      Status: MARCADO
  ```

  Ao mudar o formato, os testes de listagem continuam valendo (não fixam o texto).
- [ ] **Impressão fora da lógica:** "quem agenda não imprime" — as mensagens (`Atendimento marcado para ...`, `Remarcado`) e a listagem devem sair do demo/camada de apresentação. Sugestão: `listar_por_data` **retorna** a lista de agendamentos da data e o `__main__` formata e imprime. Bônus: os testes deixam de precisar capturar `stdout`.
- [ ] **Valores fixos soltos:** `8`, `17` e `18` ainda devem virar constantes (ex.: `INICIO_EXPEDIENTE = 8`). `FORMATO_DATA` já foi feito.
- [ ] **Tipo errado:** `hora_atendimento` está anotado como `str` em `__validar_hora_atendimento`, `__buscar_agendamento`, `__validar_disponibilidade_horario` e `remarcar`; deve ser `int`.

### Etapa 3

- [ ] Docstrings estilo Google (Args, Returns, Raises) em toda função pública. Em `adicionar`/`remarcar`, o `Raises` deve listar também `ValueError` e `TypeError` da data.
- [ ] Pelo menos um comentário de decisão. Candidatos:
  - por que a data é validada por ida e volta (`strptime` + `strftime`);
  - por que o `ValueError` do `strptime` sobe sem conversão.
- [ ] README com instruções de execução e de geração de documentação.
- [ ] Gerar documentação com `pdoc` ou `sphinx-apidoc`.

### Etapa 4

- [ ] **Mensagens de erro devem dizer qual valor causou o problema.** `FormatoDataInvalidaErro` já faz; faltam `HorarioForaIntervaloPermitidoErro`, `PisoDuracaoAtendimentoErro`, `HorarioReservadoErro` e `AgendamentoNaoEncontradoErro`.
- [ ] **Mensagem de `FormatoDataInvalidaErro`** mostra `%Y-%m-%d` (código interno do `strftime`); considerar `AAAA-MM-DD`, mais legível para o usuário. Se mudar, ajustar o teste da mensagem.
- [ ] **Regra de duração:** entre 15 e 120 minutos, em múltiplos de 15. Hoje só rejeita ≤ 0. É regra nova (não existia no código-base) → registrar no diagnóstico e na Seção 4.
- [x] ~~Regra de data: validar formato `AAAA-MM-DD`~~ — feito (ver Seção 3 para a decisão sobre as exceções).
- [x] ~~Guardas no início de `remarcar`~~ — feito (hora e data, original e nova).
- [x] ~~Guardas no início de `lst`~~ — feito: `listar_por_data` valida a data consultada.
- [ ] **Furo de tipo na barreira:** hora `8.5` e duração `30.5` são aceitas (a guarda verifica a faixa, não o tipo). Hora `'10'` só é recusada por acaso (`TypeError` da comparação `str < int`). Sugestão: `isinstance(valor, int)` no início dos validadores, lançando `TypeError` com o valor na mensagem. Ao corrigir, remover os `@unittest.expectedFailure` de `TestBarreiraTipos`.
- [ ] **Porta de entrada escondida — `Agendamento`:** `Agendamento('X', 'Y', 'banana', 99, -1, 'QUALQUER')` cria um objeto inválido sem passar por nenhuma guarda, porque as validações moram na `Agenda`. Decidir na reestruturação: tratar `Agendamento` como interno (só a `Agenda` cria) **ou** mover as guardas para dentro dele (fica impossível existir agendamento inválido). Justificar na Seção 3.

## Ordem sugerida

1. Concluir a **Etapa 2**: formato da listagem, separar impressão da lógica, constantes de expediente e o programa de demonstração imprimindo a saída idêntica.
2. Completar a **Etapa 4**: mensagens com o valor, regra de duração, furo de tipo e decisão sobre `Agendamento`.
3. **Etapa 3** por último, documentando o código já estável.

Assim fica fácil provar que o caminho feliz não mudou (evita a penalidade de −1,0) e a Seção 4 do relatório fica limpa, com cada mudança intencional registrada.
