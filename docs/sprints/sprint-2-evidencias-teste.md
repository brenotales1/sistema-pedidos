# Evidências de Testes --- Sprint 2 (E6)

## Identificação

**Projeto:** Sistema Web de Controle de Estoque para Empresa de
Comunicação Visual\
**Sprint:** Sprint 2\
**Integrantes:** - Breno Tales de Oliveira Leite --- RA 2840482423029 -
Daniel Fredi Soares Pereira --- RA 2840482421054

## 1. Comando utilizado

``` powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py" -v
```

## 2. Resultado final

``` text
----------------------------------------------------------------------
Ran 41 tests in 13.814s

OK
```

**Resultado:** 41 testes executados e 41 aprovados.\
**Taxa de aprovação:** 100%.

## 3. Casos de teste da Sprint

Os casos CT01 a CT07 previstos para a Sprint foram considerados
aprovados na validação da entrega.

  Caso   Resultado
  ------ -----------
  CT01   PASS
  CT02   PASS
  CT03   PASS
  CT04   PASS
  CT05   PASS
  CT06   PASS
  CT07   PASS

## 4. Evidências relacionadas às US #4, #5 e #6

### US #4 --- Identificação por código de barras

Foram aprovados testes relacionados à consulta por código de barras
existente e inexistente, autenticação da API, busca na camada de serviço
e garantia de que a identificação não altera o estoque.

### US #5 --- Entrada de estoque

Foram aprovados testes relacionados ao registro de entrada, atualização
de bobinas e metragem, criação do histórico, quantidade inválida,
material inexistente e autenticação da rota.

### US #6 --- Consulta de movimentações

Foram aprovados:

``` text
test_movimentacoes_estoque_sem_login
test_movimentacoes_estoque_exibe_historico
test_movimentacoes_estoque_mais_recentes_primeiro
test_movimentacoes_estoque_filtros_tipo_e_material
```

## 5. Observações

A execução apresentou `LegacyAPIWarning`, `DeprecationWarning` e
`ResourceWarning`. Esses avisos não impediram a execução e não
produziram falhas nos testes.

## 6. Conclusão

A versão entregue da Sprint 2 passou integralmente pela suíte
automatizada disponível no projeto, com **41 testes aprovados**.
