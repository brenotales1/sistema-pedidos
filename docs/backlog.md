# Backlog Priorizado — Sistema Web de Controle de Estoque para Empresa de Comunicação Visual

Este documento consolida as histórias de usuário priorizadas da aplicação, seus critérios de aceite, estimativas de esforço (em *story points*) e alocação por sprints de desenvolvimento.

---

## Tabela de Histórias de Usuário (Backlog do Produto)

| # | História de Usuário | Critérios de Aceite | Prioridade | Estimativa | Sprint Alvo |
|---|---|---|:---:|:---:|:---:|
| **1** | Como **administrador**, quero acessar o sistema com usuário e senha, para que somente usuários autorizados utilizem o sistema. | • E-mail e senha obrigatórios<br>• Credenciais inválidas exibem erro<br>• Permissões respeitam o perfil | **Must** | 3 pts | **Sprint 1** |
| **2** | Como **administrador**, quero cadastrar um material com código de barras, para que ele possa ser identificado no estoque. | • Código de barras único<br>• Descrição e quantidade obrigatórias<br>• Material salvo após validação | **Must** | 3 pts | **Sprint 1** |
| **3** | Como **funcionário**, quero consultar os materiais cadastrados, para que eu saiba o que está disponível no estoque. | • Exibe descrição, código e quantidade<br>• Permite localizar um material<br>• Informa quando não encontrado | **Must** | 3 pts | **Sprint 1** |
| **4** | Como **funcionário**, quero identificar um material pelo código de barras, para que eu não precise procurá-lo manualmente. | • Código existente identifica o material<br>• Código inexistente exibe erro<br>• Não altera o estoque se inválido | **Must** | 5 pts | **Sprint 2** |
| **5** | Como **funcionário**, quero registrar a entrada de material pelo código de barras, para que o estoque seja atualizado automaticamente. | • Quantidade maior que zero<br>• Material cadastrado<br>• Estoque atualizado<br>• Movimentação registrada | **Must** | 5 pts | **Sprint 2** |
| **6** | Como **funcionário**, quero consultar as movimentações do estoque, para que eu possa acompanhar as entradas realizadas. | • Exibe material, quantidade e data<br>• Lista as movimentações realizadas | **Should** | 3 pts | **Sprint 2** |
| **7** | Como **funcionário**, quero selecionar uma atualização do pedido, para que o cliente seja informado sobre seu andamento. | • Pedido deve existir<br>• Cliente deve estar vinculado<br>• Atualização é registrada | **Must** | 3 pts | **Sprint 3** |
| **8** | Como **funcionário**, quero enviar uma notificação pelo WhatsApp, para que o cliente receba a atualização do pedido. | • Número do cliente é validado<br>• Mensagem contém pedido e atualização<br>• Sistema informa sucesso ou falha | **Must** | 5 pts | **Sprint 3** |
| **9** | Como **funcionário**, quero que determinadas atualizações do pedido enviem uma mensagem automaticamente, para que eu não precise avisar o cliente manualmente. | • Eventos definidos disparam mensagem<br>• Cliente correto é identificado<br>• Resultado do envio é registrado | **Must** | 8 pts | **Sprint 3** |
| **10** | Como **administrador**, quero consultar as notificações enviadas, para que eu possa verificar quais clientes foram comunicados. | • Exibe cliente, pedido, data e status<br>• Diferencia envios realizados e falhos | **Should** | 3 pts | **Sprint 4** |
| **11** | Como **administrador**, quero visualizar materiais abaixo do estoque mínimo, para que eu possa identificar itens que precisam de reposição. | • Lista materiais abaixo do mínimo<br>• Exibe quantidade atual e mínima | **Should** | 5 pts | **Sprint 4** |
| **12** | Como **administrador**, quero visualizar um painel de pedidos e estoque, para que eu acompanhe a situação da empresa. | • Exibe pedidos por status<br>• Exibe materiais abaixo do mínimo<br>• Dados vêm do banco de dados | **Could** | 5 pts | **Sprint 4** |

---

## Distribuição por Sprint

### Sprint 1: Fundação & Acessos
- **#1** Acessar o sistema com usuário e senha (3 pts)
- **#2** Cadastrar material com código de barras (3 pts)
- **#3** Consultar materiais cadastrados (3 pts)
- **Total Sprint 1:** 9 pts

### Sprint 2: Entrada e Movimentação por Código de Barras
- **#4** Identificar material pelo código de barras (5 pts)
- **#5** Registrar entrada de material pelo código de barras (5 pts)
- **#6** Consultar movimentações do estoque (3 pts)
- **Total Sprint 2:** 13 pts

### Sprint 3: Notificações & Automação WhatsApp
- **#7** Selecionar atualização do pedido (3 pts)
- **#8** Enviar notificação pelo WhatsApp (5 pts)
- **#9** Envio automático de notificação por evento do pedido (8 pts)
- **Total Sprint 3:** 16 pts

### Sprint 4: Relatórios, Histórico e Dashboard
- **#10** Consultar histórico de notificações enviadas (3 pts)
- **#11** Visualizar materiais abaixo do estoque mínimo (5 pts)
- **#12** Painel consolidado de pedidos e estoque (5 pts)
- **Total Sprint 4:** 13 pts

---

**Total Geral do Backlog:** 50 Story Points
