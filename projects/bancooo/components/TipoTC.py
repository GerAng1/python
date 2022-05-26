_tarjetas = {
    'clasica': {'tipo': "Clásica", 'limite': 7500, 'anual': 699, 'min': 29, 'max': 47},
    'oro': {'tipo': "Oro", 'limite': 15000, 'anual': 959, 'min': 25, 'max': 45},
    'platino': {'tipo': "Platino", 'limite': 45000, 'anual': 1999, 'min': 16, 'max': 33},
    'black': {'tipo': "Black", 'limite': 100000, 'anual': 4599, 'min': 9.9, 'max': 26}
}

_fecha_corte = 28


class CreditCard:
    def __init__(self, tarjeta):
        self.tipo =
        self.limite = tarjeta['limite']
        self.anual = tarjeta['anual']
        self.min = tarjeta['min']
        self.max = tarjeta['max']

    def tiie():
        tiie = (_fecha_corte * 100) / 360
        return tiie

    def tia(self):
        tia = self.tiie() + (max - min)
        return tia

    def tim(self):
        tim = (self.tia() / 360) * 30
        return tim

    def get_limitee(self):
        return self.limite
