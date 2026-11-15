# UML — Modelo final de pedidos e materiais

**Equipe:** Breno Tales de Oliveira Leite (RA: 2840482423029) — Daniel Fredi Soares Pereira (RA: 2840482421054)<br>
**Atualização:** 15/11/2026

## 1. Classes do relacionamento N:N

```mermaid
classDiagram
    class Pedido {
        +id: int
        +cliente_id: int
        +status: string
        +consumos: ConsumoMaterial[]
    }
    class Material {
        +id: int
        +nome: string
        +largura_m: float
        +metros_disponiveis: float
        +consumos: ConsumoMaterial[]
    }
    class ConsumoMaterial {
        +pedido_id: int
        +material_id: int
        +quantidade_metros: float
        +principal: bool
    }
    Pedido "1" --> "0..*" ConsumoMaterial
    Material "1" --> "0..*" ConsumoMaterial
```

A classe associativa implementa a relação N:N e registra o consumo por pedido e material. A coleção pode estar vazia em pedidos antigos não identificados; pedidos novos possuem pelo menos o material principal.

## 2. Fluxo de salvamento

```mermaid
sequenceDiagram
    actor Usuario
    participant Tela
    participant Controlador
    participant Estoque
    participant Banco
    Usuario->>Tela: Informa principal e materiais adicionais
    Tela->>Controlador: Envia pedido e consumos
    Controlador->>Controlador: Valida cliente, corte, materiais e quantidades
    alt Edicao
        Controlador->>Estoque: Estorna todos os consumos anteriores
    end
    Controlador->>Estoque: Baixa cada material
    Controlador->>Banco: Grava pedido, associacoes e movimentacoes
    alt Falha
        Controlador->>Banco: Rollback integral
    else Sucesso
        Controlador->>Banco: Commit
        Controlador->>Tela: Detalhe com todos os materiais
    end
```

O envio de notificações continua ligado à transição de status. A inclusão de materiais não dispara mensagens.

Veja o [DER final](der.md), a [implementação](../models/consumo_material.py) e os [testes](../tests/test_consumo_material.py). A [UML E3](E3-uml.md) continua disponível como artefato histórico.
