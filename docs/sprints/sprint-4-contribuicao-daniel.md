# Relatório Individual de Contribuição — Sprint 4 — Daniel Fredi Soares Pereira (RA 2840482421054)

**Papel nesta sprint:** Desenvolvedor Backend & Frontend / Integrações de Regras de Negócio e Correções do MVP  
**Consolidação:** 10/11/2026

---

## 1. O que fiz

| Item / Funcionalidade | Commit / Data | Módulos Afetados | Situação |
|---|:---:|---|:---:|
| **Histórico de Notificações (US #10):** Implementação da tela `/notificacoes`, exclusiva para administradores, exibindo cliente, link do pedido, data/hora em UTC e status do envio (aceito, falha, pendente, bloqueado). Inclui paginação de 25 registros ordenados decrescentemente e filtro por resultado. | Commit `695791c`<br>(07/11/2026) | `controllers/notificacao_controller.py`, `templates/notificacoes/historico.html` | Concluído / Integrado |
| **Sanitização de Logs e Segurança:** Remoção de número de telefone e conteúdo de payloads dos logs da API Meta; aprimoramento no tratamento de falhas ao salvar resultados de notificação e respostas inválidas da API. | Commit `695791c`<br>(07/11/2026) | `services/whatsapp_service.py`, `controllers/pedido_controller.py` | Concluído / Integrado |
| **Validações e Correções de Interface:** Reforço na validação de clientes, medidas de pedidos e metragem de estoque; proteção contra injeção/interpretação de texto como HTML na consulta de código de barras; ajuste do evento Enter no leitor de código de barras para focar no campo de quantidade antes da submissão. | Commit `695791c`<br>(07/11/2026) | `templates/estoque/lista.html`, `controllers/pedido_controller.py` | Concluído / Integrado |
| **Estoque Mínimo (US #11):** Implementação do limite mínimo por material em metros, configurável pelo administrador no cadastro e listagem; destaque visual e filtro dedicado `?abaixo_minimo=1` para saldos estritamente menores que o mínimo. | Commit `652bd8f`<br>(09/11/2026) | `models/material.py`, `controllers/estoque_controller.py`, `templates/estoque/lista.html` | Concluído / Integrado |
| **Migração de Banco de Dados:** Criação da migração DDL idempotente para acrescentar a coluna `estoque_minimo` com valor padrão zero, preservando integralmente os saldos existentes. | Commit `652bd8f`<br>(09/11/2026) | `services/database_migration_service.py` | Concluído / Integrado |
| **Histórico de Movimentações (US #6):** Ampliação da rastreabilidade para cobrir estoque inicial no cadastro, adição e remoção manual de bobinas, ajustes de metragem com saldo anterior e posterior, consumo de pedidos e estornos em edições e cancelamentos, associando usuário e motivo. | Commit `652bd8f`<br>(09/11/2026) | `services/estoque_service.py`, `controllers/pedido_controller.py`, `controllers/estoque_controller.py` | Concluído / Integrado |
| **Proteção de Dados e Regras de Cancelamento:** Bloqueio da exclusão de materiais que possuem histórico de movimentações; bloqueio do cancelamento de pedidos com status "Pronto para retirada" ou "Finalizado" (inclusive via requisição direta), impedindo retorno indevido de material já utilizado ao estoque. | Commit `652bd8f`<br>(09/11/2026) | `controllers/pedido_controller.py`, `controllers/estoque_controller.py`, `templates/pedidos/novo.html` | Concluído / Integrado |
| **Regularização de Códigos de Barras Antigos:** Interface e rota para o administrador cadastrar ou corrigir códigos de barras pela listagem de estoque, com validação de unicidade e formato sem alterar saldo ou histórico. | Commit `652bd8f`<br>(09/11/2026) | `controllers/estoque_controller.py`, `templates/estoque/lista.html` | Concluído / Integrado |
| **Correções de Inicialização de Estoque:** Ajuste no seed para não repor automaticamente bobinas em materiais esgotados (saldo zero permanece zero); retirada da consolidação automática ao iniciar e distinção por largura em materiais com mesmo nome/categoria. | Commit `652bd8f`<br>(09/11/2026) | `services/material_service.py` | Concluído / Integrado |

*Nota sobre testes:* Os commits `695791c` e `652bd8f` concentraram-se na implementação funcional, rotas, migração de dados e interfaces, não incluindo testes automatizados nesta etapa.

---

## 2. Rituais que participei

- [x] Dailies/weeklies (alinhamentos de desenvolvimento e planejamento de correções do MVP)
- [x] Sprint Review (apresentação dos incrementos de estoque mínimo e tela de notificações)
- [x] Retrospectiva da Sprint 4 (fechamento dos requisitos da Sprint Final)

---

## 3. Integração com o trabalho de Breno

Todo o código funcional, rotas e regras de negócio desenvolvidos nos commits `695791c` e `652bd8f` foram entregues para a esteira de Qualidade e Testes sob responsabilidade de Breno:
- Breno elaborou a suíte completa de **43 novos testes automatizados**, cobrindo minuciosamente cada regra implementada (CT46 a CT53);
- A validação automatizada de Breno confirmou o correto funcionamento das rotas, transações atômicas com rollback, integridade de dados e ausência total de regressões na aplicação.

---

## 4. Aprendizados e limites

- **Atomicidade em Movimentações:** Ao registrar as movimentações manuais e de ciclo de vida dos pedidos na mesma transação da alteração de estoque, eliminou-se o risco de divergência entre o saldo físico e o histórico contábil.
- **Segurança de Dados e LGPD:** A sanitização dos logs de envio do WhatsApp assegura que dados sensíveis dos clientes (como telefones completos) não fiquem expostos no servidor.
- **Limitação Operacional:** Embora o sistema forneça o recurso administrativo para correção e cadastro de códigos de barras com validação, o preenchimento dos códigos das bobinas físicas antigas da empresa permanece como atividade operacional de implantação.
