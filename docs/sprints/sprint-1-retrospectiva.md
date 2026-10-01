# Ata de Retrospectiva — Sprint 1 — Sistema de Pedidos e Controle de Estoque

**Data:** 18/09/2026  
**Presentes:** Breno Tales de Oliveira Leite (RA: 2840482423029) — Daniel Fredi Soares Pereira (RA: 2840482421054)

---

## 1. Ações da retrospectiva anterior — foram aplicadas?

| Ação decidida | Aplicada? | Evidência/comentário |
|---|:---:|---|
| Definição da arquitetura base e divisão de papéis na entrega E4 | Sim | Estrutura MVC com Flask Blueprints, ORM SQLAlchemy e suíte `unittest` estabelecidas com sucesso. |

---

## 2. O que funcionou bem

- **Divisão clara de responsabilidades:** A separação entre desenvolvimento do backend/autenticação (Daniel) e engenharia de qualidade/QA/testes automatizados e refatoração (Breno) gerou alta produtividade e cobertura integral dos critérios de aceite.
- **Segurança e Isolamento por Perfis:** Os decorators `@login_required` e `@admin_required` garantiram controle de acesso elegante e robusto em todas as rotas da aplicação.
- **Suíte de Testes Ágil:** A configuração de banco de dados em memória (`sqlite:///:memory:`) para testes permitiu executar 24 testes unitários e de integração em menos de 7 segundos.

---

## 3. O que não funcionou

- **Inconsistência de Seed Inicial:** A introdução do campo obrigatório `codigo_barras` não havia sido refletida no dicionário `MATERIAIS_PADRAO`, gerando erro de banco na inicialização limpa — identificado e corrigido no PR de QA.
- **Sincronização de Branches:** Houve necessidade de alinhamento e `git pull` antes da criação da suíte de testes para consolidar as alterações de autenticação.

---

## 4. Ações para a próxima sprint

| Ação | Responsável |
|---|---|
| Implementar identificação rápida de materiais por código de barras (US #4) | Daniel Fredi |
| Implementar registro e histórico de movimentações de entrada no estoque (US #5 e US #6) | Daniel Fredi |
| Implementar testes automatizados de movimentação de estoque e validação de quantidades (CT05) | Breno Tales |
| Estruturar tabela de auditoria de movimentações no banco de dados | Breno Tales |
