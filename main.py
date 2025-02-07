import numpy as np
import matplotlib.pyplot as plt
from geometry import calculate_geometry, calculate_hn
from material_properties import calculate_concrete_properties, calculate_steel_properties
from loads import calculate_loads
from creep_calculation import phi_total
from generate_pdf import gerar_relatorio
from sympy import symbols, Eq, solve
import re  

def get_float_input(prompt):
    """Função para garantir que o usuário insira um valor numérico válido."""
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("⚠️ ERRO: Insira um número válido!")

def get_pdf_name():
    """Obtém o nome do arquivo PDF e remove caracteres inválidos."""
    pdf_name = input("\n💾 Digite o nome do arquivo PDF (sem extensão): ").strip()
    if not pdf_name:
        pdf_name = "relatorio_fluencia"
    pdf_name = re.sub(r'[<>:"/\\|?*]', '', pdf_name)  
    return pdf_name + ".pdf"

def main():
    print("\n🔹 Bem-vindo ao **Calculador de Fluência Eurocode 2** 🔹\n")

    # 🚀 Pedir os valores ao engenheiro
    lv = get_float_input("Digite o vão efetivo da viga (mm): ")
    bw = get_float_input("Digite a largura da viga (mm): ")
    h = get_float_input("Digite a altura da viga (mm): ")
    phi_pos = get_float_input("Digite o diâmetro da armadura positiva (mm): ")
    nbarras = int(get_float_input("Digite o número de barras da armadura positiva: "))
    cob = get_float_input("Digite o cobrimento da armadura (mm): ")

    fck = get_float_input("Digite a resistência característica à compressão do concreto (MPa): ")
    fyk = get_float_input("Digite a tensão de escoamento do aço (MPa): ")
    Es = get_float_input("Digite o módulo de elasticidade do aço (GPa): ")
    vs = 0.3  

    qpp = get_float_input("Digite o peso próprio da viga (kN/m): ")
    qalv = get_float_input("Digite a carga de alvenaria (kN/m): ")
    qvar = get_float_input("Digite a carga variável (kN/m): ")

    RH = get_float_input("Digite a umidade relativa (%): ")
    t0 = get_float_input("Digite a idade do concreto ao carregamento (dias): ")

    # 🚀 Cálculos Geométricos
    Ac, Ac_cm2, As, As_cm2, d = calculate_geometry(lv, bw, h, phi_pos, nbarras, cob)
    hn = calculate_hn(Ac, bw, h)

    # 🚀 Propriedades do Concreto e do Aço
    fcm, fctm, Ecm = calculate_concrete_properties(fck)
    fyk, Es, vs = calculate_steel_properties(fyk, Es, vs)

    # 🚀 Coeficientes de Norma
    gamma_c = 1.5  
    gamma_s = 1.15  

    # 🚀 Resistências de Cálculo
    fcd = fck / gamma_c  
    fyd = fyk / gamma_s  

    # 🚀 Cálculo de Cargas e Momentos
    qtotal, w, Mtd, Msd = calculate_loads(qpp, qalv, qvar, lv)

    # 🚀 Cálculo da Linha Neutra (xLN)
    xLN = symbols('xLN', real=True, positive=True)
    M1 = 0.68 * fcd * bw * xLN * (d - 0.4 * xLN) - Msd
    eq_xLN = Eq(M1, 0)
    xLN_value = min([sol.evalf() for sol in solve(eq_xLN, xLN) if sol.is_real and sol > 0], default=0)

    # 🚀 Calcular a fluência para diferentes tempos
    tempos = [30, 100, 1000, 10000, 36500, 100000, 180000]
    phi_total_values = phi_total(np.array(tempos), t0, fcm, hn, RH)

    # 🚀 Gerar e salvar o gráfico
    plt.figure(figsize=(8, 4))
    plt.plot(tempos, phi_total_values, marker='o', color='red', linestyle='-')
    plt.title(r'Coeficiente de Fluência Total $\phi(t, t_0)$ (Eurocode 2: 2023)')
    plt.xlabel('Tempo (dias)')
    plt.ylabel(r'$\phi(t, t_0)$')
    plt.grid(True)
    plt.savefig("phi_total.png")
    plt.show()

    # 🚀 Obter o nome do PDF
    pdf_name = get_pdf_name()

    # 🚀 Gerar o relatório em PDF com o nome especificado
    gerar_relatorio(lv, bw, h, fyk, Es, vs, fcd, fyd, qtotal, Mtd, Msd, xLN_value, hn, tempos, phi_total_values,"phi_total.png", pdf_name)

    print(f"\n✅ Relatório gerado com sucesso: {pdf_name}\n")

if __name__ == "__main__":
    main()
