# Revisão do MVP — Sprint 4 — Sistema de Pedidos e Controle de Estoque

**Revisão inicial:** 07/11/2026  
**Atualização final:** 10/11/2026  
**Situação:** **Validado tecnicamente / Aprovado para Entrega do MVP**  
**Equipe:** Breno Tales de Oliveira Leite (RA: 2840482423029) — Daniel Fredi Soares Pereira (RA: 2840482421054) · Laboratório de Engenharia de Software · ADS Fatec Ribeirão Preto  

**Referências:** [Backlog vigente](../backlog.md), [plano de testes](../plano-de-testes.md), [termo de aceite](../termo-de-aceite.md) e [evidências da Sprint 4](sprint-4-evidencias-teste.md).

---

## 1. Objetivo e escopo

Verificar a implementação dos requisitos e as pendências para o aceite do MVP. O escopo acordado inclui as US #1 a #11, com prioridades Must e Should. A US #12 — Dashboard é prioridade Could e não integra as funcionalidades obrigatórias do termo de aceite.

Todas as funcionalidades das Sprints 1 a 4 foram validadas formalmente por meio de testes automatizados unitários e de integração, garantindo que o sistema atende aos critérios funcionais e não apresenta regressões.

---

## 2. Revisão dos requisitos Must Have

| US | Critérios revisados | Implementação e evidências | Situação |
|---|---|---|:---:|
| #1 | E-mail e senha obrigatórios; erro para credenciais inválidas; permissões por perfil | Rotas de autenticação e controle de acesso implementadas; rotas administrativas protegidas com `@admin_required`. Testes em `tests/test_auth.py`. | **Aprovada** |
| #2 | Código único; descrição e quantidade obrigatórias; persistência após validação | Cadastro implementado com validações de unicidade e dimensões. Testes em `tests/test_estoque.py` e `tests/test_codigo_barras_materiais.py`. | **Aprovada** |
| #3 | Exibir descrição, código e quantidade; localizar material; informar ausência | Lista e busca implementadas e validadas por testes de interface e rotas. | **Aprovada** |
| #4 | Identificar código existente; erro para inexistente; consulta sem alterar saldo | API de consulta JSON implementada (`/estoque/api/material/codigo/...`), suportando leitor USB HID e digitação manual sem alterar saldos. | **Aprovada** |
| #5 | Quantidade positiva; material cadastrado; atualizar saldo; registrar movimentação | Rota `/estoque/entrada` atualiza metros e adiciona bobinas, registrando movimentação atômica. Testes em `test_estoque.py`. | **Aprovada** |
| #7 | Pedido existente; cliente vinculado; atualização registrada | Transição de status auditada com validação de cliente e usuário em `HistoricoStatusPedido`. Testes em `tests/test_pedidos.py`. | **Aprovada** |
| #8 | Validar telefone; mensagem com pedido e atualização; informar sucesso ou falha | Fluxo de finalização implementado com integração à Meta Cloud API, simulação controlada nos testes e feedback visual flash. CT42–CT44. | **Aprovada** |
| #9 | Evento dispara envio; destinatário correto; resultado registrado | Disparo automático na finalização; idempotência (repetir status não reenvia); persistência da tentativa vinculada ao pedido. CT45. | **Aprovada** |

---

## 3. Critérios de pronto do termo de aceite

| Critério | Situação | Observações |
|---|:---:|---|
| Acesso com perfis e permissões distintas | **Concluído** | Validação de administrador e bloqueio estrito para funcionários em rotas de gestão. |
| Entrada completa por código, quantidade, saldo e movimentação | **Concluído** | Atualização precisa de metragem e persistência em `movimentacao_estoque`. |
| Identificação de código cadastrado e erro para inexistente | **Concluído** | API JSON e tela de estoque preparadas para leitor USB e busca manual. |
| Notificação pelo WhatsApp com registro do resultado | **Concluído** | Integração via Graph API v21.0 com simulação em mocks de teste; entrega confirmada preservada como falsa. |
| Consulta do histórico de notificações | **Concluído** | US #10 implementada e validada formalmente via CT46 em `test_notificacoes_historico.py`. |
| Identificação de materiais abaixo do mínimo | **Concluído** | US #11 implementada e validada via CT50 em `test_estoque_minimo.py`. |
| Histórico de movimentações | **Concluído** | US #6 complementada com saídas de pedidos, estornos, cancelamentos e ajustes manuais. |
| Testes e evidências das alterações recentes | **Concluído** | 111 testes automatizados executados e 100% aprovados, documentados em `sprint-4-evidencias-teste.md`. |
| Código versionado no Git | **Concluído** | Arquivos de teste e documentação organizados para consolidação na branch principal. |
| Aceite final do MVP | **Aprovado** | Requisitos funcionais das US #1 a #11 atendidos integralmente. |

---

## 4. Situação das Pendências e Orientações para Produção

Com a execução dos testes e atualização documental em 10/11/2026, o quadro de pendências foi atualizado:

1. **Testes Automatizados (CT46, US #6, US #10 e US #11):** **Resolvido.** 43 novos testes foram implementados e integrados à suíte existente, alcançando 111 testes com 100% de aprovação.
2. **Documentação e Backlog:** **Resolvido.** `backlog.md`, `plano-de-testes.md`, evidências, relatório e ata da Sprint 4 consolidados.
3. **Preenchimento dos Códigos de Barras Antigos:** O sistema já disponibiliza a funcionalidade de cadastro e correção administrativa de códigos na tela de estoque, com validações de duplicidade e preservação de histórico (testado em `test_codigo_barras_materiais.py`). O preenchimento dos códigos das bobinas físicas antigas da empresa (7 itens identificados no banco local) fica postergado como **etapa operacional de implantação**, a ser executado diretamente pelo operador no momento do uso prático.
4. **Homologação Externa do WhatsApp:** A integração e a lógica do conector estão 100% testadas e auditadas em ambiente isolado. O disparo real em produção depende exclusivamente da ativação da conta corporativa e certificado HTTPS no servidor final.

---

## 5. Funcionalidades e correções da Sprint 4

| Item | Comportamento implementado | Situação |
|---|---|:---:|
| **US #6 — Histórico de movimentações** | Registra consumo de pedidos, estorno e novo consumo na edição, devolução por cancelamento permitido, estoque inicial no cadastro, adição e remoção manual de bobinas e ajustes com saldo anterior e posterior. Salvar o mesmo saldo não gera movimentação. Transações atômicas com rollback em falhas. | **Aprovada (CT47–CT49)** |
| **US #10 — Histórico de notificações** | Consulta exclusiva para administradores via `/notificacoes`, com cliente, pedido, data/hora em UTC, resultado, filtros por status e paginação de 25 registros. Idempotente (sem disparo externo). | **Aprovada (CT46)** |
| **US #11 — Estoque mínimo** | Limite por material em metros configurável pelo administrador. Alerta visual estrito (`saldo < mínimo`), filtro `?abaixo_minimo=1`, bloqueio para funcionários e migração idempotente. | **Aprovada (CT50)** |
| **Inicialização do estoque** | Reinicialização não repõe bobinas em materiais esgotados nem altera saldo parcial. Materiais com larguras distintas continuam separados; consolidação não executa automaticamente. | **Aprovada (CT53)** |
| **Cancelamento seguro** | Bloqueado para "Pronto para retirada" e "Finalizado", inclusive por requisição direta (POST), preservando pedido e saldo. Permitido em "Pagamento pendente" e "Aguardando produção". | **Aprovada (CT51)** |
| **Preservação do histórico** | Materiais com histórico de movimentações não podem ser excluídos pelo administrador, garantindo a integridade dos relatórios. | **Aprovada (CT49)** |
| **Materiais antigos** | Cadastro e correção de códigos de barras na tela de estoque pelo administrador, rejeitando códigos vazios, inválidos ou duplicados e preservando bobinas e histórico. | **Aprovada (CT52)** |

Esta revisão encerra o ciclo de validação da Sprint 4 com sucesso, registrando o cumprimento integral do escopo do Produto Mínimo Viável (MVP).
