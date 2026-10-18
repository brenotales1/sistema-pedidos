# Relatório Individual de Contribuição — Sprint 3 — Breno Tales de Oliveira Leite (RA 2840482423029)

**Papel nesta sprint:** Desenvolvedor Backend & Frontend / Integrações de API / Banco de Dados / Qualidade e QA

---

## 1. O que fiz

| Item | PR/commit | Status |
|---|---|---|
| Implementação do modelo `HistoricoStatusPedido` e serviço de auditoria imutável de transições de status — US #7 (`models/historico_status_pedido.py`, `services/pedido_service.py`) | Commit `3941899` | Concluído / Integrado |
| Associação obrigatória de cliente na criação e edição de pedidos com validação e modal interativo — US #7 (`models/pedido.py`, `templates/pedidos/novo.html`, `controllers/pedido_controller.py`) | Commit `3941899` | Concluído / Integrado |
| Criação de rotinas de migração de banco de dados para inclusão idempotente de `cliente_id` e compatibilidade com pedidos legados (`services/database_migration_service.py`) | Commit `3941899` | Concluído / Integrado |
| Implementação do serviço de integração com a Meta WhatsApp Cloud API (Graph API v21.0), sanitização de telefone E.164 e template `pedido_finalizado` — US #8 e #9 (`services/whatsapp_service.py`) | Commit `3941899` | Concluído / Integrado |
| Criação do modelo `NotificacaoWhatsApp` para persistência de tentativas de disparo, logs de erro e identificador `wamid` — US #8 e #9 (`models/notificacao_whatsapp.py`) | Commit `3941899` | Concluído / Integrado |
| Implementação do gatilho automático de notificação no fluxo de finalização de pedidos com feedback visual ao usuário via Flask `flash` (`controllers/pedido_controller.py`) | Commit `3941899` | Concluído / Integrado |
| Criação do endpoint de Webhook com verificação de handshake token para recebimento de eventos de entrega da Meta (`app.py`) | Commit `3941899` | Concluído / Integrado |
| Estruturação das variáveis de ambiente e padronização de dependências (`.env.example`, `requirements.txt`, `.gitignore`) | Commit `3941899` | Concluído / Integrado |
| Criação de testes automatizados para validação de vínculo de cliente, migração de esquema e integridade de pedidos (`tests/test_migracao_cliente.py`, `tests/test_pedidos.py`) | Commit `3941899` | Concluído / Integrado |

---

## 2. Rituais que participei

- [x] Dailies/weeklies (alinhamentos assíncronos e planejamento técnico da Sprint 3)
- [x] Sprint Review (apresentação dos incrementos da Sprint 3 e fluxo de notificação)
- [ ] Retrospectiva da Sprint 3

---

## 3. PRs de colegas que revisei

| PR / Commit | Autor | Comentário resumido |
|---|---|---|
| Suíte de testes automatizados de notificações Meta e documentação da Sprint 3 (CT08, CT09, CT42–CT45) | Daniel Fredi | Revisei a cobertura de testes unitários e de integração (`tests/test_whatsapp.py`, `tests/test_notificacao_persistencia.py`, `tests/test_notificacao_visual.py` e `tests/test_status_pedido.py`), garantindo o isolamento das chamadas externas com mocks e SQLite em memória. |

---

## 4. Dificuldades e o que aprendi

- **Coexistência de Número de Telefone (WhatsApp Comercial vs. Cloud API):** Enfrentamos a limitação imposta pela Meta que impede a coexistência de um mesmo número no aplicativo WhatsApp (seja pessoal ou WhatsApp Business móvel) e na WhatsApp Cloud API simultaneamente. Como a empresa precisa do número para o contato e atendimento direto aos clientes e simultaneamente para os envios automatizados do sistema, identificamos que a solução ideal para produção é utilizar o número de telefone fixo da empresa cadastrado exclusivamente na Cloud API, mantendo o número móvel para a comunicação manual da equipe.
- **Restrições de Envio no Ambiente de Testes da Meta:** Durante os testes na plataforma de desenvolvedores da Meta, deparamos com o fato de que o número de teste padrão fornecido pela Meta é americano (+1), impondo restrições rígidas no envio para números brasileiros (+55), que exigem cadastro manual prévio como destinatários verificados. Isso reforçou a necessidade de validação cuidadosa do formato E.164 (`phonenumbers`) e consolidou a decisão de ativação do número fixo comercial da própria empresa na conta empresarial da Meta.
- **Webhook e Recepção de Callbacks em Ambiente Local:** O endpoint de Webhook (`/webhook/whatsapp`) foi implementado com validação de token e suporte a eventos da Graph API. Contudo, devido ao sistema estar em ambiente de desenvolvimento local (localhost) sem exposição a uma rede pública com IP fixo ou túnel com SSL válido, a Meta não consegue realizar o callback assíncrono para notificar alterações de status (entregue/lido). Aprendi sobre os requisitos de infraestrutura e segurança necessários para webhooks corporativos, suprindo essa etapa no ambiente de desenvolvimento por meio de testes automatizados e simulação com mocks.
