# Relatório Individual de Contribuição — Sprint 3 (E7)

**Integrante:** Breno Tales de Oliveira Leite  
**RA:** 2840482423029  
**Dupla:** Daniel Fredi Soares Pereira  
**Registro:** 17/10/2026

## 1. Responsabilidades e entregas

| História | Contribuição do Breno | Situação |
|---|---|---|
| US #7 | Vínculo obrigatório do pedido com cliente por ID, formulário atualizado, validações e modelo HistoricoStatusPedido para auditar transições com usuário responsável | Concluída |
| US #8 | Conector em services/whatsapp_service.py utilizando requests e Meta WhatsApp Cloud API, validação do telefone, texto/template e tratamento de falhas | Concluída no escopo validado com API simulada |
| US #9 | Disparo após finalização efetiva, persistência de tentativas em notificacao_whatsapp e endpoint /webhook/whatsapp | Concluída no escopo implementado |

A implementação consta do commit [3941899](https://github.com/brenotales1/sistema-pedidos/commit/3941899), de autoria de Breno Leite na main. O commit reúne atualização de status com auditoria e notificações WhatsApp (US #7, #8 e #9).

## 2. Integração com o trabalho da dupla

Breno entregou a implementação funcional e os testes de pedidos/migração. Daniel adaptou os testes de notificação para Meta, validou serviço, feedback e persistência e consolidou a documentação E7. A suíte integrada registrou **93 testes aprovados**; esse total inclui o trabalho da dupla e testes de sprints anteriores.

## 3. Dificuldades técnicas e aprendizados do projeto

A integração precisou distinguir aceite da API de entrega ao destinatário, tratar texto e templates Meta e preservar o pedido finalizado diante de falha HTTP ou de rede. A persistência por transição permite rastrear a tentativa sem duplicar o envio quando Finalizado é repetido.

O webhook atual valida o desafio e recebe eventos, mas não confirma entrega no banco. Não há retentativa automática. O campo legado message_sid recebe o identificador Meta normalizado e limitado a 34 caracteres; a preservação integral do wamid fica como melhoria.

## 4. Participação e revisões

Não foram informados registros individuais de presença em reuniões ou revisões de PRs. Este relatório não atribui horas, reuniões ou aprovações sem evidência.

## 5. Evidências

- [Relatório da Sprint 3](sprint-3-relatorio.md): planejado versus entregue e incremento demonstrável.
- [Evidências dos testes](sprint-3-evidencias-teste.md): saída integral dos 93 testes aprovados.
- [Plano de testes](../plano-de-testes.md): CT42–CT45 e correspondência com CT08/CT09 de notificações.
- [Contribuição do Daniel](sprint-3-contribuicao-daniel.md): testes e documentação da entrega.

A aprovação automatizada usa mocks e SQLite isolado; não comprova entrega real no celular ou homologação de template remoto.
