import numpy as np

def calculate_geometry(lv, bw, h, phi_pos, nbarras, cob):
    """Calcula a geometria da viga."""
    Ac = bw * h  # mm², área da seção de concreto
    Ac_cm2 = Ac / 100  # cm², conversão

    # Armadura positiva
    As = nbarras * (np.pi * (phi_pos / 2)**2)  # mm², área da armadura
    As_cm2 = As / 100  # cm², conversão

    # Cálculo da altura útil
    d = h - cob - phi_pos / 2  # mm

    if d <= 0:
        print("⚠️ ERRO: A altura útil da seção (d) é negativa! Ajustando automaticamente...")
        d = max(d, 10)  # Define um valor mínimo para evitar problemas

    return Ac, Ac_cm2, As, As_cm2, d

def calculate_hn(Ac, bw, h):
    """Calcula a espessura equivalente da viga (hn)."""
    u = 2 * h + bw  # Perímetro em contato com o ambiente (mm)
    hn = (2 * Ac) / u  # mm
    return max(hn, 10)  # Garante um valor mínimo realista
