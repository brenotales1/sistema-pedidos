# Mostra Virtual — Center Pedidos

**Frase de destaque:** Sistema web de gestão de pedidos, estoque de bobinas e automação de avisos via WhatsApp para comunicação visual.

**Resumo:** Desenvolvido para uma empresa familiar de comunicação visual com 4 funcionários e ~40 pedidos semanais, o sistema substitui o controle manual e planilhas por uma plataforma web integrada. A solução centraliza a gestão de pedidos com cálculo de aproveitamento de corte, controle de estoque de bobinas por código de barras e estoque mínimo. O diferencial técnico é o envio automático de mensagens aos clientes via Meta WhatsApp Cloud API quando o pedido fica pronto, com histórico auditado e persistência desacoplada da rede, garantindo alta confiabilidade operacional.

## Equipe
| Nome completo | RA | Papéis exercidos (Sprints 1–4) |
|---|---|---|
| Breno Tales de Oliveira Leite | 2840482423029 | S1: Qualidade e testes (CT01–CT05) · S2: Leitor de código de barras e estoque · S3: Integração Meta WhatsApp API · S4: QA, suíte de 115 testes e fechamento do MVP |
| Daniel Fredi Soares Pereira | 2840482421054 | S1: Autenticação, perfis e modelos · S2: Relatório de movimentações e isolamento de banco · S3: Testes automatizados do WhatsApp · S4: Histórico de notificações, estoque mínimo e cancelamento seguro |

**Cliente / PO:** Empresa familiar de pequeno porte de comunicação visual · **Trilha:** A (TCC: Sistema Web de Controle de Estoque para Empresa de Comunicação Visual)

**Tecnologias:** Python 3.12, Flask 3.1.3, Jinja2, Flask-SQLAlchemy, SQLite, Meta WhatsApp Cloud API, Gunicorn, Render, unittest

## Links
- Vídeo: https://www.youtube.com/watch?v=42EjsnOwr6k
- Deploy: https://center-pedidos.onrender.com
- Repositório: https://github.com/brenotales1/sistema-pedidos

## Aprendizado da equipe
A engenharia ágil se consolidou no revezamento da equipe entre desenvolvimento e qualidade: critérios de aceite claros evitaram retrabalho, testes automatizados (131 aprovados) garantiram refatorações seguras de regras complexas de estoque e transações, e retrospectivas reais permitiram adaptar o escopo com foco nas prioridades de maior valor para o cliente.

## Imagens enviadas
- [capa.png](screenshots/capa.png) (1280×720)
- [tela-1.png](screenshots/tela-1.png) (1920×1080)
- [tela-2.png](screenshots/tela-2.png) (1920×1080)
- [tela-3.png](screenshots/tela-3.png) (1920×1080)
