# Relatório de Entrega — Sprint 2 — Sistema de Pedidos e Controle de Estoque

**Período:** 19/09/2026 a 02/10/2026 (Semana 8 — Entrega E6)  
**Sprint Review:** 02/10/2026  
**Equipe:** Breno Tales de Oliveira Leite (RA: 2840482423029) — Daniel Fredi Soares Pereira (RA: 2840482421054) · Laboratório de Engenharia de Software · ADS Fatec Ribeirão Preto

---

## 1. Planejado vs. entregue

| História (E2) | Planejada para esta sprint? | Entregue? | Observação |
|---|:---:|:---:|---|
| **#4 Identificar material pelo código de barras** | Sim | Sim | Implementação de endpoint REST protegido `GET /estoque/api/material/codigo/<codigo_barras>`, leitor de código de barras USB com submit automático e card interativo de dados do material (CT06). |
| **#5 Registrar entrada de material pelo código de barras** | Sim | Sim | Criação da entidade `MovimentacaoEstoque`, serviço de acréscimo de bobinas/metros com validação de quantidade positiva (`> 0`), rota `POST /estoque/entrada` e persistência de histórico (CT05, CT07). |
| **#6 Consultar movimentações do estoque** | Sim | Sim | Interface de histórico `/estoque/movimentacoes` com ordenação da mais recente para a mais antiga, filtros por tipo (entrada/saída/ajuste) e por material selecionado. |

---

## 2. Incremento funcional demonstrável

1. **Identificação Rápida de Material por Código de Barras (US #4):**
   - Leitura via código de barras com captura de evento `Enter` do leitor USB físico.
   - Endpoint JSON `/estoque/api/material/codigo/<codigo_barras>` com `@login_required`.
   - Exibição em tempo real de painel de detalhes: nome, categoria, largura, metros disponíveis e código de barras.
   - Tratamento de códigos inexistentes com mensagem clara e sem alteração no estoque.

2. **Registro de Entrada de Estoque com Validação de Quantidade (US #5):**
   - Modelo `MovimentacaoEstoque` registrando `material_id`, `tipo='entrada'`, `quantidade_metros`, `quantidade_bobinas`, `motivo`, `usuario_id` e `data_hora`.
   - Regra de negócio recusando quantidades menores ou iguais a zero com feedback visual via mensagens `flash`.
   - Atualização automática de metros totais e do array de bobinas do material.
   - Refinamento de interface ocultando botões e formulários administrativos para o perfil `funcionario`.

3. **Consulta e Histórico de Movimentações de Estoque (US #6):**
   - Tela `/estoque/movimentacoes` listando todas as operações realizadas em ordem decrescente de data/hora.
   - Filtros dinâmicos por tipo de movimentação (`entrada`, `saida`, `ajuste`) e por material.
   - Link de acesso no menu de navegação superior (`base.html`).

**Como reproduzir localmente:**
Consulte o guia passo a passo presente no [`README.md`](../README.md) na raiz do repositório.

---

## 3. Backlog atualizado

Ao fim da Sprint 2, os cards no quadro do projeto foram atualizados:
- **US #4** (Identificar material pelo código de barras) ➔ **Concluído**
- **US #5** (Registrar entrada de material pelo código de barras) ➔ **Concluído**
- **US #6** (Consultar movimentações do estoque) ➔ **Concluído**
- **Total entregue na Sprint 2:** 100% da meta da Sprint 2 (3 histórias concluídas)

**Histórias planejadas para a Sprint 3 (E7):**
- **US #7** — Selecionar uma atualização do pedido
- **US #8** — Enviar uma notificação pelo WhatsApp
- **US #9** — Disparar envio automático de WhatsApp em atualizações de pedido

---

## 4. Evidências de teste

Foram desenvolvidos **41 testes automatizados** utilizando `unittest` e Flask Test Client:
- **Testes Unitários:** Validação de hashing de senhas, conversão de medidas, algoritmo de aproveitamento de corte, regras de acréscimo/consumo/devolução de bobinas e regras de negócio de movimentação.
- **Testes de Integração:** Casos de teste formais **CT01** (login inválido), **CT02** (controle de acesso por perfil), **CT03** (unicidade de código de barras), **CT04** (busca de material inexistente), **CT05** (validação de entrada com quantidade inválida), **CT06** (identificação via API por código de barras) e **CT07** (persistência da entrada no histórico de movimentações).

**Resultado da execução:** 41 testes executados, 41 aprovados (100% de sucesso).  
Relatório detalhado disponível em: [`docs/sprints/sprint-2-evidencias-teste.md`](./sprint-2-evidencias-teste.md).

---

## 5. Retrospectiva e contribuição individual

- **Ata de Retrospectiva:** [`docs/sprints/sprint-2-retrospectiva.md`](./sprint-2-retrospectiva.md)
- **Relatório Individual — Breno Tales de Oliveira Leite (RA 2840482423029):** [`docs/sprints/sprint-2-contribuicao-breno.md`](./sprint-2-contribuicao-breno.md)
- **Relatório Individual — Daniel Fredi Soares Pereira (RA 2840482421054):** [`docs/sprints/sprint-2-contribuicao-daniel.md`](./sprint-2-contribuicao-daniel.md)

---

## 6. Riscos/impedimentos para a próxima sprint

- **Integração com API do WhatsApp (US #8 e #9):** Necessidade de definir a estratégia de envio de mensagens (provedor de mensageria/webhook ou simulação controlada para testes sem custos adicionais de disparos) e tratamento de falhas assíncronas de rede.
