from jinja2 import Template
from weasyprint import HTML
import os

def gerar_relatorio(lv, bw, h, fyk, Es, vs, fcd, fyd, qtotal, Mtd, Msd, xLN_value, hn, tempos, phi_total_values, phi_total_graph, pdf_name):
    """Gera um relatório em PDF com os resultados do cálculo."""
    
    # Verifica se a imagem existe antes de renderizar
    if not os.path.exists(phi_total_graph):
        print(f"⚠️ ERRO: A imagem {phi_total_graph} não foi encontrada!")
        return

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
        "tempos": tempos, "phi_total_values": phi_total_values,
        "phi_total_graph": os.path.abspath(phi_total_graph)  # 🔹 Converte o caminho da imagem para absoluto
    }

    # Renderizar HTML com zip incluído
    html_content = template.render(**data, zip=zip)

    # Criar o PDF (base_url="." garante que a imagem seja encontrada)
    HTML(string=html_content, base_url=".").write_pdf(pdf_name)
    print(f"\n✅ Relatório gerado com sucesso: {pdf_name}\n")
