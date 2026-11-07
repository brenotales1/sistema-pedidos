# Revisao dos requisitos obrigatorios e criterios de aceite do MVP

Data: 07/11/2026.

Referencias: [backlog vigente](../backlog.md), [termo de aceite](../termo-de-aceite.md), [evidencias da Sprint 3](sprint-3-evidencias-teste.md).

## Requisitos Must Have

Atendido tecnicamente significa implementacao identificada e evidencia automatizada existente; nao equivale a homologacao em producao.

| US | Criterios revisados | Resultado e evidencia |
|---|---|---|
| #1 | E-mail e senha obrigatorios; erro para credenciais invalidas; permissoes por perfil | Atendido tecnicamente. Rotas de autenticacao e decoradores de acesso; testes em `tests/test_auth.py`. |
| #2 | Codigo unico; descricao e quantidade obrigatorias; persistencia apos validacao | Atendido tecnicamente para novos cadastros. Validacao em `novo_estoque`, unicidade no modelo e testes de cadastro em `tests/test_estoque.py`. Materiais legados do banco local ainda possuem codigo ausente. |
| #3 | Exibir descricao, codigo e quantidade; localizar material; informar ausencia | Atendido tecnicamente. Lista e busca de estoque; testes de consulta em `tests/test_estoque.py`. A disponibilidade de codigos depende do preenchimento dos cadastros legados. |
| #4 | Identificar codigo existente; erro para inexistente; consulta sem alterar saldo | Atendido tecnicamente. API de consulta e testes existentes. Usuario confirmou identificacao manual com `7891234567890`; informou erro para codigos nao cadastrados. Leitor USB HID nao validado. |
| #5 | Quantidade positiva; material cadastrado; atualizar saldo; registrar movimentacao | Atendido tecnicamente. Rota de entrada e servico de movimentacao; testes existentes de sucesso e rejeicao. Usuario confirmou o fluxo manual nesta sessao, sem captura de tela anexada. |
| #7 | Pedido existente; cliente vinculado; atualizacao registrada | Atendido tecnicamente. Transicao de status com validacao de cliente e usuario e historico persistente; testes de pedidos e persistencia de notificacoes. |
| #8 | Validar telefone; mensagem com pedido e atualizacao; informar sucesso ou falha | Atendido tecnicamente no fluxo de finalizacao e texto livre, com API simulada nos testes. Templates personalizados dependem do conteudo aprovado na Meta; `hello_world` nao comprova o criterio de mensagem com pedido e atualizacao. Envio real e recebimento nao comprovados nesta revisao. |
| #9 | Evento dispara envio; destinatario correto; resultado registrado | Atendido tecnicamente para o evento de transicao para Finalizado. Testes CT43/CT45 cobrem resultado, destinatario e prevencao de reenvio na repeticao do mesmo status. Homologacao real do WhatsApp pendente. |

## Criterios de pronto do termo de aceite

O termo abrange Must e Should. Portanto, a implementacao dos Must nao encerra, por si so, o MVP acordado.

| Criterio | Situacao |
|---|---|
| Acesso com perfis e permissoes distintas | Evidencia automatizada existente. |
| Entrada completa por codigo, quantidade, saldo e movimentacao | Evidencia automatizada existente e confirmacao manual do usuario nesta sessao. |
| Identificacao de codigo cadastrado e erro para inexistente | Evidencia automatizada existente e confirmacao manual do usuario. |
| Notificacao do pedido ao WhatsApp com registro do resultado | Implementada e verificada com mocks; envio real e recebimento pendentes. Aceite da API nao confirma entrega. |
| Registro de notificacoes e diferenciacao de sucesso/falha | Persistencia coberta na Sprint 3; nova consulta administrativa US #10 aguarda testes pela pessoa responsavel. |
| Identificacao de materiais abaixo do minimo | Pendente: US #11 planejada; nao identificado suporte a estoque minimo nos modelos e controladores atuais. |
| Testes e evidencias das novas funcionalidades | Parcial: suite existente com 68 testes aprovados na etapa anterior desta sessao; novos ajustes e US #10 aguardam validacao formal por outra pessoa. Nenhum novo teste foi criado nesta revisao. |
| Codigo versionado no Git | Parcial: ha alteracoes locais e novos arquivos ainda nao commitados. |

## Pendencias para aceite final

- Preencher os codigos dos materiais legados que serao usados na operacao, sem substituir codigos existentes automaticamente.
- Realizar a homologacao do WhatsApp, conferindo conteudo da mensagem, destinatario e resultado, sem confundir aceite da API com entrega.
- Validar formalmente os ajustes recentes e a consulta administrativa US #10 / CT46.
- Implementar e validar a US #11, incluida no termo de aceite.
- Versionar as alteracoes e reunir as evidencias para aceite pelo responsavel do produto.
- Validar com leitor USB HID caso haja equipamento disponivel; a validacao manual nao comprova funcionamento do dispositivo fisico.

O backlog ainda marca US #5 como Em andamento, embora existam implementacao, testes e confirmacao manual do fluxo. Recomenda-se conciliar o status com o responsavel pelo aceite, considerando o escopo de validacao exigido.

Conclusao: os oito Must Have possuem implementacao e evidencias tecnicas, com as limitacoes indicadas. O MVP completo permanece com pendencias de implementacao, homologacao, testes formais e versionamento.
