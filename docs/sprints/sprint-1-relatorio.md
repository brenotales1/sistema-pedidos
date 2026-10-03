# Relatório de Entrega — Sprint 1 — Sistema de Pedidos e Controle de Estoque

**Período:** 04/09/2026 a 18/09/2026 (Semana 5 — Entrega E5)  
**Sprint Review:** 18/09/2026 
**Equipe:** Breno Tales de Oliveira Leite (RA: 2840482423029) — Daniel Fredi Soares Pereira (RA: 2840482421054) · Laboratório de Engenharia de Software · ADS Fatec Ribeirão Preto

---

## 1. Planejado vs. entregue

| História (E2) | Planejada para esta sprint? | Entregue? | Observação |
|---|:---:|:---:|---|
| **#1 Acessar o sistema com usuário e senha** | Sim | Sim | Autenticação com sessão segura (`werkzeug.security`), perfis `admin` e `funcionario`, e decorators `@login_required` e `@admin_required`. |
| **#2 Cadastrar material com código de barras** | Sim | Sim | Cadastro com validação de unicidade de `codigo_barras`, largura em metros e inicialização de bobinas de 50m. |
| **#3 Consultar materiais cadastrados** | Sim | Sim | Consulta de estoque categorizada com busca em tempo real por nome do material e código de barras. |

---

## 2. Incremento funcional demonstrável

1. **Autenticação & Controle de Acesso Baseado em Perfis (RBAC):**
   - Tela de login `/login` com feedback visual de credenciais inválidas.
   - Perfil Administrador (`admin`): acesso completo a gestão de materiais, categorias, pedidos e clientes.
   - Perfil Funcionário (`funcionario`): acesso operacional, com bloqueio automático de rotas administrativas.
   - Encerramento de sessão `/logout` com limpeza completa de cookies de sessão.
   - Barra superior no `base.html` exibindo usuário autenticado, badge de perfil e botão de Logout.

2. **Gestão de Materiais com Código de Barras Único:**
   - Modelo `Material` com restrição de unicidade em `codigo_barras`.
   - Prevenção de duplicidade tanto a nível de banco de dados quanto a nível de aplicação/formulário.
   - Seed inicial de materiais devidamente configurado com códigos de barras padrão EAN.

3. **Consulta e Filtro de Estoque:**
   - Tela `/estoque` exibindo bobinas, metragem disponível e largura formatada por categoria.
   - Campo de pesquisa que filtra simultaneamente por nome do material e por código de barras.

**Como reproduzir localmente:**
Consulte o guia passo a passo presente no [`README.md`](file:///c:/Users/breno/OneDrive/Documentos/Projetos/Projeto-TCC/README.md) na raiz do repositório.

---

## 3. Backlog atualizado

Ao fim da Sprint 1, os cards no quadro do projeto foram atualizados:
- **US #1** (Acesso com usuário e senha) ➔ **Concluído**
- **US #2** (Cadastrar material com código de barras) ➔ **Concluído**
- **US #3** (Consultar materiais cadastrados) ➔ **Concluído**
- **Total entregue na Sprint 1:** 100% da meta da Sprint 1 (3 histórias entregues)

**Histórias planejadas para a Sprint 2 (E6):**
- **US #4** — Identificar material pelo código de barras
- **US #5** — Registrar entrada de material pelo código de barras
- **US #6** — Consultar movimentações do estoque

---

## 4. Evidências de teste

Foram desenvolvidos **24 testes automatizados** utilizando `unittest` e Flask Test Client:
- **Testes Unitários:** Validação de hashing de senhas, conversão de medidas, algoritmo de cálculo de melhor aproveitamento com rotação e regras de consumo/devolução de bobinas.
- **Testes de Integração:** Casos de teste formais **CT01** (login inválido), **CT02** (controle de acesso restrito de funcionário), **CT03** (bloqueio de código de barras duplicado), **CT04** (busca de material inexistente) e **CT05** (movimentação de bobinas).

**Resultado da execução:** 24 testes executados, 24 aprovados (100% de sucesso).  
Relatório detalhado disponível em: [`docs/sprints/sprint-1-evidencias-teste.md`](file:///c:/Users/breno/OneDrive/Documentos/Projetos/Projeto-TCC/docs/sprints/sprint-1-evidencias-teste.md).

---

## 5. Retrospectiva e contribuição individual

- **Ata de Retrospectiva:** [`docs/sprints/sprint-1-retrospectiva.md`](file:///c:/Users/breno/OneDrive/Documentos/Projetos/Projeto-TCC/docs/sprints/sprint-1-retrospectiva.md)
- **Relatório Individual — Breno Tales de Oliveira Leite (RA 2840482423029):** [`docs/sprints/sprint-1-contribuicao-breno.md`](file:///c:/Users/breno/OneDrive/Documentos/Projetos/Projeto-TCC/docs/sprints/sprint-1-contribuicao-breno.md)
- **Relatório Individual — Daniel Fredi Soares Pereira (RA 2840482421054):** [`docs/sprints/sprint-1-contribuicao-daniel.md`](file:///c:/Users/breno/OneDrive/Documentos/Projetos/Projeto-TCC/docs/sprints/sprint-1-contribuicao-daniel.md)

---

## 6. Riscos/impedimentos para a próxima sprint

- **Entrada rápida por Leitor de Código de Barras (US #4 e #5):** Garantir que a tela de movimentação receba o input do leitor USB com submit automático ou foco contínuo no campo, minimizando a necessidade de interação com o mouse na bancada de trabalho. A equipe já alinhou a arquitetura do endpoint de leitura para o início da Sprint 2.
