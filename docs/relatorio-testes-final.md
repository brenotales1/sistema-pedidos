# Relatório de Testes Executados — Sistema Web de Controle de Estoque para Empresa de Comunicação Visual

**Entrega:** E9 — Relatório consolidado de testes executados<br>
**Equipe:** Breno Tales de Oliveira Leite (RA: 2840482423029) — Daniel Fredi Soares Pereira (RA: 2840482421054) · Laboratório de Engenharia de Software · ADS Fatec Ribeirão Preto<br>
**Data da bateria final:** 15/11/2026<br>
**Referência de calendário da entrega:** Semana 13 (06/11/2026)<br>
**Versão avaliada:** commit `caed757`<br>
**Escopo testado:** funcionalidades Must + Should, itens 1 a 11 do [Termo de Aceite do Projeto — E2b](E2-termo-de-aceite.md).<br>
**Situação:** regressão automatizada concluída; escopo aceito pelo PO; assinatura pendente.

---

## 1. Resumo executivo

| Métrica | Valor |
|---|---|
| Total de testes automatizados executados | 115 |
| Passaram | 115 |
| Falharam | 0 |
| Erros de execução | 0 |
| Testes ignorados | 0 |
| Taxa de sucesso da suíte | 100% |
| Duração informada pelo runner | 28,515 segundos |
| Casos do plano consolidados | CT01–CT55 (55 cenários; não equivalem a 55 métodos de teste) |
| Cobertura automatizada (linhas/branches) | Não mensurada; ferramenta coverage não instalada no ambiente |
| Aceite do cliente/PO | Aceito pelo PO; assinatura pendente |
| Avaliação do escopo pelo PO | Aceito pelo PO; ver seção 4 |

A execução atual confirma a regressão dos módulos de autenticação, clientes, pedidos, estoque e notificações. Os cenários negativos aprovados comprovam a rejeição esperada de entradas ou operações inválidas; não representam testes falhos. A taxa de sucesso de 100% refere-se aos testes executados, sem equivaler a 100% de cobertura do código ou à aprovação formal do cliente.

### Ambiente e reprodução

Python do ambiente virtual local (`.venv`), runner `unittest`, Flask Test Client, SQLite isolado de testes e `unittest.mock` nas chamadas externas. A suíte automatizada utiliza simulações e não comprova leitura por equipamento físico nem entrega real de mensagens. Separadamente, a equipe confirmou que o webhook foi configurado e que as mensagens estão chegando ao cliente; ver seção 4.

Comando executado no PowerShell, na raiz do projeto:

```powershell
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -v
```

Resumo retornado pelo runner nesta execução:

```text
Ran 115 tests in 28.515s

OK
```

O bloco acima é um extrato do resultado, não o log integral. Durante a execução ocorreram avisos de depreciação de `datetime.utcnow()` e `Query.get()`, sem reprovação de testes.

---

## 2. Casos de teste — visão consolidada

A referência é o [plano atualizado](plano-de-testes.md), derivado do [plano E4b](E4-plano-de-testes.md), e as evidências das [Sprints 1](sprints/sprint-1-evidencias-teste.md), [2](sprints/sprint-2-evidencias-teste.md), [3](sprints/sprint-3-evidencias-teste.md) e [4](sprints/sprint-4-evidencias-teste.md). A tabela agrupa os 55 IDs sem somar execuções repetidas de sprints anteriores.

| ID | Área | Tipo | Resultado | Observação / evidência |
|---|---|---|---|---|
| CT01–CT02, CT08–CT14 | Autenticação, sessão e permissões — US #1 | Unitário / integração | Passou | `tests/test_auth.py`; login, logout, hash e acesso por perfil |
| CT03–CT07, CT20–CT29 | Cadastro, consulta, identificação e entrada de materiais — US #2–#5 | Unitário / integração | Passou | `tests/test_estoque.py`; códigos válidos/inexistentes/duplicados, validações, saldo e movimentação |
| CT15–CT19 | Cadastro, edição e consulta de clientes | Integração | Passou | `tests/test_clientes.py`; suporte ao fluxo de pedidos |
| CT30–CT35 | Histórico, filtros, bobinas, baixa e estorno — US #6 | Unitário / integração | Passou | `tests/test_estoque.py`; acesso, ordenação e consistência |
| CT36–CT40 | Medidas, corte e ciclo do pedido — US #7 e suporte | Unitário / integração | Passou | `tests/test_pedidos.py`; cálculo, consumo, cancelamento e status |
| CT41 | Isolamento dos testes | Configuração da suíte | Atendido na execução | Bancos isolados configurados pelos testes; cenário transversal, não um método adicional |
| CT42–CT45 | Notificações e disparo automático — US #7–#9 | Unitário / integração com mocks | Passou | `test_whatsapp.py`, `test_notificacao_visual.py` e `test_notificacao_persistencia.py`; sucesso, erros, telefone inválido e não duplicação |
| CT46 | Histórico de notificações — US #10 | Integração | Passou | `tests/test_notificacoes_historico.py`; admin, filtros, paginação e consulta sem reenvio |
| CT47–CT49 | Movimentações de pedidos e manuais; integridade — US #6 | Integração | Passou | `tests/test_movimentacoes_sprint4.py`; estorno, atomicidade e bloqueio de exclusão |
| CT50 | Estoque mínimo — US #11 | Integração | Passou | `tests/test_estoque_minimo.py`; limite, permissões, persistência e filtro |
| CT51 | Cancelamento conforme status | Integração | Passou | `tests/test_cancelamento_pedido.py`; bloqueio inclusive por POST direto |
| CT52 | Regularização de códigos de barras — US #2–#5 | Integração | Passou | `tests/test_codigo_barras_materiais.py`; preservação de estoque/histórico |
| CT53 | Preservação do estoque na inicialização | Integração | Passou | `tests/test_inicializacao_estoque.py`; saldos zerados/parciais e larguras distintas |
| CT54–CT55 | Duplicidade e identificador de cliente | Integração | Passou | `tests/test_clientes.py`; validação e identificador #ID |

Os nomes de arquivos sem diretório na linha CT42–CT45 pertencem a `tests/`. Os cenários complementares de migração e associação de clientes, contrato HTTP, templates e webhook também foram incluídos na suíte.

### 2.1. Contagem por módulo na bateria final

| Arquivo em tests/ | Executados | Passaram |
|---|---:|---:|
| test_auth.py | 9 | 9 |
| test_clientes.py | 9 | 9 |
| test_pedidos.py | 8 | 8 |
| test_migracao_cliente.py | 3 | 3 |
| test_estoque.py | 22 | 22 |
| test_whatsapp.py | 9 | 9 |
| test_notificacao_visual.py | 6 | 6 |
| test_notificacao_persistencia.py | 6 | 6 |
| test_movimentacoes_sprint4.py | 12 | 12 |
| test_notificacoes_historico.py | 7 | 7 |
| test_estoque_minimo.py | 8 | 8 |
| test_cancelamento_pedido.py | 5 | 5 |
| test_inicializacao_estoque.py | 4 | 4 |
| test_codigo_barras_materiais.py | 7 | 7 |
| **Total** | **115** | **115** |

**Conciliação das evidências anteriores:** corrigimos a contagem da seção 7 do plano de 111 para 115 testes, incluindo as quatro ampliações nos módulos já existentes. O plano, a evidência E8 e esta bateria passam a apresentar o mesmo total.

---

## 3. Bugs encontrados nesta bateria

Nenhum teste automatizado falhou nesta rodada. Registramos abaixo a correção da contagem no plano e os avisos de manutenção observados durante a execução.

| # | Descrição | Severidade | Status |
|---|---|---|---|
| E9-D01 | Plano informava 111 testes, omitindo quatro ampliações nos módulos existentes | Baixa — documental | Corrigido: seção 7 atualizada para 115 testes |
| E9-T01 | Uso de `datetime.utcnow()` gera DeprecationWarning | Baixa — manutenção | Pendente de atualização; sem falha observada na bateria |
| E9-T02 | Uso de `Query.get()` gera LegacyAPIWarning | Baixa — manutenção | Pendente de atualização; sem falha observada na bateria |

As correções de cancelamento seguro, estoque mínimo e atomicidade já descritas na [retrospectiva da Sprint 4](sprints/sprint-4-retrospectiva.md) são antecedentes da regressão, não bugs novos desta rodada. Seus testes passaram nesta execução.

---

## 4. Testes de aceitação com cliente/PO

**Cliente/PO:** Breno Tales de Oliveira Leite, dono do produto conforme E2b.<br>
**Data da avaliação:** 15/11/2026.<br>
**Participantes:** Breno Tales de Oliveira Leite (RA: 2840482423029) e Daniel Fredi Soares Pereira (RA: 2840482421054).<br>
**Resultado:** escopo aceito sem ressalvas pelo PO. Assinatura pendente no termo E9b.

Registramos abaixo o parecer do PO e os resultados disponíveis para cada área. Os resultados automatizados têm referência na seção 2. Para o WhatsApp, também registramos a confirmação de recebimento pelo cliente. Não há descrição individual dos demais testes manuais; por isso, seus resultados técnicos são identificados como automatizados.

| ID | Área avaliada | Referência E2b | Resultado registrado e origem da evidência | Parecer do PO |
|---|---|---|---|---|
| AM01 | Autenticação e permissões | 1 | Suíte automatizada aprovada: login, sessão, permissões e bloqueios por perfil | Aceito |
| AM02 | Cadastro, consulta e identificação de materiais | 2, 3, 4 | Suíte automatizada aprovada: códigos válidos e inexistentes, duplicidade e busca por código | Aceito |
| AM03 | Entrada por código de barras e histórico | 5, 6 | Suíte automatizada aprovada: entrada atualiza saldo e movimentação. Sem registro anexado de uso de leitor físico | Aceito |
| AM04 | Andamento dos pedidos e movimentações | 6, 7 | Suíte automatizada aprovada: atualização de status, consumo, edição e estorno | Aceito |
| AM05 | Notificações pelo WhatsApp | 8, 9 | Validação real: [captura do pedido #3](screenshots/whatsapp-pedido-3.png) mostra a mensagem recebida às 00:36. Webhook configurado conforme avaliação. Suíte com mocks aprovada para falhas e repetição de status | Aceito |
| AM06 | Histórico de notificações | 10 | Suíte automatizada aprovada: acesso administrativo, filtros, paginação e consulta sem reenvio | Aceito |
| AM07 | Estoque mínimo | 11 | Suíte automatizada aprovada: configuração, alerta abaixo do limite e filtro de reposição | Aceito |
| AM08 | Validações e integridade | Transversal | Suíte automatizada aprovada: cancelamento por status, operações inválidas e preservação de saldo na inicialização | Aceito |

**WhatsApp em ambiente real:** o webhook está configurado e as mensagens enviadas pelo sistema estão chegando ao cliente. Registramos essa confirmação em 15/11/2026, separadamente dos 115 testes automatizados. O [anexo de evidências](E9-evidencias-aceitacao.md) reúne os registros disponíveis; a [captura anexada](screenshots/whatsapp-pedido-3.png) comprova o recebimento da notificação do pedido #3 às 00:36. Não há log do provedor anexado.

**Formalização:** falta anexar a assinatura física/digital ou o e-mail de confirmação do PO ao [Termo de Aceite do Cliente — E9b](E9-termo-de-aceite-cliente.md).



## 5. Atualização posterior — N:N na E10

Após esta bateria de 115 testes, implementamos a relação N:N Pedido–Material por ConsumoMaterial. A nova suíte foi executada separadamente, com **131 testes aprovados** (115 anteriores e 16 novos). O [relatório complementar](E10-validacao-nn.md) e o [log](E10-testes-nn.txt) registram essa execução.

O resultado e o aceite históricos das seções anteriores correspondem à versão originalmente avaliada. A mudança de interface e de modelo foi validada localmente; não foi apresentada como uma nova aprovação do PO nem como funcionalidade já publicada no Render.
