import numpy as np

def beta_bc(fcm):
    """Efeito da resistência do concreto na fluência básica."""
    return 1.8 / (fcm ** 0.7)

def beta_bct(t, t0):
    """Tempo de desenvolvimento da fluência básica."""
    delta_t = (t - t0) + 1
    delta_t = np.maximum(delta_t, 1e-6)  # Evita valores negativos ou zero
    return np.log((((30 / t0) + 0.035) ** 2) * delta_t)

def phi_bc(t, t0, fcm):
    """Calcula o coeficiente de fluência básica."""
    return beta_bc(fcm) * beta_bct(t, t0)

def beta_dcfm(fcm):
    """Fator de fluência dependente do fcm."""
    return 412 / (fcm ** 1.4)

def beta_dcRH(RH, hn):
    """Fator de fluência dependente da umidade relativa e espessura equivalente."""
    return (1 - RH / 100) / ((hn * 0.1 / 100) ** (1 / 3))

def beta_dct0(t0):
    """Fator dependente da idade do concreto no carregamento."""
    return 1 / (0.1 + (t0 ** 0.2))

def beta_dc(t, t0, hn, fcm):
    """Fator de desenvolvimento da fluência de secagem."""
    gamma_t0 = 1 / (2.3 + 3.5 * np.sqrt(np.maximum(t0, 1e-6)))  # Garante que t0 > 0
    beta_h = 1.5 * hn + 250 * np.sqrt(35 / fcm)

    divisor = (beta_h + t - t0)
    divisor = np.maximum(divisor, 1e-6)  # Evita divisão por zero
    
    return ((t - t0) / divisor) ** gamma_t0

def phi_dc(t, t0, fcm, hn, RH):
    """Calcula o coeficiente de fluência de secagem."""
    return beta_dcfm(fcm) * beta_dcRH(RH, hn) * beta_dct0(t0) * beta_dc(t, t0, hn, fcm)

def phi_total(t, t0, fcm, hn, RH):
    """Calcula o coeficiente de fluência total."""
    return phi_bc(t, t0, fcm) + phi_dc(t, t0, fcm, hn, RH)
