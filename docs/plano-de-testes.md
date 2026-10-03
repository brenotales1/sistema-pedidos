# Plano de Testes — Sistema Web de Controle de Estoque para Empresa de Comunicação Visual

**Equipe:** Breno Tales de Oliveira Leite (RA: 2840482423029) — Daniel Fredi Soares Pereira (RA: 2840482421054) · Laboratório de Engenharia de Software · ADS Fatec Ribeirão Preto

---

## 1. Estratégia

| Tipo de teste | O que cobre | Ferramenta | Quando roda |
|---|---|---|---|
| **Unitário** | Regras de negócio isoladas (validações de cadastro, cálculo de dimensões, movimentação de bobinas e aproveitamento de corte) | Python `unittest` | A cada PR (CI) |
| **Integração** | Rotas da API, controle de acesso RBAC e controladores Flask contra banco de teste isolado | Flask Test Client + `unittest` | A cada PR (CI) |
| **Manual / Aceitação** | Fluxos completos de ponta a ponta antes de cada entrega | Roteiro manual com leitor USB | Ao fim de cada sprint |

---

## 2. Critério de bloqueio de merge

Nenhum PR é aceito na `main` ou `develop` se: (a) algum teste automatizado existente quebrar; (b) uma nova regra de negócio for adicionada sem teste correspondente; (c) não houver revisão e aprovação de ao menos 1 outro integrante da equipe.

---

## 3. Casos de teste planejados (41 testes automatizados)

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
| **CT37** | — | Algoritmo de aproveitamento de corte (padrão vs. rotacionado) | Cálculo de orientação ideal de corte em bobina de material | Escolha automática da orientação com menor desperdício de área | **Alta** |
| **CT38** | — | Criação de pedido realiza baixa de metragem no estoque | Criação de pedido com dimensões e material especificado | Metragem consumida é subtraída do estoque do material | **Alta** |
| **CT39** | — | Cancelamento de pedido estorna metragem ao estoque do material | Exclusão/cancelamento de pedido existente | Metragem é creditada de volta ao saldo do material | **Alta** |
| **CT40** | — | Atualização de status de pedido no fluxo de produção | Transição de status (ex.: 'Pendente' -> 'Em Produção' -> 'Concluído') | Novo status é persistido no banco de dados | **Média** |
| **CT41** | — | Isolamento de banco de dados nos testes automatizados | Execução do setup de testes com `database_test.db` isolado | Testes rodam sem concorrência ou conflito com o banco de dev | **Alta** |
