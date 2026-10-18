# Relatório Individual de Contribuição — Sprint 3 — Daniel Fredi Soares Pereira (RA 2840482421054)

**Papel nesta sprint:** Testes automatizados de notificações e documentação da E7  
**Consolidação:** 18/10/2026

## 1. O que foi desenvolvido nesta entrega

| Item | Arquivo | Situação |
|---|---|---|
| 9 testes do contrato Meta: HTTP 200/201, falhas, telefone, templates, configuração, bloqueio testing e webhook | `tests/test_whatsapp.py` | Implementado e aprovado |
| 6 testes de flash renderizado e resultado persistido | `tests/test_notificacao_visual.py` | Implementado e aprovado |
| 6 testes de auditoria, falhas persistidas, prevenção de duplicidade e nova finalização | `tests/test_notificacao_persistencia.py` | Implementado e aprovado |
| Infraestrutura SQLite em memória, fixtures fictícias, mocks e bloqueio HTTP adicional | `tests/notificacao_base.py` | Implementado |
| Relatório, retrospectiva técnica, evidências e contribuição individual | `docs/sprints/sprint-3-*.md` | Documentado |
| Atualização de histórias e casos formais CT42–CT45 | `docs/backlog.md` e `docs/plano-de-testes.md` | Atualizado |

Os arquivos foram preparados no diretório de trabalho; nenhum hash de commit ou revisão de colega é atribuído a esta entrega.

## 2. Validação realizada

Execução de `python -B -m unittest discover -s tests -q` no ambiente virtual do projeto: **68 testes aprovados**, sendo 47 existentes e 21 adicionados. [Evidências e log completo](sprint-3-evidencias-teste.md).

As chamadas à Meta são simuladas em `requests.post`. Uma barreira em `requests.sessions.Session.request` impede acesso HTTP real durante os novos testes. O banco usado é `sqlite:///:memory:`, sem alteração do banco de desenvolvimento.

## 3. Integração com o trabalho de Breno

A contribuição usa o serviço `services/whatsapp_service.py`, o fluxo de status e os modelos implementados por Breno. Os testes exercitam essas implementações diretamente, incluindo auditoria e flash, sem substituir o conector por um resultado pronto nos testes de integração.

Não foram informadas participações em rituais, aprovações de PRs ou revisões formais; esses registros devem ser preenchidos pela dupla conforme sua realização.

## 4. Aprendizados e limites

- Separar aceite de envio e confirmação de entrega evita evidências incorretas.
- Persistir a transição antes da integração externa mantém o pedido consistente em falhas da API.
- Instalar os mocks antes de desativar testing permite validar o caminho de sucesso com uma proteção adicional de rede.
- O formato atual do identificador Meta é sanitizado pelo conector; os testes documentam o comportamento existente.
- A comprovação desta entrega é automatizada com mocks; não houve envio real ou confirmação de recebimento em aparelho.
