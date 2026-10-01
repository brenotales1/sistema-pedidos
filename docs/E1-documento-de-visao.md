# Documento de Visão — Sistema Web de Controle de Estoque para Empresa de Comunicação Visual

**Equipe:** Daniel Fredi Soares Pereira (2840482421054), Breno Tales de Oliveira Leite (2840482423029)  
**Trilha:** A (vinculada ao TCC)  
**Origem do problema:** Cliente real — empresa familiar de pequeno porte / adaptação de TCC  
**Data:** 21/08/2026  

---

## 1. Problema

A empresa de comunicação visual é uma empresa familiar de pequeno porte, com 4 funcionários, que realiza em média 40 pedidos por semana e utiliza materiais como lonas, adesivos, ACM, tintas, chapas de poliestireno (PS), solventes, panos de limpeza e outros insumos. As tintas são utilizadas em duas máquinas, com quatro cores para cada uma. O ACM é adquirido conforme a necessidade, principalmente quando há um pedido que utiliza esse material.

Atualmente, parte do controle de pedidos e estoque depende de registros e conferências manuais. O contato com clientes sobre o andamento dos pedidos pode consumir aproximadamente 4 horas por semana, considerando cerca de 40 notificações realizadas manualmente. A empresa ainda não possui um sistema de controle de estoque. A conferência dos materiais é realizada manualmente pelo menos uma vez por semana, abrangendo aproximadamente 30 materiais distribuídos entre diferentes categorias. Considerando uma média de 2 minutos por material para localizar, conferir e registrar a quantidade disponível, a verificação semanal representa aproximadamente 56 minutos, ou cerca de 1 hora de trabalho por semana.

Esses processos aumentam o risco de erros de registro, esquecimentos nas notificações e divergências na quantidade disponível em estoque. O Laboratório irá atuar na automação da comunicação com os clientes pelo WhatsApp e no apoio ao controle do estoque, sem incluir a entrada de materiais por código de barras, pois essa operação ainda não faz parte da rotina da empresa.

---

## 2. Público-alvo e perfis de usuário

| Perfil | Quem é | O que faz no sistema |
|---|---|---|
| **Administrador** | Responsável pela gestão da empresa | Gerencia usuários, clientes, pedidos, materiais e estoque |
| **Funcionário** | Colaborador responsável pela operação | Consulta pedidos e auxilia no controle e conferência dos materiais |

---

## 3. Visão da solução

O sistema centraliza o gerenciamento de pedidos e o controle de estoque da empresa de comunicação visual. Durante o Laboratório, será incorporada uma integração ao sistema existente: uma API para envio de notificações aos clientes pelo WhatsApp. A integração reduzirá a necessidade de comunicação manual. O sistema também apoiará o registro e a consulta das quantidades de materiais, considerando a rotina atual de conferência manual semanal.

---

## 4. Objetivos do MVP (o que o semestre entrega)

- Reduzir de aproximadamente 4 horas para no máximo 1 hora por semana o tempo gasto com notificações manuais aos clientes sobre o andamento dos pedidos.
- Apoiar o controle dos aproximadamente 30 materiais utilizados na empresa, organizados por categorias e com consulta das quantidades disponíveis.
- Reduzir erros e esquecimentos relacionados ao controle manual de materiais e às notificações dos clientes.
- Atingir pelo menos 95% de sucesso nos testes da nova integração com o WhatsApp, incluindo cenários de operação válida e tratamento de erros.
- Manter registros das conferências e alterações de materiais realizadas no sistema.

---

## 5. Fora de escopo (explicitamente)

- Desenvolvimento de aplicativo mobile nativo, pois o incremento será realizado na aplicação web existente.
- Integração com outros aplicativos de mensagens além do WhatsApp, pois o foco do semestre será a comunicação por esse canal.
- Automação de compras e reposição de materiais junto a fornecedores.
- Entrada de materiais por código de barras no escopo manual básico do TCC, sendo desenvolvido como incremento de automação no Laboratório.

---

## 6. Requisitos mínimos do §3 do Manual — como este projeto cobre cada um

| Requisito mínimo | Como este projeto cobre |
|---|---|
| **Autenticação com 2+ perfis** | Login com perfis Administrador e Funcionário/Estoquista, com permissões distintas |
| **6+ entidades com relacionamento N:N** | Usuário, Perfil, Cliente, Pedido, ItemPedido, Produto/Serviço, Material e MovimentaçãoEstoque; N:N entre Pedido e Material por meio de ConsumoMaterial |
| **Regra de negócio não trivial** | Eventos dos pedidos podem disparar notificações pelo WhatsApp; o sistema também registra e consulta informações de materiais e aproveitamento de corte |
| **Consulta agregada (relatório/dashboard)** | Dashboard com pedidos por status e informações de materiais/estoque |
| **Validações em interface e banco** | Campos obrigatórios, quantidades válidas e constraints de integridade no banco |
| **Deploy público por URL** | Sistema será implantado em ambiente público para demonstração durante as Sprint Reviews |
| **Repositório Git com README** | Código versionado em repositório Git, com README contendo instalação, execução e configuração das integrações |

---

## 7. Riscos identificados

| Risco | Impacto | Mitigação |
|---|---|---|
| **Instabilidade ou limitação da API de WhatsApp** | Alto | Implementar tratamento de erros e registrar falhas de envio |
| **Falha ou inconsistência no registro de materiais** | Médio | Validar os dados informados e manter histórico das alterações |
| **Inconsistência nas informações de estoque** | Alto | Centralizar os registros no sistema e manter conferência manual periódica |
| **Dificuldade de integração com o sistema existente** | Médio | Desenvolver as APIs de forma incremental e realizar testes de integração |
