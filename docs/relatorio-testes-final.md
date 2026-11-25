# Relatório de Testes Executados — Sistema Web de Controle de Estoque para Empresa de Comunicação Visual

**Entrega:** E9/E10 — Relatório consolidado de testes executados<br>
**Equipe:** Breno Tales de Oliveira Leite (RA: 2840482423029) — Daniel Fredi Soares Pereira (RA: 2840482421054) · Laboratório de Engenharia de Software · ADS Fatec Ribeirão Preto<br>
**Data da bateria final:** 15/11/2026<br>
**Referência de calendário da entrega:** Semana 13 (06/11/2026)<br>
**Versão avaliada:** commit `9e8df58` (inclui N:N por ConsumoMaterial)<br>
**Escopo testado:** funcionalidades Must + Should, itens 1 a 11 do [Termo de Aceite do Projeto — E2b](E2-termo-de-aceite.md), mais a relação N:N Pedido–Material da E10.<br>
**Situação:** regressão automatizada concluída; escopo aceito pelo PO; assinatura pendente.

---

## 1. Resumo executivo

| Métrica | Valor |
|---|---|
| Total de testes automatizados executados | 131 |
| Passaram | 131 |
| Falharam | 0 |
| Erros de execução | 0 |
| Testes ignorados | 0 |
| Taxa de sucesso da suíte | 100% |
| Duração informada pelo runner | 18,575 segundos |
| Cobertura automatizada (linhas/branches) | Não mensurada; ferramenta coverage não instalada no ambiente |
| Aceite do cliente real | Homologado sem ressalvas por Paulo Rogério Leite (Center Comunicação Visual) |

A execução confirma a regressão dos módulos de autenticação, clientes, pedidos, estoque, notificações e consumo N:N. Os cenários negativos aprovados comprovam que o sistema rejeita entradas ou operações inválidas como esperado; não representam testes falhos. A taxa de 100% refere-se aos testes executados, sem significar cobertura total do código.

### Ambiente e reprodução

Python do ambiente virtual local (`.venv`), runner `unittest`, Flask Test Client, SQLite em memória e `unittest.mock` para chamadas externas. A suíte usa simulações e não comprova leitura por equipamento físico nem entrega real de mensagens.

Comando executado no PowerShell, na raiz do projeto:

```powershell
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -v
```

Resultado retornado pelo runner:

```text
Ran 131 tests in 18.575s

OK
```

Durante a execução ocorreram avisos de `datetime.utcnow()` e `Query.get()`, sem reprovar nenhum teste.

---

## 2. Lista completa dos 131 testes

### 2.1. test_auth.py — Autenticação e permissões (9 testes)

| # | Teste | O que verifica |
|---|---|---|
| 1 | test_acesso_permitido_perfil_admin | Admin tem acesso liberado a todas as rotas |
| 2 | test_bloqueio_rotas_sem_login | Sem login, redireciona para a tela de login |
| 3 | test_ct01_login_credenciais_invalidas | Login com dados errados é recusado com mensagem de erro |
| 4 | test_ct02_acesso_restrito_perfil_funcionario | Funcionário não acessa rotas de administrador |
| 5 | test_login_credenciais_validas | Login correto autentica e cria a sessão |
| 6 | test_logout | Logout limpa a sessão e redireciona para login |
| 7 | test_tela_estoque_exibe_acoes_administrativas_para_admin | Admin vê todos os botões de gestão no estoque |
| 8 | test_tela_estoque_oculta_acoes_administrativas_para_funcionario | Funcionário não vê botões de admin no estoque |
| 9 | test_usuario_definir_e_verificar_senha | Hash de senha é gerado e verificado corretamente |

### 2.2. test_cancelamento_pedido.py — Cancelamento por status (5 testes)

| # | Teste | O que verifica |
|---|---|---|
| 10 | test_bloquear_cancelamento_em_finalizado_requisicao_direta | Bloqueia cancelamento de pedido "Finalizado", mesmo por POST direto |
| 11 | test_bloquear_cancelamento_em_pronto_para_retirada_requisicao_direta | Bloqueia cancelamento de "Pronto para retirada", mesmo por POST direto |
| 12 | test_cancelamento_permitido_em_aguardando_producao | Permite cancelar quando status é "Aguardando produção", devolvendo estoque |
| 13 | test_cancelamento_permitido_em_pagamento_pendente | Permite cancelar quando status é "Pagamento pendente", com estorno |
| 14 | test_interface_oculta_botao_cancelamento_para_pronto_e_finalizado | Botão de cancelar aparece só nos status permitidos |

### 2.3. test_clientes.py — Cadastro e gestão de clientes (9 testes)

| # | Teste | O que verifica |
|---|---|---|
| 15 | test_cadastro_cliente_nome_duplicado | Nome já existente mostra erro de duplicidade |
| 16 | test_cadastro_cliente_nome_obrigatorio | Sem nome, mostra erro de validação |
| 17 | test_cadastro_novo_cliente_valido | Dados válidos salvam o cliente no banco |
| 18 | test_cadastro_rapido_cliente_json | Cadastro rápido via JSON retorna ID e nome |
| 19 | test_cadastro_rapido_cliente_nome_duplicado | JSON com nome duplicado retorna erro 400 |
| 20 | test_edicao_cliente | Edição altera os dados do cliente existente |
| 21 | test_edicao_cliente_nome_duplicado | Editar para nome de outro cliente é recusado |
| 22 | test_identificador_cliente | Cliente tem identificador com prefixo '#' |
| 23 | test_listagem_clientes | Listagem exibe os dados dos clientes cadastrados |

### 2.4. test_codigo_barras_materiais.py — Código de barras (7 testes)

| # | Teste | O que verifica |
|---|---|---|
| 24 | test_admin_cadastra_e_corrige_codigo_barras | Admin cadastra e corrige o código com sucesso |
| 25 | test_confirmar_consulta_e_entrada_usando_codigo_salvo | Material é localizado e permite entrada pelo código atualizado |
| 26 | test_funcionario_nao_pode_alterar_codigo_barras | Funcionário não tem permissão para alterar código |
| 27 | test_preservar_estoque_e_historico_ao_alterar_codigo | Alterar código mantém bobinas, saldo e histórico intactos |
| 28 | test_rejeitar_codigo_barras_duplicado | Código já usado por outro material é recusado |
| 29 | test_rejeitar_codigo_barras_invalido | Códigos com mais de 50 caracteres ou caracteres inválidos são recusados |
| 30 | test_rejeitar_codigo_barras_vazio | Código vazio ou só com espaços é recusado |

### 2.5. test_consumo_material.py — Relação N:N Pedido–Material (16 testes · E10)

| # | Teste | O que verifica |
|---|---|---|
| 31 | test_n_para_n_dois_pedidos_compartilham_dois_materiais | Dois pedidos compartilham os mesmos dois materiais; saldos e movimentações batem |
| 32 | test_editar_substitui_consumos_e_estorna_material_removido | Editar pedido troca materiais, estorna o removido e consome o novo |
| 33 | test_editar_sem_alterar_nao_duplica_vinculos_nem_consumo | Salvar sem alterar não duplica vínculos nem consome novamente |
| 34 | test_cancelar_estorna_todos_e_remove_associacoes | Cancelar devolve estoque de todos os materiais e limpa as associações |
| 35 | test_cancelamento_bloqueado_preserva_todos_os_consumos | Cancelar pedido "Finalizado" não mexe nos consumos nem no estoque |
| 36 | test_adicionais_invalidos_nao_alteram_pedido_estoque_historico | Valores inválidos (0, negativos, "nan", "inf", letras) não criam pedido |
| 37 | test_material_inexistente_repetido_ou_lista_incompleta_rejeitados | Material inexistente, duplicado, mesmo do principal ou lista incompleta são recusados |
| 38 | test_falha_no_segundo_consumo_desfaz_primeiro | Se o segundo consumo falha, o primeiro é desfeito automaticamente |
| 39 | test_falha_commit_edicao_preserva_pedido_consumos_saldos_historico | Falha no banco durante edição preserva tudo como estava antes |
| 40 | test_material_associado_nao_pode_ser_excluido_mesmo_sem_movimentacao | Material vinculado a um pedido não pode ser excluído |
| 41 | test_detalhe_busca_e_cancelamento_usam_id_mesmo_apos_renomear | Renomear material não quebra detalhe, busca nem cancelamento |
| 42 | test_migracao_legada_idempotente_sem_baixa_e_reinicio_preserva | Migração de pedidos antigos é feita uma vez só, sem baixar estoque novamente |
| 43 | test_edicao_invalida_preserva_consumos_anteriores | Editar com valor acima do estoque mantém os consumos originais |
| 44 | test_falha_commit_cancelamento_desfaz_todos_os_estornos | Falha no banco durante cancelamento desfaz todos os estornos |
| 45 | test_legado_sem_material_identificavel_nao_e_associado_nem_estornado | Pedido antigo sem material válido não é associado nem estornado |
| 46 | test_constraints_impedem_consumo_zero_e_vinculo_duplicado | Banco recusa consumo de 0 metros e vínculo duplicado por constraints |

### 2.6. test_estoque.py — Materiais e estoque (22 testes)

| # | Teste | O que verifica |
|---|---|---|
| 47 | test_api_identificacao_nao_altera_estoque | Identificar material não altera saldo |
| 48 | test_api_material_por_codigo_existente | API retorna 200 com dados do material identificado |
| 49 | test_api_material_por_codigo_inexistente | API retorna 404 para código que não existe |
| 50 | test_api_material_por_codigo_sem_login | API sem login redireciona para a tela de login |
| 51 | test_buscar_material_por_codigo_barras_service | Busca por código funciona na camada de serviço |
| 52 | test_cadastro_material_com_sucesso | Cadastro com dados válidos salva o material |
| 53 | test_consulta_material_por_codigo_barras_existente | Busca por código existente localiza o material |
| 54 | test_consumo_e_devolucao_material | Baixa e devolução de estoque funcionam corretamente |
| 55 | test_ct03_cadastro_material_codigo_barras_duplicado | Código de barras duplicado é recusado no cadastro |
| 56 | test_ct04_consulta_material_inexistente | Busca por material que não existe retorna página sem resultados |
| 57 | test_ct05_ct07_rota_entrada_estoque_sucesso | Rota de entrada adiciona bobinas e grava no histórico |
| 58 | test_movimentacoes_estoque_exibe_historico | Tela exibe as movimentações registradas |
| 59 | test_movimentacoes_estoque_filtros_tipo_e_material | Filtros por tipo e material funcionam |
| 60 | test_movimentacoes_estoque_mais_recentes_primeiro | Movimentações aparecem da mais recente para a mais antiga |
| 61 | test_movimentacoes_estoque_sem_login | Rota de movimentações exige login |
| 62 | test_registrar_entrada_estoque_service_recusa_quantidade_invalida | Quantidade de bobinas ≤ 0 é recusada |
| 63 | test_registrar_entrada_estoque_service_sucesso | Entrada adiciona bobinas, atualiza metragem e registra movimentação |
| 64 | test_regras_servico_bobinas | Adição, remoção e ajuste de metragem funcionam no serviço |
| 65 | test_rota_entrada_estoque_material_inexistente | Entrada com código inexistente é recusada |
| 66 | test_rota_entrada_estoque_quantidade_invalida | Rota recusa quantidade ≤ 0 |
| 67 | test_rota_entrada_estoque_sem_login | Rota de entrada exige login |
| 68 | test_validacao_campos_invalidos_cadastro_material | Largura ou unidades ≤ 0 são recusadas no cadastro |

### 2.7. test_estoque_minimo.py — Estoque mínimo (8 testes)

| # | Teste | O que verifica |
|---|---|---|
| 69 | test_alerta_somente_quando_saldo_menor_que_minimo | Alerta aparece só quando saldo está abaixo do mínimo configurado |
| 70 | test_bloqueio_edicao_estoque_minimo_para_funcionario | Funcionário não pode alterar o estoque mínimo |
| 71 | test_cadastro_material_com_estoque_minimo_admin | Admin cadastra material com limite mínimo definido |
| 72 | test_edicao_estoque_minimo_admin | Admin edita o estoque mínimo com sucesso |
| 73 | test_filtro_abaixo_minimo_na_tela_estoque | Filtro exibe apenas materiais abaixo do mínimo |
| 74 | test_migracao_estoque_minimo_preservando_dados | Migração garante a coluna sem alterar saldos existentes |
| 75 | test_persistencia_estoque_minimo | Valor do mínimo é salvo corretamente no banco |
| 76 | test_rejeicao_valores_invalidos_estoque_minimo | Valores negativos ou inválidos são recusados |

### 2.8. test_inicializacao_estoque.py — Inicialização e preservação (4 testes)

| # | Teste | O que verifica |
|---|---|---|
| 77 | test_consolidacao_nao_executa_automaticamente | Consolidação de materiais repetidos não roda sozinha na inicialização |
| 78 | test_materiais_com_larguras_diferentes_continuam_separados | Materiais com mesma categoria/nome mas larguras diferentes continuam separados |
| 79 | test_reiniciar_nao_altera_saldo_parcial | Reiniciar o app não mexe no saldo parcial de materiais |
| 80 | test_reiniciar_nao_repoe_material_esgotado | Reiniciar o app não repõe bobinas de material esgotado |

### 2.9. test_migracao_cliente.py — Migração de clientes (3 testes)

| # | Teste | O que verifica |
|---|---|---|
| 81 | test_associa_apenas_nome_exato_unico_e_preserva_dados | Migração associa apenas por nome exato e preserva dados |
| 82 | test_falha_reverte_coluna_dados_e_marcador | Falha na migração reverte todas as alterações |
| 83 | test_reexecucao_nao_reassocia_pedidos_pendentes | Rodar a migração de novo não reassocia pedidos já pendentes |

### 2.10. test_movimentacoes_sprint4.py — Movimentações e integridade (12 testes)

| # | Teste | O que verifica |
|---|---|---|
| 84 | test_adicao_manual_de_bobina_registra_entrada | Adicionar bobina manualmente registra entrada de 1 unidade e 50 metros |
| 85 | test_ajuste_manual_registra_diferenca_e_saldo_anterior_posterior | Ajuste manual registra a diferença e mostra saldo antes/depois |
| 86 | test_cadastro_material_registra_entrada_no_historico | Cadastrar material novo registra entrada no histórico |
| 87 | test_cancelar_pedido_registra_devolucao | Cancelar pedido registra devolução com material, quantidade e motivo |
| 88 | test_criar_pedido_registra_saida_com_todos_os_detalhes | Criar pedido registra saída com todos os detalhes |
| 89 | test_editar_pedido_registra_estorno_e_novo_consumo | Editar pedido registra estorno da versão anterior e novo consumo |
| 90 | test_falha_na_gravacao_desfaz_ambos_saldo_e_historico | Falha no banco desfaz saldo e histórico ao mesmo tempo |
| 91 | test_filtros_e_ordenacao_do_historico | Filtros por tipo e material funcionam; ordenação é da mais recente |
| 92 | test_material_com_movimentacoes_nao_pode_ser_excluido | Material com histórico não pode ser excluído |
| 93 | test_operacao_rejeitada_nao_altera_saldo_nem_historico | Operação inválida não altera saldo nem cria movimentação |
| 94 | test_remocao_manual_de_bobina_registra_saida_da_metragem_removida | Remover bobina registra saída da metragem removida |
| 95 | test_salvar_mesmo_saldo_nao_gera_movimentacao | Salvar o mesmo saldo não cria registro desnecessário |

### 2.11. test_notificacao_persistencia.py — Persistência de notificações (6 testes)

| # | Teste | O que verifica |
|---|---|---|
| 96 | test_ct43_erro_rede_persistido | Erro de rede é salvo no banco com resultado "falha" |
| 97 | test_ct43_falhas_http_persistidas_sem_desfazer_finalizacao | Falhas HTTP são salvas sem desfazer a finalização do pedido |
| 98 | test_ct45_auditoria_destinatario_e_aceite_sem_entrega | Registro de auditoria inclui destinatário e aceite, sem confirmar entrega |
| 99 | test_ct45_outro_status_nao_dispara_e_nova_finalizacao_cria_tentativa | Outro status não dispara; nova finalização cria nova tentativa |
| 100 | test_ct45_repetir_status_nao_duplica_nem_reenvia | Repetir o mesmo status não duplica nem reenvia |
| 101 | test_testing_persiste_bloqueio_e_finaliza_sem_rede | Em modo teste, bloqueia envio e finaliza sem chamada de rede |

### 2.12. test_notificacao_visual.py — Mensagens visuais de notificação (6 testes)

| # | Teste | O que verifica |
|---|---|---|
| 102 | test_ct42_flash_sucesso_e_persistencia | Mensagem de sucesso aparece na tela e é salva no banco |
| 103 | test_ct43_flash_erro_rede_preserva_pedido | Erro de rede mostra aviso na tela mas preserva o pedido |
| 104 | test_ct43_flash_falha_api_preserva_pedido | Falha da API mostra aviso mas preserva o pedido |
| 105 | test_ct44_flash_telefone_ausente | Telefone ausente mostra aviso na tela |
| 106 | test_ct44_flash_telefone_invalido | Telefone inválido mostra aviso na tela |
| 107 | test_flash_bloqueio_testing_sem_http | Em modo teste, mostra bloqueio sem fazer chamada HTTP |

### 2.13. test_notificacoes_historico.py — Histórico de notificações (7 testes)

| # | Teste | O que verifica |
|---|---|---|
| 108 | test_ct46_acesso_exclusivo_administrador | Anônimo redireciona para login; funcionário é bloqueado |
| 109 | test_ct46_consultar_nao_envia_mensagens_nem_altera_registros | Consultar o histórico não envia mensagens nem altera dados |
| 110 | test_ct46_dados_exibidos_corretos | Tabela exibe cliente, pedido, data e resultado corretos |
| 111 | test_ct46_filtros_status | Filtros por status retornam só as notificações correspondentes |
| 112 | test_ct46_lista_vazia | Lista vazia exibe mensagem informativa sem erro |
| 113 | test_ct46_ordenacao_decrescente | Notificações aparecem da mais recente para a mais antiga |
| 114 | test_ct46_paginacao_25_registros | Paginação divide em 25 registros por página |

### 2.14. test_pedidos.py — Pedidos e cálculo de corte (8 testes)

| # | Teste | O que verifica |
|---|---|---|
| 115 | test_atualizar_status_pedido | Atualizar status reflete no banco |
| 116 | test_calculo_aproveitamento_corte_padrao_e_rotacionado | Algoritmo escolhe a orientação que menos desperdiça |
| 117 | test_cancelamento_pedido_estorna_estoque | Cancelar pedido exclui o registro e devolve a metragem |
| 118 | test_cliente_invalido_nao_baixa_estoque | Cliente inválido não consome estoque |
| 119 | test_conversao_medidas | Conversão de cm e m funciona com precisão |
| 120 | test_fluxo_criacao_pedido_com_baixa_estoque | Criar pedido baixa a metragem do material |
| 121 | test_homonimos_selecionados_por_id_e_historico_preservado | Clientes com mesmo nome são identificados por ID |
| 122 | test_legado_editavel_sem_associacao_e_vinculo_explicito | Pedido antigo sem associação pode ser editado e vinculado |

### 2.15. test_whatsapp.py — Integração WhatsApp (9 testes)

| # | Teste | O que verifica |
|---|---|---|
| 123 | test_ct42_sucesso_200_e_201_e_contrato_http | Envio com sucesso retorna dados corretos e respeita o contrato HTTP |
| 124 | test_ct43_erros_de_rede_e_json | Erros de rede e JSON malformado são tratados sem quebrar |
| 125 | test_ct43_falhas_http | Falhas HTTP (400, 500) são registradas corretamente |
| 126 | test_ct44_sem_destinatario_nao_chama_api | Sem destinatário válido, a API da Meta não é chamada |
| 127 | test_desabilitado_status_incompativel_e_credenciais_ausentes | Sistema desabilitado, status incompatível ou credenciais ausentes são tratados |
| 128 | test_normalizacao_e_rejeicao_de_telefones | Telefones são normalizados; inválidos são recusados |
| 129 | test_template_com_parametros_e_hello_world | Template com parâmetros e hello_world são enviados corretamente |
| 130 | test_testing_bloqueia_mesmo_com_configuracao_valida | Em modo teste, envio é bloqueado mesmo com configuração válida |
| 131 | test_webhook_verificacao_e_recebimento_sem_confirmar_entrega | Webhook valida assinatura e recebe eventos sem confirmar entrega |

---

## 3. Contagem por módulo

| Arquivo em tests/ | Executados | Passaram |
|---|---:|---:|
| test_auth.py | 9 | 9 |
| test_cancelamento_pedido.py | 5 | 5 |
| test_clientes.py | 9 | 9 |
| test_codigo_barras_materiais.py | 7 | 7 |
| test_consumo_material.py | 16 | 16 |
| test_estoque.py | 22 | 22 |
| test_estoque_minimo.py | 8 | 8 |
| test_inicializacao_estoque.py | 4 | 4 |
| test_migracao_cliente.py | 3 | 3 |
| test_movimentacoes_sprint4.py | 12 | 12 |
| test_notificacao_persistencia.py | 6 | 6 |
| test_notificacao_visual.py | 6 | 6 |
| test_notificacoes_historico.py | 7 | 7 |
| test_pedidos.py | 8 | 8 |
| test_whatsapp.py | 9 | 9 |
| **Total** | **131** | **131** |

Os 16 testes de `test_consumo_material.py` são novos da E10 e cobrem a relação N:N por ConsumoMaterial. Os demais 115 testes já existiam e continuam passando normalmente.

---

## 4. Bugs encontrados nesta bateria

Nenhum teste falhou. Registramos abaixo os avisos de manutenção observados durante a execução.

| # | Descrição | Severidade | Status |
|---|---|---|---|
| E9-T01 | Uso de `datetime.utcnow()` gera DeprecationWarning | Baixa — manutenção | Pendente; sem falha na bateria |
| E9-T02 | Uso de `Query.get()` gera LegacyAPIWarning | Baixa — manutenção | Pendente; sem falha na bateria |

---

## 5. Testes de aceitação com cliente real e PO

**Cliente Real / Homologador:** Paulo Rogério Leite, Proprietário da Center Comunicação Visual.<br>
**Product Owner da Equipe:** Breno Tales de Oliveira Leite.<br>
**Data da avaliação:** 15/11/2026.<br>
**Participantes:** Paulo Rogério Leite (Cliente Real), Breno Tales de Oliveira Leite (RA: 2840482423029) e Daniel Fredi Soares Pereira (RA: 2840482421054).<br>
**Resultado:** escopo aceito sem ressalvas pelo cliente real e validado pela equipe.

| ID | Área avaliada | Referência E2b | Resultado e evidência | Parecer do Cliente Real |
|---|---|---|---|---|
| AM01 | Autenticação e permissões | 1 | Suíte aprovada: login, sessão, permissões e bloqueios por perfil | Aceito |
| AM02 | Cadastro, consulta e identificação de materiais | 2, 3, 4 | Suíte aprovada: códigos válidos e inexistentes, duplicidade e busca | Aceito |
| AM03 | Entrada por código de barras e histórico | 5, 6 | Suíte aprovada: entrada atualiza saldo e movimentação | Aceito |
| AM04 | Pedidos, movimentações e consumo N:N | 6, 7, E10 | Suíte aprovada: status, consumo, edição, estorno e múltiplos materiais por pedido | Aceito |
| AM05 | Notificações pelo WhatsApp | 8, 9 | [Captura do pedido #3](screenshots/whatsapp-pedido-3.png): mensagem recebida às 00:36. Suíte com mocks aprovada | Aceito |
| AM06 | Histórico de notificações | 10 | Suíte aprovada: acesso administrativo, filtros, paginação e consulta sem reenvio | Aceito |
| AM07 | Estoque mínimo | 11 | Suíte aprovada: configuração, alerta e filtro de reposição | Aceito |
| AM08 | Validações e integridade | Transversal | Suíte aprovada: cancelamento por status, operações inválidas, atomicidade e preservação de saldo | Aceito |

**WhatsApp em ambiente real:** o webhook está configurado e as mensagens enviadas pelo sistema estão chegando ao cliente. O [anexo de evidências](E9-evidencias-aceitacao.md) reúne os registros disponíveis; a [captura anexada](screenshots/whatsapp-pedido-3.png) comprova o recebimento da notificação do pedido #3 às 00:36.
