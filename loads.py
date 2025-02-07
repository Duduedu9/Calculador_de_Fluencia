def calculate_loads(qpp, qalv, qvar, lv):
    """Calcula as cargas e os momentos da viga."""
    qtotal = (1.35 * (qpp + qalv)) + (1.5 * qvar)  # kN/m, carga total
    w = qtotal * lv  # kN, carga distribuída

    Msd = (w * lv**2) / 8  # kN·m, momento solicitante
    Mtd = Msd  # Assumindo que o momento de cálculo seja igual ao solicitante

    return qtotal, w, Mtd, Msd
