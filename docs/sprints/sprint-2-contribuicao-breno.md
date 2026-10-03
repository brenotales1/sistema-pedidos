# Relatório Individual de Contribuição — Sprint 2 — Breno Tales de Oliveira Leite (RA 2840482423029)

**Papel nesta sprint:** Desenvolvedor Backend & Frontend / Qualidade e QA / Testes Automatizados

---

## 1. O que fiz

| Item | PR/commit | Status |
|---|---|---|
| Planejamento da Sprint 2: Atualização do Backlog, DER e Plano de Testes com CT06 e CT07 (`docs/backlog.md`, `docs/der.md`, `docs/plano-de-testes.md`) | Commit `660525e` | Mergeado |
| Implementação do serviço de busca e API de identificação de material por código de barras — US #4 (`services/material_service.py`, `controllers/estoque_controller.py`) | Commit `2273ce9` | Mergeado |
| Interface de identificação rápida de material com leitor USB e exibição de card interativo — US #4 (`templates/estoque/lista.html`, `static/css/lista.css`) | Commit `ead291a` | Mergeado |
| Criação de testes unitários e de integração para a API de identificação por código de barras cobrindo CT06 (`tests/test_estoque.py`) | Commit `f465806` | Mergeado |
| Ocultação de botões e ações administrativas para o perfil funcionário na listagem de estoque (`templates/estoque/lista.html`) | Commit `2fa419e` | Mergeado |
| Criação de testes automatizados de controle de acesso visual por perfil de usuário (`tests/test_auth.py`) | Commit `43a1223` | Mergeado |
| Implementação do modelo `MovimentacaoEstoque` e serviço de registro de entrada de estoque — US #5 (`models/movimentacao_estoque.py`, `services/estoque_service.py`) | Commit `f8486bf` | Mergeado |
| Interface integrada de entrada rápida de estoque por código de barras — US #5 (`templates/estoque/lista.html`, `controllers/estoque_controller.py`) | Commit `dcc4f1f` | Mergeado |
| Criação de testes automatizados para validação de entrada de estoque e persistência de movimentações cobrindo CT05 e CT07 (`tests/test_estoque.py`) | Commit `da62ae4` | Mergeado |

---

## 2. Rituais que participei

- [x] Dailies/weeklies (alinhamentos assíncronos e reuniões de planejamento da Sprint 2)
- [x] Sprint Review (apresentação dos incrementos da Sprint 2)
- [ ] Retrospectiva da Sprint 2

---

## 3. PRs de colegas que revisei

| PR / Commit | Autor | Comentário resumido |
|---|---|---|
| Commit `f63a915` (Isolamento de banco de dados nos testes) | Daniel Fredi | Boa otimizacao criando database_test.db isolado no TestCase.setUp, garantindo que os testes não afetem o banco de desenvolvimento local. |
| Commit `eac4bf1` (Consulta e relatório de movimentações do estoque — US #6) | Daniel Fredi | Revisei a implementação da rota GET /estoque/movimentacoes, os filtros por tipo e material e a listagem ordenada da mais recente para a mais antiga. |

---

## 4. Dificuldades e o que aprendi

- **Fluxo de Leitura USB e APIs Dinâmicas:** Aprendi a estruturar endpoints REST com resposta JSON limpa consumidos por eventos de teclado em tempo real (tecla `Enter` enviada pelo leitor físico de código de barras), permitindo carregar dinamicamente os dados do material na interface sem recarregar a página.
- **Rastreabilidade de Estoque e Modelagem de Auditoria:** Compreendi a importância de separar o estoque atual da linha do tempo imutável de movimentações (`movimentacao_estoque`), possibilitando a futura emissão de relatórios de auditoria e consumo.
