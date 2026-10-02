# Relatório de Entrega --- Sprint 2 (E6)

## Identificação

**Projeto:** Sistema Web de Controle de Estoque para Empresa de
Comunicação Visual\
**Disciplina:** Laboratório de Engenharia de Software\
**Sprint:** Sprint 2\
**Entrega:** E6 --- Encerramento da Sprint 2\
**Integrantes:** - Breno Tales de Oliveira Leite --- RA 2840482423029 -
Daniel Fredi Soares Pereira --- RA 2840482421054

**Pontuação da Sprint:** 13 pontos

## 1. Objetivo da Sprint

A Sprint 2 teve como foco a evolução do controle de estoque por meio de
funcionalidades relacionadas à identificação de materiais por código de
barras, registro de entradas de estoque e consulta do histórico de
movimentações.

## 2. Histórias de Usuário concluídas

### US #4 --- Identificação por Código de Barras

**Situação:** Concluída.

Foi implementada uma API para localizar materiais utilizando o código de
barras cadastrado no sistema.

-   Rota protegida: `/estoque/api/material/codigo/<codigo_barras>`
-   Busca do material pela camada de serviço.
-   Retorno dos dados do material identificado.
-   Tratamento para código inexistente.
-   Testes automatizados de autenticação, material existente,
    inexistente e não alteração do estoque.

### US #5 --- Registro de Entrada por Código de Barras

**Situação:** Concluída.

Foi implementado o registro de entrada de estoque utilizando o material
identificado por código de barras.

-   Rota: `/estoque/entrada`
-   Registro da entrada de bobinas.
-   Atualização da quantidade e da metragem disponível.
-   Registro de uma `MovimentacaoEstoque`.
-   Validação da quantidade de bobinas.
-   Tratamento de material inexistente.
-   Proteção por autenticação.

### US #6 --- Consulta e Relatório de Movimentações

**Situação:** Concluída.

Foi implementada uma tela para consulta do histórico de movimentações do
estoque.

-   Rota: `/estoque/movimentacoes`
-   Acesso protegido por autenticação.
-   Movimentações mais recentes primeiro.
-   Filtro por tipo de movimentação.
-   Filtro por material.
-   Exibição de data/hora, material, tipo, quantidade, usuário
    responsável e motivo.
-   Link para a tela no menu principal.

## 3. Testes e validação

A suíte completa de testes foi executada após a implementação da Sprint
2.

``` text
Ran 41 tests in 13.814s

OK
```

Todos os 41 testes foram aprovados.

Os testes da US #6 validaram o bloqueio sem login, a exibição do
histórico, a ordenação das movimentações e os filtros por tipo e
material.

Foram apresentados avisos de compatibilidade/depreciação durante a
execução, mas nenhum causou falha de teste.

## 4. Controle de versão

### Correção do isolamento dos testes

``` text
f63a915 fix(test): isola banco de dados dos testes
```

### Implementação da US #6

``` text
eac4bf1 feat(estoque): adiciona tela de consulta e relatorio de movimentacoes do estoque
```

Os commits foram publicados no repositório remoto após a validação da
suíte.

## 5. Resultado da Sprint

As US #4, #5 e #6 previstas para a Sprint 2 foram concluídas,
totalizando **13 pontos**.

**Status final: CONCLUÍDA.**
