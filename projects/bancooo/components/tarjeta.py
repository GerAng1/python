from datetime import date


class Tarjeta:
    def __init__(self, no_tarjeta, nip):
        self.no_tarjeta = no_tarjeta
        self.nip = nip
        self.fecha_expe = date.today()
        self.fecha_expi = date.today().replace(year=(date.today().year + 5))

    def compras(cantidad):
        print("Compras desde tarjeta.py! Cantidad:", cantidad)

    def retiros(cantidad):
        print("Retiros desde tarjeta.py! Cantidad:", cantidad)

    def print_tipo():
        pass

    def print_tarjeta():
        pass

    def get_no_tarjeta(self):
        return self.no_tarjeta

    def get_nip(self):
        return self.nip

    def get_mes(self):
        return self.fecha_expe.month

    def get_anno_expe(self):
        return self.fecha_expe.year

    def get_expi_year(self):
        return self.fecha_expi.year
