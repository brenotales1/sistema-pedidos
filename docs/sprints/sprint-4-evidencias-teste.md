# Evidências de Teste — Sprint 4 — Sistema de Pedidos e Controle de Estoque

**Entrega:** E8 — Validação Final do MVP  
**Data da consolidação:** 10/11/2026  
**Resultado:** **111 testes executados · 111 aprovados (100% de sucesso) · 0 falhas · 0 erros · 0 regressões**  
**Equipe:** Breno Tales de Oliveira Leite (RA: 2840482423029) — Daniel Fredi Soares Pereira (RA: 2840482421054) · Laboratório de Engenharia de Software · ADS Fatec Ribeirão Preto  
**Desenvolvimento dos testes e execução:** Breno Tales de Oliveira Leite  
**Implementação dos requisitos validados:** Daniel Fredi Soares Pereira (Commits `695791c` e `652bd8f`)  
**Ambiente:** Python 3.12 (`.venv`), Flask Test Client, SQLite em memória (`sqlite:///:memory:`), isolamento com mocks (`unittest.mock`).

---

## 1. Resumo Executivo da Execução

A suíte completa foi executada com o runner oficial `unittest`, cobrindo tanto as funcionalidades pré-existentes (Sprints 1 a 3) quanto os novos requisitos e correções validados na Sprint 4:

```powershell
$env:Path = "$PWD\.venv\Scripts;$env:Path"
python -B -m unittest discover -s tests -v
```

### Síntese por Módulo de Teste

| Arquivo de Teste | Área Funcional / História | Testes Executados | Status |
|---|---|:---:|:---:|
| `tests/test_auth.py` | US #1: Autenticação, perfis e permissões | 9 | **Aprovado (100%)** |
| `tests/test_clientes.py` | Cadastro, edição e listagem de clientes | 5 | **Aprovado (100%)** |
| `tests/test_pedidos.py` | Pedidos, vínculos e cálculo de corte | 8 | **Aprovado (100%)** |
| `tests/test_migracao_cliente.py` | Migração DDL e integridade de clientes | 3 | **Aprovado (100%)** |
| `tests/test_estoque.py` | US #2, #3, #4, #5: Cadastro, busca e entradas | 22 | **Aprovado (100%)** |
| `tests/test_whatsapp.py` | US #8, #9: Contrato Meta, templates e webhook | 9 | **Aprovado (100%)** |
| `tests/test_notificacao_visual.py` | US #8: Feedback flash e visual | 6 | **Aprovado (100%)** |
| `tests/test_notificacao_persistencia.py` | US #9: Auditoria e persistência de tentativas | 6 | **Aprovado (100%)** |
| **`tests/test_movimentacoes_sprint4.py`** | **US #6: Ciclo de pedidos, ajustes manuais e histórico** | **12** | **Aprovado (100%)** |
| **`tests/test_notificacoes_historico.py`** | **US #10: Consulta administrativa CT46** | **7** | **Aprovado (100%)** |
| **`tests/test_estoque_minimo.py`** | **US #11: Limites, alertas estritos e filtros** | **8** | **Aprovado (100%)** |
| **`tests/test_cancelamento_pedido.py`** | **Cancelamento condicional e bloqueios diretos** | **5** | **Aprovado (100%)** |
| **`tests/test_inicializacao_estoque.py`** | **Inicialização, saldos parciais e consolidação** | **4** | **Aprovado (100%)** |
| **`tests/test_codigo_barras_materiais.py`** | **Regularização de códigos e preservação de histórico** | **7** | **Aprovado (100%)** |
| **Total Consolidado** | **Suíte Completa do MVP** | **111** | **100% OK** |

---

## 2. Detalhamento dos Testes Específicos da Sprint 4

### 2.1. US #6 — Movimentações de Estoque e Consistência (`test_movimentacoes_sprint4.py`)

- `test_criar_pedido_registra_saida_com_todos_os_detalhes`: Criar pedido gera saída de metragem no estoque com material, metragem, usuário da sessão e motivo `Consumo do pedido #X`.
- `test_editar_pedido_registra_estorno_e_novo_consumo`: Editar pedido estorna a metragem anterior (tipo `entrada`, motivo `Estorno para edição do pedido #X`) e registra nova `saida` do novo consumo.
- `test_cancelar_pedido_registra_devolucao`: Cancelar pedido estorna a metragem consumida com tipo `entrada` e motivo `Estorno por cancelamento do pedido #X`.
- `test_cadastro_material_registra_entrada_no_historico`: Novo material registra entrada das bobinas iniciais (50m por unidade) com motivo `Estoque inicial no cadastro do material`.
- `test_adicao_manual_de_bobina_registra_entrada`: Adicionar bobina manual pelo admin registra entrada de 50m com motivo `Adição manual de bobina`.
- `test_remocao_manual_de_bobina_registra_saida_da_metragem_removida`: Remover bobina registra saída com a metragem exata da bobina retirada.
- `test_ajuste_manual_registra_diferenca_e_saldo_anterior_posterior`: Ajuste manual registra tipo `ajuste`, a diferença absoluta em metros e o motivo descritivo `Ajuste manual: X m → Y m`.
- `test_salvar_mesmo_saldo_nao_gera_movimentacao`: Submeter exatamente a mesma metragem atual não gera registro espúrio no histórico de movimentações.
- `test_operacao_rejeitada_nao_altera_saldo_nem_historico`: Quantidade negativa ou inválida é rejeitada com flash de erro, mantendo saldo e histórico intocados.
- `test_falha_na_gravacao_desfaz_ambos_saldo_e_historico`: Simulação de erro com rollback desfaz tanto a alteração das bobinas quanto o registro da movimentação.
- `test_material_com_movimentacoes_nao_pode_ser_excluido`: Rota de exclusão bloqueia materiais que possuem histórico de movimentações associado.
- `test_filtros_e_ordenacao_do_historico`: Listagem de movimentações respeita filtros por tipo (`entrada`, `saida`, `ajuste`), por `material_id` e ordenação decrescente por `data_hora` e `id`.

### 2.2. US #10 — Histórico de Notificações / CT46 (`test_notificacoes_historico.py`)

- `test_ct46_acesso_exclusivo_administrador`: Acesso sem autenticação redireciona para login (302); usuário com perfil funcionário é barrado (302 para `/`); administrador obtém status 200 OK.
- `test_ct46_dados_exibidos_corretos`: Tabela renderiza com precisão o nome do cliente, identificador do pedido `#X`, data/hora em UTC e rótulo do status de envio.
- `test_ct46_filtros_status`: Filtro `?status=aceito` e `?status=falha` filtram os registros correspondentes; status inválido exibe todos os registros.
- `test_ct46_paginacao_25_registros`: Carga de 30 notificações divide a exibição em páginas de 25 itens com controle de anterior/próxima.
- `test_ct46_ordenacao_decrescente`: As notificações mais recentes aparecem antes das mais antigas.
- `test_ct46_lista_vazia`: Renderiza a mensagem informativa "Nenhuma notificação encontrada" sem quebrar o layout.
- `test_ct46_consultar_nao_envia_mensagens_nem_altera_registros`: Acesso à tela de consulta não executa nenhuma chamada HTTP externa nem altera ou cria registros no banco de dados.

### 2.3. US #11 — Gestão de Estoque Mínimo (`test_estoque_minimo.py`)

- `test_cadastro_material_com_estoque_minimo_admin`: Administrador cadastra material com estoque mínimo configurado em metros.
- `test_edicao_estoque_minimo_admin`: Administrador atualiza o limite de estoque mínimo via formulário com persistência no banco.
- `test_bloqueio_edicao_estoque_minimo_para_funcionario`: Funcionário não tem permissão para alterar o estoque mínimo (redirecionado com bloqueio).
- `test_rejeicao_valores_invalidos_estoque_minimo`: Entradas negativas, não numéricas ou inválidas são rejeitadas com mensagem amigável, preservando o valor anterior.
- `test_alerta_somente_quando_saldo_menor_que_minimo`: A propriedade `abaixo_estoque_minimo` e o alerta visual são acionados estritamente quando `saldo < mínimo`. Quando `saldo == mínimo`, o material é considerado "Dentro do limite".
- `test_filtro_abaixo_minimo_na_tela_estoque`: Filtro `?abaixo_minimo=1` filtra exclusivamente materiais em situação de reposição.
- `test_persistencia_estoque_minimo`: Verificação de leitura e escrita garantindo persistência do limite no banco de dados.
- `test_migracao_estoque_minimo_preservando_dados`: Rotina `garantir_coluna_estoque_minimo_material()` preserva limites existentes e saldos sem sobrescrita.

### 2.4. Regras de Cancelamento Condicional (`test_cancelamento_pedido.py`)

- `test_cancelamento_permitido_em_pagamento_pendente`: Cancelamento autorizado; estorna metragem ao saldo, registra entrada no histórico e remove o pedido.
- `test_cancelamento_permitido_em_aguardando_producao`: Cancelamento autorizado na fase de aguardo de produção com devolução de material.
- `test_bloquear_cancelamento_em_pronto_para_retirada_requisicao_direta`: Cancelamento bloqueado via POST direto quando o pedido está "Pronto para retirada"; pedido e estoque permanecem intocados.
- `test_bloquear_cancelamento_em_finalizado_requisicao_direta`: Cancelamento bloqueado via POST direto quando o pedido está "Finalizado"; pedido e estoque permanecem intocados.
- `test_interface_oculta_botao_cancelamento_para_pronto_e_finalizado`: A tela de edição do pedido oculta o botão de cancelamento para os status não canceláveis.

### 2.5. Inicialização e Preservação de Dados (`test_inicializacao_estoque.py`)

- `test_reiniciar_nao_repoe_material_esgotado`: Executar `seed_materials()` repetidamente não repõe bobinas para materiais com saldo zerado.
- `test_reiniciar_nao_altera_saldo_parcial`: Materiais com metragem fracionada (ex.: 17.85m) mantêm seu saldo parcial sem restauração arbitrária de bobinas completas.
- `test_materiais_com_larguras_diferentes_continuam_separados`: Variações de mesma categoria e nome com larguras distintas permanecem como registros independentes.
- `test_consolidacao_nao_executa_automaticamente`: A inicialização do app (`preparar_banco`) não chama a consolidação forçada de materiais.

### 2.6. Regularização de Códigos de Barras Antigos (`test_codigo_barras_materiais.py`)

- `test_admin_cadastra_e_corrige_codigo_barras`: Administrador preenche ou corrige código de barras na tela de estoque com sucesso.
- `test_funcionario_nao_pode_alterar_codigo_barras`: Bloqueio a usuários do perfil funcionário.
- `test_rejeitar_codigo_barras_vazio`: Rejeita strings vazias ou só com espaços.
- `test_rejeitar_codigo_barras_invalido`: Rejeita códigos com mais de 50 caracteres ou caracteres de controle ASCII.
- `test_rejeitar_codigo_barras_duplicado`: Rejeita código que já pertença a outro material cadastrado.
- `test_preservar_estoque_e_historico_ao_alterar_codigo`: A atualização do código de barras mantém intactas as bobinas, o saldo de metros e as movimentações antigas.
- `test_confirmar_consulta_e_entrada_usando_codigo_salvo`: O novo código é imediatamente localizável na busca `/estoque?busca=...`, na API `/estoque/api/material/codigo/...` e permite dar entrada física via leitor `/estoque/entrada`.

---

## 3. Log de Execução da Suíte Completa

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
test_bloquear_cancelamento_em_finalizado_requisicao_direta (test_cancelamento_pedido.CancelamentoPedidoTestCase) ... ok
test_bloquear_cancelamento_em_pronto_para_retirada_requisicao_direta (test_cancelamento_pedido.CancelamentoPedidoTestCase) ... ok
test_cancelamento_permitido_em_aguardando_producao (test_cancelamento_pedido.CancelamentoPedidoTestCase) ... ok
test_cancelamento_permitido_em_pagamento_pendente (test_cancelamento_pedido.CancelamentoPedidoTestCase) ... ok
test_interface_oculta_botao_cancelamento_para_pronto_e_finalizado (test_cancelamento_pedido.CancelamentoPedidoTestCase) ... ok
test_cadastro_cliente_nome_obrigatorio (test_clientes.ClientesTestCase) ... ok
test_cadastro_novo_cliente_valido (test_clientes.ClientesTestCase) ... ok
test_cadastro_rapido_cliente_json (test_clientes.ClientesTestCase) ... ok
test_edicao_cliente (test_clientes.ClientesTestCase) ... ok
test_listagem_clientes (test_clientes.ClientesTestCase) ... ok
test_admin_cadastra_e_corrige_codigo_barras (test_codigo_barras_materiais.CodigoBarrasMateriaisTestCase) ... ok
test_confirmar_consulta_e_entrada_usando_codigo_salvo (test_codigo_barras_materiais.CodigoBarrasMateriaisTestCase) ... ok
test_funcionario_nao_pode_alterar_codigo_barras (test_codigo_barras_materiais.CodigoBarrasMateriaisTestCase) ... ok
test_preservar_estoque_e_historico_ao_alterar_codigo (test_codigo_barras_materiais.CodigoBarrasMateriaisTestCase) ... ok
test_rejeitar_codigo_barras_duplicado (test_codigo_barras_materiais.CodigoBarrasMateriaisTestCase) ... ok
test_rejeitar_codigo_barras_invalido (test_codigo_barras_materiais.CodigoBarrasMateriaisTestCase) ... ok
test_rejeitar_codigo_barras_vazio (test_codigo_barras_materiais.CodigoBarrasMateriaisTestCase) ... ok
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
test_regras_servico_bobinas (test_estoque.EstoqueTestCase) ... ok
test_registrar_entrada_estoque_service_recusa_quantidade_invalida (test_estoque.EstoqueTestCase) ... ok
test_registrar_entrada_estoque_service_sucesso (test_estoque.EstoqueTestCase) ... ok
test_rota_entrada_estoque_material_inexistente (test_estoque.EstoqueTestCase) ... ok
test_rota_entrada_estoque_quantidade_invalida (test_estoque.EstoqueTestCase) ... ok
test_rota_entrada_estoque_sem_login (test_estoque.EstoqueTestCase) ... ok
test_validacao_campos_invalidos_cadastro_material (test_estoque.EstoqueTestCase) ... ok
test_alerta_somente_quando_saldo_menor_que_minimo (test_estoque_minimo.EstoqueMinimoTestCase) ... ok
test_bloqueio_edicao_estoque_minimo_para_funcionario (test_estoque_minimo.EstoqueMinimoTestCase) ... ok
test_cadastro_material_com_estoque_minimo_admin (test_estoque_minimo.EstoqueMinimoTestCase) ... ok
test_edicao_estoque_minimo_admin (test_estoque_minimo.EstoqueMinimoTestCase) ... ok
test_filtro_abaixo_minimo_na_tela_estoque (test_estoque_minimo.EstoqueMinimoTestCase) ... ok
test_migracao_estoque_minimo_preservando_dados (test_estoque_minimo.EstoqueMinimoTestCase) ... ok
test_persistencia_estoque_minimo (test_estoque_minimo.EstoqueMinimoTestCase) ... ok
test_rejeicao_valores_invalidos_estoque_minimo (test_estoque_minimo.EstoqueMinimoTestCase) ... ok
test_consolidacao_nao_executa_automaticamente (test_inicializacao_estoque.InicializacaoEstoqueTestCase) ... ok
test_materiais_com_larguras_diferentes_continuam_separados (test_inicializacao_estoque.InicializacaoEstoqueTestCase) ... ok
test_reiniciar_nao_altera_saldo_parcial (test_inicializacao_estoque.InicializacaoEstoqueTestCase) ... ok
test_reiniciar_nao_repoe_material_esgotado (test_inicializacao_estoque.InicializacaoEstoqueTestCase) ... ok
test_associa_apenas_nome_exato_unico_e_preserva_dados (test_migracao_cliente.MigracaoClienteTestCase) ... ok
test_falha_reverte_coluna_dados_e_marcador (test_migracao_cliente.MigracaoClienteTestCase) ... ok
test_reexecucao_nao_reassocia_pedidos_pendentes (test_migracao_cliente.MigracaoClienteTestCase) ... ok
test_adicao_manual_de_bobina_registra_entrada (test_movimentacoes_sprint4.MovimentacoesEstoqueTestCase) ... ok
test_ajuste_manual_registra_diferenca_e_saldo_anterior_posterior (test_movimentacoes_sprint4.MovimentacoesEstoqueTestCase) ... ok
test_cadastro_material_registra_entrada_no_historico (test_movimentacoes_sprint4.MovimentacoesEstoqueTestCase) ... ok
test_cancelar_pedido_registra_devolucao (test_movimentacoes_sprint4.MovimentacoesEstoqueTestCase) ... ok
test_criar_pedido_registra_saida_com_todos_os_detalhes (test_movimentacoes_sprint4.MovimentacoesEstoqueTestCase) ... ok
test_editar_pedido_registra_estorno_e_novo_consumo (test_movimentacoes_sprint4.MovimentacoesEstoqueTestCase) ... ok
test_falha_na_gravacao_desfaz_ambos_saldo_e_historico (test_movimentacoes_sprint4.MovimentacoesEstoqueTestCase) ... ok
test_filtros_e_ordenacao_do_historico (test_movimentacoes_sprint4.MovimentacoesEstoqueTestCase) ... ok
test_material_com_movimentacoes_nao_pode_ser_excluido (test_movimentacoes_sprint4.MovimentacoesEstoqueTestCase) ... ok
test_operacao_rejeitada_nao_altera_saldo_nem_historico (test_movimentacoes_sprint4.MovimentacoesEstoqueTestCase) ... ok
test_remocao_manual_de_bobina_registra_saida_da_metragem_removida (test_movimentacoes_sprint4.MovimentacoesEstoqueTestCase) ... ok
test_salvar_mesmo_saldo_nao_gera_movimentacao (test_movimentacoes_sprint4.MovimentacoesEstoqueTestCase) ... ok
test_ct43_erro_rede_persistido (test_notificacao_persistencia.NotificacaoPersistenciaTestCase) ... ok
test_ct43_falhas_http_persistidas_sem_desfazer_finalizacao (test_notificacao_persistencia.NotificacaoPersistenciaTestCase) ... ok
test_ct45_auditoria_destinatario_e_aceite_sem_entrega (test_notificacao_persistencia.NotificacaoPersistenciaTestCase) ... ok
test_ct45_reabrir_e_finalizar_novamente_cria_nova_tentativa (test_notificacao_persistencia.NotificacaoPersistenciaTestCase) ... ok
test_ct45_repetir_status_nao_duplica_nem_reenvia (test_notificacao_persistencia.NotificacaoPersistenciaTestCase) ... ok
test_transicao_para_outro_status_nao_cria_tentativa (test_notificacao_persistencia.NotificacaoPersistenciaTestCase) ... ok
test_ct42_sucesso_com_template_renderiza_flash_sucesso (test_notificacao_visual.NotificacaoVisualTestCase) ... ok
test_ct42_sucesso_renderiza_flash_sucesso (test_notificacao_visual.NotificacaoVisualTestCase) ... ok
test_ct43_erro_conexao_renderiza_flash_erro (test_notificacao_visual.NotificacaoVisualTestCase) ... ok
test_ct43_falha_http_renderiza_flash_erro (test_notificacao_visual.NotificacaoVisualTestCase) ... ok
test_ct44_telefone_invalido_renderiza_flash_erro (test_notificacao_visual.NotificacaoVisualTestCase) ... ok
test_desabilitado_renderiza_flash_info (test_notificacao_visual.NotificacaoVisualTestCase) ... ok
test_ct46_acesso_exclusivo_administrador (test_notificacoes_historico.NotificacoesHistoricoTestCase) ... ok
test_ct46_consultar_nao_envia_mensagens_nem_altera_registros (test_notificacoes_historico.NotificacoesHistoricoTestCase) ... ok
test_ct46_dados_exibidos_corretos (test_notificacoes_historico.NotificacoesHistoricoTestCase) ... ok
test_ct46_filtros_status (test_notificacoes_historico.NotificacoesHistoricoTestCase) ... ok
test_ct46_lista_vazia (test_notificacoes_historico.NotificacoesHistoricoTestCase) ... ok
test_ct46_ordenacao_decrescente (test_notificacoes_historico.NotificacoesHistoricoTestCase) ... ok
test_ct46_paginacao_25_registros (test_notificacoes_historico.NotificacoesHistoricoTestCase) ... ok
test_atualizar_status_pedido (test_pedidos.PedidosTestCase) ... ok
test_calculo_aproveitamento_corte_padrao_e_rotacionado (test_pedidos.PedidosTestCase) ... ok
test_cancelamento_pedido_estorna_estoque (test_pedidos.PedidosTestCase) ... ok
test_cliente_invalido_nao_baixa_estoque (test_pedidos.PedidosTestCase) ... ok
test_conversao_medidas (test_pedidos.PedidosTestCase) ... ok
test_fluxo_criacao_pedido_com_baixa_estoque (test_pedidos.PedidosTestCase) ... ok
test_homonimos_selecionados_por_id_e_historico_preservado (test_pedidos.PedidosTestCase) ... ok
test_legado_editavel_sem_associacao_e_vinculo_explicito (test_pedidos.PedidosTestCase) ... ok
test_ct42_envio_sucesso_com_destinatario_normalizado (test_whatsapp.WhatsAppTestCase) ... ok
test_ct43_falhas_e_erros_de_rede (test_whatsapp.WhatsAppTestCase) ... ok
test_ct44_cliente_sem_telefone_ou_invalido (test_whatsapp.WhatsAppTestCase) ... ok
test_desabilitado_status_incompativel_e_credenciais_ausentes (test_whatsapp.WhatsAppTestCase) ... ok
test_normalizacao_e_rejeicao_de_telefones (test_whatsapp.WhatsAppTestCase) ... ok
test_template_com_parametros_e_hello_world (test_whatsapp.WhatsAppTestCase) ... ok
test_testing_bloqueia_mesmo_com_configuracao_valida (test_whatsapp.WhatsAppTestCase) ... ok
test_webhook_verificacao_e_recebimento_sem_confirmar_entrega (test_whatsapp.WhatsAppTestCase) ... ok

----------------------------------------------------------------------
Ran 111 tests in 15.746s

OK
```

---

## 4. Conclusão da Validação

A execução confirma que todos os requisitos do Termo de Aceite correspondentes às US #1 a #11 foram entregues com cobertura automatizada de ponta a ponta, sem regressões nos módulos de autenticação, clientes, pedidos, controle de estoque e notificações.
