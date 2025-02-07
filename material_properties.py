def calculate_concrete_properties(fck):
    """Calcula as propriedades do concreto."""
    fcm = fck + 8  # MPa, resistência média do concreto
    fctm = 0.3 * (fck ** (2/3))  # MPa, resistência média à tração
    Ecm = 22 * ((fcm / 10) ** 0.3)  # GPa, módulo de elasticidade
    return fcm, fctm, Ecm

def calculate_steel_properties(fyk, Es, vs=0.3):
    """Calcula as propriedades do aço."""
    Es = Es * 1000  # Converter GPa para MPa
    return fyk, Es, vs
