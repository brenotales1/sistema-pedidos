# Revisão do MVP — Sprint 4 — Sistema de Pedidos e Controle de Estoque

**Revisão inicial:** 07/11/2026  
**Atualização:** 09/11/2026  
**Situação:** Em validação  
**Equipe:** Breno Tales de Oliveira Leite (RA: 2840482423029) — Daniel Fredi Soares Pereira (RA: 2840482421054) · Laboratório de Engenharia de Software · ADS Fatec Ribeirão Preto

**Referências:** [Backlog vigente](../backlog.md), [termo de aceite](../termo-de-aceite.md) e [evidências da Sprint 3](sprint-3-evidencias-teste.md).

---

## 1. Objetivo e escopo

Verificar a implementação dos requisitos e as pendências para o aceite do MVP. O escopo acordado inclui as US #1 a #11, com prioridades Must e Should. A US #12 — Dashboard é prioridade Could e não integra as funcionalidades obrigatórias do termo de aceite.

A implementação identificada e os testes anteriores não equivalem à homologação em produção nem comprovam alterações posteriores. A validação dos ajustes recentes e o registro das evidências ficam com a pessoa responsável pelos testes.

---

## 2. Revisão dos requisitos Must Have

| US | Critérios revisados | Implementação e evidências anteriores |
|---|---|---|
| #1 | E-mail e senha obrigatórios; erro para credenciais inválidas; permissões por perfil | Rotas de autenticação e controle de acesso implementadas; testes em `tests/test_auth.py`. Novas rotas administrativas aguardam validação. |
| #2 | Código único; descrição e quantidade obrigatórias; persistência após validação | Cadastro implementado, com validações, unicidade no modelo e testes em `tests/test_estoque.py`. Regularização dos códigos antigos pendente. |
| #3 | Exibir descrição, código e quantidade; localizar material; informar ausência | Lista e busca implementadas, com testes existentes. A identificação dos materiais antigos depende do preenchimento dos códigos. |
| #4 | Identificar código existente; erro para inexistente; consulta sem alterar saldo | API de consulta implementada, com testes existentes. Há relato de conferência por digitação manual, ainda sem evidência formal anexada nesta revisão. Leitor USB HID não validado. |
| #5 | Quantidade positiva; material cadastrado; atualizar saldo; registrar movimentação | Entrada implementada, com testes existentes de sucesso e rejeição. Concluída no backlog. Há relato de conferência manual do fluxo, sem captura de tela anexada nesta revisão. |
| #7 | Pedido existente; cliente vinculado; atualização registrada | Transição de status com validação de cliente e usuário e histórico persistente; testes existentes de pedidos e notificações. |
| #8 | Validar telefone; mensagem com pedido e atualização; informar sucesso ou falha | Fluxo de finalização implementado, com API simulada nos testes. Templates dependem do conteúdo aprovado na Meta; `hello_world` não comprova mensagem com pedido e atualização. Envio e recebimento reais pendentes. |
| #9 | Evento dispara envio; destinatário correto; resultado registrado | Implementado na transição para Finalizado. CT43/CT45 cobrem resultado, destinatário e prevenção de reenvio ao repetir o mesmo status. Homologação real pendente. |

---

## 3. Critérios de pronto do termo de aceite

A conclusão depende da validação dos requisitos Must e Should e do cumprimento das condições de entrega.

| Critério | Situação |
|---|---|
| Acesso com perfis e permissões distintas | Evidências anteriores existentes; novas rotas aguardam validação. |
| Entrada completa por código, quantidade, saldo e movimentação | Implementada, com testes existentes; evidências finais deverão ser consolidadas. |
| Identificação de código cadastrado e erro para inexistente | Implementada; regularização dos cadastros antigos pendente. |
| Notificação pelo WhatsApp com registro do resultado | Verificada anteriormente com mocks; homologação real pendente. Aceite da API não confirma entrega. |
| Consulta do histórico de notificações | US #10 implementada; CT46 aguarda validação. |
| Identificação de materiais abaixo do mínimo | US #11 implementada; aguarda validação. |
| Histórico de movimentações | US #6 implementada; complementos aguardam validação. |
| Testes e evidências das alterações recentes | Pendentes, sob responsabilidade da pessoa encarregada dos testes. |
| Código versionado no Git | Há alterações locais ainda não commitadas. |
| Aceite final | Pendente de validação e aprovação do responsável pelo produto. |

---

## 4. Pendências para aceite final

- Preencher os códigos reais dos materiais antigos usados na operação. A tela de estoque já permite cadastrar e corrigir códigos pelo administrador, preservando saldo e histórico; esse novo fluxo aguarda testes. A consulta local de 09/11/2026 identificou sete materiais sem código.
- Realizar a homologação do WhatsApp, conferindo conteúdo da mensagem, destinatário e resultado, distinguindo aceite da API de recebimento pelo cliente.
- Validar a consulta administrativa US #10 / CT46: permissões, dados exibidos, filtros, ordenação, paginação e histórico vazio, sem disparar mensagens.
- Validar a US #11: configuração e persistência do mínimo, permissões, valores inválidos, migração, comparação do saldo e filtros.
- Validar os complementos da US #6, as correções da inicialização, o bloqueio de cancelamento e a edição dos códigos de barras. Executar a suíte existente para verificar regressões em pedidos, clientes, estoque, autenticação e notificações.
- Preparar o documento de evidências da Sprint 4 com resultados reais, data, responsável e registros da execução.
- Versionar as alterações, alinhar o backlog aos resultados aprovados e registrar o aceite final pelo responsável pelo produto.
- Validar com leitor USB HID caso haja equipamento disponível; a digitação manual não comprova o funcionamento do dispositivo físico.

---

## 5. Funcionalidades e correções da Sprint 4

| Item | Comportamento implementado | Situação |
|---|---|---|
| US #6 — Histórico de movimentações | Registra consumo dos pedidos, estorno e novo consumo na edição, devolução por cancelamento permitido, estoque inicial no cadastro, adição e remoção manual de bobinas e ajustes de metragem. Inclui usuário e motivo; ajustes informam saldo anterior e posterior. Salvar o mesmo saldo não cria movimentação. Os registros ficam na mesma transação da alteração. | Implementada; complementos aguardam validação. O backlog ainda indica Em andamento. |
| US #10 — Histórico de notificações | Consulta exclusiva para administradores, com cliente, pedido, data/hora em UTC, resultado, filtro e paginação de 25 registros. Não dispara mensagens nem confirma entrega ao cliente. | Implementada; aguardando testes do CT46. |
| US #11 — Estoque mínimo | Limite por material em metros, configurável pelo administrador no cadastro e na listagem. Exibe saldo e mínimo, destaca valores estritamente abaixo do limite e permite filtrar. A migração adiciona mínimo zero aos materiais existentes sem alterar os saldos e preserva limites já cadastrados. | Implementada; aguardando testes. |
| Inicialização do estoque | Materiais existentes sem bobinas permanecem esgotados; somente os materiais criados pelo seed recebem estoque inicial. | Aguardando validação final. |
| Consolidação de materiais | Não executa automaticamente ao iniciar. A consolidação explícita diferencia as larguras; não recupera dados alterados anteriormente. | Aguardando validação final. |
| Cancelamento | Bloqueado para Pronto para retirada e Finalizado, inclusive por requisição direta; botão oculto nesses casos. Nos status anteriores, devolve a metragem e registra entrada. A regra pressupõe que o material ainda não foi utilizado fisicamente nesses status. | Aguardando validação final. |
| Preservação do histórico | Materiais com movimentações não podem ser excluídos. Movimentações antigas não registradas não são reconstruídas. | Aguardando validação final. |
| Materiais antigos | Cadastro e correção administrativa do código de barras na tela de estoque, com rejeição de códigos vazios, inválidos ou usados por outro material. Preserva bobinas e movimentações. | Implementada; aguardando testes e preenchimento dos códigos reais. |

Esta revisão mantém a entrega em validação. Nenhum teste foi criado ou executado nesta atualização documental; resultados e aprovação final deverão ser registrados após a execução pela pessoa responsável.
