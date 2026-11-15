# E10 — Validação da Relação N:N Pedido ↔ Material

**Equipe:** Breno Tales de Oliveira Leite (RA: 2840482423029) — Daniel Fredi Soares Pereira (RA: 2840482421054)<br>
**Data:** 15/11/2026<br>
**Ambiente:** Python da .venv, SQLite em memória, Flask Test Client e mocks. Sem acesso ao banco de produção e sem envio real de mensagens.

## 1. Implementação

A tabela [ConsumoMaterial](../models/consumo_material.py) associa Pedido e Material por chave primária composta, quantidade positiva em metros e identificação do material principal. O formulário permite adicionar outros materiais e o detalhe mostra todos os consumos.

Um pedido pode usar vários materiais, e cada material pode aparecer em vários pedidos. O [teste de cardinalidade](../tests/test_consumo_material.py) cria dois pedidos com dois materiais em comum e verifica quatro associações, o relacionamento inverso e os saldos.

## 2. Cenários novos

| Grupo | Verificações |
|---|---|
| Cardinalidade e exibição | Dois pedidos compartilham materiais; detalhe e busca incluem materiais adicionais |
| Edição | Troca/remoção de materiais, estorno dos anteriores e preservação ao salvar os mesmos dados |
| Cancelamento | Devolução de todos os materiais e remoção das associações; bloqueio por status |
| Validações | Material inexistente, repetido ou principal duplicado; campos incompletos; consumo zero, negativo, não finito, menor que a precisão e superior ao estoque |
| Atomicidade | Falha no segundo consumo, falha de commit na edição e no cancelamento preservam o estado anterior |
| Integridade | PK composta e CHECK de quantidade; exclusão de material vinculado bloqueada |
| Migração | Banco existente sem tabela associativa, execução idempotente sem segunda baixa; legado não identificável não recebe associação inventada |

**Novos testes:** 16 métodos em [test_consumo_material.py](../tests/test_consumo_material.py).<br>
**Regressão:** 115 testes anteriores.<br>
**Suíte atual:** 131 testes. Resultado e duração no [log integral](E10-testes-nn.txt).

## 3. Reprodução

No PowerShell, usando uma configuração isolada também para a aplicação carregada na importação:

```powershell
$env:DATABASE_URL = "sqlite:///:memory:"
$env:WHATSAPP_ENABLED = "false"
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -v
```

As variáveis acima valem para esse terminal. A suíte não usa o banco de desenvolvimento nem credenciais reais para mensagens.

## 4. Aplicação sobre dados existentes

Faça backup do arquivo SQLite antes de iniciar a nova versão. Na inicialização, a tabela é criada e a migração associa pedidos antigos sem alterar saldos. Materiais antigos não identificados exigem regularização antes de edição/cancelamento.

Esta validação é da implementação local. A captura e o aceite anteriores da E9 não foram tratados como validação dessa nova interface; o deploy e a captura atualizada do formulário ficam para a publicação da versão.
