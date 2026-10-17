# Relatório Individual — Daniel Fredi Soares Pereira — Sprint 3 (E7)

**RA:** 2840482421054
**Validação:** 17/10/2026
**Dupla:** Breno Tales de Oliveira Leite

## 1. Responsabilidade na sprint

Desenvolvimento e adaptação dos testes automatizados de notificação (CT08/CT09 de notificações, formalizados como CT42–CT45), execução da regressão e documentação da E7. O vínculo com cliente, histórico de status e conector Meta são contribuições do Breno.

## 2. Entregas técnicas

- `tests/test_whatsapp.py`: normalização de telefone, payload texto/template, HTTP 200/201 com wamid, HTTP 400/500, timeout, conexão, JSON inválido, configuração incompleta e bloqueio em TESTING.
- `tests/test_notificacao_visual.py`: flash de sucesso/erro, cliente com telefone inválido ou ausente, integração desativada e status repetido.
- `tests/test_notificacao_persistencia.py`: resultado aceito/falha, auditoria UTC, destinatário por ID entre homônimos, unicidade, migração idempotente, falha de persistência, commit anterior ao envio e webhook.
- Preservação dos cenários de auditoria da US #7 em `tests/test_status_pedido.py` com fixture compatível com Meta.

Credenciais e telefones usados são fictícios. SQLite em memória e bloqueios de socket/transporte impedem acesso externo nos novos testes. TESTING=False é utilizado somente nos cenários com HTTP mockado para alcançar o caminho de envio.

## 3. Documentação e resultado

Consolidados relatório, retrospectiva e evidências da Sprint 3; backlog atualizado para US #7, #8 e #9 Concluída e plano formal com CT42–CT45 executados. Resultado completo e comando reproduzível em [evidências](sprint-3-evidencias-teste.md).

## 4. Limites da contribuição

Validação automatizada com respostas simuladas, sem afirmar envio real ou entrega no aparelho. Não foram gravadas credenciais, alterado o banco principal nesta implementação ou realizados commit/push. A branch local permanece a existente; arquivos da integração foram restaurados da origin/main porque o pull não pôde integrar as alterações locais.
