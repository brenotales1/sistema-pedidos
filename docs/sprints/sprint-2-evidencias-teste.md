# Evidências de Teste — Sprint 2 — Sistema de Pedidos e Controle de Estoque

**Equipe:** Breno Tales de Oliveira Leite (RA: 2840482423029) — Daniel Fredi Soares Pereira (RA: 2840482421054) · Laboratório de Engenharia de Software · ADS Fatec Ribeirão Preto

---

## 1. Tabela de Execução de Casos de Teste

| ID | Caso de teste | Tipo | Resultado | Evidência |
|:---:|---|:---:|:---:|---|
| **CT01** | Login com credenciais inválidas exibe mensagem de erro e recusa acesso | Integração | **Passou** | `tests/test_auth.py:test_ct01_login_credenciais_invalidas` |
| **CT02** | Acesso restrito de acordo com o perfil (Funcionário bloqueado em rotas admin) | Integração | **Passou** | `tests/test_auth.py:test_ct02_acesso_restrito_perfil_funcionario` |
| **CT03** | Cadastro de material com código de barras duplicado é recusado (constraint de unicidade) | Integração | **Passou** | `tests/test_estoque.py:test_ct03_cadastro_material_codigo_barras_duplicado` |
| **CT04** | Consulta por material inexistente no estoque filtra lista sem erros | Integração | **Passou** | `tests/test_estoque.py:test_ct04_consulta_material_inexistente` |
| **CT05** | Entrada de estoque com quantidade inválida (menor ou igual a zero) é recusada | Unitário + Integração | **Passou** | `tests/test_estoque.py:test_registrar_entrada_estoque_service_recusa_quantidade_invalida` |
| **CT06** | Identificação de material por código de barras via API (código existente retorna 200; inexistente retorna 404) | Integração | **Passou** | `tests/test_estoque.py:test_api_material_por_codigo_existente` |
| **CT07** | Registro de entrada de estoque válida e persistência no histórico de movimentações | Integração | **Passou** | `tests/test_estoque.py:test_ct05_ct07_rota_entrada_estoque_sucesso` |
| **CT08** | Login com credenciais válidas autentica e cria sessão | Integração | **Passou** | `tests/test_auth.py:test_login_credenciais_validas` |
| **CT09** | Acesso permitido a rotas restritas para perfil admin | Integração | **Passou** | `tests/test_auth.py:test_acesso_permitido_perfil_admin` |
| **CT10** | Bloqueio e redirecionamento para `/login` ao acessar rotas protegidas sem sessão | Integração | **Passou** | `tests/test_auth.py:test_bloqueio_rotas_sem_login` |
| **CT11** | Logout limpa a sessão do usuário e redireciona para login | Integração | **Passou** | `tests/test_auth.py:test_logout` |
| **CT12** | Geração e validação de hash de senha seguro no modelo `Usuario` | Unitário | **Passou** | `tests/test_auth.py:test_usuario_definir_e_verificar_senha` |
| **CT13** | Renderização de interface exibindo ações administrativas para perfil admin | Integração | **Passou** | `tests/test_auth.py:test_tela_estoque_exibe_acoes_administrativas_para_admin` |
| **CT14** | Ocultação de ações e botões administrativos na interface para perfil funcionário | Integração | **Passou** | `tests/test_auth.py:test_tela_estoque_oculta_acoes_administrativas_para_funcionario` |
| **CT15** | Validação de obrigatoriedade do nome no cadastro de cliente | Integração | **Passou** | `tests/test_clientes.py:test_cadastro_cliente_nome_obrigatorio` |
| **CT16** | Cadastro de novo cliente com dados válidos e persistência no banco | Integração | **Passou** | `tests/test_clientes.py:test_cadastro_novo_cliente_valido` |
| **CT17** | Cadastro rápido de cliente via API JSON retornando ID e nome | Integração | **Passou** | `tests/test_clientes.py:test_cadastro_rapido_cliente_json` |
| **CT18** | Edição e atualização de dados de cliente existente | Integração | **Passou** | `tests/test_clientes.py:test_edicao_cliente` |
| **CT19** | Listagem e consulta de clientes cadastrados | Integração | **Passou** | `tests/test_clientes.py:test_listagem_clientes` |
| **CT20** | Cadastro de material com dados válidos e código de barras único | Integração | **Passou** | `tests/test_estoque.py:test_cadastro_material_com_sucesso` |
| **CT21** | Validação de dimensões e quantidades inválidas (<= 0) no cadastro de material | Unitário + Integração | **Passou** | `tests/test_estoque.py:test_validacao_campos_invalidos_cadastro_material` |
| **CT22** | Busca de material por código de barras existente na tela de estoque | Integração | **Passou** | `tests/test_estoque.py:test_consulta_material_por_codigo_barras_existente` |
| **CT23** | API de identificação de material por código de barras exige autenticação | Integração | **Passou** | `tests/test_estoque.py:test_api_material_por_codigo_sem_login` |
| **CT24** | API de identificação de material não altera saldo de estoque | Integração | **Passou** | `tests/test_estoque.py:test_api_identificacao_nao_altera_estoque` |
| **CT25** | Serviço de busca por código de barras no banco de dados (`material_service`) | Unitário | **Passou** | `tests/test_estoque.py:test_buscar_material_por_codigo_barras_service` |
| **CT26** | Serviço de registro de entrada de estoque atualiza metragem e cria movimentação | Unitário | **Passou** | `tests/test_estoque.py:test_registrar_entrada_estoque_service_sucesso` |
| **CT27** | Rota de entrada de estoque exige autenticação de login | Integração | **Passou** | `tests/test_estoque.py:test_rota_entrada_estoque_sem_login` |
| **CT28** | Rota de entrada de estoque recusa código de barras inexistente | Integração | **Passou** | `tests/test_estoque.py:test_rota_entrada_estoque_material_inexistente` |
| **CT29** | Rota de entrada de estoque recusa quantidade de bobinas inválida (<= 0) | Integração | **Passou** | `tests/test_estoque.py:test_rota_entrada_estoque_quantidade_invalida` |
| **CT30** | Rota de movimentações de estoque exige autenticação de login | Integração | **Passou** | `tests/test_estoque.py:test_movimentacoes_estoque_sem_login` |
| **CT31** | Tela de movimentações exibe histórico persistido no banco | Integração | **Passou** | `tests/test_estoque.py:test_movimentacoes_estoque_exibe_historico` |
| **CT32** | Movimentações são listadas em ordem decrescente (mais recentes primeiro) | Integração | **Passou** | `tests/test_estoque.py:test_movimentacoes_estoque_mais_recentes_primeiro` |
| **CT33** | Filtros por tipo de movimentação e por material funcionam corretamente | Integração | **Passou** | `tests/test_estoque.py:test_movimentacoes_estoque_filtros_tipo_e_material` |
| **CT34** | Adição, remoção e redistribuição de bobinas no `estoque_service` | Unitário | **Passou** | `tests/test_estoque.py:test_regras_servico_bobinas` |
| **CT35** | Baixa automatizada e estorno de bobinas no estoque | Unitário | **Passou** | `tests/test_estoque.py:test_consumo_e_devolucao_material` |
| **CT36** | Conversão de medidas (cm para m) com precisão | Unitário | **Passou** | `tests/test_pedidos.py:test_conversao_medidas` |
| **CT37** | Algoritmo de aproveitamento de corte (corte padrão vs. rotacionado) | Unitário | **Passou** | `tests/test_pedidos.py:test_calculo_aproveitamento_corte_padrao_e_rotacionado` |
| **CT38** | Criação de pedido realiza baixa de metragem no estoque | Integração | **Passou** | `tests/test_pedidos.py:test_fluxo_criacao_pedido_com_baixa_estoque` |
| **CT39** | Cancelamento de pedido estorna metragem ao estoque do material | Integração | **Passou** | `tests/test_pedidos.py:test_cancelamento_pedido_estorna_estoque` |
| **CT40** | Atualização de status de pedido no fluxo de produção | Integração | **Passou** | `tests/test_pedidos.py:test_atualizar_status_pedido` |
| **CT41** | Isolamento do banco de dados de teste (`database_test.db`) em fixtures | Integração | **Passou** | `tests/base.py:BaseTestCase` |

---

## 2. Cobertura Automatizada nesta Sprint

- **Framework de Testes:** Python `unittest` com Flask Test Client
- **Total de Testes:** 41 testes automatizados
- **Taxa de Sucesso:** 100% (41 passaram, 0 falhas, 0 erros)
- **Tempo de Execução:** ~8.6 segundos
- **Comando de Execução:**
  ```powershell
  python -m unittest discover -s tests -p "test_*.py" -v
  ```

### Log de Execução:
```text
test_acesso_permitido_perfil_admin (test_auth.AuthTestCase) ... ok
test_bloqueio_rotas_sem_login (test_auth.AuthTestCase) ... ok
test_ct01_login_credenciais_invalidas (test_auth.AuthTestCase) ... ok
test_ct02_acesso_restrito_perfil_funcionario (test_auth.AuthTestCase) ... ok
test_login_credenciais_validas (test_auth.AuthTestCase) ... ok
test_logout (test_auth.AuthTestCase) ... ok
test_tela_estoque_exibe_acoes_administrativas_para_admin (test_auth.AuthTestCase) ... ok
test_tela_estoque_oculta_acoes_administrativas_para_funcionario (test_auth.AuthTestCase) ... ok
test_usuario_definir_e_verificar_senha (test_auth.AuthTestCase) ... ok
test_cadastro_cliente_nome_obrigatorio (test_clientes.ClientesTestCase) ... ok
test_cadastro_novo_cliente_valido (test_clientes.ClientesTestCase) ... ok
test_cadastro_rapido_cliente_json (test_clientes.ClientesTestCase) ... ok
test_edicao_cliente (test_clientes.ClientesTestCase) ... ok
test_listagem_clientes (test_clientes.ClientesTestCase) ... ok
test_api_identificacao_nao_altera_estoque (test_estoque.EstoqueTestCase) ... ok
test_api_material_por_codigo_existente (test_estoque.EstoqueTestCase) ... ok
test_api_material_por_codigo_inexistente (test_estoque.EstoqueTestCase) ... ok
test_api_material_por_codigo_sem_login (test_estoque.EstoqueTestCase) ... ok
test_buscar_material_por_codigo_barras_service (test_estoque.EstoqueTestCase) ... ok
test_cadastro_material_com_sucesso (test_estoque.EstoqueTestCase) ... ok
test_consulta_material_por_codigo_barras_existente (test_estoque.EstoqueTestCase) ... ok
test_consumo_e_devolucao_material (test_estoque.EstoqueTestCase) ... ok
test_ct03_cadastro_material_codigo_barras_duplicado (test_estoque.EstoqueTestCase) ... ok
test_ct04_consulta_material_inexistente (test_estoque.EstoqueTestCase) ... ok
test_ct05_ct07_rota_entrada_estoque_sucesso (test_estoque.EstoqueTestCase) ... ok
test_movimentacoes_estoque_exibe_historico (test_estoque.EstoqueTestCase) ... ok
test_movimentacoes_estoque_filtros_tipo_e_material (test_estoque.EstoqueTestCase) ... ok
test_movimentacoes_estoque_mais_recentes_primeiro (test_estoque.EstoqueTestCase) ... ok
test_movimentacoes_estoque_sem_login (test_estoque.EstoqueTestCase) ... ok
test_registrar_entrada_estoque_service_recusa_quantidade_invalida (test_estoque.EstoqueTestCase) ... ok
test_registrar_entrada_estoque_service_sucesso (test_estoque.EstoqueTestCase) ... ok
test_regras_servico_bobinas (test_estoque.EstoqueTestCase) ... ok
test_rota_entrada_estoque_material_inexistente (test_estoque.EstoqueTestCase) ... ok
test_rota_entrada_estoque_quantidade_invalida (test_estoque.EstoqueTestCase) ... ok
test_rota_entrada_estoque_sem_login (test_estoque.EstoqueTestCase) ... ok
test_validacao_campos_invalidos_cadastro_material (test_estoque.EstoqueTestCase) ... ok
test_atualizar_status_pedido (test_pedidos.PedidosTestCase) ... ok
test_calculo_aproveitamento_corte_padrao_e_rotacionado (test_pedidos.PedidosTestCase) ... ok
test_cancelamento_pedido_estorna_estoque (test_pedidos.PedidosTestCase) ... ok
test_conversao_medidas (test_pedidos.PedidosTestCase) ... ok
test_fluxo_criacao_pedido_com_baixa_estoque (test_pedidos.PedidosTestCase) ... ok

----------------------------------------------------------------------
Ran 41 tests in 8.652s

OK
```
