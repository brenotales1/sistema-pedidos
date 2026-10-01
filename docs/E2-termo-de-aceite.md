# Termo de Aceite do Projeto — Sistema Web de Controle de Estoque para Empresa de Comunicação Visual

**Equipe:** Daniel Fredi Soares Pereira (RA 2840482421054), Breno Tales de Oliveira Leite (RA 2840482423029)  
**Trilha:** A1 (Breno Tales de Oliveira Leite é o dono do produto, vinculado ao TCC)  
**Data:** 28/08/2026  

---

## 1. Escopo aceito para o semestre (funcionalidades Must + Should)

1. Autenticação de usuários com perfis distintos e permissões diferentes.
2. Cadastro de materiais com código de barras.
3. Consulta de materiais cadastrados no estoque.
4. Identificação de materiais por código de barras.
5. Registro de entrada de materiais utilizando código de barras.
6. Consulta do histórico de movimentações do estoque.
7. Registro de atualizações no andamento dos pedidos.
8. Envio de notificações aos clientes pelo WhatsApp.
9. Envio automático de notificações após determinados eventos do pedido.
10. Consulta do histórico de notificações enviadas.
11. Visualização de materiais abaixo do estoque mínimo.

---

## 2. Critérios de pronto do MVP (Definition of Done)

- [ ] Administrador e funcionário conseguem acessar o sistema com perfis e permissões diferentes.
- [ ] Fluxo de entrada de estoque funciona de ponta a ponta: código de barras → identificação do material → quantidade → atualização do estoque → registro da movimentação.
- [ ] Sistema identifica códigos de barras cadastrados e informa erro para códigos inexistentes.
- [ ] Fluxo de notificação funciona de ponta a ponta: atualização do pedido → identificação do cliente → envio pelo WhatsApp → registro do resultado.
- [ ] Sistema registra as notificações realizadas e diferencia envios realizados e falhos.
- [ ] Sistema identifica materiais abaixo do estoque mínimo.
- [ ] Novas funcionalidades possuem testes e evidências de execução.
- [ ] Código das funcionalidades desenvolvidas está versionado no repositório Git.

---

## 3. Stack tecnológica definida

| Camada | Tecnologia |
|---|---|
| **Frontend** | HTML, CSS e JavaScript |
| **Backend** | Python + Flask |
| **Banco de dados** | SQLite + SQLAlchemy |
| **Deploy** | [a definir — previsto para Sprint 4] |

---

## 4. Papéis iniciais da equipe (Sprint 1)

| Integrante | Papel |
|---|---|
| **Breno Tales de Oliveira Leite** | Product Owner / Dono do Produto |
| **Daniel Fredi Soares Pereira** | Desenvolvedor |
