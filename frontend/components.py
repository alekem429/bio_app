from dash import html

icons = {
    "be": {"name": "bi-caret-right-fill", "color": "#0000FF"},
    "w": {"name": "bi-caret-up-fill", "color": "#00FF00"},
    "s": {"name": "bi-caret-down-fill", "color": "#FF0000"}
}

palette = [
    '#34af86', '#d18e32', '#ee61f4', '#ae9d31', '#8795f4',
    '#f565cc', '#35ad9e', '#f66ab3', '#f87638', '#3aa6d9',
    '#3ba4e6', '#34af8f', '#dc6ff4', '#f55ee9', '#f76e9a',
    '#33b07a', '#f668c0', '#9ca231', '#38a9c5', '#36ada4',
    '#cc7af4', '#37abb0', '#37abb7', '#63ae31', '#f77277',
    '#33b16b', '#dc8932', '#77ab31', '#e98132', '#36acaa',
    '#f77189', '#ac89f4', '#f66ca7', '#4aa0f4', '#42b231',
    '#a5a031', '#bc82f4', '#f562da', '#37aabe', '#c79332',
    '#39a8ce', '#6e9bf4', '#32b252', '#9b8ff4', '#f7745f',
    '#86a831', '#35ae97', '#92a531', '#b69a32', '#be9732'
]


def generate_color_palette(items):
    items = sorted(items, key=lambda gene: gene['id'])
    return {item['id']: palette[i % len(palette)] for i, item in enumerate(items)}


def flatten_data(data, colors_genes, colors_factors):
    rows = []
    for item in data:
        description = item['description']
        factors = generate_gene_divs(item['factors'], colors_genes)
        genes = generate_gene_divs(item['genes'], colors_factors)

        rows.append(html.Tr([
            html.Td(item['id']),
            html.Td(description),
            html.Td(factors),
            html.Td(genes)
        ], className="mw-100"))
    return rows


def generate_gene_divs(items, colors):
    gene_divs = []
    for i, item in enumerate(items):
        color = colors[item['id']]
        gene_divs.append(
            html.Div(
                [
                    html.Span(item['name'], className="item-name"),
                    html.Span(className=f"bi {icons[item['activation']]['name']}",
                              style={"color": icons[item['activation']]['color']})
                ],
                style={
                    "backgroundColor": color,
                },
                className="table-item"
            )
        )
    return html.Div(gene_divs, className="item-container")
