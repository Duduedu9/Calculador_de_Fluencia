from jinja2 import Template
from weasyprint import HTML

def gerar_relatorio(lv, bw, h, fyk, Es, vs, fcd, fyd, qtotal, Mtd, Msd, xLN_value, hn, tempos, phi_total_values, pdf_name):
    """Gera um relatório em PDF com os resultados do cálculo."""
    
    # Ler o template HTML
    with open("report_template.html", "r", encoding="utf-8") as file:
        template_source = file.read()
        template = Template(template_source)

    # Criar um dicionário com os dados
    data = {
        "lv": lv, "bw": bw, "h": h,
        "fyk": fyk, "Es": Es, "vs": vs,
        "fcd": fcd, "fyd": fyd,
        "qtotal": qtotal, "Mtd": Mtd, "Msd": Msd,
        "xLN_value": xLN_value, "hn": hn,
        "tempos": tempos, "phi_total_values": phi_total_values
    }

    # Renderizar HTML com zip incluído
    html_content = template.render(**data, zip=zip)

    # Criar o PDF
    HTML(string=html_content).write_pdf(pdf_name)
    print(f"\n✅ Relatório gerado com sucesso: {pdf_name}\n")
