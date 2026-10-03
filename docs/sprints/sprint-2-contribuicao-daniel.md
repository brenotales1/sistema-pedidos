# Relatório Individual de Contribuição — Sprint 2 — Daniel Fredi Soares Pereira (RA 2840482421054)

**Papel nesta sprint:** Desenvolvedor Backend / Relatórios / Infraestrutura de Testes

---

## 1. O que fiz

| Item | PR/commit | Status |
|---|---|---|
| Isolamento do banco de dados de testes utilizando arquivo temporário `database_test.db` para evitar concorrência com o banco local (`tests/base.py`) | Commit `f63a915` | Mergeado |
| Implementação do serviço de listagem e filtros de movimentações de estoque em ordem decrescente — US #6 (`services/estoque_service.py`) | Commit `eac4bf1` | Mergeado |
| Criação da rota protegida `GET /estoque/movimentacoes` com suporte a filtros por tipo e material (`controllers/estoque_controller.py`) | Commit `eac4bf1` | Mergeado |
| Desenvolvimento do template responsivo de movimentações e inclusão do link de acesso no menu de navegação superior (`templates/estoque/movimentacoes.html`, `templates/base.html`) | Commit `eac4bf1` | Mergeado |
| Criação de 4 testes automatizados para autenticação, listagem, ordenação e filtros de movimentações (`tests/test_estoque.py`) | Commit `eac4bf1` | Mergeado |
| Consolidação da documentação de encerramento da Sprint 2 na entrega E6 (`docs/sprints/`) | Commit `08c8390` | Mergeado |

---

## 2. Rituais que participei

- [x] Dailies/weeklies (alinhamentos de desenvolvimento da Sprint 2)
- [x] Sprint Review (apresentação dos incrementos da Sprint 2)
- [ ] Retrospectiva da Sprint 2

---

## 3. PRs de colegas que revisei

| PR / Commit | Autor | Comentário resumido |
|---|---|---|
| Commit `2273ce9` e `ead291a` (Busca e identificação rápida por código de barras — US #4) | Breno Tales | Aprovei o endpoint `/estoque/api/material/codigo/<codigo_barras>` e a integração visual para leitor USB com captura automática. |
| Commit `f8486bf` e `dcc4f1f` (Model MovimentacaoEstoque e painel de entrada de estoque — US #5) | Breno Tales | Aprovei o modelo `MovimentacaoEstoque`, a regra de negócio de entrada de bobinas e a ocultação de botões restritos para perfil funcionário. |
| Commits `f465806`, `43a1223` e `da62ae4` (Testes automatizados cobrindo CT05, CT06 e CT07) | Breno Tales | Validei a execução completa da suíte de testes com cobertura para os novos cenários de teste da sprint. |

---

## 4. Dificuldades e o que aprendi

- **Filtros Dinâmicos com SQLAlchemy:** Aprofundei o uso de queries condicionais no SQLAlchemy combinando filtros opcionais de tipo de movimentação e ID de material de forma limpa no service.
- **Isolamento de Banco em Testes:** Entendi a importância de gerenciar a criação e destruição de instâncias de teste em arquivo dedicado para evitar vazamento de estado e conflitos com a base de desenvolvimento.
