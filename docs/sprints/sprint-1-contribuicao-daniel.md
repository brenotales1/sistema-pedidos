# Relatório Individual de Contribuição — Sprint 1 — Daniel Fredi Soares Pereira (RA 2840482421054)

**Papel nesta sprint:** Desenvolvedor Backend / Autenticação / Interface

---

## 1. O que fiz

| Item | PR/commit | Status |
|---|---|---|
| Criação do modelo `Usuario` com hashing de senhas seguro e papéis (`admin`/`funcionario`) (`models/usuario.py`) | Commit `a7088f8` | Mergeado |
| Implementação do controlador de autenticação `/login` e `/logout` (`controllers/auth_controller.py`) e template de login (`templates/login.html`) | Commit `a7088f8` | Mergeado |
| Criação dos decorators de segurança de rotas `@login_required` e `@admin_required` (`controllers/auth_required.py`) | Commit `a7088f8` | Mergeado |
| Adição de `codigo_barras` único no modelo `Material` e campos no formulário de cadastro de estoque (`models/material.py`, `controllers/estoque_controller.py`) | Commit `a7088f8` | Mergeado |
| Implementação de filtro de busca por código de barras e nome na tela de estoque (`estoque_controller.py`) | Commit `a7088f8` | Mergeado |
| Criação do script de inicialização de usuários `criar_usuario.py` | Commit `a7088f8` | Mergeado |

---

## 2. Rituais que participei

- [x] Dailies/weeklies (alinhamentos de desenvolvimento da Sprint 1)
- [x] Sprint Review (apresentação dos incrementos de funcionalidade)
- [x] Retrospectiva da Sprint 1

---

## 3. PRs de colegas que revisei

| PR / Commit | Autor | Comentário resumido |
|---|---|---|
| Commit `b90dbb5` (Correção do seed de materiais com código de barras) | Breno Tales | Aprovei a adição dos códigos EAN nos materiais padrão do seed, evitando erros na criação de banco novo. |
| Commit `231fc96` (Barra superior de navegação com Logout) | Breno Tales | Excelente adição de usabilidade para exibir o usuário ativo e link de logout. |
| Commit `31a8c3b` (Suíte de testes automatizados com 24 testes) | Breno Tales | Validei a execução dos 24 testes no ambiente local e aprovei a cobertura dos cenários CT01 a CT05. |

---

## 4. Dificuldades e o que aprendi

- **Gerenciamento de Sessão Flask e Decorators:** Aprendi a estruturar decorators customizados para encapsular a verificação de sessão e redirecionamento de usuários não autorizados sem duplicar código nas rotas.
- **Formatação e Validação de Código de Barras:** Compreendi a importância de tratar a unicidade e formatos de strings de código de barras para permitir integração futura com leitores físicos USB na Sprint 2.
