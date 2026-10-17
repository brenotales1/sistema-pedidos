# Evidências de Teste — Sprint 3 (E7)

**Data:** 17/10/2026
**Responsável:** Daniel Fredi Soares Pereira
**Ambiente:** Windows, Python do .venv, unittest, Flask Test Client e SQLite em memória.

## 1. Reprodução

```powershell
.\.venv\Scripts\Activate.ps1
python -B -m unittest discover -s tests -q
```

Nesta captura, o executável do .venv foi utilizado diretamente com os mesmos argumentos. O Python global inicialmente falhou por dependências ausentes; esse resultado não foi contado como aprovação. Os avisos de depreciação existentes são mantidos no log.

## 2. Cenários verificados

CT42–CT45: sucesso HTTP 200/201 e wamid, montagem de texto/templates Meta, flash, persistência, falhas HTTP 400/500 e de rede, telefone inválido/ausente, bloqueio TESTING, cliente por ID, ausência de duplicidade, commit antes do envio, migração e webhook. Regressão inclui autenticação, clientes, estoque e pedidos.

Respostas HTTP são simuladas e os novos testes bloqueiam transporte externo; nenhum envio real comprova entrega. Todos os dados do log são de fixtures fictícias. .env e instance/database.db não são utilizados pelos novos testes.

## 3. Saída integral da execução

Código de saída: **0**.

```text
C:\Users\T-GAMER\sistema-pedidos\.venv\Lib\site-packages\flask_sqlalchemy\query.py:30: LegacyAPIWarning: The Query.get() method is considered legacy as of the 1.x series of SQLAlchemy and becomes a legacy construct in 2.0. The method is now available as Session.get() (deprecated since: 2.0) (Background on SQLAlchemy 2.0 at: https://sqlalche.me/e/b8d9)

  rv = self.get(ident)

C:\Users\T-GAMER\sistema-pedidos\tests\test_clientes.py:89: LegacyAPIWarning: The Query.get() method is considered legacy as of the 1.x series of SQLAlchemy and becomes a legacy construct in 2.0. The method is now available as Session.get() (deprecated since: 2.0) (Background on SQLAlchemy 2.0 at: https://sqlalche.me/e/b8d9)

  cli_atualizado = Cliente.query.get(cli_id)

C:\Users\T-GAMER\sistema-pedidos\services\estoque_service.py:57: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).

  data_hora=datetime.utcnow(),

C:\Users\T-GAMER\sistema-pedidos\.venv\Lib\site-packages\sqlalchemy\sql\schema.py:4296: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).

  return util.wrap_callable(lambda ctx: fn(), fn)  # type: ignore[call-arg, no-any-return, no-untyped-call]  # noqa: E501

[2026-10-17 15:12:49,904] INFO in whatsapp_service: WhatsApp avaliacao: pedido=1

[2026-10-17 15:12:49,907] INFO in whatsapp_service: WhatsApp Meta solicitacao: pedido=1 destino=5511999999999

[2026-10-17 15:12:49,907] INFO in whatsapp_service: WhatsApp aceito pela Meta: pedido=1 msg_id=wamid.exemplo123

[2026-10-17 15:12:49,907] INFO in whatsapp_service: WhatsApp resultado: pedido=1 envio_solicitado=True resultado=aceito msg_id=wamidexemplo123 codigo_erro=None

[2026-10-17 15:12:49,942] INFO in whatsapp_service: WhatsApp avaliacao: pedido=1

[2026-10-17 15:12:49,943] INFO in whatsapp_service: WhatsApp Meta solicitacao: pedido=1 destino=5511999999999

[2026-10-17 15:12:49,943] INFO in whatsapp_service: WhatsApp aceito pela Meta: pedido=1 msg_id=wamid.exemplo123

[2026-10-17 15:12:49,943] INFO in whatsapp_service: WhatsApp resultado: pedido=1 envio_solicitado=True resultado=aceito msg_id=wamidexemplo123 codigo_erro=None

[2026-10-17 15:12:49,974] INFO in whatsapp_service: WhatsApp avaliacao: pedido=1

[2026-10-17 15:12:49,975] WARNING in whatsapp_service: WhatsApp ignorado: pedido=1 motivo=configuracao_incompleta_meta

[2026-10-17 15:12:49,975] WARNING in whatsapp_service: WhatsApp resultado: pedido=1 envio_solicitado=False resultado=configuracao_invalida msg_id=None codigo_erro=None

[2026-10-17 15:12:50,007] INFO in whatsapp_service: WhatsApp avaliacao: pedido=1

[2026-10-17 15:12:50,007] INFO in whatsapp_service: WhatsApp Meta solicitacao: pedido=1 destino=5521999999999

[2026-10-17 15:12:50,007] INFO in whatsapp_service: WhatsApp aceito pela Meta: pedido=1 msg_id=wamid.exemplo123

[2026-10-17 15:12:50,007] INFO in whatsapp_service: WhatsApp resultado: pedido=1 envio_solicitado=True resultado=aceito msg_id=wamidexemplo123 codigo_erro=None

[2026-10-17 15:12:50,037] INFO in pedido_service: WhatsApp transicao: pedido=1 envio_solicitado=False resultado=status_inalterado

[2026-10-17 15:12:50,038] INFO in pedido_service: WhatsApp transicao: pedido=1 envio_solicitado=False resultado=status_inalterado

[2026-10-17 15:12:50,045] INFO in pedido_service: WhatsApp transicao: pedido=1 envio_solicitado=False resultado=sem_transicao_para_finalizado

[2026-10-17 15:12:50,046] INFO in pedido_service: WhatsApp transicao: pedido=1 envio_solicitado=False resultado=status_inalterado

[2026-10-17 15:12:50,048] INFO in pedido_service: WhatsApp transicao: pedido=1 envio_solicitado=False resultado=sem_transicao_para_finalizado

[2026-10-17 15:12:50,049] INFO in pedido_service: WhatsApp transicao: pedido=1 envio_solicitado=False resultado=status_inalterado

[2026-10-17 15:12:50,053] INFO in whatsapp_service: WhatsApp avaliacao: pedido=1

[2026-10-17 15:12:50,053] INFO in whatsapp_service: WhatsApp Meta solicitacao: pedido=1 destino=5511999999999

[2026-10-17 15:12:50,053] INFO in whatsapp_service: WhatsApp aceito pela Meta: pedido=1 msg_id=wamid.exemplo123

[2026-10-17 15:12:50,054] INFO in whatsapp_service: WhatsApp resultado: pedido=1 envio_solicitado=True resultado=aceito msg_id=wamidexemplo123 codigo_erro=None

[2026-10-17 15:12:50,069] INFO in pedido_service: WhatsApp transicao: pedido=1 envio_solicitado=False resultado=status_inalterado

[2026-10-17 15:12:50,098] INFO in whatsapp_service: WhatsApp avaliacao: pedido=1

[2026-10-17 15:12:50,098] INFO in whatsapp_service: WhatsApp resultado: pedido=1 envio_solicitado=False resultado=desabilitado msg_id=None codigo_erro=None

[2026-10-17 15:12:50,102] INFO in pedido_service: WhatsApp transicao: pedido=1 envio_solicitado=False resultado=sem_transicao_para_finalizado

[2026-10-17 15:12:50,105] INFO in whatsapp_service: WhatsApp avaliacao: pedido=1

[2026-10-17 15:12:50,105] INFO in whatsapp_service: WhatsApp resultado: pedido=1 envio_solicitado=False resultado=bloqueado_testing msg_id=None codigo_erro=None

[2026-10-17 15:12:50,135] INFO in whatsapp_service: WhatsApp avaliacao: pedido=1

[2026-10-17 15:12:50,135] INFO in whatsapp_service: WhatsApp Meta solicitacao: pedido=1 destino=5511999999999

[2026-10-17 15:12:50,135] INFO in whatsapp_service: WhatsApp aceito pela Meta: pedido=1 msg_id=wamid.exemplo123

[2026-10-17 15:12:50,135] INFO in whatsapp_service: WhatsApp resultado: pedido=1 envio_solicitado=True resultado=aceito msg_id=wamidexemplo123 codigo_erro=None

[2026-10-17 15:12:50,136] WARNING in pedido_service: WhatsApp: resultado da tentativa nao persistido

[2026-10-17 15:12:50,138] INFO in pedido_service: WhatsApp transicao: pedido=1 envio_solicitado=False resultado=status_inalterado

[2026-10-17 15:12:50,167] INFO in whatsapp_service: WhatsApp avaliacao: pedido=1

[2026-10-17 15:12:50,167] INFO in whatsapp_service: WhatsApp Meta solicitacao: pedido=1 destino=5511999999999

[2026-10-17 15:12:50,168] WARNING in whatsapp_service: Falha WhatsApp Meta: pedido=1 status_http=400 resposta=<MagicMock name='post().text' id='2679485187136'>

[2026-10-17 15:12:50,168] WARNING in whatsapp_service: WhatsApp resultado: pedido=1 envio_solicitado=True resultado=falha msg_id=None codigo_erro=400

[2026-10-17 15:12:50,198] INFO in whatsapp_service: WhatsApp avaliacao: pedido=1

[2026-10-17 15:12:50,198] INFO in whatsapp_service: WhatsApp Meta solicitacao: pedido=1 destino=5511999999999

[2026-10-17 15:12:50,198] INFO in whatsapp_service: WhatsApp aceito pela Meta: pedido=1 msg_id=wamid.exemplo123

[2026-10-17 15:12:50,199] INFO in whatsapp_service: WhatsApp resultado: pedido=1 envio_solicitado=True resultado=aceito msg_id=wamidexemplo123 codigo_erro=None

[2026-10-17 15:12:50,229] INFO in whatsapp_service: WhatsApp avaliacao: pedido=1

[2026-10-17 15:12:50,230] INFO in whatsapp_service: WhatsApp Meta solicitacao: pedido=1 destino=5511999999999

[2026-10-17 15:12:50,230] WARNING in whatsapp_service: Falha WhatsApp Meta: pedido=1 status_http=500 resposta=<MagicMock name='post().text' id='2679485191840'>

[2026-10-17 15:12:50,230] WARNING in whatsapp_service: WhatsApp resultado: pedido=1 envio_solicitado=True resultado=falha msg_id=None codigo_erro=500

[2026-10-17 15:12:50,261] INFO in whatsapp_service: WhatsApp avaliacao: pedido=1

[2026-10-17 15:12:50,261] INFO in whatsapp_service: WhatsApp Meta solicitacao: pedido=1 destino=5511999999999

[2026-10-17 15:12:50,261] INFO in whatsapp_service: WhatsApp aceito pela Meta: pedido=1 msg_id=wamid.exemplo123

[2026-10-17 15:12:50,261] INFO in whatsapp_service: WhatsApp resultado: pedido=1 envio_solicitado=True resultado=aceito msg_id=wamidexemplo123 codigo_erro=None

[2026-10-17 15:12:50,295] INFO in whatsapp_service: WhatsApp avaliacao: pedido=1

[2026-10-17 15:12:50,296] INFO in whatsapp_service: WhatsApp Meta solicitacao: pedido=1 destino=5511999999999

[2026-10-17 15:12:50,296] INFO in whatsapp_service: WhatsApp aceito pela Meta: pedido=1 msg_id=wamid.exemplo123

[2026-10-17 15:12:50,296] INFO in whatsapp_service: WhatsApp resultado: pedido=1 envio_solicitado=True resultado=aceito msg_id=wamidexemplo123 codigo_erro=None

[2026-10-17 15:12:50,327] INFO in pedido_service: WhatsApp transicao: pedido=1 envio_solicitado=False resultado=sem_transicao_para_finalizado

[2026-10-17 15:12:50,332] INFO in whatsapp_service: WhatsApp avaliacao: pedido=1

[2026-10-17 15:12:50,333] INFO in whatsapp_service: WhatsApp Meta solicitacao: pedido=1 destino=5511999999999

[2026-10-17 15:12:50,333] INFO in whatsapp_service: WhatsApp aceito pela Meta: pedido=1 msg_id=wamid.exemplo123

[2026-10-17 15:12:50,333] INFO in whatsapp_service: WhatsApp resultado: pedido=1 envio_solicitado=True resultado=aceito msg_id=wamidexemplo123 codigo_erro=None

[2026-10-17 15:12:50,335] INFO in pedido_service: WhatsApp transicao: pedido=1 envio_solicitado=False resultado=status_inalterado

[2026-10-17 15:12:50,338] INFO in pedido_service: WhatsApp transicao: pedido=1 envio_solicitado=False resultado=sem_transicao_para_finalizado

[2026-10-17 15:12:50,341] INFO in whatsapp_service: WhatsApp avaliacao: pedido=1

[2026-10-17 15:12:50,341] INFO in whatsapp_service: WhatsApp Meta solicitacao: pedido=1 destino=5511999999999

[2026-10-17 15:12:50,341] INFO in whatsapp_service: WhatsApp aceito pela Meta: pedido=1 msg_id=wamid.exemplo123

[2026-10-17 15:12:50,341] INFO in whatsapp_service: WhatsApp resultado: pedido=1 envio_solicitado=True resultado=aceito msg_id=wamidexemplo123 codigo_erro=None

[2026-10-17 15:12:50,371] INFO in whatsapp_service: WhatsApp avaliacao: pedido=1

[2026-10-17 15:12:50,372] INFO in whatsapp_service: WhatsApp ignorado: pedido=1 motivo=cliente_ou_telefone_invalido

[2026-10-17 15:12:50,372] INFO in whatsapp_service: WhatsApp resultado: pedido=1 envio_solicitado=False resultado=sem_destinatario msg_id=None codigo_erro=None

[2026-10-17 15:12:50,402] INFO in whatsapp_service: WhatsApp avaliacao: pedido=1

[2026-10-17 15:12:50,403] INFO in whatsapp_service: WhatsApp Meta solicitacao: pedido=1 destino=5511999999999

[2026-10-17 15:12:50,403] WARNING in whatsapp_service: Falha WhatsApp Meta: pedido=1 motivo=erro_no_envio

[2026-10-17 15:12:50,403] WARNING in whatsapp_service: WhatsApp resultado: pedido=1 envio_solicitado=True resultado=falha msg_id=None codigo_erro=None

[2026-10-17 15:12:50,430] INFO in app: Webhook Meta validado com sucesso!

[2026-10-17 15:12:50,430] WARNING in app: Tentativa de verificacao de webhook Meta falhou. Token invalido ou nao configurado.

[2026-10-17 15:12:50,431] INFO in app: Webhook Meta evento recebido: {'entry': []}

[2026-10-17 15:12:50,460] INFO in whatsapp_service: WhatsApp avaliacao: pedido=1

[2026-10-17 15:12:50,461] INFO in whatsapp_service: WhatsApp Meta solicitacao: pedido=1 destino=5511999999999

[2026-10-17 15:12:50,461] INFO in whatsapp_service: WhatsApp aceito pela Meta: pedido=1 msg_id=wamid.exemplo123

[2026-10-17 15:12:50,461] INFO in whatsapp_service: WhatsApp resultado: pedido=1 envio_solicitado=True resultado=aceito msg_id=wamidexemplo123 codigo_erro=None

[2026-10-17 15:12:50,510] INFO in whatsapp_service: WhatsApp avaliacao: pedido=1

[2026-10-17 15:12:50,510] WARNING in whatsapp_service: WhatsApp ignorado: pedido=1 motivo=configuracao_incompleta_meta

[2026-10-17 15:12:50,510] WARNING in whatsapp_service: WhatsApp resultado: pedido=1 envio_solicitado=False resultado=configuracao_invalida msg_id=None codigo_erro=None

[2026-10-17 15:12:50,551] INFO in whatsapp_service: WhatsApp avaliacao: pedido=1

[2026-10-17 15:12:50,551] INFO in whatsapp_service: WhatsApp resultado: pedido=1 envio_solicitado=False resultado=desabilitado msg_id=None codigo_erro=None

[2026-10-17 15:12:50,595] INFO in pedido_service: WhatsApp transicao: pedido=1 envio_solicitado=False resultado=sem_transicao_para_finalizado

[2026-10-17 15:12:50,598] INFO in whatsapp_service: WhatsApp avaliacao: pedido=1

[2026-10-17 15:12:50,598] INFO in whatsapp_service: WhatsApp Meta solicitacao: pedido=1 destino=5511999999999

[2026-10-17 15:12:50,599] WARNING in whatsapp_service: Falha WhatsApp Meta: pedido=1 status_http=400 resposta=<MagicMock name='post().text' id='2679489736928'>

[2026-10-17 15:12:50,599] WARNING in whatsapp_service: WhatsApp resultado: pedido=1 envio_solicitado=True resultado=falha msg_id=None codigo_erro=400

[2026-10-17 15:12:50,616] INFO in pedido_service: WhatsApp transicao: pedido=1 envio_solicitado=False resultado=sem_transicao_para_finalizado

[2026-10-17 15:12:50,618] INFO in whatsapp_service: WhatsApp avaliacao: pedido=1

[2026-10-17 15:12:50,619] INFO in whatsapp_service: WhatsApp Meta solicitacao: pedido=1 destino=5511999999999

[2026-10-17 15:12:50,619] WARNING in whatsapp_service: Falha WhatsApp Meta: pedido=1 status_http=500 resposta=<MagicMock name='post().text' id='2679489736928'>

[2026-10-17 15:12:50,619] WARNING in whatsapp_service: WhatsApp resultado: pedido=1 envio_solicitado=True resultado=falha msg_id=None codigo_erro=500

[2026-10-17 15:12:50,650] INFO in whatsapp_service: WhatsApp avaliacao: pedido=1

[2026-10-17 15:12:50,650] INFO in whatsapp_service: WhatsApp Meta solicitacao: pedido=1 destino=5511999999999

[2026-10-17 15:12:50,650] WARNING in whatsapp_service: Falha WhatsApp Meta: pedido=1 motivo=erro_no_envio

[2026-10-17 15:12:50,650] WARNING in whatsapp_service: WhatsApp resultado: pedido=1 envio_solicitado=True resultado=falha msg_id=None codigo_erro=None

[2026-10-17 15:12:50,691] INFO in pedido_service: WhatsApp transicao: pedido=1 envio_solicitado=False resultado=sem_transicao_para_finalizado

[2026-10-17 15:12:50,736] INFO in whatsapp_service: WhatsApp avaliacao: pedido=1

[2026-10-17 15:12:50,736] INFO in whatsapp_service: WhatsApp ignorado: pedido=1 motivo=cliente_ou_telefone_invalido

[2026-10-17 15:12:50,736] INFO in whatsapp_service: WhatsApp resultado: pedido=1 envio_solicitado=False resultado=sem_destinatario msg_id=None codigo_erro=None

[2026-10-17 15:12:50,790] INFO in whatsapp_service: WhatsApp avaliacao: pedido=1

[2026-10-17 15:12:50,791] INFO in whatsapp_service: WhatsApp Meta solicitacao: pedido=1 destino=5511999999999

[2026-10-17 15:12:50,791] INFO in whatsapp_service: WhatsApp aceito pela Meta: pedido=1 msg_id=wamid.exemplo123

[2026-10-17 15:12:50,791] INFO in whatsapp_service: WhatsApp resultado: pedido=1 envio_solicitado=True resultado=aceito msg_id=wamidexemplo123 codigo_erro=None

[2026-10-17 15:12:50,806] INFO in pedido_service: WhatsApp transicao: pedido=1 envio_solicitado=False resultado=status_inalterado

[2026-10-17 15:12:50,853] INFO in whatsapp_service: WhatsApp avaliacao: pedido=1

[2026-10-17 15:12:50,853] INFO in whatsapp_service: WhatsApp ignorado: pedido=1 motivo=cliente_ou_telefone_invalido

[2026-10-17 15:12:50,854] INFO in whatsapp_service: WhatsApp resultado: pedido=1 envio_solicitado=False resultado=sem_destinatario msg_id=None codigo_erro=None

[2026-10-17 15:12:50,902] INFO in whatsapp_service: WhatsApp avaliacao: pedido=1

[2026-10-17 15:12:50,902] INFO in whatsapp_service: WhatsApp resultado: pedido=1 envio_solicitado=False resultado=bloqueado_testing msg_id=None codigo_erro=None

[2026-10-17 15:12:50,945] INFO in whatsapp_service: WhatsApp avaliacao: pedido=1

[2026-10-17 15:12:50,946] INFO in whatsapp_service: WhatsApp Meta solicitacao: pedido=1 destino=5511999999999

[2026-10-17 15:12:50,946] WARNING in whatsapp_service: Falha WhatsApp Meta: pedido=1 motivo=erro_no_envio

[2026-10-17 15:12:50,947] WARNING in whatsapp_service: WhatsApp resultado: pedido=1 envio_solicitado=True resultado=falha msg_id=None codigo_erro=None

[2026-10-17 15:12:51,295] INFO in pedido_service: WhatsApp transicao: pedido=1 envio_solicitado=False resultado=sem_transicao_para_finalizado

C:\Users\T-GAMER\sistema-pedidos\tests\test_pedidos.py:226: LegacyAPIWarning: The Query.get() method is considered legacy as of the 1.x series of SQLAlchemy and becomes a legacy construct in 2.0. The method is now available as Session.get() (deprecated since: 2.0) (Background on SQLAlchemy 2.0 at: https://sqlalche.me/e/b8d9)

  pedido_atualizado = Pedido.query.get(pedido_id)

C:\Users\T-GAMER\sistema-pedidos\tests\test_pedidos.py:189: LegacyAPIWarning: The Query.get() method is considered legacy as of the 1.x series of SQLAlchemy and becomes a legacy construct in 2.0. The method is now available as Session.get() (deprecated since: 2.0) (Background on SQLAlchemy 2.0 at: https://sqlalche.me/e/b8d9)

  pedido_cancelado = Pedido.query.get(pedido_id)

[2026-10-17 15:12:53,477] INFO in pedido_service: WhatsApp transicao: pedido=1 envio_solicitado=False resultado=sem_transicao_para_finalizado

[2026-10-17 15:12:53,489] INFO in pedido_service: WhatsApp transicao: pedido=1 envio_solicitado=False resultado=status_inalterado

[2026-10-17 15:12:53,573] INFO in pedido_service: WhatsApp transicao: pedido=1 envio_solicitado=False resultado=sem_transicao_para_finalizado

[2026-10-17 15:12:53,655] WARNING in whatsapp_service: WhatsApp ignorado: pedido=5 motivo=configuracao_incompleta_meta

[2026-10-17 15:12:53,655] WARNING in whatsapp_service: WhatsApp resultado: pedido=5 envio_solicitado=False resultado=configuracao_invalida msg_id=None codigo_erro=None

[2026-10-17 15:12:53,655] WARNING in whatsapp_service: WhatsApp ignorado: pedido=5 motivo=configuracao_incompleta_meta

[2026-10-17 15:12:53,656] WARNING in whatsapp_service: WhatsApp resultado: pedido=5 envio_solicitado=False resultado=configuracao_invalida msg_id=None codigo_erro=None

[2026-10-17 15:12:53,660] WARNING in whatsapp_service: Falha WhatsApp Meta: pedido=5 motivo=erro_no_envio

[2026-10-17 15:12:53,660] WARNING in whatsapp_service: WhatsApp resultado: pedido=5 envio_solicitado=True resultado=falha msg_id=None codigo_erro=None

[2026-10-17 15:12:53,660] WARNING in whatsapp_service: Falha WhatsApp Meta: pedido=5 motivo=erro_no_envio

[2026-10-17 15:12:53,660] WARNING in whatsapp_service: WhatsApp resultado: pedido=5 envio_solicitado=True resultado=falha msg_id=None codigo_erro=None

[2026-10-17 15:12:53,660] WARNING in whatsapp_service: Falha WhatsApp Meta: pedido=5 motivo=erro_no_envio

[2026-10-17 15:12:53,664] WARNING in whatsapp_service: WhatsApp resultado: pedido=5 envio_solicitado=True resultado=falha msg_id=None codigo_erro=None

[2026-10-17 15:12:53,668] WARNING in whatsapp_service: Falha WhatsApp Meta: pedido=5 status_http=400 resposta=<MagicMock name='post().text' id='2679489735584'>

[2026-10-17 15:12:53,668] WARNING in whatsapp_service: WhatsApp resultado: pedido=5 envio_solicitado=True resultado=falha msg_id=None codigo_erro=400

[2026-10-17 15:12:53,668] WARNING in whatsapp_service: Falha WhatsApp Meta: pedido=5 status_http=500 resposta=<MagicMock name='post().text' id='2679489735584'>

[2026-10-17 15:12:53,668] WARNING in whatsapp_service: WhatsApp resultado: pedido=5 envio_solicitado=True resultado=falha msg_id=None codigo_erro=500

----------------------------------------------------------------------

Ran 93 tests in 15.362s



OK


```
