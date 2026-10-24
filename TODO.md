# TODO — AgendaFácil

**Prazo: 25/10/2026, 23h59.** Atraso: −1,0 por dia.

Detalhes e justificativas de cada item estão em `ANOTACOES.md`.

## 1. Decisões a tomar

- [ ] **Status `REMARCADO`:** o `rem` do código-base mantinha `MARCADO`. Decidir entre voltar a manter `MARCADO` ou manter `REMARCADO` e justificar na Seção 3 do relatório. Isso muda o caminho feliz, e sem justificativa custa −1,0.
- [ ] **`remarcar` valida a hora original:** remarcar "das 20h" lança `HorarioForaIntervaloPermitidoErro`, e não `AgendamentoNaoEncontradoErro`. Decidir se mantém.

## 2. Código

- [x] ~~**Tipo da hora:** trocar `str` por `int` em `hora_atendimento` e `nova_hora_atendimento`~~ (assinaturas em `agenda.py`, `agendamento_entidade.py` e `agenda_utilitario.py`).
- [x] ~~**Mensagens com o valor que causou o erro** (o enunciado pede "qual valor causou o problema")~~: as cinco exceções e `tests/test_erros.py`.
- [x] ~~**Furo de tipo:** hora `8.5` e duração `45.0` são aceitas. Verificar `isinstance(valor, int)` nos validadores e remover os 4 `@unittest.expectedFailure`.~~

## 3. Documentação

- [ ] **Docstrings** (Args, Returns, Raises) em toda função pública:
  - [ ] `src/agendamento_entidade.py`:
    - [x] ~~`marcar` e `remarcar`~~.
    - [x] ~~Construtor~~.
    - [ ] `se_validar`, `atualizar_data` e `atualizar_hora_atendimento`: já têm docstring, mas falta o `Raises` (as exceções dos validadores: `HorarioForaIntervaloPermitidoErro`, `ConsultaIntervaloDuracaoErro`, `ConsultaMultiploDuracaoErro`, `FormatoDataInvalidaErro`, `ValueError`, `TypeError`).
  - [ ] `src/agenda_utilitario.py`: `validar_hora_atendimento` e `validar_duracao`.
  - [ ] `src/data_utilitarios.py`: `validar_data`.
  - [ ] `cli.py`.
- [x] ~~**Ajustes nas docstrings de `src/agenda.py`:**~~
  - [x] ~~No `Returns` de `__verificar_agendamento_por_doutor`, trocar "paciente" por "doutor".~~
  - [x] ~~Trocar os `(str)` da hora por `(int)` quando o tipo for corrigido.~~
- [ ] **Comentário de decisão** (pelo menos um). Candidatos:
  - a validação de data por ida e volta (`strptime` e depois `strftime`);
  - o `ValueError` do `strptime` subindo sem conversão;
  - o `AGENDAMENTO_HORA_LIMITE - 1` na mensagem de expediente;
  - o `FORMATO_DATA` morando em `constantes.py`.
- [ ] **`README.md` na raiz:** o que é o sistema, como executar (`python3 -m src.agenda`, `python3 cli.py`, `python3 -m unittest`), como gerar a documentação e quem fez.
- [ ] **Documentação de API:** gerar com `pdoc` ou `sphinx-apidoc` na pasta `docs/`, ou deixar o comando no README. Hoje `docs/README.md` está vazio.

## 4. Relatório (`relatorio.tex`)

- [ ] **Identificação:** preencher integrantes e matrícula, e trocar o repositório por `https://github.com/JerbesonViny/boas-praticas-projeto-faculdade`.
- [ ] **`\integrantes`:** trocar o `\\` por `\newline`, porque o `\\` quebra a tabela de identificação.
- [ ] **Seções 2, 3 e 4:** revisar o rascunho e reescrever no seu estilo.
- [ ] **Seção 3:** registrar a decisão sobre o status `REMARCADO`, se ele for mantido.
- [ ] **Seção 5:** comandos de execução, de geração da documentação, a pasta `docs/` e a saída da demonstração.
- [ ] **Seção 6:** declarar o uso de IA (obrigatório).
- [ ] **Tamanho:** são 7 páginas para um limite de 4.
  - [ ] A tabela de diagnóstico sai cortada no PDF (as linhas 6 a 10 não aparecem). Trocar por `xltabular` ou encurtar.
  - [ ] Página 2 em branco.
  - [ ] Linha 3 do diagnóstico muito longa. A parte "objeto/dicionário" é solução e caberia na Seção 2.
- [ ] **Erros de digitação:** "Manutenabilidade" → "Manutenibilidade" (3 vezes), "acessa" → "acessada", "utilizassemos" → "utilizássemos", "estariamos" → "estaríamos", "apena" → "apenas".
- [ ] Linha 8 do diagnóstico: reescrever no seu estilo.
- [ ] Recompilar e atualizar o `relatorio.pdf`.

## 5. Entrega

- [ ] Tirar do Git `orientacoes/.~lock.Projeto_Unidade1_Modelo_Relatorio.docx#` e acrescentar `.~lock.*#` ao `.gitignore`.
- [ ] Confirmar que o professor tem acesso ao repositório.
- [ ] Rodar `python3 -m unittest` e `python3 -m src.agenda` uma última vez.
- [ ] `git push`.
