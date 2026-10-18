# Evidências de Teste — Sprint 3 — Sistema de Pedidos e Controle de Estoque

**Equipe:** Breno Tales de Oliveira Leite (RA: 2840482423029) — Daniel Fredi Soares Pereira (RA: 2840482421054) · Laboratório de Engenharia de Software · ADS Fatec Ribeirão Preto  
**Consolidação:** 18/10/2026 — Entrega E7

---

## 1. Tabela de Execução de Casos de Teste

| ID | Caso de teste | Tipo | Resultado | Evidência |
|:---:|---|:---:|:---:|---|
| **CT42** | HTTP 200/201 retorna aceite e envia o payload correto à Meta | Unitário | **Passou** | `tests/test_whatsapp.py:test_ct42_sucesso_200_e_201_e_contrato_http` |
| **CT42** | Aceite exibe flash de sucesso e persiste o resultado | Integração | **Passou** | `tests/test_notificacao_visual.py:test_ct42_flash_sucesso_e_persistencia` |
| **CT43** | HTTP 400/500 retorna falha com código de erro | Unitário | **Passou** | `tests/test_whatsapp.py:test_ct43_falhas_http` |
| **CT43** | Erros de rede e JSON inválido são tratados | Unitário | **Passou** | `tests/test_whatsapp.py:test_ct43_erros_de_rede_e_json` |
| **CT43** | Falha da API exibe flash de erro e preserva o pedido | Integração | **Passou** | `tests/test_notificacao_visual.py:test_ct43_flash_falha_api_preserva_pedido` |
| **CT43** | Timeout exibe flash de erro e preserva o pedido | Integração | **Passou** | `tests/test_notificacao_visual.py:test_ct43_flash_erro_rede_preserva_pedido` |
| **CT43** | Falhas HTTP são persistidas sem desfazer a finalização | Integração | **Passou** | `tests/test_notificacao_persistencia.py:test_ct43_falhas_http_persistidas_sem_desfazer_finalizacao` |
| **CT43** | Erro de conexão é persistido como falha | Integração | **Passou** | `tests/test_notificacao_persistencia.py:test_ct43_erro_rede_persistido` |
| **CT44** | Telefone inválido/ausente ou cliente ausente impede chamada à API | Unitário | **Passou** | `tests/test_whatsapp.py:test_ct44_sem_destinatario_nao_chama_api` |
| **CT44** | Telefone inválido exibe orientação de correção | Integração | **Passou** | `tests/test_notificacao_visual.py:test_ct44_flash_telefone_invalido` |
| **CT44** | Telefone ausente exibe orientação de correção | Integração | **Passou** | `tests/test_notificacao_visual.py:test_ct44_flash_telefone_ausente` |
| **CT45** | Tentativa registra cliente, pedido e histórico, sem confirmar entrega | Integração | **Passou** | `tests/test_notificacao_persistencia.py:test_ct45_auditoria_destinatario_e_aceite_sem_entrega` |
| **CT45** | Repetir status não duplica tentativa nem reenvia mensagem | Integração | **Passou** | `tests/test_notificacao_persistencia.py:test_ct45_repetir_status_nao_duplica_nem_reenvia` |
| **CT45** | Outros status não enviam; nova finalização cria nova tentativa | Integração | **Passou** | `tests/test_notificacao_persistencia.py:test_ct45_outro_status_nao_dispara_e_nova_finalizacao_cria_tentativa` |
| **Complementar** | Normalização E.164 e rejeição de telefones inválidos | Unitário | **Passou** | `tests/test_whatsapp.py:test_normalizacao_e_rejeicao_de_telefones` |
| **Complementar** | Templates com parâmetros e hello_world usam payload esperado | Unitário | **Passou** | `tests/test_whatsapp.py:test_template_com_parametros_e_hello_world` |
| **Complementar** | Testing bloqueia envio mesmo com configuração válida | Unitário | **Passou** | `tests/test_whatsapp.py:test_testing_bloqueia_mesmo_com_configuracao_valida` |
| **Complementar** | Serviço desabilitado, status incompatível e credenciais ausentes impedem envio | Unitário | **Passou** | `tests/test_whatsapp.py:test_desabilitado_status_incompativel_e_credenciais_ausentes` |
| **Complementar** | Webhook valida inscrição e recebe evento sem confirmar entrega | Integração | **Passou** | `tests/test_whatsapp.py:test_webhook_verificacao_e_recebimento_sem_confirmar_entrega` |
| **Complementar** | Bloqueio testing exibe flash sem chamada HTTP | Integração | **Passou** | `tests/test_notificacao_visual.py:test_flash_bloqueio_testing_sem_http` |
| **Complementar** | Bloqueio testing é persistido e pedido finaliza sem rede | Integração | **Passou** | `tests/test_notificacao_persistencia.py:test_testing_persiste_bloqueio_e_finaliza_sem_rede` |

A tabela detalha os 21 testes adicionados nesta sprint. CT42–CT45 possuem múltiplas verificações automatizadas, apresentadas individualmente. Os testes complementares não recebem novos IDs formais.

Os 47 testes anteriores também foram aprovados na execução completa, abrangendo autenticação, clientes, estoque, pedidos e migração. Os rótulos CT08/CT09 de notificações do planejamento antigo correspondem a CT42–CT45; os IDs históricos de autenticação foram preservados. Consulte o [plano de testes](../plano-de-testes.md#6-execução-formal--sprint-3-e7).

---

## 2. Cobertura Automatizada nesta Sprint

- **Framework de Testes:** Python `unittest` com Flask Test Client e `unittest.mock`
- **Total de Testes:** 68 testes automatizados (47 existentes e 21 novos)
- **Taxa de Sucesso:** 100% (68 passaram, 0 falhas, 0 erros)
- **Tempo de Execução:** 14,737 segundos
- **Banco de Testes:** SQLite em memória (`sqlite:///:memory:`)
- **Comando de Execução:**

```powershell
$env:Path = "$PWD\.venv\Scripts;$env:Path"
python -B -m unittest discover -s tests -q
```

A execução utiliza o ambiente virtual existente do projeto. Os novos testes usam credenciais fictícias, mock de `requests.post` e bloqueio adicional da sessão HTTP, sem envio real de mensagens. O log abaixo foi preservado integralmente da execução já registrada; esta alteração modifica apenas a apresentação do documento.

### Log de Execução:


```text
C:\Users\T-GAMER\sistema-pedidos\.venv\Lib\site-packages\flask_sqlalchemy\query.py:30: LegacyAPIWarning: The Query.get() method is considered legacy as of the 1.x series of SQLAlchemy and becomes a legacy construct in 2.0. The method is now available as Session.get() (deprecated since: 2.0) (Background on SQLAlchemy 2.0 at: https://sqlalche.me/e/b8d9)
  rv = self.get(ident)
C:\Users\T-GAMER\sistema-pedidos\tests\test_clientes.py:89: LegacyAPIWarning: The Query.get() method is considered legacy as of the 1.x series of SQLAlchemy and becomes a legacy construct in 2.0. The method is now available as Session.get() (deprecated since: 2.0) (Background on SQLAlchemy 2.0 at: https://sqlalche.me/e/b8d9)
  cli_atualizado = Cliente.query.get(cli_id)
C:\Users\T-GAMER\sistema-pedidos\services\estoque_service.py:57: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
  data_hora=datetime.utcnow(),
C:\Users\T-GAMER\sistema-pedidos\.venv\Lib\site-packages\sqlalchemy\sql\schema.py:4296: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
  return util.wrap_callable(lambda ctx: fn(), fn)  # type: ignore[call-arg, no-any-return, no-untyped-call]  # noqa: E501
[2026-10-18 02:55:25,557] INFO in whatsapp_service: WhatsApp avaliacao: pedido=1
[2026-10-18 02:55:25,559] INFO in whatsapp_service: WhatsApp Meta solicitacao: pedido=1 destino=5511999999999
[2026-10-18 02:55:25,559] WARNING in whatsapp_service: Falha WhatsApp Meta: pedido=1 motivo=erro_no_envio
[2026-10-18 02:55:25,559] WARNING in whatsapp_service: WhatsApp resultado: pedido=1 envio_solicitado=True resultado=falha msg_id=None codigo_erro=None
[2026-10-18 02:55:25,604] INFO in whatsapp_service: WhatsApp avaliacao: pedido=1
[2026-10-18 02:55:25,605] INFO in whatsapp_service: WhatsApp Meta solicitacao: pedido=1 destino=5511999999999
[2026-10-18 02:55:25,605] WARNING in whatsapp_service: Falha WhatsApp Meta: pedido=1 status_http=400 resposta=<Mock name='post().text' id='1479042537456'>
[2026-10-18 02:55:25,605] WARNING in whatsapp_service: WhatsApp resultado: pedido=1 envio_solicitado=True resultado=falha msg_id=None codigo_erro=400
[2026-10-18 02:55:25,619] INFO in pedido_service: WhatsApp transicao: pedido=1 envio_solicitado=False resultado=sem_transicao_para_finalizado
[2026-10-18 02:55:25,623] INFO in whatsapp_service: WhatsApp avaliacao: pedido=1
[2026-10-18 02:55:25,623] INFO in whatsapp_service: WhatsApp Meta solicitacao: pedido=1 destino=5511999999999
[2026-10-18 02:55:25,623] WARNING in whatsapp_service: Falha WhatsApp Meta: pedido=1 status_http=500 resposta=<Mock name='post().text' id='1479042537456'>
[2026-10-18 02:55:25,623] WARNING in whatsapp_service: WhatsApp resultado: pedido=1 envio_solicitado=True resultado=falha msg_id=None codigo_erro=500
[2026-10-18 02:55:25,629] INFO in pedido_service: WhatsApp transicao: pedido=1 envio_solicitado=False resultado=sem_transicao_para_finalizado
[2026-10-18 02:55:25,659] INFO in whatsapp_service: WhatsApp avaliacao: pedido=1
[2026-10-18 02:55:25,659] INFO in whatsapp_service: WhatsApp Meta solicitacao: pedido=1 destino=5511999999999
[2026-10-18 02:55:25,659] INFO in whatsapp_service: WhatsApp aceito pela Meta: pedido=1 msg_id=wamid.TESTE123
[2026-10-18 02:55:25,659] INFO in whatsapp_service: WhatsApp resultado: pedido=1 envio_solicitado=True resultado=aceito msg_id=wamidTESTE123 codigo_erro=None
[2026-10-18 02:55:25,702] INFO in pedido_service: WhatsApp transicao: pedido=1 envio_solicitado=False resultado=sem_transicao_para_finalizado
[2026-10-18 02:55:25,718] INFO in whatsapp_service: WhatsApp avaliacao: pedido=1
[2026-10-18 02:55:25,719] INFO in whatsapp_service: WhatsApp Meta solicitacao: pedido=1 destino=5511999999999
[2026-10-18 02:55:25,719] INFO in whatsapp_service: WhatsApp aceito pela Meta: pedido=1 msg_id=wamid.TESTE123
[2026-10-18 02:55:25,719] INFO in whatsapp_service: WhatsApp resultado: pedido=1 envio_solicitado=True resultado=aceito msg_id=wamidTESTE123 codigo_erro=None
[2026-10-18 02:55:25,724] INFO in pedido_service: WhatsApp transicao: pedido=1 envio_solicitado=False resultado=sem_transicao_para_finalizado
[2026-10-18 02:55:25,727] INFO in whatsapp_service: WhatsApp avaliacao: pedido=1
[2026-10-18 02:55:25,727] INFO in whatsapp_service: WhatsApp Meta solicitacao: pedido=1 destino=5511999999999
[2026-10-18 02:55:25,727] INFO in whatsapp_service: WhatsApp aceito pela Meta: pedido=1 msg_id=wamid.TESTE123
[2026-10-18 02:55:25,727] INFO in whatsapp_service: WhatsApp resultado: pedido=1 envio_solicitado=True resultado=aceito msg_id=wamidTESTE123 codigo_erro=None
[2026-10-18 02:55:25,774] INFO in whatsapp_service: WhatsApp avaliacao: pedido=1
[2026-10-18 02:55:25,775] INFO in whatsapp_service: WhatsApp Meta solicitacao: pedido=1 destino=5511999999999
[2026-10-18 02:55:25,775] INFO in whatsapp_service: WhatsApp aceito pela Meta: pedido=1 msg_id=wamid.TESTE123
[2026-10-18 02:55:25,775] INFO in whatsapp_service: WhatsApp resultado: pedido=1 envio_solicitado=True resultado=aceito msg_id=wamidTESTE123 codigo_erro=None
[2026-10-18 02:55:25,787] INFO in pedido_service: WhatsApp transicao: pedido=1 envio_solicitado=False resultado=status_inalterado
[2026-10-18 02:55:25,820] INFO in whatsapp_service: WhatsApp avaliacao: pedido=1
[2026-10-18 02:55:25,820] INFO in whatsapp_service: WhatsApp resultado: pedido=1 envio_solicitado=False resultado=bloqueado_testing msg_id=None codigo_erro=None
[2026-10-18 02:55:25,860] INFO in whatsapp_service: WhatsApp avaliacao: pedido=1
[2026-10-18 02:55:25,861] INFO in whatsapp_service: WhatsApp Meta solicitacao: pedido=1 destino=5511999999999
[2026-10-18 02:55:25,861] INFO in whatsapp_service: WhatsApp aceito pela Meta: pedido=1 msg_id=wamid.TESTE123
[2026-10-18 02:55:25,861] INFO in whatsapp_service: WhatsApp resultado: pedido=1 envio_solicitado=True resultado=aceito msg_id=wamidTESTE123 codigo_erro=None
[2026-10-18 02:55:25,903] INFO in whatsapp_service: WhatsApp avaliacao: pedido=1
[2026-10-18 02:55:25,904] INFO in whatsapp_service: WhatsApp Meta solicitacao: pedido=1 destino=5511999999999
[2026-10-18 02:55:25,904] WARNING in whatsapp_service: Falha WhatsApp Meta: pedido=1 motivo=erro_no_envio
[2026-10-18 02:55:25,904] WARNING in whatsapp_service: WhatsApp resultado: pedido=1 envio_solicitado=True resultado=falha msg_id=None codigo_erro=None
[2026-10-18 02:55:25,944] INFO in whatsapp_service: WhatsApp avaliacao: pedido=1
[2026-10-18 02:55:25,944] INFO in whatsapp_service: WhatsApp Meta solicitacao: pedido=1 destino=5511999999999
[2026-10-18 02:55:25,944] WARNING in whatsapp_service: Falha WhatsApp Meta: pedido=1 status_http=500 resposta=<Mock name='post().text' id='1479071550496'>
[2026-10-18 02:55:25,944] WARNING in whatsapp_service: WhatsApp resultado: pedido=1 envio_solicitado=True resultado=falha msg_id=None codigo_erro=500
[2026-10-18 02:55:25,986] INFO in whatsapp_service: WhatsApp avaliacao: pedido=1
[2026-10-18 02:55:25,986] INFO in whatsapp_service: WhatsApp ignorado: pedido=1 motivo=cliente_ou_telefone_invalido
[2026-10-18 02:55:25,986] INFO in whatsapp_service: WhatsApp resultado: pedido=1 envio_solicitado=False resultado=sem_destinatario msg_id=None codigo_erro=None
[2026-10-18 02:55:26,030] INFO in whatsapp_service: WhatsApp avaliacao: pedido=1
[2026-10-18 02:55:26,030] INFO in whatsapp_service: WhatsApp ignorado: pedido=1 motivo=cliente_ou_telefone_invalido
[2026-10-18 02:55:26,030] INFO in whatsapp_service: WhatsApp resultado: pedido=1 envio_solicitado=False resultado=sem_destinatario msg_id=None codigo_erro=None
[2026-10-18 02:55:26,071] INFO in whatsapp_service: WhatsApp avaliacao: pedido=1
[2026-10-18 02:55:26,071] INFO in whatsapp_service: WhatsApp resultado: pedido=1 envio_solicitado=False resultado=bloqueado_testing msg_id=None codigo_erro=None
[2026-10-18 02:55:26,401] INFO in pedido_service: WhatsApp transicao: pedido=1 envio_solicitado=False resultado=sem_transicao_para_finalizado
C:\Users\T-GAMER\sistema-pedidos\tests\test_pedidos.py:226: LegacyAPIWarning: The Query.get() method is considered legacy as of the 1.x series of SQLAlchemy and becomes a legacy construct in 2.0. The method is now available as Session.get() (deprecated since: 2.0) (Background on SQLAlchemy 2.0 at: https://sqlalche.me/e/b8d9)
  pedido_atualizado = Pedido.query.get(pedido_id)
C:\Users\T-GAMER\sistema-pedidos\tests\test_pedidos.py:189: LegacyAPIWarning: The Query.get() method is considered legacy as of the 1.x series of SQLAlchemy and becomes a legacy construct in 2.0. The method is now available as Session.get() (deprecated since: 2.0) (Background on SQLAlchemy 2.0 at: https://sqlalche.me/e/b8d9)
  pedido_cancelado = Pedido.query.get(pedido_id)
[2026-10-18 02:55:28,488] INFO in whatsapp_service: WhatsApp avaliacao: pedido=42
[2026-10-18 02:55:28,488] INFO in whatsapp_service: WhatsApp Meta solicitacao: pedido=42 destino=5511999999999
[2026-10-18 02:55:28,488] INFO in whatsapp_service: WhatsApp aceito pela Meta: pedido=42 msg_id=wamid.TESTE123
[2026-10-18 02:55:28,488] INFO in whatsapp_service: WhatsApp resultado: pedido=42 envio_solicitado=True resultado=aceito msg_id=wamidTESTE123 codigo_erro=None
[2026-10-18 02:55:28,488] INFO in whatsapp_service: WhatsApp avaliacao: pedido=42
[2026-10-18 02:55:28,488] INFO in whatsapp_service: WhatsApp Meta solicitacao: pedido=42 destino=5511999999999
[2026-10-18 02:55:28,488] INFO in whatsapp_service: WhatsApp aceito pela Meta: pedido=42 msg_id=wamid.TESTE123
[2026-10-18 02:55:28,488] INFO in whatsapp_service: WhatsApp resultado: pedido=42 envio_solicitado=True resultado=aceito msg_id=wamidTESTE123 codigo_erro=None
[2026-10-18 02:55:28,512] INFO in whatsapp_service: WhatsApp avaliacao: pedido=42
[2026-10-18 02:55:28,512] INFO in whatsapp_service: WhatsApp Meta solicitacao: pedido=42 destino=5511999999999
[2026-10-18 02:55:28,512] WARNING in whatsapp_service: Falha WhatsApp Meta: pedido=42 motivo=erro_no_envio
[2026-10-18 02:55:28,512] WARNING in whatsapp_service: WhatsApp resultado: pedido=42 envio_solicitado=True resultado=falha msg_id=None codigo_erro=None
[2026-10-18 02:55:28,512] INFO in whatsapp_service: WhatsApp avaliacao: pedido=42
[2026-10-18 02:55:28,512] INFO in whatsapp_service: WhatsApp Meta solicitacao: pedido=42 destino=5511999999999
[2026-10-18 02:55:28,512] WARNING in whatsapp_service: Falha WhatsApp Meta: pedido=42 motivo=erro_no_envio
[2026-10-18 02:55:28,512] WARNING in whatsapp_service: WhatsApp resultado: pedido=42 envio_solicitado=True resultado=falha msg_id=None codigo_erro=None
[2026-10-18 02:55:28,513] INFO in whatsapp_service: WhatsApp avaliacao: pedido=42
[2026-10-18 02:55:28,513] INFO in whatsapp_service: WhatsApp Meta solicitacao: pedido=42 destino=5511999999999
[2026-10-18 02:55:28,513] WARNING in whatsapp_service: Falha WhatsApp Meta: pedido=42 motivo=erro_no_envio
[2026-10-18 02:55:28,513] WARNING in whatsapp_service: WhatsApp resultado: pedido=42 envio_solicitado=True resultado=falha msg_id=None codigo_erro=None
[2026-10-18 02:55:28,536] INFO in whatsapp_service: WhatsApp avaliacao: pedido=42
[2026-10-18 02:55:28,536] INFO in whatsapp_service: WhatsApp Meta solicitacao: pedido=42 destino=5511999999999
[2026-10-18 02:55:28,536] WARNING in whatsapp_service: Falha WhatsApp Meta: pedido=42 status_http=400 resposta=Erro simulado
[2026-10-18 02:55:28,536] WARNING in whatsapp_service: WhatsApp resultado: pedido=42 envio_solicitado=True resultado=falha msg_id=None codigo_erro=400
[2026-10-18 02:55:28,536] INFO in whatsapp_service: WhatsApp avaliacao: pedido=42
[2026-10-18 02:55:28,536] INFO in whatsapp_service: WhatsApp Meta solicitacao: pedido=42 destino=5511999999999
[2026-10-18 02:55:28,536] WARNING in whatsapp_service: Falha WhatsApp Meta: pedido=42 status_http=500 resposta=Erro simulado
[2026-10-18 02:55:28,536] WARNING in whatsapp_service: WhatsApp resultado: pedido=42 envio_solicitado=True resultado=falha msg_id=None codigo_erro=500
[2026-10-18 02:55:28,560] INFO in whatsapp_service: WhatsApp avaliacao: pedido=42
[2026-10-18 02:55:28,560] INFO in whatsapp_service: WhatsApp ignorado: pedido=42 motivo=cliente_ou_telefone_invalido
[2026-10-18 02:55:28,560] INFO in whatsapp_service: WhatsApp resultado: pedido=42 envio_solicitado=False resultado=sem_destinatario msg_id=None codigo_erro=None
[2026-10-18 02:55:28,560] INFO in whatsapp_service: WhatsApp avaliacao: pedido=42
[2026-10-18 02:55:28,560] INFO in whatsapp_service: WhatsApp ignorado: pedido=42 motivo=cliente_ou_telefone_invalido
[2026-10-18 02:55:28,560] INFO in whatsapp_service: WhatsApp resultado: pedido=42 envio_solicitado=False resultado=sem_destinatario msg_id=None codigo_erro=None
[2026-10-18 02:55:28,560] INFO in whatsapp_service: WhatsApp avaliacao: pedido=42
[2026-10-18 02:55:28,560] INFO in whatsapp_service: WhatsApp ignorado: pedido=42 motivo=cliente_ou_telefone_invalido
[2026-10-18 02:55:28,560] INFO in whatsapp_service: WhatsApp resultado: pedido=42 envio_solicitado=False resultado=sem_destinatario msg_id=None codigo_erro=None
[2026-10-18 02:55:28,560] INFO in whatsapp_service: WhatsApp avaliacao: pedido=42
[2026-10-18 02:55:28,560] INFO in whatsapp_service: WhatsApp ignorado: pedido=42 motivo=cliente_ou_telefone_invalido
[2026-10-18 02:55:28,560] INFO in whatsapp_service: WhatsApp resultado: pedido=42 envio_solicitado=False resultado=sem_destinatario msg_id=None codigo_erro=None
[2026-10-18 02:55:28,561] INFO in whatsapp_service: WhatsApp avaliacao: pedido=42
[2026-10-18 02:55:28,561] INFO in whatsapp_service: WhatsApp ignorado: pedido=42 motivo=cliente_ou_telefone_invalido
[2026-10-18 02:55:28,561] INFO in whatsapp_service: WhatsApp resultado: pedido=42 envio_solicitado=False resultado=sem_destinatario msg_id=None codigo_erro=None
[2026-10-18 02:55:28,584] INFO in whatsapp_service: WhatsApp avaliacao: pedido=42
[2026-10-18 02:55:28,585] INFO in whatsapp_service: WhatsApp resultado: pedido=42 envio_solicitado=False resultado=desabilitado msg_id=None codigo_erro=None
[2026-10-18 02:55:28,585] INFO in whatsapp_service: WhatsApp avaliacao: pedido=42
[2026-10-18 02:55:28,585] INFO in whatsapp_service: WhatsApp resultado: pedido=42 envio_solicitado=False resultado=status_incompativel msg_id=None codigo_erro=None
[2026-10-18 02:55:28,585] INFO in whatsapp_service: WhatsApp avaliacao: pedido=42
[2026-10-18 02:55:28,585] WARNING in whatsapp_service: WhatsApp ignorado: pedido=42 motivo=configuracao_incompleta_meta
[2026-10-18 02:55:28,585] WARNING in whatsapp_service: WhatsApp resultado: pedido=42 envio_solicitado=False resultado=configuracao_invalida msg_id=None codigo_erro=None
[2026-10-18 02:55:28,586] INFO in whatsapp_service: WhatsApp avaliacao: pedido=42
[2026-10-18 02:55:28,586] WARNING in whatsapp_service: WhatsApp ignorado: pedido=42 motivo=configuracao_incompleta_meta
[2026-10-18 02:55:28,586] WARNING in whatsapp_service: WhatsApp resultado: pedido=42 envio_solicitado=False resultado=configuracao_invalida msg_id=None codigo_erro=None
[2026-10-18 02:55:28,634] INFO in whatsapp_service: WhatsApp avaliacao: pedido=42
[2026-10-18 02:55:28,635] INFO in whatsapp_service: WhatsApp Meta solicitacao: pedido=42 destino=5511999999999
[2026-10-18 02:55:28,635] INFO in whatsapp_service: WhatsApp aceito pela Meta: pedido=42 msg_id=wamid.TESTE123
[2026-10-18 02:55:28,635] INFO in whatsapp_service: WhatsApp resultado: pedido=42 envio_solicitado=True resultado=aceito msg_id=wamidTESTE123 codigo_erro=None
[2026-10-18 02:55:28,635] INFO in whatsapp_service: WhatsApp avaliacao: pedido=42
[2026-10-18 02:55:28,636] INFO in whatsapp_service: WhatsApp Meta solicitacao: pedido=42 destino=5511999999999
[2026-10-18 02:55:28,636] INFO in whatsapp_service: WhatsApp aceito pela Meta: pedido=42 msg_id=wamid.TESTE123
[2026-10-18 02:55:28,636] INFO in whatsapp_service: WhatsApp resultado: pedido=42 envio_solicitado=True resultado=aceito msg_id=wamidTESTE123 codigo_erro=None
[2026-10-18 02:55:28,661] INFO in whatsapp_service: WhatsApp avaliacao: pedido=42
[2026-10-18 02:55:28,661] INFO in whatsapp_service: WhatsApp resultado: pedido=42 envio_solicitado=False resultado=bloqueado_testing msg_id=None codigo_erro=None
[2026-10-18 02:55:28,685] INFO in app: Webhook Meta validado com sucesso!
[2026-10-18 02:55:28,685] WARNING in app: Tentativa de verificacao de webhook Meta falhou. Token invalido ou nao configurado.
[2026-10-18 02:55:28,686] INFO in app: Webhook Meta evento recebido: {'entry': []}
----------------------------------------------------------------------
Ran 68 tests in 14.737s

OK

```

---

## 3. Observações sobre a Execução

Os avisos de depreciação de Query.get e datetime.utcnow vêm do código existente. As mensagens WARNING de falha são esperadas nas simulações negativas e não significam falha de teste. Os horários abaixo são emitidos pelo logger do ambiente executor; a data de consolidação acima segue o contexto local do projeto.

Aceite HTTP não significa entrega: entrega_confirmada permanece falsa. O webhook atual apenas verifica o token de inscrição e recebe eventos; não atualiza entrega. O identificador wamid é sanitizado pelo conector existente. Estes testes não validam credenciais reais, acesso à Meta ou recebimento em aparelho.
