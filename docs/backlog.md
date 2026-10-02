# Backlog Priorizado — Sistema Web de Controle de Estoque para Empresa de Comunicação Visual

Este documento consolida as histórias de usuário priorizadas da aplicação, seus critérios de aceite, estimativas de prazo (semana de entrega) e alocação por sprints de desenvolvimento.

---

## Tabela de Histórias de Usuário (Backlog do Produto)

| # | História de Usuário | Critérios de Aceite | Prioridade | Estimativa | Sprint Alvo | Status |
|:---:|---|---|:---:|:---:|:---:|:---:|
| **1** | Como **administrador**, quero acessar o sistema com usuário e senha, para que somente usuários autorizados utilizem o sistema. | • E-mail e senha obrigatórios<br>• Credenciais inválidas exibem erro<br>• Permissões respeitam o perfil | **Must** | Sem. 5 | **Sprint 1** | **Concluída** |
| **2** | Como **administrador**, quero cadastrar um material com código de barras, para que ele possa ser identificado no estoque. | • Código de barras único<br>• Descrição e quantidade obrigatórias<br>• Material salvo após validação | **Must** | Sem. 5 | **Sprint 1** | **Concluída** |
| **3** | Como **funcionário**, quero consultar os materiais cadastrados, para que eu saiba o que está disponível no estoque. | • Exibe descrição, código e quantidade<br>• Permite localizar um material<br>• Informa quando não encontrado | **Must** | Sem. 5 | **Sprint 1** | **Concluída** |
| **4** | Como **funcionário**, quero identificar um material pelo código de barras, para que eu não precise procurá-lo manualmente. | • Código existente identifica o material<br>• Código inexistente exibe erro<br>• Não altera o estoque se inválido | **Must** | Sem. 8 | **Sprint 2** | **Concluída** |
| **5** | Como **funcionário**, quero registrar a entrada de material pelo código de barras, para que o estoque seja atualizado automaticamente. | • Quantidade maior que zero<br>• Material cadastrado<br>• Estoque atualizado<br>• Movimentação registrada | **Must** | Sem. 8 | **Sprint 2** | **Em andamento** |
| **6** | Como **funcionário**, quero consultar as movimentações do estoque, para que eu possa acompanhar as entradas realizadas. | • Exibe material, quantidade e data<br>• Lista as movimentações realizadas | **Should** | Sem. 8 | **Sprint 2** | **Em andamento** |
| **7** | Como **funcionário**, quero selecionar uma atualização do pedido, para que o cliente seja informado sobre seu andamento. | • Pedido deve existir<br>• Cliente deve estar vinculado<br>• Atualização é registrada | **Must** | Sem. 10 | **Sprint 3** | *Planejada* |
| **8** | Como **funcionário**, quero enviar uma notificação pelo WhatsApp, para que o cliente receba a atualização do pedido. | • Número do cliente é validado<br>• Mensagem contém pedido e atualização<br>• Sistema informa sucesso ou falha | **Must** | Sem. 10 | **Sprint 3** | *Planejada* |
| **9** | Como **funcionário**, quero que determinadas atualizações do pedido enviem uma mensagem automaticamente, para que eu não precise avisar o cliente manualmente. | • Eventos definidos disparam mensagem<br>• Cliente correto é identificado<br>• Resultado do envio é registrado | **Must** | Sem. 10 | **Sprint 3** | *Planejada* |
| **10** | Como **administrador**, quero consultar as notificações enviadas, para que eu possa verificar quais clientes foram comunicados. | • Exibe cliente, pedido, data e status<br>• Diferencia envios realizados e falhos | **Should** | Sem. 12 | **Sprint 4** | *Planejada* |
| **11** | Como **administrador**, quero visualizar materiais abaixo do estoque mínimo, para que eu possa identificar itens que precisam de reposição. | • Lista materiais abaixo do mínimo<br>• Exibe quantidade atual e mínima | **Should** | Sem. 12 | **Sprint 4** | *Planejada* |
| **12** | Como **administrador**, quero visualizar um painel de pedidos e estoque, para que eu acompanhe a situação da empresa. | • Exibe pedidos por status<br>• Exibe materiais abaixo do mínimo<br>• Dados vêm do banco de dados | **Could** | Sem. 12 | **Sprint 4** | *Planejada* |

---

## Distribuição por Sprint

### Sprint 1: Fundação & Acessos (✅ Concluída — Sem. 5)
- **#1** Acessar o sistema com usuário e senha (Sem. 5) — Concluído
- **#2** Cadastrar material com código de barras (Sem. 5) — Concluído
- **#3** Consultar materiais cadastrados (Sem. 5) — Concluído

### Sprint 2: Entrada e Movimentação por Código de Barras (🔄 Em andamento — Sem. 8)
- **#4** Identificar material pelo código de barras (Sem. 8) — Concluído
- **#5** Registrar entrada de material pelo código de barras (Sem. 8) — Em andamento
- **#6** Consultar movimentações do estoque (Sem. 8) — Em andamento

### Sprint 3: Notificações & Automação WhatsApp (⏳ Planejada — Sem. 10)
- **#7** Selecionar atualização do pedido (Sem. 10)
- **#8** Enviar notificação pelo WhatsApp (Sem. 10)
- **#9** Envio automático de notificação por evento do pedido (Sem. 10)

### Sprint 4: Relatórios, Histórico e Dashboard (⏳ Planejada — Sem. 12)
- **#10** Consultar histórico de notificações enviadas (Sem. 12)
- **#11** Visualizar materiais abaixo do estoque mínimo (Sem. 12)
- **#12** Painel consolidado de pedidos e estoque (Sem. 12)
