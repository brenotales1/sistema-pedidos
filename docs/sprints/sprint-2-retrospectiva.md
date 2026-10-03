# Ata de Retrospectiva — Sprint 2 — Sistema de Pedidos e Controle de Estoque

**Data:** 02/10/2026  
**Presentes:** Breno Tales de Oliveira Leite (RA: 2840482423029) — Daniel Fredi Soares Pereira (RA: 2840482421054)

---

## 1. Ações da retrospectiva anterior — foram aplicadas?

| Ação decidida | Aplicada? | Evidência/comentário |
|---|:---:|---|
| Implementar identificação rápida de materiais por código de barras (US #4) | Sim | Endpoint REST `/estoque/api/material/codigo/<codigo_barras>` e card interativo com suporte a leitor USB entregues com sucesso. |
| Implementar registro e histórico de movimentações de entrada no estoque (US #5 e US #6) | Sim | Rota `/estoque/entrada`, tela `/estoque/movimentacoes` e persistência automática de movimentações implementadas. |
| Implementar testes automatizados de movimentação de estoque e validação de quantidades (CT05 e CT07) | Sim | Testes automatizados cobrindo CT05, CT06 e CT07 desenvolvidos elevando a suíte para 41 testes com 100% de sucesso. |
| Estruturar tabela de auditoria de movimentações no banco de dados | Sim | Modelo `MovimentacaoEstoque` mapeado no banco com relacionamentos e histórico imutável. |

---
Para otimizar o fluxo de entrega, Breno assumiu o fluxo de entrada e identificação por leitor (US #4 e #5), enquanto Daniel focou no relatório de movimentações (US #6), infraestrutura de testes e documentação.
## 2. O que funcionou bem

- **Agilidade na Entrada de Estoque:** A integração com o leitor de código de barras USB permitiu a identificação instantânea do material sem necessidade de digitação ou busca manual.
- **Rastreabilidade Completa:** Todas as entradas realizadas agora geram registros detalhados com data/hora, quantidade de bobinas, metragem e motivo.
- **Qualidade Assegurada com 41 Testes:** A suíte de testes unitários e de integração expandiu de 24 para 41 testes, cobrindo todos os cenários críticos (CT01 a CT07) com isolamento total de banco.
- **Experiência do Usuário (RBAC UI):** A interface do funcionário foi ajustada para exibir apenas as ações operacionais pertinentes, ocultando controles administrativos desnecessários.

---

## 3. O que não funcionou

- **Concorrência com Banco de Testes Inicial:** No início da sprint, alguns testes compartilhavam o banco de desenvolvimento local gerando bloqueio temporário do SQLite — resolvido com a refatoração do `database_test.db` isolado.
- **Ajuste Fino de Layout em Telas Menores:** Foi necessário ajustar o espaçamento do painel de movimentações para evitar quebras visuais em telas com resolução menor.

---

## 4. Ações para a próxima sprint

| Ação | Responsável |
|---|---|
| Implementar seleção de atualização de status do pedido para disparo de avisos (US #7) | Breno Tales |
| Implementar envio de notificação via WhatsApp para clientes (US #8) | Breno Tales e Daniel Fredi |
| Implementar disparos automáticos de mensagens em eventos de mudança de status (US #9) | Breno Tales e Daniel Fredi |
| Desenvolver casos de teste automatizados para o módulo de notificações (CT08 e CT09) | Daniel Fredi |