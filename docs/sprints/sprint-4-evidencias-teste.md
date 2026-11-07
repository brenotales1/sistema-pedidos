# Sprint 4 - US #10 / CT46

Data: 07/11/2026.

Implementada a consulta administrativa em `/notificacoes`, acessivel pelo menu de administradores. Exibe cliente, link para pedido, data/hora em UTC e resultado da tentativa. Inclui filtro por status e paginacao de 25 registros, em ordem decrescente de data e ID.

O aceite pela API nao representa entrega confirmada. Falhas, pendencias e envios bloqueados ou desativados recebem rotulos distintos. A consulta nao dispara mensagens nem altera as tentativas persistidas.

## Validacao pendente
