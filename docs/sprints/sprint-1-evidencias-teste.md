# Evidências de Teste — Sprint 1 — Sistema de Pedidos e Controle de Estoque

**Equipe:** Breno Tales de Oliveira Leite (RA: 2840482423029) — Daniel Fredi Soares Pereira (RA: 2840482421054) · Laboratório de Engenharia de Software · ADS Fatec Ribeirão Preto

---

## 1. Tabela de Execução de Casos de Teste

| ID | Caso de teste | Tipo | Resultado | Evidência |
|:---:|---|:---:|:---:|---|
| **CT01** | Login com credenciais inválidas exibe mensagem de erro e recusa acesso | Integração | **Passou** | `tests/test_auth.py:test_ct01_login_credenciais_invalidas` |
| **CT02** | Acesso restrito de acordo com o perfil (Funcionário bloqueado em rotas admin) | Integração | **Passou** | `tests/test_auth.py:test_ct02_acesso_restrito_perfil_funcionario` |
| **CT03** | Cadastro de material com código de barras duplicado é recusado (constraint de unicidade) | Integração | **Passou** | `tests/test_estoque.py:test_ct03_cadastro_material_codigo_barras_duplicado` |
| **CT04** | Consulta por material inexistente no estoque filtra lista sem erros | Integração | **Passou** | `tests/test_estoque.py:test_ct04_consulta_material_inexistente` |
| **CT05** | Validação de quantidades e dimensões inválidas (menores ou iguais a zero) no cadastro de material | Unitário + Integração | **Passou** | `tests/test_estoque.py:test_validacao_campos_invalidos_cadastro_material` |
| — | Login com credenciais válidas autentica e cria sessão | Integração | **Passou** | `tests/test_auth.py:test_login_credenciais_validas` |
| — | Redirecionamento para `/login` ao acessar rotas protegidas sem sessão | Integração | **Passou** | `tests/test_auth.py:test_bloqueio_rotas_sem_login` |
| — | Logout limpa sessão e redireciona | Integração | **Passou** | `tests/test_auth.py:test_logout` |
| — | Geração e validação de hash de senha seguro no modelo `Usuario` | Unitário | **Passou** | `tests/test_auth.py:test_usuario_definir_e_verificar_senha` |
| — | Cadastro de material com dados válidos e código de barras único | Integração | **Passou** | `tests/test_estoque.py:test_cadastro_material_com_sucesso` |
| — | Busca de material por código de barras existente | Integração | **Passou** | `tests/test_estoque.py:test_consulta_material_por_codigo_barras_existente` |
| — | Adição, remoção e redistribuição de bobinas no `estoque_service` | Unitário | **Passou** | `tests/test_estoque.py:test_regras_servico_bobinas` |
| — | Baixa automatizada e estorno de bobinas no estoque | Unitário | **Passou** | `tests/test_estoque.py:test_consumo_e_devolucao_material` |
| — | Conversão de medidas (cm para m) com arredondamento seguro | Unitário | **Passou** | `tests/test_pedidos.py:test_conversao_medidas` |
| — | Algoritmo de aproveitamento de corte (corte padrão vs. rotacionado) | Unitário | **Passou** | `tests/test_pedidos.py:test_calculo_aproveitamento_corte_padrao_e_rotacionado` |
| — | Criação de pedido realiza baixa de metragem no estoque | Integração | **Passou** | `tests/test_pedidos.py:test_fluxo_criacao_pedido_com_baixa_estoque` |
| — | Cancelamento de pedido estorna metragem ao estoque do material | Integração | **Passou** | `tests/test_pedidos.py:test_cancelamento_pedido_estorna_estoque` |
| — | Atualização de status de pedido no fluxo de produção | Integração | **Passou** | `tests/test_pedidos.py:test_atualizar_status_pedido` |
| — | Listagem, criação e edição de clientes com autenticação | Integração | **Passou** | `tests/test_clientes.py` (5 testes) |

---

## 2. Cobertura Automatizada nesta Sprint

- **Framework de Testes:** Python `unittest` com Flask Test Client
- **Total de Testes:** 24 testes automatizados
- **Taxa de Sucesso:** 100% (24 passaram, 0 falhas, 0 erros)
- **Tempo de Execução:** ~6.3 segundos
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
test_usuario_definir_e_verificar_senha (test_auth.AuthTestCase) ... ok
test_cadastro_cliente_nome_obrigatorio (test_clientes.ClientesTestCase) ... ok
test_cadastro_novo_cliente_valido (test_clientes.ClientesTestCase) ... ok
test_cadastro_rapido_cliente_json (test_clientes.ClientesTestCase) ... ok
test_edicao_cliente (test_clientes.ClientesTestCase) ... ok
test_listagem_clientes (test_clientes.ClientesTestCase) ... ok
test_cadastro_material_com_sucesso (test_estoque.EstoqueTestCase) ... ok
test_consulta_material_por_codigo_barras_existente (test_estoque.EstoqueTestCase) ... ok
test_consumo_e_devolucao_material (test_estoque.EstoqueTestCase) ... ok
test_ct03_cadastro_material_codigo_barras_duplicado (test_estoque.EstoqueTestCase) ... ok
test_ct04_consulta_material_inexistente (test_estoque.EstoqueTestCase) ... ok
test_regras_servico_bobinas (test_estoque.EstoqueTestCase) ... ok
test_validacao_campos_invalidos_cadastro_material (test_estoque.EstoqueTestCase) ... ok
test_atualizar_status_pedido (test_pedidos.PedidosTestCase) ... ok
test_calculo_aproveitamento_corte_padrao_e_rotacionado (test_pedidos.PedidosTestCase) ... ok
test_cancelamento_pedido_estorna_estoque (test_pedidos.PedidosTestCase) ... ok
test_conversao_medidas (test_pedidos.PedidosTestCase) ... ok
test_fluxo_criacao_pedido_com_baixa_estoque (test_pedidos.PedidosTestCase) ... ok

----------------------------------------------------------------------
Ran 24 tests in 6.314s

OK
```
