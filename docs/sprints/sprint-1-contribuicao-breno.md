# Relatório Individual de Contribuição — Sprint 1 — Breno Tales de Oliveira Leite (RA 2840482423029)

**Papel nesta sprint:** Qualidade e QA / Testes Automatizados / Refatoração

---

## 1. O que fiz

| Item | PR/commit | Status |
|---|---|---|
| Correção do seed de materiais padrão adicionando `codigo_barras` obrigatório (`services/material_service.py`) | Commit `b90dbb5` | Mergeado |
| Implementação da barra superior de navegação com status do usuário logado, badge de perfil e botão de Logout (`base.html`, `lista.css`) | Commit `231fc96` | Mergeado |
| Criação da suíte de testes automatizados com 24 testes unitários e de integração (`tests/test_auth.py`, `tests/test_estoque.py`, `tests/test_pedidos.py`, `tests/test_clientes.py`) cobrindo CT01 a CT05 | Commit `31a8c3b` | Mergeado |
| Organização, prefixação e sincronização dos documentos das entregas E1 a E4 e elaboração dos documentos da entrega E5 (`docs/sprints/`) | Commit de documentação | Mergeado |

---

## 2. Rituais que participei

- [x] Dailies/weeklies (alinhamentos assíncronos e reuniões de planejamento)
- [x] Sprint Review (apresentação do incremento da Sprint 1)
- [x] Retrospectiva da Sprint 1

---

## 3. PRs de colegas que revisei

| PR / Commit | Autor | Comentário resumido |
|---|---|---|
| Commit `a7088f8` (Implementação Sprint 1: Login, código de barras e consulta) | Daniel Fredi | Identifiquei que o campo `codigo_barras` precisava ser incluído também no seed de inicialização `MATERIAIS_PADRAO` para evitar erro de banco limpo, e solicitei a inclusão de `@login_required` nos controllers. |

---

## 4. Dificuldades e o que aprendi

- **Isolamento de banco em testes Flask:** O principal desafio foi estruturar fixtures com banco SQLite em memória (`sqlite:///:memory:`) que respeitassem os dados semeados automaticamente pelo `create_app()` sem causar conflito de chave única (`UNIQUE constraint`) nos testes de cadastro.
- **Validação do algoritmo de corte:** Compreendi a fundo as regras matemáticas do algoritmo de aproveitamento de corte em `pedido_service.py` (que avalia rotação e desperdício de área da bobina), o que permitiu escrever asserções precisas para testar o consumo real de metros de material.
