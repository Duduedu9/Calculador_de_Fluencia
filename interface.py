from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QGridLayout, QMessageBox)
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import Qt
import sys
import numpy as np
import matplotlib.pyplot as plt
from geometry import calculate_geometry, calculate_hn
from material_properties import calculate_concrete_properties, calculate_steel_properties
from loads import calculate_loads
from creep_calculation import phi_total
from generate_pdf import gerar_relatorio
from sympy import symbols, Eq, solve
import re

class FluenciaApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Fluência - Eurocode 2")
        self.setGeometry(100, 100, 600, 750)
        self.setStyleSheet("""
            QWidget { background-color: #0D47A1; color: white; }
            QLabel { font-size: 12pt; }
            QLineEdit {
                background-color: white; color: black; 
                border: 1px solid #64B5F6; padding: 5px; border-radius: 5px;
            }
            QPushButton {
                background-color: #1565C0; color: white; 
                font-size: 12pt; padding: 8px; border-radius: 5px;
            }
            QPushButton:hover { background-color: #1E88E5; }
        """)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 🔹 Título
        title = QLabel("Calculadora de Fluência - Eurocode 2")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # 🔹 Grid para inputs
        grid = QGridLayout()
        self.inputs = {}

        labels = [
            "Vão efetivo da viga (mm):", "Largura da viga (mm):", "Altura da viga (mm):",
            "Diâmetro da armadura positiva (mm):", "Número de barras:", "Cobrimento (mm):",
            "Fck (MPa):", "Fyk (MPa):", "Es (GPa):", "Peso próprio (kN/m):",
            "Carga de alvenaria (kN/m):", "Carga variável (kN/m):",
            "Umidade relativa (%):", "Idade do concreto ao carregamento (dias):"
        ]

        for i, label in enumerate(labels):
            lbl = QLabel(label)
            lbl.setFont(QFont("Arial", 10))
            self.inputs[label] = QLineEdit()
            self.inputs[label].setPlaceholderText("Digite um valor...")
            grid.addWidget(lbl, i, 0)
            grid.addWidget(self.inputs[label], i, 1)

        layout.addLayout(grid)

        # 🔹 Botão Calcular
        self.calc_button = QPushButton("Calcular e Gerar PDF")
        self.calc_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.calc_button.clicked.connect(self.calcular_fluencia)
        layout.addWidget(self.calc_button)

        # 🔹 Exibir Gráfico
        self.graph_label = QLabel()
        self.graph_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.graph_label)

        self.setLayout(layout)

    def calcular_fluencia(self):
        try:
            # 🔹 Capturar dados inseridos
            lv = float(self.inputs["Vão efetivo da viga (mm):"].text())
            bw = float(self.inputs["Largura da viga (mm):"].text())
            h = float(self.inputs["Altura da viga (mm):"].text())
            phi_pos = float(self.inputs["Diâmetro da armadura positiva (mm):"].text())
            nbarras = int(self.inputs["Número de barras:"].text())
            cob = float(self.inputs["Cobrimento (mm):"].text())
            fck = float(self.inputs["Fck (MPa):"].text())
            fyk = float(self.inputs["Fyk (MPa):"].text())
            Es = float(self.inputs["Es (GPa):"].text())
            qpp = float(self.inputs["Peso próprio (kN/m):"].text())
            qalv = float(self.inputs["Carga de alvenaria (kN/m):"].text())
            qvar = float(self.inputs["Carga variável (kN/m):"].text())
            RH = float(self.inputs["Umidade relativa (%):"].text())
            t0 = float(self.inputs["Idade do concreto ao carregamento (dias):"].text())

            # 🚀 Cálculos Geométricos
            Ac, Ac_cm2, As, As_cm2, d = calculate_geometry(lv, bw, h, phi_pos, nbarras, cob)
            hn = calculate_hn(Ac, bw, h)

            # 🚀 Propriedades do Concreto e do Aço
            fcm, fctm, Ecm = calculate_concrete_properties(fck)
            fyk, Es, vs = calculate_steel_properties(fyk, Es, 0.3)

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

            # 🚀 Gerar gráfico
            grafico_path = "phi_total.png"
            plt.figure(figsize=(8, 4))
            plt.plot(tempos, phi_total_values, marker='o', color='red', linestyle='-')
            plt.title(r'Coeficiente de Fluência Total $\phi(t, t_0)$')
            plt.xlabel('Tempo (dias)')
            plt.ylabel(r'$\phi(t, t_0)$')
            plt.grid(True)
            plt.savefig(grafico_path, dpi=100)
            plt.close()

            # 🔹 Atualizar exibição do gráfico na interface
            self.graph_label.setPixmap(QPixmap(grafico_path).scaled(400, 200, Qt.KeepAspectRatio))

            # 🔹 Gerar PDF
            pdf_name = "relatorio_fluencia.pdf"
            gerar_relatorio(lv, bw, h, fyk, Es, vs, fcd, fyd, qtotal, Mtd, Msd, xLN_value, hn, tempos, phi_total_values, grafico_path, pdf_name)

            QMessageBox.information(self, "Sucesso", f"Relatório gerado: {pdf_name}")

        except ValueError:
            QMessageBox.warning(self, "Erro", "Por favor, insira valores numéricos válidos.")

# 🔹 Inicializar a aplicação
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FluenciaApp()
    window.show()
    sys.exit(app.exec())
