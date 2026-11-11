# Relatório Individual de Contribuição — Sprint 4 — Breno Tales de Oliveira Leite (RA 2840482423029)

**Papel nesta sprint:** Engenheiro de Testes Automatizados / Garantia de Qualidade (QA) / Consolidação Documental e Validação do MVP  
**Consolidação:** 10/11/2026

---

## 1. O que fiz

| Item / Atividade | Arquivo / Módulo | Situação |
|---|---|:---:|
| **Testes da US #6 (Movimentações e Consistência):** Criação de 12 testes automatizados cobrindo saídas em pedidos, estornos em edições, devoluções em cancelamentos, entradas manuais (cadastro e adição), remoção com metragem deduzida, ajuste com saldo anterior/posterior, idempotência ao salvar mesmo saldo, rollback em falhas e bloqueio de exclusão de materiais com histórico | `tests/test_movimentacoes_sprint4.py` | Implementado e aprovado (12 testes) |
| **Testes da US #10 / CT46 (Histórico de Notificações):** Criação de 7 testes cobrindo acesso exclusivo de administrador (bloqueio a anônimos e funcionários), conferência de cliente, pedido, data/hora UTC e resultado, filtros por status, paginação em lotes de 25 registros, ordenação decrescente, tratamento de lista vazia e garantia de que a consulta não dispara mensagens nem altera dados | `tests/test_notificacoes_historico.py` | Implementado e aprovado (7 testes) |
| **Testes da US #11 (Estoque Mínimo):** Criação de 8 testes validando cadastro e edição por admin, bloqueio a funcionários, rejeição de valores negativos/não numéricos, verificação estrita de que o alerta só ocorre para `saldo < mínimo`, filtro de listagem `?abaixo_minimo=1`, persistência e migração preservando saldos | `tests/test_estoque_minimo.py` | Implementado e aprovado (8 testes) |
| **Testes de Cancelamento Condicional:** Criação de 5 testes validando cancelamento permitido em "Pagamento pendente" e "Aguardando produção" com estorno ao estoque, bloqueio estrito em "Pronto para retirada" e "Finalizado" (inclusive por requisição direta POST) com preservação de pedido e saldo, e ocultação visual do botão | `tests/test_cancelamento_pedido.py` | Implementado e aprovado (5 testes) |
| **Testes de Inicialização Segura de Estoque:** Criação de 4 testes garantindo que o reinício (`seed_materials`) não repõe bobinas em materiais esgotados (saldo zero), não altera saldos parciais, mantém larguras distintas separadas e não executa consolidação automática | `tests/test_inicializacao_estoque.py` | Implementado e aprovado (4 testes) |
| **Testes de Códigos de Barras de Materiais:** Criação de 7 testes cobrindo cadastro e correção de códigos pelo admin, bloqueio a funcionários, rejeição de código vazio, duplicado ou inválido (> 50 chars ou controle), preservação de bobinas/histórico e confirmação de busca, consulta via API e entrada de estoque via leitor com o código salvo | `tests/test_codigo_barras_materiais.py` | Implementado e aprovado (7 testes) |
| **Execução e Validação de Regressão da Suíte Completa:** Execução integrada dos 111 testes automatizados (68 pré-existentes + 43 novos), confirmando 100% de aprovação e ausência total de regressões nos módulos de autenticação, clientes, pedidos, estoque e WhatsApp | Suíte completa em `tests/` | Concluído (111 testes OK) |
| **Consolidação Documental e Alinhamento do MVP:** Atualização do Backlog Priorizado (`docs/backlog.md`), atualização do Plano de Testes com CT46 a CT53 (`docs/plano-de-testes.md`), elaboração das Evidências de Teste (`sprint-4-evidencias-teste.md`), Relatório de Entrega (`sprint-4-relatorio.md`), Retrospectiva (`sprint-4-retrospectiva.md`) e Revisão do MVP (`sprint-4-revisao-mvp.md`) | `docs/` e `docs/sprints/` | Concluído / Integrado |

---

## 2. Rituais que participei

- [x] Dailies/weeklies (alinhamentos de validação técnica e critérios de aceite do MVP)
- [x] Sprint Review (apresentação dos resultados dos testes automatizados e evidências de conformidade das US #6, #10 e #11)
- [x] Retrospectiva da Sprint 4 (fechamento dos critérios de aceite e consolidação da entrega final)

---

## 3. PRs e Entregas de colegas que revisei e testei

| Entrega / Commit | Autor | Comentário resumido |
|---|---|---|
| Commit `695791c` (07/11/2026): Tela `/notificacoes`, sanitização de logs, validações de pedidos e ajuste no Enter do leitor | Daniel Fredi | Revisei as implementações e criei a bateria de testes automatizados do CT46 (`tests/test_notificacoes_historico.py`), validando permissões, paginação, filtros e garantia de não-disparo de mensagens durante a navegação. |
| Commit `652bd8f` (09/11/2026): Estoque mínimo, ampliação do histórico de movimentações, bloqueios de cancelamento, migração DDL e edição de códigos de barras | Daniel Fredi | Revisei o código e concebi os 36 testes específicos de estoque mínimo, movimentações atômicas, cancelamento seguro, inicialização e códigos de barras, assegurando cobertura total de regras de borda. |

---

## 4. Dificuldades e o que aprendi

- **Construção de Testes de Isolamento sem Efeitos Colaterais:** Para testar a rota `/notificacoes` garantindo que ela não realiza requisições HTTP externas nem altera registros, utilizei patches e mocks de rede, certificando que a consulta administrativa seja estritamente somente-leitura.
- **Validação de Casos de Borda e Transações Atômicas:** Testar falhas forçadas com `rollback` permitiu comprovar que, se a gravação de uma movimentação falhar, a alteração física de metragem é desfeita simultaneamente, prevenindo desvios entre saldo e histórico.
- **Cobertura Completa do MVP:** A implementação dos 43 testes adicionais e a auditoria de regressão sobre os 68 testes existentes garantiram que a entrega atinge 111 testes automatizados aprovados, formalizando a aprovação técnica para a banca avaliadora da Fatec.
