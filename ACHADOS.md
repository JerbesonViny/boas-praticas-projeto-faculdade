# Achados

Conceitos que apareceram durante o desenvolvimento do trabalho.

---

## 1. Variáveis são referências, não caixas

Em Python, uma variável é um **nome ligado a um objeto**. Atribuir (`=`) nunca copia o objeto — só cria mais um nome apontando para ele. Listas também guardam referências, não os objetos em si.

```python
agendamento = self.__buscar_agendamento(...)   # aponta para o objeto que está na lista
agendamento.data = nova_data                   # altera esse objeto → a lista "vê" a mudança
```

```
self.__agendamentos[0] ──┐
                         ├──► Agendamento(data='2026-10-05', hora=9, ...)
agendamento ─────────────┘
```

Para confirmar que dois nomes apontam para o mesmo objeto, use `is` (identidade), não `==` (igualdade de valor):

```python
a = agenda[0]
a is agenda[0]   # True
```

**Nome do conceito:** *aliasing* — dois nomes (*aliases*) para o mesmo objeto.

**Onde apareceu:** no `remarcar`, ao buscar o agendamento e alterá-lo pela variável. O `rem` do código-base dependia do mesmo mecanismo (`a[2] = nd` altera a lista dentro de `ag`).

---

## 2. Mutar ≠ reatribuir

```python
agendamento.data = nova_data       # MUTA o objeto     → a lista é afetada
agendamento = Agendamento(...)     # REATRIBUI o nome  → a lista NÃO é afetada
```

Reatribuir só faz o nome apontar para outro objeto; o antigo continua intacto na lista.

---

## 3. Mutabilidade

| Mutáveis | Imutáveis |
|---|---|
| `list`, `dict`, `set`, objetos de classes comuns | `int`, `float`, `str`, `tuple`, `bool` |

Em imutáveis não há como mutar — toda "alteração" cria um objeto novo e reatribui o nome:

```python
x = 5
y = x
y += 1      # cria um int novo; x continua 5
```

É a mutabilidade que decide se uma mudança feita por um nome aparece pelo outro.

---

## 4. Cópia explícita

Se precisar de uma cópia de verdade, ela tem que ser pedida:

```python
import copy

copia = copy.copy(agendamento)       # rasa: copia o objeto, mas compartilha os objetos internos
copia = copy.deepcopy(agendamento)   # profunda: copia também os objetos internos, recursivamente
```

---

## 5. Passagem por valor, por referência e por atribuição

Duas perguntas definem o modelo:

1. A função recebe uma **cópia** ou o **próprio objeto**?
2. Se a função **reatribuir** o parâmetro, a variável de quem chamou muda?

| Modelo | Recebe | Mutar afeta quem chamou? | Reatribuir afeta quem chamou? | Exemplos |
|---|---|---|---|---|
| **Por valor** | Cópia do valor | Não | Não | C/C++ (padrão), primitivos em Java |
| **Por referência** | Apelido da própria variável | Sim | **Sim** | C++ com `&`, `ref` em C# |
| **Por atribuição** | Cópia **da referência** | Sim (se mutável) | **Não** | Python; objetos em Java e JavaScript |

### Por valor (C++)

```cpp
void muda(Agendamento a) {
    a.hora = 10;            // mexe só na cópia
}
// quem chamou não vê nada
```

### Por referência (C++)

```cpp
void muda(Agendamento& a) {
    a.hora = 10;            // altera o original
    a = Agendamento{15};    // substitui o original
}
// quem chamou vê hora = 15
```

Teste clássico: uma função `swap(a, b)` só consegue trocar as variáveis de quem chamou com passagem por referência.

### Por atribuição (Python)

Na entrada da função, é como se o Python fizesse `parametro = argumento` — daí o nome.

```python
def muda(a):
    a.hora_atendimento = 10      # muta o objeto compartilhado → quem chamou VÊ
    a = Agendamento(...)         # só redireciona o nome local → quem chamou NÃO vê

ag = Agendamento(..., hora_atendimento=9, ...)
muda(ag)
# ag.hora_atendimento == 10
```

Parece referência quando você muta e parece valor quando você reatribui — porque o que é copiado é a **referência**, não o objeto. Com imutáveis, o efeito prático é igual ao da passagem por valor.

**Nomes:** *pass by assignment* (documentação do Python), *call by sharing* (Barbara Liskov, CLU, 1974), *pass by object reference*. A especificação do Java descreve o mesmo mecanismo como "tudo é passado por valor — e o valor de um objeto é a referência".

---

## 6. Argumentos nomeados evitam bugs de ordem

Chamada posicional com a ordem trocada:

```python
# assinatura:  __buscar_agendamento(data, hora_atendimento, nome_doutor, nome_paciente)
self.__buscar_agendamento(data, nome_doutor, hora_atendimento)   # hora e doutor invertidos
```

Python não reclama da troca (os tipos não são verificados em tempo de execução) — o conflito simplesmente nunca seria encontrado. Com argumentos nomeados, a ordem deixa de importar:

```python
self.__buscar_agendamento(
    data=data,
    hora_atendimento=hora_atendimento,
    nome_doutor=nome_doutor,
)
```

Para **obrigar** o uso de nomes, use `*` na assinatura — tudo depois dele só pode ser passado por nome:

```python
def __buscar_agendamento(self, *, data, hora_atendimento, nome_doutor=None, nome_paciente=None):
    ...
```

**Onde apareceu:** em `__validar_disponibilidade_horario`, que quebrou 9 dos 16 testes.

---

## 7. Desempacotar um retorno que pode ser `None`

```python
indice, agendamento = self.__buscar_agendamento(...)   # se retornar None → TypeError aqui
if not agendamento:                                     # nunca chega nesta linha
    raise AgendamentoNaoEncontradoErro()
```

Uma função que termina sem `return` devolve `None` implicitamente, e `None` não pode ser desempacotado. Solução: retornar um único valor (`Optional[Agendamento]`) e checar antes de usar.

---

## 8. Docstrings no estilo Google

Primeira instrução dentro da função, entre aspas triplas:

```python
def adicionar(self, nome_paciente: str, ..., duracao_minutos: int) -> None:
    """Marca um atendimento para o paciente com o profissional informado.

    Args:
        nome_paciente: Nome do paciente.
        duracao_minutos: Duração do atendimento em minutos.

    Raises:
        HorarioForaIntervaloPermitidoErro: Se a hora estiver fora do expediente.
        HorarioReservadoErro: Se o profissional já tiver atendimento na mesma data e hora.
    """
```

- **Resumo** na primeira linha; descrição opcional após uma linha em branco.
- **Args:** `nome (tipo): descrição` — o tipo pode ser omitido se já houver type hint.
- **Returns:** tipo e significado do retorno (pode ser omitido quando é `None`).
- **Raises:** cada exceção e quando ela ocorre.
- Visualizar: `help(funcao)` ou `funcao.__doc__`.

---

## 9. Testes também testam o código, não o contrário

Quando o código muda e os testes quebram, a primeira pergunta é: **o teste está errado ou o código está?** No caso do `__buscar_agendamento`, os testes não precisaram de nenhuma mudança — eles fizeram exatamente seu papel, que é apontar a regressão.

---

## 10. `raise` × `assert`

| | `raise` | `assert` |
|---|---|---|
| O que faz | Lança a exceção escolhida, sempre | Se a condição for falsa, lança `AssertionError` |
| Pode ser desligado? | **Não** | **Sim** (`python -O`) |
| Quem causa a falha | Quem **chamou** (entrada ruim, estado inesperado) | **O próprio código** (bug) |
| Para que serve | Rejeitar situações *possíveis* | Documentar e conferir o que *nunca* deveria acontecer |

`assert cond, msg` equivale a:

```python
if __debug__:
    if not cond:
        raise AssertionError(msg)
```

`__debug__` é `True` por padrão e `False` com `python -O` (ou `PYTHONOPTIMIZE=1`). Nesse modo o compilador **remove** os `assert` do bytecode. `-OO` remove também as docstrings.

```
$ python3 demo.py        →  AssertionError: Hora fora do expediente: 20
$ python3 -O demo.py     →  aceita        (o assert sumiu)
```

**Consequência:** validar entrada com `assert` é um bug esperando para acontecer — basta rodar com `-O` e o sistema volta a aceitar 20h, duração negativa e qualquer data, falhando em silêncio.

**Pegadinhas:**
- `assert (cond, 'msg')` — tupla não vazia é sempre verdadeira; o assert nunca falha (o Python emite `SyntaxWarning: assertion is always true`).
- `self.assertEqual`, `self.assertRaises` etc. do `unittest` são **métodos**, não o comando `assert` — o `-O` não os afeta.

---

## 11. Guardas: onde, o quê e quando validar

A pergunta que separa `raise` de `assert`: **quem pode causar essa falha?**

- **Quem chama** (usuário, CLI, outro módulo) → é uma **pré-condição do contrato** → valide com `raise` uma exceção específica.
- **Só um bug meu** → é um **invariante** → `assert` (ou nada).

### Onde: na fronteira de confiança

A fronteira é por onde dados de fora entram no sistema: métodos **públicos** (`adicionar`, `remarcar`, `listar_por_data`), a CLI, leitura de arquivos, rede. Ali, toda entrada é tratada como hostil.

Dentro da fronteira (métodos privados como `__verificar_agendamento_por_doutor`), os dados **já passaram pelas guardas** — revalidar tudo em cada função só polui o código. Se quiser registrar uma suposição interna, `assert`.

```
  CLI / chamador externo
          │  dados não confiáveis
          ▼
 ┌─────────────────────────┐
 │ adicionar / remarcar /  │  ← guardas com raise (fronteira)
 │ listar_por_data         │
 ├─────────────────────────┤
 │ __buscar, __verificar…  │  ← dados já validados; no máximo assert
 │ self.__agendamentos     │
 └─────────────────────────┘
```

**Cuidado com fronteiras escondidas:** toda classe/função pública é uma porta de entrada. `Agendamento('X', 'Y', 'banana', 99, -1, 'QUALQUER')` cria um objeto inválido sem passar por nenhuma guarda, porque as validações moram na `Agenda`. Ou `Agendamento` é tratado como interno (só a `Agenda` cria), ou as guardas passam a morar nele — e aí é impossível existir um agendamento inválido.

### O quê: tudo de que a operação depende para estar correta

1. **Tipo** — `'10'` como hora gera `TypeError` só por acaso (comparação `str < int`); `8.5` passa sem erro.
2. **Formato** — data `AAAA-MM-DD`.
3. **Faixa / regra de negócio** — expediente, duração.
4. **Estado** — horário livre, agendamento existente. Não é "entrada malformada", mas é pré-condição: a operação não pode prosseguir. Também é `raise`, porque é uma situação **possível**, não um bug.

### Quando: antes de qualquer efeito colateral

"Antes de qualquer operação" significa **antes de mudar qualquer estado** (o `append`, a atribuição de `agendamento.data`). Se a validação falhar no meio de uma alteração, o sistema fica meio-alterado — dado corrompido. Validar tudo primeiro e só então alterar garante que a operação é **tudo ou nada**. É isso que o teste "remarcação rejeitada mantém o horário original" verifica.

Ordem prática: validações baratas e sem estado (tipo, formato, faixa) primeiro; validações que consultam o estado (conflito, existência) depois; alteração por último.
