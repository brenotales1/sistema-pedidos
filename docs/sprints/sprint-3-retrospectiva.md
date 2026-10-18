# Ata de Retrospectiva — Sprint 3 — Sistema de Pedidos e Controle de Estoque

**Consolidação técnica:** 18/10/2026 — Entrega E7  
**Equipe:** Breno Tales de Oliveira Leite (RA: 2840482423029) — Daniel Fredi Soares Pereira (RA: 2840482421054)

Este registro reúne conclusões verificáveis da implementação e da execução dos testes. A realização de reunião, presenças e decisões consensuais devem ser confirmadas pela dupla; não foram informadas nesta entrega.

## 1. Ações da retrospectiva anterior

| Ação da Sprint 2 | Resultado verificável |
|---|---|
| Implementar atualização de pedido (US #7) | Cliente associado e histórico de transição implementados por Breno. |
| Implementar conector e envio automático (US #8 e #9) | Meta Cloud API via requests, evento de finalização e tentativa persistida. |
| Desenvolver testes de notificação (Daniel) | 21 testes novos; 68 testes aprovados no total. |

## 2. O que funcionou bem

- A divisão entre implementação de Breno e validação/documentação de Daniel permitiu exercitar o conector existente sem alterar seu comportamento.
- A finalização é persistida antes da chamada externa: falhas da Meta e de rede não desfazem o pedido.
- O SQLite em memória e os mocks tornam os cenários reproduzíveis sem credenciais de produção.
- O histórico permite relacionar cada tentativa ao cliente, pedido e usuário responsável pela transição.

## 3. Dificuldades e soluções verificadas

| Dificuldade técnica | Solução aplicada ou validada |
|---|---|
| Diferenciar aceite HTTP de entrega ao cliente | Testes exigem `aceito` e `entrega_confirmada=False`; documentação explicita o limite do webhook. |
| Exercitar HTTP 400/500, timeout e erro de conexão | Mocks de `requests.post` verificam `falha` e preservação do pedido. |
| Testar sucesso apesar do bloqueio em modo testing | Desativação local de testing apenas depois de instalar o mock e a barreira adicional na sessão HTTP. |
| Evitar telefone e credenciais reais nos testes | Fixtures fictícias e substituição das variáveis Meta, com restauração automática. |
| Python global sem dependências | Utilização do ambiente `.venv` já existente no projeto. |
| IDs CT08/CT09 já usados no plano | Mantidos os IDs de autenticação; notificações formalizadas em CT42–CT45, com equivalência explicitada. |

## 4. Melhorias propostas para a próxima sprint

| Ação proposta | Responsabilidade sugerida |
|---|---|
| Implementar consulta administrativa de notificações (US #10 / CT46) | Dupla |
| Preservar identificador Meta integral e correlacionar callbacks de entrega | Breno, com testes de Daniel |
| Revisar autenticação dos eventos POST do webhook antes de utilizá-los para atualizar registros | Dupla |
| Reduzir exposição de telefone/payload nos logs operacionais | Dupla |
| Atualizar chamadas legadas SQLAlchemy e datetime sinalizadas na suíte | Dupla |

As responsabilidades acima são propostas técnicas para alinhamento, sem registrar compromissos ou rituais não confirmados.
