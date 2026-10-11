# Categorias do diagnóstico (Etapa 1)

O enunciado e o modelo do relatório **só nomeiam** as cinco categorias do checklist da Aula 2 — as definições não estão no material do projeto. O que segue é o significado usual de cada uma em revisão de código, com exemplos tirados de `codigo-base/agenda_base.py`. **Conferir com os slides da Aula 2**, caso o professor tenha dado um recorte diferente.

---

## 1. Adequação e lógica

**O código faz o que deveria fazer?** Erros de lógica, regras de negócio ausentes ou erradas, casos não tratados, comportamento diferente do esperado.

- Regras de duração (15 a 120 min, múltiplos de 15) e de data (`AAAA-MM-DD`) não existem no código-base — o enunciado diz que "descobrir quais [regras] são quais faz parte do diagnóstico".
- `rem` remarca para qualquer hora, inclusive fora do expediente, sem as validações que `add` faz.
- O comentário de `lst` diz "lista os atendimentos do mês", mas a função compara a data exata (um dia só).

## 2. Manutenibilidade

**É fácil entender e alterar sem quebrar?** Nomes ruins, estruturas opacas, duplicação, comentários inúteis ou mentirosos.

- Nomes `add`, `rem`, `lst`, `p`, `pr`, `d`, `h`, `dur`, `ag`, `a`, `b`, `ok` não dizem o que são.
- Acesso por índice (`a[2]`, `a[3]`, `a[5]`): é preciso decorar a ordem dos campos, e mudar essa ordem quebra tudo sem aviso.
- Laço de verificação de conflito **duplicado** em `add` e `rem`.
- Comentários de ruído (`# adiciona na lista`), código morto comentado (`desmarcar`), TODO vencido, cabeçalho com histórico de alterações.

## 3. Organização e estética

**Como o código está estruturado e apresentado?** Funções com várias responsabilidades, aninhamento profundo, estado global, valores fixos soltos, formatação.

- `add` valida, agenda **e** imprime (o enunciado pede "quem valida não agenda, quem agenda não imprime").
- Quatro níveis de `if` aninhados em `add`.
- Lista global `ag`, modificável de qualquer lugar.
- Valores fixos soltos: `8`, `18`, `"MARCADO"`.
- Programa de demonstração no nível do módulo, sem `if __name__ == '__main__'` — executa até quando o arquivo é importado.

## 4. Programação defensiva e segurança

**Como o código lida com entradas ruins e erros?** Validação, guardas, exceções, erros engolidos.

- `except: pass` engole qualquer erro.
- `if` sem `else` fazem a função falhar em silêncio (linha 1 já preenchida no relatório).
- `rem` também falha em silêncio quando o atendimento não existe.
- Nenhuma verificação de tipo (data `None` é aceita).
- Erros comunicados com `print` em vez de exceção — quem chama não tem como reagir.

## 5. Desempenho e recursos

**Uso razoável de tempo e memória?** Trabalho repetido, laços desnecessários, estruturas inadequadas. Num sistema pequeno é a categoria mais difícil — tudo bem a anomalia ser modesta, desde que o efeito seja explicado.

- O laço de conflito em `add` não para (`break`) ao encontrar conflito; continua percorrendo a lista inteira.
- `rem` também não para depois de remarcar: o laço externo segue após encontrar o atendimento.
- Toda busca (conflito, remarcação, listagem) percorre a lista inteira. Indexar por data ou por `(profissional, data, hora)` num `dict` evitaria isso — boa candidata a **dívida assumida** na Seção 2: em volume pequeno não compensa, e dá para justificar.

---

## Como classificar quando uma anomalia cabe em mais de uma categoria

Algumas anomalias tocam mais de uma categoria (a duplicação do laço de conflito afeta manutenção e organização). O que importa é escolher uma e explicar o **efeito prático**. Os critérios de avaliação ajudam a decidir:

| Critério de avaliação | Pontos | Sugere classificar em |
|---|---|---|
| Diagnóstico — anomalias identificadas, classificadas e justificadas | 2,0 | — |
| Organização — uma responsabilidade por função, sem duplicação, sem valores fixos soltos | 2,5 | Organização e estética |
| Nomenclatura — nomes descritivos e convenção da linguagem | 1,5 | Manutenibilidade |
| Documentação — contrato das funções públicas, README, comentários de decisão | 2,0 | Manutenibilidade |
| Programação defensiva — validação, guardas, exceções específicas, nenhum erro engolido | 2,0 | Programação defensiva e segurança |

## Lembretes do modelo do relatório

- Mínimo de **dez** anomalias, com pelo menos **uma em cada** categoria.
- Em "onde", apontar função, variável ou linha — "está tudo errado" não é localização.
- Em "por que é um problema", escrever o **efeito prático** sobre quem lê ou mantém o código, não a regra violada.
- Numerar: a Seção 2 se refere às anomalias pelo número.
