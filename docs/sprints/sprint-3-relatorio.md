# Relatório de Entrega — Sprint 3 — Sistema de Pedidos e Controle de Estoque

**Entrega:** E7 — Semana 10  
**Consolidação técnica:** 18/10/2026  
**Equipe:** Breno Tales de Oliveira Leite (RA: 2840482423029) — Daniel Fredi Soares Pereira (RA: 2840482421054) · Laboratório de Engenharia de Software · ADS Fatec Ribeirão Preto

## 1. Planejado vs. entregue

| História | Planejada? | Entregue? | Incremento e evidência |
|---|:---:|:---:|---|
| #7 Selecionar uma atualização do pedido | Sim | Sim | Cliente obrigatório no cadastro; edição de legado com vínculo explícito; transições auditadas em `HistoricoStatusPedido`. Regressão em `test_pedidos.py` e `test_migracao_cliente.py`. |
| #8 Enviar uma notificação pelo WhatsApp | Sim | Sim | Conector via `requests` para Meta Cloud API; telefone validado, texto ou template, retorno de aceite/falha e feedback flash. CT42–CT44. |
| #9 Envio automático por evento do pedido | Sim | Sim | Transição para `Finalizado` cria tentativa vinculada ao histórico, chama o conector e persiste o resultado. Repetir o mesmo status não reenvia. CT45. |

**Meta técnica entregue:** 3 histórias concluídas, com testes automatizados de contrato HTTP, interface e persistência. Breno implementou os fluxos e o conector; Daniel acrescentou 21 testes e a documentação da E7.

## 2. Incremento funcional demonstrável

1. Autenticar um funcionário, cadastrar ou selecionar um cliente e associá-lo a um pedido.
2. Alterar o status do pedido: a aplicação registra usuário responsável, status anterior e novo status.
3. Na transição para `Finalizado`, criar uma tentativa em `notificacao_whatsapp` e solicitar o envio ao telefone do cliente.
4. Para HTTP 200/201 simulado, registrar `aceito` e mostrar sucesso; para HTTP 400/500 ou erro de rede, registrar `falha`, avisar o operador e preservar o pedido finalizado.
5. Para telefone inválido/ausente, impedir a chamada HTTP, registrar `sem_destinatario` e orientar a correção do cadastro.
6. Com `TESTING=True`, registrar `bloqueado_testing` sem chamada externa.

**Demonstração segura:** executar os testes indicados nas [evidências](sprint-3-evidencias-teste.md). As simulações usam dados e credenciais fictícios, banco SQLite em memória e barreira adicional contra acesso HTTP real.

## 3. Backlog atualizado

As US #7, #8 e #9 estão marcadas como **Concluída** no [backlog](../backlog.md). A consulta administrativa do histórico de notificações (US #10 / CT46) permanece prevista para a Sprint 4.

## 4. Evidências de teste

A suíte passou de 47 para **68 testes**, com **68 aprovados (100%)**. Foram adicionados 9 testes do conector, 6 de feedback visual e 6 de persistência. Os subcenários HTTP/telefone são exercitados com `subTest`.

Comando: `python -B -m unittest discover -s tests -q`, usando o Python do ambiente `.venv`. O [log integral](sprint-3-evidencias-teste.md) contém o resumo, os avisos de depreciação existentes e os eventos simulados de erro esperados.

## 5. Retrospectiva e contribuição individual

- [Retrospectiva técnica](sprint-3-retrospectiva.md)
- [Contribuição de Daniel Fredi](sprint-3-contribuicao-daniel.md)

## 6. Limites e próximos passos

O resultado `aceito` representa a aceitação da requisição pela Meta. O webhook atual valida a assinatura de inscrição por token e recebe eventos, mas não atualiza a confirmação de entrega no banco; `entrega_confirmada` permanece falsa. A validação automatizada não comprova entrega em aparelho real.

O conector atual sanitiza e limita o identificador Meta a 34 caracteres. Preservar o `wamid` integral e correlacionar callbacks são melhorias para a evolução do histórico. A prevenção de duplicidade cobre repetição do status; uma nova transição de reabertura e finalização gera outra tentativa.
