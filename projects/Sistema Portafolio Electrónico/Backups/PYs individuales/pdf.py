from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.rect(5, 5.1, 205.9, 269.4)
        self.set_xy(12.1,8.4)
        self.image("../util/logo.png", w = 69.6, h = 34)
        self.set_font("Times", "B", 22)
        self.set_xy(78.6, 12.7)
        self.cell(txt = "Confirmación de Operación Forward", align = "C")
        self.ln(17)
        self.cell(125.7)
        self.cell(txt = "Fecha: " + fecha, align = "R")

    def footer(self):
        self.set_y(-15)
        self.set_font('Times', 'I', 8)
        self.cell(0, 10, 'Página ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')


def genera_carta(tipo_carta, derivado, timestamp_hoy, tasa_cambio):
    fecha_inicio = derivado['Fecha Evento'].strptime("%d/%b/%Y, %H:%M:%S")
    fecha_final = derivado['Fecha Cobro'].strptime("%d/%b/%Y")
    plazo = (fecha_final - fecha_inicio).days

    datos_tabla1 = [
    ["Referencia / fecha", timestamp_hoy.strftime("%d/%b/%Y-%H:%M:%S")],
    ["Evento", tipo_carta]
    ]

    if tipo_carta == "Forward Adquirido":
        datos_tabla2 = [
        ["Monto pactado", moneyfy(derivado['Monto pactado'])],
        ["Tipo de cambio al día de contratación", moneyfy(tipo_cambio)],
        ["Precio Forward", moneyfy(derivado['Precio Forward'])],
        ["Plazo", plazo + " días"],
        ["Fecha liquidación", derivado['Fecha Cobro']],
        ]
    elif tipo_carta ==  "Forward Liquidado":
        datos_tabla2 = [
        ["Monto pactado", moneyfy(derivado['Monto pactado'])],
        ["Tipo de cambio al día de contratación", moneyfy(tipo_cambio)],
        ["Precio Forward", moneyfy(derivado['Precio Forward'])],
        ["Plazo", plazo + " días"],
        ["Fecha liquidación", derivado['Fecha Cobro']],
        ["Tipo de cambio al día de liquidación", moneyfy(tasa_cambio)]
        ]

    pdf = PDF(format = "Letter")
    pdf.add_page()

    pdf.set_font("Times", "B", 13)
    pdf.ln(25)
    pdf.cell(txt = "Dirigido a:")
    pdf.ln(5)
    pdf.cell(txt = "Eduardo Rubinstein Meizner")
    pdf.ln(20)
    pdf.set_font("Times", "", 11)
    pdf.cell(txt = "Estimado Sr.")
    pdf.ln(10)
    pdf.cell(txt = "Hemos procedido a realizar la siguiente operación Forward de acuerdo a su instrucción realizado.")
    pdf.ln(10)
    pdf.cell(txt = "1. Detalles de la operación")
    pdf.ln(10)
    pdf.set_font("Times", "B", 11)
    pdf.cell(txt = "Términos Generales")
    pdf.ln(15)

    pdf.set_line_width(0.0035)
    alternate = 0
    for row in datos_tabla1:
        pdf.cell(30)
        cont = 0
        for datum in row:
            if cont == 0:
                pdf.set_fill_color(220, 220, 220)
                pdf.set_font("helvetica", "B", 10)
                pdf.cell(h = 9, w = 69.1, txt = datum, border = 1, fill = True)
                cont = 1
            else:
                pdf.set_font("helvetica", "", 10)
                if alternate % 2 == 0:
                    pdf.set_fill_color(245, 245, 245)
                    pdf.cell(h = 9, w = 69.1, txt = datum, border = 1, fill = True)
                    alternate += 1
                else:
                    pdf.cell(h = 9, w = 69.1, txt = datum, border = 1)
                    alternate += 1
                cont = 0
        pdf.ln()

    pdf.ln(15)
    pdf.set_font("Times", "", 11)
    pdf.cell(txt = "De acuerdo con nuestro acuerdo de la fecha de negociación como se indica anteriormente, confirmamos la siguiente")
    pdf.ln()
    pdf.cell(txt = 'operación "' + tipo_carta + '".')
    pdf.ln(15)

    for row in datos_tabla2:
        pdf.cell(30)
        cont = 0
        for datum in row:
            if cont == 0:
                pdf.set_fill_color(220, 220, 220)
                pdf.set_font("helvetica", "B", 10)
                pdf.cell(h = 9, w = 69.1, txt = datum, border = 1, fill = True)
                cont = 1
            else:
                pdf.set_font("helvetica", "", 10)
                if alternate == 1:
                    pdf.set_fill_color(245, 245, 245)
                    pdf.cell(h = 9, w = 69.1, txt = datum, border = 1, fill = True)
                    alternate = 0
                else:
                    pdf.cell(h = 9, w = 69.1, txt = datum, border = 1)
                    alternate = 1
                cont = 0
        pdf.ln()

    pdf.ln(20)
    pdf.set_font("Times", "I", 11)
    pdf.cell(w = 190, txt = "Gracias por hacer uso de este sistema.", align = "C")

    pdf.output('Factura.pdf')
