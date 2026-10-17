# Relatório de Entrega — Sprint 3 (E7)

**Equipe:** Breno Tales de Oliveira Leite e Daniel Fredi Soares Pereira
**Registro da validação:** 17/10/2026
**Projeto:** Sistema Web de Controle de Estoque para Empresa de Comunicação Visual

## 1. Planejado vs. entregue

| História | Planejado | Entregue | Evidência |
|---|---|---|---|
| US #7 | Selecionar atualização de pedido com cliente vinculado | Concluída: vínculo por ID, validação de status e histórico com responsável | `test_pedidos.py`, `test_migracao_cliente.py`, `test_status_pedido.py` |
| US #8 | Enviar notificação WhatsApp com feedback | Concluída no escopo automatizado: Meta Cloud API via requests, telefone validado, mensagem com pedido e finalização, flash de sucesso/erro | CT42 e CT44 |
| US #9 | Disparar mensagem automaticamente e registrar resultado | Concluída: transição efetiva para Finalizado, destinatário por ID e tentativa persistida | CT43 e CT45 |

## 2. Incremento funcional demonstrável

1. Cadastrar um cliente com telefone válido e selecionar seu cadastro no pedido.
2. Atualizar o pedido: o histórico registra status anterior/novo e usuário responsável.
3. Finalizar: o serviço usa o telefone do cliente vinculado, monta texto com número do pedido e finalização ou template Meta configurado e solicita envio após o commit.
4. A interface informa sucesso ou falha; a tabela `notificacao_whatsapp` registra evento, data/hora UTC, cliente, pedido e resultado.
5. Repetir Finalizado não reenvia. Uma nova finalização após reabertura cria outra tentativa.

Para demonstração reproduzível sem credenciais, executar os testes de integração com Flask Test Client: HTTP 200/201 e identificador wamid são simulados; HTTP 400/500 e falhas de conexão preservam a finalização e registram falha.

## 3. Validação e backlog

US #7, #8 e #9 marcadas como Concluída no [backlog](../backlog.md). Casos CT42–CT45 registrados no [plano de testes](../plano-de-testes.md). Saída integral da suíte nas [evidências](sprint-3-evidencias-teste.md).

## 4. Divisão de responsabilidades

Breno implementou vínculo obrigatório, histórico e conector Meta. Daniel adaptou os testes de notificação para requests/Meta, validou a integração com SQLite isolado e consolidou a documentação E7.

## 5. Limites e próximos passos

O aceite simulado pela API não comprova entrega no celular. O webhook existente valida o desafio e recebe eventos; não atualiza confirmação de entrega. Não há retentativa automática. Se falhar a gravação após envio, a tentativa permanece pendente e não há reenvio pela repetição do status.

O conector do Breno remove pontuação do wamid e limita o identificador a 34 caracteres antes de persistir no campo legado `message_sid`; os testes registram esse comportamento. Preservar o identificador completo exige evolução do modelo e migração. `hello_world` é template de demonstração; para uso funcional, configurar texto livre ou template aprovado com parâmetros de cliente/pedido. A tela de histórico de notificações pertence à US #10 / Sprint 4.
