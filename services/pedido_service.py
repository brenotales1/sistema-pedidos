import unicodedata


def normalizar_busca(valor):
    texto = str(valor or "").strip().lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(char for char in texto if not unicodedata.combining(char))
    return "".join(texto.split())


def converter_para_metros(valor_texto, unidade):
    valor = float(str(valor_texto).replace(",", "."))
    if unidade == "cm":
        return round(valor / 100, 2)
    return round(valor, 2)


def formatar_metros(valor):
    return f"{valor:.2f}".replace(".", ",") + "m"


def formatar_area(valor):
    return f"{valor:.2f}".replace(".", ",") + " m²"


def calcular_melhor_aproveitamento(variacoes, largura_m, altura_m, quantidade, extra_stock=None):
    extra_stock = extra_stock or {}
    area_total = round(largura_m * altura_m * quantidade, 2)
    candidatos = []

    for variacao in variacoes:
        opcoes = []

        if largura_m <= variacao.largura_m:
            opcoes.append(
                {
                    "orientacao": "Padrao",
                    "metros_por_unidade": altura_m,
                    "medida_na_bobina": largura_m,
                }
            )

        if altura_m <= variacao.largura_m:
            opcoes.append(
                {
                    "orientacao": "Rotacionado",
                    "metros_por_unidade": largura_m,
                    "medida_na_bobina": altura_m,
                }
            )

        if not opcoes:
            continue

        melhor_opcao = min(
            opcoes,
            key=lambda opcao: (
                opcao["metros_por_unidade"],
                round(variacao.largura_m - opcao["medida_na_bobina"], 2),
                variacao.largura_m,
            ),
        )

        metros_consumidos = round(melhor_opcao["metros_por_unidade"] * quantidade, 2)
        metros_disponiveis = round(variacao.metros_disponiveis + extra_stock.get(variacao.id, 0), 2)
        metros_restantes_apos_pedido = round(metros_disponiveis - metros_consumidos, 2)
        area_consumida = round(variacao.largura_m * metros_consumidos, 2)
        desperdicio_total = round(area_consumida - area_total, 2)

        if metros_restantes_apos_pedido < 0:
            continue

        candidatos.append(
            {
                "material": variacao,
                "orientacao": melhor_opcao["orientacao"],
                "metros_por_unidade": round(melhor_opcao["metros_por_unidade"], 2),
                "metros_consumidos": metros_consumidos,
                "largura_rolo": round(variacao.largura_m, 2),
                "medida_na_bobina": round(melhor_opcao["medida_na_bobina"], 2),
                "sobra_largura": round(variacao.largura_m - melhor_opcao["medida_na_bobina"], 2),
                "area_consumida": area_consumida,
                "desperdicio_total": desperdicio_total,
                "metros_restantes_apos_pedido": metros_restantes_apos_pedido,
            }
        )

    if not candidatos:
        return None

    return min(
        candidatos,
        key=lambda candidato: (
            candidato["desperdicio_total"],
            candidato["largura_rolo"],
            candidato["metros_consumidos"],
            candidato["sobra_largura"],
        ),
    )
