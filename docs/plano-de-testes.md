# Plano de Testes — Sistema Web de Controle de Estoque para Empresa de Comunicação Visual

**Equipe:** Breno Tales de Oliveira Leite (RA: 2840482423029) — Daniel Fredi Soares Pereira (RA: 2840482421054) · Laboratório de Engenharia de Software · ADS Fatec Ribeirão Preto

---

## 1. Estratégia

| Tipo de teste | O que cobre | Ferramenta | Quando roda |
|---|---|---|---|
| **Unitário** | Regras de negócio isoladas (validações, cálculo de corte e estoque) | Python `unittest` | A cada alteração e PR |
| **Integração** | Rotas da aplicação, permissões de usuário e banco de testes | Flask Test Client + `unittest` | A cada PR |
| **Manual / Aceitação** | Fluxos completos na interface (incluindo o leitor de código de barras) | Roteiro manual | Ao fim de cada sprint |

*Observação sobre o WhatsApp:* Nos testes automatizados, simulamos o envio das mensagens usando mocks (`unittest.mock`), sem disparar mensagens reais para não gastar créditos de API e nem colocar números de telefone reais nos testes.

---

## 2. Critério de bloqueio de merge

Nenhum PR deve ser aceito na `main` ou `develop` se: (a) algum teste automatizado existente falhar; (b) uma nova regra for adicionada sem teste correspondente; ou (c) faltar a revisão de pelo menos um outro integrante da equipe.

---

## 3. Casos de teste

### 3.1. Casos implementados (Sprints 1 e 2 — 41 testes)

| ID | História (E2) | Cenário | Entrada | Resultado esperado | Prioridade |
|:---:|:---:|---|---|---|:---:|
| **CT01** | #1 | Login com credenciais inválidas | `email = "admin@empresa.com.br"`, `senha = "senha_errada"` | Sistema recusa o acesso e exibe mensagem de erro | **Alta** |
| **CT02** | #1 | Acesso restrito de acordo com o perfil | Usuário com perfil `Funcionário` tentando acessar rota exclusiva de administrador | Sistema bloqueia o acesso e exibe mensagem de permissão negada | **Alta** |
| **CT03** | #2 | Cadastro de material com código de barras duplicado | `codigo_barras = "7890000000011"` (já cadastrado no banco) | Sistema recusa o cadastro (constraint de unicidade) e informa erro | **Alta** |
| **CT04** | #3 | Consulta por material inexistente no estoque | Busca por código ou nome não cadastrado | Sistema informa que o material não foi encontrado | **Média** |
| **CT05** | #5 | Entrada de estoque com quantidade inválida (menor ou igual a zero) | `quantidade_bobinas = 0` ou `quantidade_bobinas = -2` | Sistema recusa a movimentação e exige quantidade positiva | **Alta** |
| **CT06** | #4 | Identificação de material por código de barras via API | `GET /estoque/api/material/codigo/<codigo>` | Código existente retorna 200 com JSON; inexistente retorna 404; não altera estoque | **Alta** |
| **CT07** | #5, #6 | Registro de entrada de estoque válida e persistência no histórico | `codigo_barras = "7890000000011"`, `quantidade_bobinas = 2` | Estoque do material é incrementado e a movimentação é gravada na tabela `movimentacao_estoque` | **Alta** |
| **CT08** | #1 | Login com credenciais válidas | E-mail e senha corretos cadastrados no banco | Usuário é autenticado e sessão de login é criada com sucesso | **Alta** |
| **CT09** | #1 | Acesso permitido a rotas administrativas para perfil admin | Usuário autenticado como Administrador acessando rotas de gestão | Acesso concedido com sucesso sem bloqueios | **Alta** |
| **CT10** | #1 | Bloqueio e redirecionamento de rotas protegidas sem autenticação | Tentativa de acesso a rota protegida sem sessão ativa | Redirecionamento automático para a tela `/login` | **Alta** |
| **CT11** | #1 | Logout do sistema | Usuário autenticado aciona a rota `/logout` | Sessão é encerrada, cookies limpos e redirecionado para login | **Média** |
| **CT12** | #1 | Hashing seguro de senha no modelo `Usuario` | Criação de usuário com senha em texto plano | Senha é armazenada com hash criptográfico (`generate_password_hash`) | **Alta** |
| **CT13** | #1 | Renderização de interface exibindo ações administrativas para admin | Acesso à tela `/estoque` com perfil Administrador | Exibe botões de cadastro, edição e exclusão de materiais | **Média** |
| **CT14** | #1 | Ocultação de botões administrativos na tela de estoque para funcionário | Acesso à tela `/estoque` com perfil Funcionário | Oculta botões administrativos, mantendo apenas consulta e entrada | **Média** |
| **CT15** | — | Validação de obrigatoriedade do nome no cadastro de cliente | Formulário de cliente enviado com nome em branco | Sistema recusa cadastro e exibe mensagem de validação | **Média** |
| **CT16** | — | Cadastro de novo cliente com dados válidos | Nome, telefone e e-mail válidos informados | Cliente é cadastrado e persistido com sucesso no banco | **Média** |
| **CT17** | — | Cadastro rápido de cliente via API JSON | Payload JSON `{ "nome": "Cliente Teste", "telefone": "..." }` | Retorna status 201 com ID e nome do cliente cadastrado | **Média** |
| **CT18** | — | Edição e atualização de cliente existente | Alteração de dados cadastrais de cliente existente | Registro do cliente é atualizado no banco | **Média** |
| **CT19** | — | Listagem e consulta de clientes cadastrados | Acesso à tela de listagem `/clientes` | Exibe todos os clientes cadastrados | **Média** |
| **CT20** | #2 | Cadastro de material com dados válidos e código único | Nome, categoria, largura, metros e código de barras único | Material é salvo e bobina inicial é criada no banco | **Alta** |
| **CT21** | #2 | Validação de dimensões e quantidades inválidas no material | Largura <= 0 ou unidades <= 0 no formulário de material | Sistema recusa o cadastro e informa campos inválidos | **Alta** |
| **CT22** | #3 | Consulta de material por código de barras existente | Filtro de busca na tela `/estoque` com código cadastrado | Lista exibe apenas o material correspondente | **Média** |
| **CT23** | #4 | API de identificação de material exige autenticação | Requisição `GET /estoque/api/material/codigo/<codigo>` sem login | Redirecionamento para a página de login | **Alta** |
| **CT24** | #4 | API de identificação não altera o saldo de estoque | Chamada à API de identificação por código de barras | Saldo de metros e bobinas permanece exatamente inalterado | **Alta** |
| **CT25** | #4 | Busca por código de barras na camada de serviço (`material_service`) | Execução de `buscar_material_por_codigo_barras(codigo)` | Retorna o objeto `Material` correto ou `None` | **Alta** |
| **CT26** | #5 | Serviço de entrada de estoque atualiza metragem e cria movimentação | Execução de `registrar_entrada_estoque(material, quantidade_bobinas=2)` | Metragem atualizada e registro salvo em `MovimentacaoEstoque` | **Alta** |
| **CT27** | #5 | Rota de entrada de estoque exige autenticação | Envio `POST /estoque/entrada` sem usuário autenticado | Redirecionamento para a página de login | **Alta** |
| **CT28** | #5 | Rota de entrada de estoque recusa código de barras inexistente | Envio de código de barras não cadastrado no banco | Exibe flash de erro e não registra movimentação | **Alta** |
| **CT29** | #5 | Rota de entrada de estoque recusa quantidade de bobinas inválida | Envio de formulário com `quantidade_bobinas = 0` ou negativa | Exibe mensagem de erro e não altera estoque | **Alta** |
| **CT30** | #6 | Rota de movimentações de estoque exige autenticação | Acesso à rota `GET /estoque/movimentacoes` sem login | Redirecionamento para a página de login | **Alta** |
| **CT31** | #6 | Tela de movimentações exibe histórico persistido no banco | Acesso autenticado à tela `/estoque/movimentacoes` | Tabela lista registros de movimentação com data, tipo e quantidade | **Alta** |
| **CT32** | #6 | Movimentações listadas em ordem decrescente (mais recentes primeiro) | Consulta de histórico com múltiplas movimentações | Registros ordenados com `data_hora` decrescente | **Média** |
| **CT33** | #6 | Filtros por tipo de movimentação e por material no histórico | Aplicação de filtros combinados na tela de movimentações | Exibe apenas as movimentações correspondentes aos filtros | **Média** |
| **CT34** | — | Adição, remoção e redistribuição de bobinas no `estoque_service` | Operações de acréscimo e ajuste de metragem de bobinas | Metragem total sincronizada com precisão | **Média** |
| **CT35** | — | Baixa automatizada e estorno de bobinas no estoque | Consumo de metragem em pedido e cancelamento com devolução | Saldo recalculado e bobinas atualizadas | **Média** |
| **CT36** | — | Conversão de medidas (cm para m) com precisão | Conversão de valores em centímetros para metros | Retorno numérico exato com arredondamento seguro | **Média** |
| **CT37** | Cálculo de corte | Algoritmo de aproveitamento de corte (padrão vs. rotacionado) | Dimensões da peça e medidas das bobinas cadastradas | Escolha da orientação que menos gera sobra e rejeição de medidas inválidas | **Alta** |
| **CT38** | — | Criação de pedido realiza baixa de metragem no estoque | Pedido criado com medidas e material especificado | Metragem consumida é descontada do estoque | **Alta** |
| **CT39** | — | Cancelamento de pedido estorna metragem ao estoque | Cancelamento de um pedido existente | Metragem é devolvida ao saldo do material | **Alta** |
| **CT40** | — | Atualização de status de pedido no fluxo de produção | Mudança de status do pedido ('Pendente', 'Em Produção', 'Concluído') | Novo status é salvo no banco de dados | **Média** |
| **CT41** | — | Isolamento de banco de dados nos testes automatizados | Execução dos testes usando banco isolado (`database_test.db`) | Testes rodam sem mexer no banco de desenvolvimento | **Alta** |

---

### 3.2. Notificações — CT42 a CT45 executados na Sprint 3; CT46 planejado para Sprint 4

| ID | História (E2) | Cenário | Entrada | Resultado esperado | Prioridade |
|:---:|:---:|---|---|---|:---:|
| **CT42** | #7, #8 | Envio de notificação no WhatsApp com sucesso | Pedido atualizado e telefone válido do cliente | Pedido finalizado; HTTP 200/201 com wamid simulado retorna aceito; flash de sucesso; entrega_confirmada permanece falsa | **Alta** |
| **CT43** | #8, #9 | Falha ou erro no envio do WhatsApp | Serviço de envio simulando erro (timeout ou API fora) | Sistema avisa que houve erro no envio e não grava como enviado | **Alta** |
| **CT44** | #7, #8 | Cliente com telefone inválido ou sem número | Pedido com cliente sem telefone ou formato incorreto | Sistema barra o envio e avisa que o telefone precisa ser corrigido | **Alta** |
| **CT45** | #9 | Envio automático quando o pedido muda de status | Pedido alterado para 'Finalizado' | Sistema dispara automaticamente e registra tentativa vinculada ao histórico; repetir status não reenvia | **Alta** |
| **CT46** | #10 | Consulta do histórico de mensagens enviadas | Administrador acessando a tela de histórico | Lista as notificações enviadas com pedido, cliente, data e status | **Média** |

---

## 4. Evidências de execução

A cada entrega de sprint, salvamos os resultados dos testes e prints nas pastas:
- `docs/sprints/` (relatórios e logs de execução dos testes)
- `docs/screenshots/` (capturas de tela do sistema em funcionamento)

---

## 5. Rastreabilidade com o Backlog

- **#1 (Login e perfis):** CT01, CT02, CT08–CT14
- **#2 (Cadastro com código de barras):** CT03, CT20, CT21
- **#3 (Consulta de estoque):** CT04, CT22
- **#4 (Identificação por código de barras):** CT06, CT23–CT25
- **#5 (Entrada de material):** CT05, CT07, CT26–CT29
- **#6 (Histórico de movimentações):** CT07, CT30–CT33
- **Cálculo de aproveitamento de corte:** CT36, CT37, CT38, CT39
- **#7 e #8 (Envio manual de WhatsApp):** CT42, CT43, CT44
- **#9 (Envio automático de WhatsApp):** CT43, CT45
- **#10 (Histórico de notificações):** CT46

## 6. Execução formal — Sprint 3 (E7)

**Data de consolidação:** 18/10/2026. **Resultado:** 68 testes aprovados, incluindo 21 novos testes de notificações. Cada método conta como um teste; subcenários usam subTest.

Os rótulos CT08/CT09 de notificações citados no planejamento da retrospectiva da Sprint 2 correspondem aqui a CT42–CT45. CT08 e CT09 da tabela histórica continuam designando autenticação.

**Pré-condições comuns:** cliente e usuário fictícios, sessão autenticada, SQLite em memória e variáveis Meta fictícias. Para caminhos de envio, TESTING=False apenas após instalar o mock de requests.post e a barreira na sessão HTTP. Para testar a proteção nativa, TESTING=True e WHATSAPP_ENABLED=True.

| ID | Procedimento automatizado | Verificações | Execução/evidência |
|---|---|---|---|
| CT42 (#7, #8) | Finalizar pedido; simular resposta Meta 200/201 com messages[0].id | Payload contém cliente/pedido ou parâmetros de template; destino normalizado; timeout; resultado aceito; flash sucesso; tentativa persistida sem entrega confirmada | Aprovado — test_whatsapp.py, test_notificacao_visual.py, test_notificacao_persistencia.py |
| CT43 (#8, #9) | Simular HTTP 400/500, Timeout, ConnectionError e JSON inválido | Resultado falha; código HTTP quando disponível; flash erro; pedido continua Finalizado; sem identificador de sucesso | Aprovado — três módulos de notificação |
| CT44 (#7, #8) | Usar telefone inválido, vazio ou None; testar também pedido sem cliente no serviço | Não chama requests.post; sem_destinatario; flash orienta corrigir telefone; pedido permanece finalizado quando possui cliente vinculado | Aprovado — test_whatsapp.py e test_notificacao_visual.py |
| CT45 (#9) | Finalizar, repetir status, alterar outro status, reabrir e finalizar novamente | Uma tentativa por transição; histórico com usuário; outros status não enviam; nova finalização cria nova tentativa | Aprovado — test_notificacao_persistencia.py |
| Proteção de testes (#8, #9) | Finalizar com TESTING=True, serviço habilitado e credenciais fictícias preenchidas | bloqueado_testing no serviço/banco/flash; nenhuma chamada HTTP | Aprovado — três módulos de notificação |

**Casos complementares:** conector desabilitado, credenciais ausentes, status incompatível, templates com parâmetros e hello_world, normalização de telefone e contrato básico GET/POST do webhook. O recebimento do webhook não comprova entrega.

**Reprodução no PowerShell:**

```powershell
$env:Path = "$PWD\.venv\Scripts;$env:Path"
python -B -m unittest discover -s tests -q
```

[Evidências com log integral e limitações](sprints/sprint-3-evidencias-teste.md). CT46 continua planejado; não integra os casos aprovados desta sprint.
