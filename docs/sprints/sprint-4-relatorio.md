# Relatório de Entrega — Sprint 4 — Sistema de Pedidos e Controle de Estoque

**Entrega:** E8 — Semana 12 (Entrega Final do MVP)  
**Consolidação técnica:** 10/11/2026  
**Equipe:** Breno Tales de Oliveira Leite (RA: 2840482423029) — Daniel Fredi Soares Pereira (RA: 2840482421054) · Laboratório de Engenharia de Software · ADS Fatec Ribeirão Preto

---

## 1. Planejado vs. entregue

| História | Planejada? | Entregue? | Incremento e evidência |
|---|:---:|:---:|---|
| **#6 Histórico de movimentações (complementos)** | Sim | Sim | Registro atômico de saídas de pedidos, estornos em edições, devoluções em cancelamentos e operações manuais (adição, remoção e ajustes com saldo anterior/posterior). Bloqueio de exclusão para materiais com movimentações. CT47–CT49. |
| **#10 Histórico de notificações (CT46)** | Sim | Sim | Tela administrativa `/notificacoes` com listagem das tentativas de envio pelo WhatsApp, dados de cliente, pedido, data/hora em UTC, status de envio, paginação de 25 itens e filtro por status. CT46. |
| **#11 Visualização de estoque mínimo** | Sim | Sim | Configuração de estoque mínimo por material em metros pelo administrador, bloqueio a funcionários, alerta estrito (`saldo < minimo`) e filtro de busca `?abaixo_minimo=1`. CT50. |
| **Cancelamento condicional de pedidos** | Sim | Sim | Permitido em "Pagamento pendente" e "Aguardando produção" (estorno de metragem ao saldo); bloqueio estrito em "Pronto para retirada" e "Finalizado", inclusive por requisição direta. CT51. |
| **Regularização de códigos de barras antigos** | Sim | Sim | Cadastro e correção de códigos de barras na tela de estoque pelo administrador, com validações de duplicidade e formato, preservando histórico de bobinas e movimentações. CT52. |
| **Inicialização segura de estoque** | Sim | Sim | Reinicialização (`seed_materials`) preserva materiais esgotados (saldo zero) e saldos parciais; não executa consolidação automática. CT53. |

**Meta técnica entregue:** 100% dos requisitos Must Have e Should Have do escopo do MVP implementados e cobertos por testes automatizados. Daniel Fredi implementou as funcionalidades, rotas, telas e migrações nos commits `695791c` (07/11/2026) e `652bd8f` (09/11/2026); Breno Tales desenvolveu os 43 testes automatizados de validação (CT46–CT53), executou a suíte completa de 111 testes (100% aprovados sem regressões) e consolidou a documentação de encerramento do MVP.

---

## 2. Incremento funcional demonstrável

1. **Gestão de Limite e Alerta de Estoque Mínimo (US #11):** Administradores definem o limite mínimo de metragem. O sistema alerta visualmente na tabela de estoque os itens estritamente abaixo do mínimo e permite filtrar com um clique apenas os itens que necessitam de reposição.
2. **Histórico Completo de Notificações WhatsApp (US #10 / CT46):** Tela restrita a administradores que consolida as tentativas de envio disparadas pela Meta Cloud API, indicando data, destinatário, status do envio (aceito, falha, sem destinatário) e paginação.
3. **Auditoria Rigorosa de Movimentações (US #6):** Cada pedido gerado, editado ou cancelado gera automaticamente sua respectiva movimentação (`saida` ou `entrada` de estorno). Alterações manuais pelo administrador gravam o usuário, a metragem movimentada e, no caso de ajuste, o saldo anterior e posterior.
4. **Cancelamento Seguro:** O sistema impede o cancelamento de pedidos cujo material já foi consumido na produção ("Pronto para retirada" e "Finalizado"), protegendo o estoque de devoluções inconsistentes.
5. **Regularização de Códigos de Barras:** Materiais antigos podem ter seus códigos cadastrados e corrigidos a qualquer momento pelo administrador, permitindo leitura via leitor físico USB HID e busca imediata.

---

## 3. Backlog atualizado

Todas as histórias obrigatórias (Must Have) e de alto valor (Should Have) foram marcadas como **Concluída** no [backlog](../backlog.md):
- US #1, #2, #3, #4, #5, #6, #7, #8, #9, #10 e #11 finalizadas com sucesso.
- A US #12 (Dashboard consolidado) foi mantida como prioridade *Could* para versões pós-MVP, conforme previsto no termo de abertura e declaração de escopo.

---

## 4. Evidências de teste

A suíte completa atingiu **111 testes automatizados**, todos aprovados com isolamento de banco de dados e simulação controlada de integrações externas:
- Comando de execução: `python -B -m unittest discover -s tests -v`
- O detalhamento completo da execução e o log integral constam em [Evidências da Sprint 4](sprint-4-evidencias-teste.md).

---

## 5. Retrospectiva e contribuição individual

- [Ata de Retrospectiva da Sprint 4](sprint-4-retrospectiva.md)
- [Relatório de Contribuição de Breno Tales](sprint-4-contribuicao-breno.md)
- [Relatório de Contribuição de Daniel Fredi](sprint-4-contribuicao-daniel.md)

---

## 6. Situação de Entrega e Aceite do MVP

O sistema encontra-se tecnicamente pronto, testado e estável. Para a operação física final, resta apenas o preenchimento operacional dos códigos físicos de barras dos materiais antigos no banco de produção pela interface administrativa e a vinculação da URL de produção com certificado SSL no painel Meta Business.
