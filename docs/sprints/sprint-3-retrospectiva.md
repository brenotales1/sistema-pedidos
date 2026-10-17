# Ata de Retrospectiva — Sprint 3 (E7)

**Equipe:** Breno Tales de Oliveira Leite e Daniel Fredi Soares Pereira
**Registro:** 17/10/2026. Consolidação técnica da entrega; sem atribuir falas ou reunião não registrada.

## 1. O que funcionou bem

A divisão entre implementação do Breno e validação/documentação do Daniel permitiu exercitar o fluxo completo sem chamadas externas. A factory Flask aceita SQLite em memória. Separar o commit do pedido da tentativa de envio preserva a operação quando a API falha. A restrição por transição evita tentativas duplicadas.

## 2. Dificuldades e soluções

A pasta local ainda continha uma integração Twilio divergente da main. Os arquivos da integração foram substituídos pela versão Meta do Breno, conforme autorização de Daniel. Mocks e expectativas antigas do SDK foram adaptados para `requests.post`, payload JSON, Bearer fictício e retorno wamid.

Os testes cobrem as particularidades dos templates Meta: parâmetros de cliente/pedido nos templates funcionais e ausência de parâmetros em `hello_world`. Erros HTTP 400/500, timeout e conexão são simulados sem comprometer a finalização. O Python global não tinha as dependências; a execução aprovada usou o ambiente virtual existente.

## 3. Melhorias para a próxima sprint

| Ação | Responsabilidade proposta | Critério de verificação |
|---|---|---|
| Preservar wamid completo com migração | Breno | Identificador da API mantido sem truncamento |
| Processar callbacks com autenticação e atualizar entrega | Breno | Testes de evento válido, inválido e repetido |
| Reduzir dados pessoais nos logs do conector/webhook | Dupla | Logs sem telefone, credenciais ou payload bruto |
| Substituir usos legados de Query.get e utcnow | Dupla | Suíte sem os avisos correspondentes |
| Evoluir consulta administrativa de notificações (US #10) | Dupla | Cliente, pedido, data e resultado consultáveis |

## 4. Aprendizados

Aceite HTTP não equivale a entrega. Um teste de integração deve verificar conjuntamente feedback, status do pedido e resultado persistido. `TESTING=True` precisa bloquear envio mesmo com integração habilitada e credenciais configuradas. Casos CT08/CT09 de notificações citados na retrospectiva anterior são identificados como CT42/CT43 para preservar os IDs históricos de autenticação.
