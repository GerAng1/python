# Aplicación que registra serie de acciones que han sido adquiridos,
# permite la compra y venta de acciones.
#
# ** ESCRIBE ARCHIVOS
# ** SE CONECTA A INTERNET PARA OBTENER PRECIO DE ACCION
# ** MENÚ INTERACTIVO
# ** compara fechas
# ** genera PDFs

# importando librerías necesarias
import sys # para salir del programa
import csv # para escribir y leer csv
import locale # para leer strings de numeros con comas y agregar formato de $$
import requests # para obtener html de sitio web
from fpdf import FPDF # para generar PDFs
from time import sleep # para UX, atrasa el despliegue
from random import uniform # para generar tipos de cambio aleatorios
from datetime import datetime, timedelta # para guardar fecha de transacciones
from tabulate import tabulate # para el formato de tablas
from bs4 import BeautifulSoup as BS # para leer html


# configuracion de región para formato de $$$
locale.setlocale(locale.LC_ALL, 'en_US') # no hay es-MX pero se ve igual


# CLASES

# Para el PDF
class PDF(FPDF):
    def header(self):
        self.rect(5, 5.1, 205.9, 269.4)
        self.set_xy(12.1,8.4)
        self.image("util/logo.png", w = 69.6, h = 34)
        self.set_font("Times", "B", 22)
        self.set_xy(78.6, 12.7)
        self.cell(txt = "Confirmación de Operación Forward", align = "C")
        self.ln(17)
        self.cell(125.7)
        self.cell(txt = "Fecha: " + datetime.now().strftime("%d/%b/%Y"), align = "R")

    def footer(self):
        self.set_y(-15)
        self.set_font('Times', 'I', 8)
        self.cell(0, 10, 'Página ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')


# FUNCIONES AUXILIARES (acciones concretas)

# genera un PDF con la información del derivado
def genera_carta(tipo_carta, derivado, timestamp_hoy, tasa_cambio):
    fecha_inicio = datetime.strptime(derivado['Fecha Evento'], "%d/%b/%Y, %H:%M:%S")
    fecha_final = datetime.strptime(derivado['Fecha Cobro'], "%d/%b/%Y")
    plazo = (fecha_final - fecha_inicio).days

    datos_tabla1 = [
    ["Referencia / fecha", timestamp_hoy.strftime("%d/%b/%Y-%H:%M:%S")],
    ["Evento", tipo_carta]
    ]

    if tipo_carta == "Forward Adquirido":
        datos_tabla2 = [
        ["Monto pactado", moneyfy(float(derivado['Monto pactado'])) + " " + derivado['Divisa']],
        ["Tipo de cambio al día de contratación", moneyfy(tasa_cambio) + " MXN"],
        ["Precio Forward", moneyfy(derivado['Precio Forward']) + " MXN"],
        ["Plazo", str(plazo) + " días"],
        ["Fecha liquidación", derivado['Fecha Cobro']],
        ]
    elif tipo_carta ==  "Forward Liquidado":
        datos_tabla2 = [
        ["Monto pactado", moneyfy(float(derivado['Monto pactado'])) + " " + derivado['Divisa']],
        ["Precio Forward", moneyfy(float(derivado['Precio Forward'])) + " MXN"],
        ["Plazo", str(plazo) + " días"],
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

    pdf.output(timestamp_hoy.strftime("%d%b%Y_%H%M%S") + '.pdf')


# obtiene la cantidad neta de dinero efectivo
# regresa un float
def get_current_cash():
    inicial = 1500000.00
    compras = 0.0
    ventas = 0.0

    # restamos compras y abonamos ventas de acciones en capitales
    with open("util/transacciones_capitales.csv", 'r') as efectivo_csv:
        diccs = csv.DictReader(efectivo_csv)
        for row in diccs:
            if "Compra" in row['Evento']:
                compras += float(row['Costo Total'])
            elif "Venta" in row['Evento'] or "Cobro" in row['Evento']:
                ventas += float(row['Costo Total'])
            else:
                print("ERROR #173")

    # restamos compras de derivados (no sumamos porque son otras divisas)
    with open("util/transacciones_derivados.csv", 'r') as derivados_csv:
        diccs = csv.DictReader(derivados_csv)
        for row in diccs:
            if "Liquidado" in row['Evento']:
                compras += float(row['Total'])
            elif "Compra" in row['Evento']:
                compras += float(row['Total'])
            elif "Venta" in row['Evento']:
                ventas += float(row['Total'])

            else:
                pass


    total = inicial - compras + ventas

    return total


# obtiene el valor total del portafolio basado en su total ponderado
# regresa un float
def get_valor_portafolio_capitales():
    total = 0.0
    with open("util/resumen_capitales.csv", 'r') as portafolio_csv:
        diccs = csv.DictReader(portafolio_csv)
        for row in diccs:
            total += float(row["Total Ponderado"])
            # La linea de abajo te da el valor real del portafolio
            # total += (get_precio_accion(row['Ticker']) * float(row['Cantidad']))

    return total


# obtiene el valor total del portafolio basado en su tasas de cambio
# regresa un float
def get_valor_portafolio_derivados():
    total = 0.0
    with open("util/resumen_derivados.csv", 'r') as portafolio_csv:
        diccs = csv.DictReader(portafolio_csv)
        for row in diccs:
            total += float(row['Equivalente'])

    return total


# obtiene la cantidad neta de dinero que ha obtenido el sistema
# regresa un float
def get_current_comissions():
    total = 0.0
    with open("util/transacciones_capitales.csv", 'r') as commisions_csv:
        diccs = csv.DictReader(commisions_csv)
        for row in diccs:
            total += abs(float(row['Comisión Sistema (1.7%)']))

    with open("util/transacciones_derivados.csv", 'r') as commisions_csv:
        diccs = csv.DictReader(commisions_csv)
        for row in diccs:
            total += abs(float(row['Comisión (0.27%)']))

    return total


# obtiene el precio actual de una divisa en MXN
# regresa un float
def get_current_divisa(divisa):
    url = "https://www.google.com/search?q="
    url += divisa
    url += "+to+mxn"

    # obtiene el request de la url
    data = requests.get(url)
    soup = BS(data.text, 'html.parser')

    # TESTING para hallar texto
    # with open('htmldivisa.html', 'w') as doc:
    #     doc.write(data.text)

    pesos_dirty = soup.find(attrs={"class": "BNeawe iBp4i AP7Wnd"}).text
    pesos_clean = pesos_dirty.split()[0]
    trabado = False

    return locale.atof(pesos_clean)


# obtener el precio actual de una acción
# regresa float
def get_precio_accion(accion):
    url = "https://www.google.com/search?q="
    url += accion
    url += "+precio+accion"

    # obtiene el request de la url
    data = requests.get(url)

    # TESTING para ver html si todo bien
    # with open('util/htmlprecioaccion.html', 'w') as doc:
    #      doc.write(data.text)

    # convierte a texto el html
    soup = BS(data.text, 'html.parser')

    # Primero vemos si si aparece el precio en google y su divisa
    find_currency = str(soup.find_all(attrs={"class": "r0bn4c rQMQod"}))
    find_currency2 = str(soup.find_all(attrs={"class": "xUrNXd UMOHqf"}))

    # encuentra metadata filtrada
    ans = soup.find(attrs={"class": "BNeawe iBp4i AP7Wnd"}).text
    price_sin_formato = locale.atof(ans.split()[0])

    if "USD" in find_currency or "USD" in find_currency2:
        # Convirtiendo a pesos mexicanos
        price_sin_formato *= get_current_divisa("USD")
    elif "MXN" in find_currency or "MXN" in find_currency2:
        pass
    else:
        return "NO SE ENCONTRÓ EL PRECIO"

    return price_sin_formato


# hace el neteo de las acciones que siguen en el portafolio del cliente
# regresa float con promedio ponderado
def nettea_esto(ticker):
    cont = 0
    suma_precios = 0.0

    with open('util/transacciones_capitales.csv', 'r') as leer_trans:
        list_diccs = csv.DictReader(leer_trans)
        for dicc in list_diccs:
            if "Compra " + ticker in dicc["Evento"] and dicc["Vendido"] == "no":
                cont += 1
                suma_precios += float(dicc["Precio Unitario (MXN)"])


    precio_ponderado = suma_precios / cont

    return precio_ponderado if cont > 0 else 0


# adelanta el cobro de derivados al usar datos de un año atrás
# para uso ilustrativo solamente
def speedup(timestamp_derivado):

    # actualizando portafolio de capitales
    new_diccs = []
    with open('util/transacciones_derivados.csv', 'r') as leer_der:
        diccs = csv.DictReader(leer_der)
        existe = False

        for row in diccs:
            if row['Fecha Evento'] == timestamp_derivado:
                existe = True

                dicc_rangos_divisas = {
                    'USD': [19.7, 21.49],
                    'EUR': [23.84, 25.39],
                    'CAD': [15.85, 16.98]
                }

                r_usado = dicc_rangos_divisas.get(row['Divisa'], "ERROR #")
                nuevo_forward = round(uniform(r_usado[0], r_usado[1]), 2)

                nuevo_inicio = datetime.strptime(row['Fecha Evento'], "%d/%b/%Y, %H:%M:%S")
                nuevo_inicio = nuevo_inicio - timedelta(weeks = 52)

                nuevo_final = datetime.strptime(row['Fecha Cobro'], "%d/%b/%Y")
                nuevo_final = nuevo_final - timedelta(weeks = 52)

                new_row = {
                    'Fecha Evento': nuevo_inicio.strftime("%d/%b/%Y, %H:%M:%S"),
                    'Evento': row['Evento'],
                    'Divisa': row['Divisa'],
                    'Monto pactado': row['Monto pactado'],
                    'Precio Forward': nuevo_forward,
                    'Comisión (0.27%)': row['Comisión (0.27%)'],
                    'Plazo (Días)': row['Plazo (Días)'],
                    'Fecha Cobro': nuevo_final.strftime("%d/%b/%Y"),
                    'Total': row['Total'],
                    'Finalizado': row['Finalizado']
                    }
            else:
                new_row = {
                    'Fecha Evento': row['Fecha Evento'],
                    'Evento': row['Evento'],
                    'Divisa': row['Divisa'],
                    'Monto pactado': row['Monto pactado'],
                    'Precio Forward': row['Precio Forward'],
                    'Comisión (0.27%)': row['Comisión (0.27%)'],
                    'Plazo (Días)': row['Plazo (Días)'],
                    'Fecha Cobro': row['Fecha Cobro'],
                    'Total': row['Total'],
                    'Finalizado': row['Finalizado']
                    }
            new_diccs.append(new_row)

        if not existe:
            print("Error #230: No halló la fecha")

    # reagregando registros a derivados
    with open('util/transacciones_derivados.csv', 'w') as op:
      campos = ['Fecha Evento',
      'Evento',
      'Divisa',
      'Monto pactado',
      'Precio Forward',
      'Comisión (0.27%)',
      'Plazo (Días)',
      'Fecha Cobro',
      'Total',
      'Finalizado'
      ]

      output_writer = csv.DictWriter(op, fieldnames=campos)
      output_writer.writeheader()

      for registro in new_diccs:
        output_writer.writerow(registro)

    cobrar_derivados()


# determina el mejor curso a tomar para la venta de una acción: FIFO o LIFO
def best_ifo(ticker, acciones_vendidas, continuar):

    registros_transacciones_fifo = []
    registros_transacciones_lifo = []
    ganancia = get_precio_accion(ticker) * acciones_vendidas

    with open('util/transacciones_capitales.csv', 'r') as leer_trans:
        transacciones = csv.DictReader(leer_trans)

        for registro in transacciones:
            registro_fifo = registro.copy()
            registro_lifo = registro.copy()
            registros_transacciones_fifo.append(registro_fifo)
            registros_transacciones_lifo.append(registro_lifo)

    for i in range(acciones_vendidas):
        cont_fifo = 0
        cont_lifo = 0
        precio_ponderado_fifo = 0.0
        precio_ponderado_lifo = 0.0
        ganancia_fifo = 0.0
        ganancia_lifo = 0.0

        # sacar precio ponderado con FIFO (no tomamos en cuenta el primero)
        for entrada in registros_transacciones_fifo:
            if ticker in entrada['Evento'] and entrada['Vendido'] == "no" and cont_fifo == 0:
                cont_fifo += 1
                entrada['Vendido'] = "si"
                ganancia_fifo = float(entrada['Precio Unitario (MXN)'])
            elif ticker in entrada['Evento'] and entrada['Vendido'] == "no":
                precio_ponderado_fifo += float(entrada["Precio Unitario (MXN)"])
                cont_fifo += 1
            else:
                pass

        if cont_fifo - 1 < 1:
            pass
        else:
            precio_ponderado_fifo /= (cont_fifo - 1)

        fifo_formateado = moneyfy(precio_ponderado_fifo)
        print(" Precio ponderado de acciones restantes si usamos FIFO:", fifo_formateado)

        # sacar precio ponderado con LIFO
        cont_lifo = cont_fifo - 1
        for entrada in registros_transacciones_lifo:
            if ticker in entrada['Evento'] and entrada['Vendido'] == "no" and cont_lifo > 0:
                precio_ponderado_lifo += float(entrada["Precio Unitario (MXN)"])
                cont_lifo -= 1
            elif ticker in entrada['Evento'] and entrada['Vendido'] == "no":
                entrada['Vendido'] = "si"
                ganancia_lifo = float(entrada['Precio Unitario (MXN)'])

        if cont_fifo - 1 < 1:
            pass
        else:
            precio_ponderado_lifo /= (cont_fifo - 1)

        lifo_formateado = moneyfy(precio_ponderado_lifo)
        print(" Precio ponderado de acciones restantes si usamos LIFO:", lifo_formateado)
        print()

        if precio_ponderado_fifo > precio_ponderado_lifo:
            registros_transacciones_lifo = []
            for registro in registros_transacciones_fifo:
                registro_temp = registro.copy()
                registros_transacciones_lifo.append(registro_temp)
            ganancia -= ganancia_fifo
        else:
            registros_transacciones_fifo = []
            for registro in registros_transacciones_lifo:
                registro_temp = registro.copy()
                registros_transacciones_fifo.append(registro_temp)
            ganancia -= ganancia_lifo

        sleep(1)

    # A partir de aquí se trabaja sobre los archivos
        if continuar:
            new_diccs = []
            # ver cuál accion venderá
            if precio_ponderado_fifo > precio_ponderado_lifo:
                print(" Usaremos FIFO\n")
                existe = False

                # actualizando valores
                with open('util/transacciones_capitales.csv', 'r') as leer_trans:
                    diccs = csv.DictReader(leer_trans)

                    for row in diccs:
                        if ticker in row['Evento'] and row['Vendido'] == "no" and existe == False:
                            existe = True

                            ganancia = float(row['Precio Unitario (MXN)'])

                            new_row = {
                                'Fecha Transacción': row['Fecha Transacción'],
                                'Evento': row['Evento'],
                                'Precio Unitario (MXN)': row['Precio Unitario (MXN)'],
                                'IVA (16%)': row['IVA (16%)'],
                                'Comisión Sistema (1.7%)': row['Comisión Sistema (1.7%)'],
                                'Costo Total': row['Costo Total'],
                                'Precio Dólar': row['Precio Dólar'],
                                'Vendido': "si"
                                }

                        else:
                            new_row = {
                                'Fecha Transacción': row['Fecha Transacción'],
                                'Evento': row['Evento'],
                                'Precio Unitario (MXN)': row['Precio Unitario (MXN)'],
                                'IVA (16%)': row['IVA (16%)'],
                                'Comisión Sistema (1.7%)': row['Comisión Sistema (1.7%)'],
                                'Costo Total': row['Costo Total'],
                                'Precio Dólar': row['Precio Dólar'],
                                'Vendido': row['Vendido']
                                }
                        new_diccs.append(new_row)

                    if not existe:
                        print("Error 336: Si vendiste, debe haber una accion", ticker, "no vendida.")

            # lifo es mejor
            else:
                print(" Usaremos LIFO\n")

                # actualizando valores
                cont = cont_fifo - 1
                with open('util/transacciones_capitales.csv', 'r') as leer_trans:
                    diccs = csv.DictReader(leer_trans)

                    for row in diccs:
                        if ticker in row['Evento'] and row['Vendido'] == "no" and cont == 0:

                            new_row = {
                                'Fecha Transacción': row['Fecha Transacción'],
                                'Evento': row['Evento'],
                                'Precio Unitario (MXN)': row['Precio Unitario (MXN)'],
                                'IVA (16%)': row['IVA (16%)'],
                                'Comisión Sistema (1.7%)': row['Comisión Sistema (1.7%)'],
                                'Costo Total': row['Costo Total'],
                                'Precio Dólar': row['Precio Dólar'],
                                'Vendido': "si"
                                }
                        else:
                            new_row = {
                                'Fecha Transacción': row['Fecha Transacción'],
                                'Evento': row['Evento'],
                                'Precio Unitario (MXN)': row['Precio Unitario (MXN)'],
                                'IVA (16%)': row['IVA (16%)'],
                                'Comisión Sistema (1.7%)': row['Comisión Sistema (1.7%)'],
                                'Costo Total': row['Costo Total'],
                                'Precio Dólar': row['Precio Dólar'],
                                'Vendido': row['Vendido']
                                }
                        if ticker in row['Evento'] and row['Vendido'] == "no" and cont > 0:
                            cont -= 1

                        new_diccs.append(new_row)

            # agregando registro a transacciones
            with open('util/transacciones_capitales.csv', 'w') as op:
                campos = ['Fecha Transacción',
                'Evento',
                'Precio Unitario (MXN)',
                'IVA (16%)',
                'Comisión Sistema (1.7%)',
                'Costo Total',
                'Precio Dólar',
                'Vendido']
                output_writer = csv.DictWriter(op, fieldnames=campos)
                output_writer.writeheader()
                for registro in new_diccs:
                    output_writer.writerow(registro)

    return ganancia


# agrega a doc registro de compra de accion
def compra_accion(ticker):
    timestamp = datetime.now().strftime("%d/%b/%Y, %H:%M:%S")
    acciones_compradas = int(input(" ¿Cuántas acciones quieres comprar?: "))
    precio_accion = get_precio_accion(ticker)
    comision_sistema = precio_accion * 0.017

    print("\n El total sería de:")
    print(" " + moneyfy(precio_accion + comision_sistema))
    print(" Incluye comisión por uso de este sistema (1.7% del total)\n")

    # valida si tiene efectivo suficiente para realizar compra
    if (precio_accion + comision_sistema) > get_current_cash():
        print("\n No cuentas con líquido suficiente para hacer la compra.")
        print(" Deposite más dinero, venda acciones o cambie a MXN sus otras divisas.")
        input(" Presione ENTER para continuar...")
        return

    print(" ¿Proceder con compra?")
    decision = input("  [Sí/No]: ").lower()

    if decision[0] == "s":
        dicc_accion = [{
        'Fecha Transacción': timestamp,
        'Evento': "Compra " + ticker,
        'Precio Unitario (MXN)': precio_accion,
        'IVA (16%)': 0.0,
        'Comisión Sistema (1.7%)': comision_sistema,
        'Costo Total': precio_accion + comision_sistema,
        'Precio Dólar': get_current_divisa("USD"),
        'Vendido': "no"
        }]

        # agregando registro de transaccion a lista
        with open('util/transacciones_capitales.csv', 'a') as detalles_csv:
          campos = ['Fecha Transacción',
          'Evento',
          'Precio Unitario (MXN)',
          'IVA (16%)',
          'Comisión Sistema (1.7%)',
          'Costo Total',
          'Precio Dólar',
          'Vendido']
          output_writer = csv.DictWriter(detalles_csv, fieldnames=campos)

          # Descomenta el siguiente solo para generar la fila de encabezados
          # output_writer.writeheader()
          for i in range(acciones_compradas):
            for registro in dicc_accion:
                output_writer.writerow(registro)

        # actualizando portafolio de capitales
        new_diccs = []
        with open('util/resumen_capitales.csv', 'r') as leer_capitales:
            diccs = csv.DictReader(leer_capitales)
            existe = False

            for row in diccs:
                if ticker in row['Ticker']:
                    existe = True

                    precio_ponderado = nettea_esto(ticker)

                    new_row = {
                        'Ticker': row['Ticker'],
                        'Precio Unitario Ponderado': precio_ponderado,
                        'Cantidad': int(row['Cantidad']) + acciones_compradas,
                        'Total Ponderado': (precio_ponderado
                                                * (int(row['Cantidad']) + acciones_compradas))
                        }
                else:
                    new_row = {
                        'Ticker': row['Ticker'],
                        'Precio Unitario Ponderado': row['Precio Unitario Ponderado'],
                        'Cantidad': row['Cantidad'],
                        'Total Ponderado': row['Total Ponderado']}
                new_diccs.append(new_row)

            if not existe:
                new_row = {
                    'Ticker': ticker,
                    'Precio Unitario Ponderado': precio_accion,
                    'Cantidad': acciones_compradas,
                    'Total Ponderado': precio_accion + comision_sistema
                }
                new_diccs.append(new_row)

        # agregando registro a capitales
        with open('util/resumen_capitales.csv', 'w') as op:
          campos = ['Ticker','Precio Unitario Ponderado','Cantidad','Total Ponderado']
          output_writer = csv.DictWriter(op, fieldnames=campos)
          output_writer.writeheader()
          for registro in new_diccs:
            output_writer.writerow(registro)

        print(" ¡Enhorabuena! Has comprado", acciones_compradas, "acciones de", ticker)
        print(" Efectivo restante:", moneyfy(get_current_cash()))
    else: # No se confirmó la compra
        print(" Anulando compra...")


# agrega a doc registro de venta de accion
def vende_accion(ticker):
    print(" ¿Cuántas acciones quieres vender?")
    acciones_vendidas = int(input(" (Núm. de acciones): "))

    # validacion de tener acciones para Vender
    disponibles = 0
    with open('util/resumen_capitales.csv', 'r') as validar_capitales:
        diccs = csv.DictReader(validar_capitales)

        for row in diccs:
            if ticker in row['Ticker']:
                disponibles = int(row['Cantidad'])
            else:
                pass

    if disponibles < acciones_vendidas:
        print(" No hay suficientes acciones para vender. Disponibles:", disponibles)
        input(" Presione ENTER para continuar...")
        return

    # Si estamos aquí, es porque hay acciones para vender
    precio_accion = get_precio_accion(ticker)
    print("\n Las acciones de", ticker, "se encuentran actualmente a", moneyfy(precio_accion))

    # Obtenemos las ganancias para sacar IVA (El false es para que no actualice nada aún)
    ganancias = best_ifo(ticker, acciones_vendidas, False)
    comision_sistema = ((precio_accion * acciones_vendidas) + (ganancias * 0.16)) * 0.017

    print("\n El total que gana usted sería de:")
    print("", moneyfy((precio_accion * acciones_vendidas) - comision_sistema - (ganancias * 0.16)))

    desglose = [
    {'Concepto': "Acción " + ticker,
     'Cantidad': acciones_vendidas,
     'Total': moneyfy(precio_accion * acciones_vendidas)},
     {'Concepto': "Comisión Sistema (1.7% de acciones vendidas)",
     'Cantidad': 1,
     'Total': "-" + moneyfy(comision_sistema)},
     {'Concepto': "IVA (16% de las ganancias netas)",
     'Cantidad': 1,
     'Total': "-" + moneyfy(ganancias * 0.16)},
     {'Concepto': "TOTAL",
     'Total': moneyfy((precio_accion * acciones_vendidas) - comision_sistema - (ganancias * 0.16))}
     ]

    print(tabulate(desglose, headers="keys", tablefmt="github"))

    print("\n ¿Proceder con venta?")
    decision = input("  [Sí/No]: ").lower()
    print()
    sleep(1)

    if decision[0] == "s":
        timestamp = datetime.now().strftime("%d/%b/%Y, %H:%M:%S")
        dicc_accion = [{
        'Fecha Transacción': timestamp,
        'Evento': "Venta " + ticker,
        'Precio Unitario (MXN)': precio_accion,
        'IVA (16%)': ganancias * -0.16,
        'Comisión Sistema (1.7%)': comision_sistema * -1,
        'Costo Total': precio_accion + comision_sistema + (ganancias * 0.16),
        'Precio Dólar': get_current_divisa("USD"),
        'Vendido': "si"
        }]

        # agregando registro de transaccion a lista
        with open('util/transacciones_capitales.csv', 'a') as detalles_csv:
            campos = ['Fecha Transacción',
            'Evento',
            'Precio Unitario (MXN)',
            'IVA (16%)',
            'Comisión Sistema (1.7%)',
            'Costo Total',
            'Precio Dólar',
            'Vendido']

            # agregando registro de venta
            output_writer = csv.DictWriter(detalles_csv, fieldnames=campos)
            # Descomenta el siguiente solo para generar la fila de encabezados
            # output_writer.writeheader()
            for i in range(acciones_vendidas):
                for registro in dicc_accion:
                    output_writer.writerow(registro)

        # actualizando registros vendidos
        best_ifo(ticker, acciones_vendidas, True)

        # actualizando portafolio de capitales
        new_diccs = []
        with open('util/resumen_capitales.csv', 'r') as leer_capitales:
            diccs = csv.DictReader(leer_capitales)
            existe = False

            for row in diccs:
                if ticker in row['Ticker']:
                    existe = True

                    precio_ponderado = nettea_esto(ticker)
                    nueva_cantidad = int(row['Cantidad']) - acciones_vendidas

                    new_row = {
                    'Ticker': row['Ticker'],
                    'Precio Unitario Ponderado': precio_ponderado,
                    'Cantidad': nueva_cantidad,
                    'Total Ponderado': precio_ponderado * nueva_cantidad}
                else:
                    new_row = {
                    'Ticker': row['Ticker'],
                    'Precio Unitario Ponderado': row['Precio Unitario Ponderado'],
                    'Cantidad': row['Cantidad'],
                    'Total Ponderado': row['Total Ponderado']}

                new_diccs.append(new_row)

            if not existe:
                print("Error 645: No deberías poder vender algo que no tienes")

        # agregando registro a capitales
        with open('util/resumen_capitales.csv', 'w') as op:
          campos = ['Ticker','Precio Unitario Ponderado','Cantidad','Total Ponderado']
          output_writer = csv.DictWriter(op, fieldnames=campos)
          output_writer.writeheader()

          for registro in new_diccs:
            output_writer.writerow(registro)

        print(" ¡Enhorabuena! Has vendido", acciones_vendidas, "acciones de", ticker)
        print(" Efectivo restante:", moneyfy(get_current_cash()))
    else: # No se confirmó la compra
        print(" Anulando venta...")


# compra una divisa
def compra_divisa(divisa, tipo_cambio_actual):
    total_en_banco = 0
    monto = 0
    confirma_monto = 1
    while (monto != confirma_monto):
        print("\n Ingrese el monto de " + divisa + " que quiere comprar.")
        monto_sucio = input("  (Núm. entero): ")

        monto = int(monto_sucio.replace(",", ""))

        print("\n Ingresó " + moneyfy(monto) + " " + divisa + ". Reingrese el valor para confirmar.")
        confirma_monto_sucio = input("  Confirme el monto: ")

        confirma_monto = int(confirma_monto_sucio.replace(",",""))

        if monto != confirma_monto:
            print("\n Montos no coincidieron, intente nuevamente.\n")

        sleep(1)

    if get_current_cash() < monto:
        print(" El monto ingresado excede lo que tiene en el banco. Regresando a menú.")
        input(" Presione ENTER para continuar...")
        return

    # Si estamos aquí, es porque hay suficiente de la divisa para Vender
    total_mxn = tipo_cambio_actual * monto
    print(" Usted estará obteniendo " + moneyfy(total_mxn) + " MXN.")

    desglose = [
    {'Concepto': "Divisa " + divisa,
     'Monto': moneyfy(monto),
     'Tipo Cambio': moneyfy(tipo_cambio_actual),
     'Total': moneyfy(total_mxn)},
     {'Concepto': "TOTAL",
     'Total': moneyfy(total_mxn)}
     ]

    print(tabulate(desglose, headers="keys", tablefmt="github"))

    print("\n ¿Proceder con compra?")
    decision = input("  [Sí/No]: ").lower()
    print()
    sleep(1)

    if decision[0] != "s":
        print(" Anulando compra...")
        return

    # Se procede con compra de divisa
    timestamp = datetime.now()
    divisa_comprada = [{
    'Fecha Evento': timestamp.strftime("%d/%b/%Y, %H:%M:%S"),
    'Evento': "Compra " + divisa,
    'Divisa': divisa,
    'Monto pactado': monto,
    'Precio Forward': "N/A",
    'Comisión (0.27%)': 0,
    'Plazo (Días)': 0,
    'Fecha Cobro': timestamp.strftime("%d/%b/%Y"),
    'Total': total_mxn,
    'Finalizado': "si"
    }]

    # agregando registro de transaccion a lista
    with open('util/transacciones_derivados.csv', 'a') as detalles_csv:
        campos = [
        'Fecha Evento',
        'Evento',
        'Divisa',
        'Monto pactado',
        'Precio Forward',
        'Comisión (0.27%)',
        'Plazo (Días)',
        'Fecha Cobro',
        'Total',
        'Finalizado'
        ]

        # agregando registro de venta
        output_writer = csv.DictWriter(detalles_csv, fieldnames=campos)
        # Descomenta el siguiente solo para generar la fila de encabezados
        # output_writer.writeheader()
        for registro in divisa_comprada:
            output_writer.writerow(registro)

    # actualizando resumen de derivados
    new_diccs = []
    with open('util/resumen_derivados.csv', 'r') as leer_derivados:
        diccs = csv.DictReader(leer_derivados)

        divisa_existe = False

        for row in diccs:
            if divisa in row['Divisa']:
                divisa_existe = True
                nueva_cantidad = int(row['Cantidad']) + monto

                new_row = {
                'Divisa': row['Divisa'],
                'Cantidad': nueva_cantidad,
                'Tasa de Cambio': tipo_cambio_actual,
                'Última Actualización': row['Última Actualización'],
                'Equivalente': tipo_cambio_actual * nueva_cantidad
                }
            else:
                new_row = {
                'Divisa': row['Divisa'],
                'Cantidad': row['Cantidad'],
                'Tasa de Cambio': row['Tasa de Cambio'],
                'Última Actualización': row['Última Actualización'],
                'Equivalente': row['Equivalente']
                }

            new_diccs.append(new_row)

        # Quedaria pendiente agregar opcion de append si es una nueva divisa

    # re-agregando registro a derivados
    with open('util/resumen_derivados.csv', 'w') as op:
      campos = [
      'Divisa',
      'Cantidad',
      'Tasa de Cambio',
      'Última Actualización',
      'Equivalente'
      ]

      output_writer = csv.DictWriter(op, fieldnames=campos)
      output_writer.writeheader()
      for registro in new_diccs:
        output_writer.writerow(registro)

    print(" ¡Enhorabuena! Has comprado", moneyfy(monto), divisa)
    print(" Efectivo restante:", moneyfy(get_current_cash()))


# vende una divisa
def venta_divisa(divisa, tipo_cambio_actual):
    total_en_banco = 0
    monto = 0
    confirma_monto = 1
    while (monto != confirma_monto):
        print("\n Ingrese el monto de " + divisa + " que quiere vender.")
        monto_sucio = input("  (Núm. entero): ")

        monto = int(monto_sucio.replace(",", ""))

        print("\n Ingresó " + moneyfy(monto) + " " + divisa + ". Reingrese el valor para confirmar.")
        confirma_monto_sucio = input("  Confirme el monto: ")

        confirma_monto = int(confirma_monto_sucio.replace(",",""))

        if monto != confirma_monto:
            print("\n Montos no coincidieron, intente nuevamente.\n")

        sleep(1)

    with open('util/resumen_derivados.csv', 'r') as derivados_csv:
        diccs = csv.DictReader(derivados_csv)

        for row in diccs:
            if forward['Divisa'] == divisa:
                total_en_banco = float(row['Cantidad'])

    if total_en_banco < monto:
        print(" El monto ingresado excede lo que tiene en el banco. Regresando a menú.")
        input(" Presione ENTER para continuar...")
        return

    # Si estamos aquí, es porque hay suficiente de la divisa para Vender
    total_mxn = tipo_cambio_actual * monto
    comision_sistema = total_mxn * 0.0027
    print(" Usted estará obteniendo " + moneyfy(total_mxn - comision_sistema) + " MXN.")

    desglose = [
    {'Concepto': "Divisa " + divisa,
     'Monto': moneyfy(monto),
     'Tipo Cambio': moneyfy(tipo_cambio_actual),
     'Total': moneyfy(total_mxn)},
     {'Concepto': "Comisión Sistema (0.27% de total)",
     'Cantidad': 1,
     'Total': "-" + moneyfy(comision_sistema)},
     {'Concepto': "TOTAL",
     'Total': moneyfy(total_mxn - comision_sistema)}
     ]

    print(tabulate(desglose, headers="keys", tablefmt="github"))

    print("\n ¿Proceder con venta?")
    decision = input("  [Sí/No]: ").lower()
    print()
    sleep(1)

    if decision[0] != "s":
        print(" Anulando venta...")
        return

    # Se procede con venta de divisa
    timestamp = datetime.now()
    divisa_vendida = [{
    'Fecha Evento': timestamp.strftime("%d/%b/%Y, %H:%M:%S"),
    'Evento': "Venta " + divisa,
    'Divisa': divisa,
    'Monto pactado': monto,
    'Precio Forward': "N/A",
    'Comisión (0.27%)': comision_sistema * -1,
    'Plazo (Días)': 0,
    'Fecha Cobro': timestamp.strftime("%d/%b/%Y"),
    'Total': total_mxn - comision_sistema,
    'Finalizado': "si"
    }]

    # agregando registro de transaccion a lista
    with open('util/transacciones_derivados.csv', 'a') as detalles_csv:
        campos = ['Fecha Transacción',
        'Evento',
        'Precio Unitario (MXN)',
        'IVA (16%)',
        'Comisión Sistema (1.7%)',
        'Costo Total',
        'Precio Dólar',
        'Vendido']

        # agregando registro de venta
        output_writer = csv.DictWriter(detalles_csv, fieldnames=campos)
        # Descomenta el siguiente solo para generar la fila de encabezados
        # output_writer.writeheader()
        for registro in divisa_vendida:
            output_writer.writerow(registro)

    # actualizando resumen de derivados
    new_diccs = []
    with open('util/resumen_derivados.csv', 'r') as leer_derivados:
        diccs = csv.DictReader(leer_derivados)

        for row in diccs:
            if divisa in row['Divisa']:

                nueva_cantidad = int(row['Cantidad']) - monto


                new_row = {
                'Divisa': row['Divisa'],
                'Cantidad': nueva_cantidad,
                'Tasa de Cambio': tipo_cambio_actual,
                'Última Actualización': row['Última Actualización'],
                'Equivalente': tipo_cambio_actual * nueva_cantidad
                }
            else:
                new_row = {
                'Divisa': row['Divisa'],
                'Cantidad': row['Cantidad'],
                'Tasa de Cambio': row['Tasa de Cambio'],
                'Última Actualización': row['Última Actualización'],
                'Equivalente': row['Equivalente']
                }

            new_diccs.append(new_row)

    # re-agregando registro a derivados
    with open('util/resumen_derivados.csv', 'w') as op:
      campos = [
      'Divisa',
      'Cantidad',
      'Tasa de Cambio',
      'Última Actualización',
      'Equivalente'
      ]

      output_writer = csv.DictWriter(op, fieldnames=campos)
      output_writer.writeheader()
      for registro in new_diccs:
        output_writer.writerow(registro)

    print(" ¡Enhorabuena! Has vendido", moneyfy(monto), divisa)
    print(" Efectivo restante:", moneyfy(get_current_cash()))


# genera un forward de la divisa
def forward_divisa(divisa, tipo_cambio):
    timestamp_hoy = datetime.now()
    monto = 0
    confirma_monto = 1

    t_interes_mex = 1.05
    dicc_tasas_interes = {
        'USD': 1.0025,
        'EUR': 1.0025,
        'CAD': 1.0075
    }

    t_usada = dicc_tasas_interes.get(divisa, "ERROR #1109")

    while (monto != confirma_monto):
        print("\n Ingrese el monto de " + divisa + " que quieres comprar. ")
        monto_sucio = input("  (Núm. entero): ")

        monto = int(monto_sucio.replace(",", ""))

        print("\n Ingresó " + moneyfy(monto) + " " + divisa + ". Reingrese el valor para confirmar.")
        confirma_monto_sucio = input("  Confirme el monto: ")

        confirma_monto = int(confirma_monto_sucio.replace(",",""))

        if monto != confirma_monto:
            print("\n Montos no coincidieron, intente nuevamente.\n")

        sleep(1)

    print("\n Ingrese el plazo que desee.")
    plazo = int(input("  (Núm. de días): "))

    fin_plazo = (timestamp_hoy + timedelta(days = plazo)).strftime("%d/%b/%Y")
    print("\n La fecha de cobro sería el:", fin_plazo)

    precio_forward = tipo_cambio * ((t_interes_mex/plazo)/(t_usada/plazo))

    print("\n El precio forward será de:", moneyfy(precio_forward), divisa)
    print(" El valor nominal es de:", moneyfy(monto * precio_forward), "MXN*")
    print(" (*Tome en cuenta que el día de cobro se aumentará un 0.27% de comisión por el uso del sistema.)")


    print(" ¿Proceder con compra?")
    continuar = input("  [Sí/No]: ").lower()

    if continuar[0] != 's':
        print(" Regresando a menú principal...")
        return

    # Actualización de archivo transacciones_derivados.csv
    dicc_forward = [{
    'Fecha Evento': timestamp_hoy.strftime("%d/%b/%Y, %H:%M:%S"),
    'Evento': "Forward Adquirido",
    'Divisa': divisa,
    'Monto pactado': monto,
    'Precio Forward': precio_forward,
    'Comisión (0.27%)': 0.0,
    'Plazo (Días)': plazo,
    'Fecha Cobro': fin_plazo,
    'Total': moneyfy(monto * precio_forward) + " (Nominal)",
    'Finalizado': "no"
    }]


    sleep(1)
    genera_carta("Forward Adquirido", dicc_forward[0], timestamp_hoy, tipo_cambio)
    print(" ¡Enhorabuena! Se ha generado una carta para confirmar la adquisión.")
    print(" Lo podrá encontrar como: " + timestamp_hoy.strftime("%d%b%Y_%H%M%S") + '.pdf')
    input(" Presione ENTER para continuar.")
    sleep(1)

    # agregando registro de evento a lista
    with open('util/transacciones_derivados.csv', 'a') as derivados_csv:
      campos = ['Fecha Evento',
      'Evento',
      'Divisa',
      'Monto pactado',
      'Precio Forward',
      'Comisión (0.27%)',
      'Plazo (Días)',
      'Fecha Cobro',
      'Total',
      'Finalizado']
      output_writer = csv.DictWriter(derivados_csv, fieldnames=campos)

      # Descomenta el siguiente solo para generar la fila de encabezados
      # output_writer.writeheader()
      for registro in dicc_forward:
        output_writer.writerow(registro)

    print()
    print(" *Experimental* ¿Te gustaría usar datos históricos para cobrar ahora mismo tu contrato?")
    print(" (Se tomarán los tipos de cambio de un año atrás)")
    print()
    speedup_ans = input("  [Sí/No]: ").lower()

    if speedup_ans[0] == 's':
        speedup(timestamp_hoy.strftime("%d/%b/%Y, %H:%M:%S"))
    else:
        print(" Favor de regresar el", fin_plazo, "para la finalización del contrato.")


# genera una opción de la divisa
def opcion_divisa(divisa, tipo_cambio):
    print("Under Construction")


# Valida si hay derivados por cobrar, los ejerce y notifica de proximos a vencer
def cobrar_derivados():
    ahorita = datetime.now()

    # meter derivados a sus listas correspondientes
    forwards_a_cobrar = []
    opciones_a_cobrar = []
    derivados_proximos = []
    with open('util/transacciones_derivados.csv', 'r') as derivados_csv:
        registros = csv.DictReader(derivados_csv)

        for dicc in registros:
            fecha_cobro = datetime.strptime(dicc['Fecha Cobro'], "%d/%b/%Y")
            if dicc['Finalizado'] == "no" and (ahorita - fecha_cobro).days >= 0:
                if "Forward" in dicc['Evento']:
                    forwards_a_cobrar.append(dicc)
                elif "Opción" in dicc['Evento']:
                    opciones_a_cobrar.append(dicc)
                else:
                    print("ERROR #919: Sólo hay Opciones o forwards (o está vacío)")
            elif dicc['Finalizado'] == "no" and (ahorita - fecha_cobro).days > -9:
                derivados_proximos.append(dicc)

    # cobro es básicamente actualizar el registro + agregar a resumen
    # cobro de derivados
    if forwards_a_cobrar:
        for forward in forwards_a_cobrar:
            tasa_actual = get_current_divisa(forward['Divisa'])
            cobertura = (float(forward['Precio Forward']) - tasa_actual) * float(forward['Monto pactado'])

            forward_con_cobertura = (float(forward['Monto pactado']) * tasa_actual) + cobertura
            comision_sistema = forward_con_cobertura * 0.0027

            total_a_cobrar = forward_con_cobertura + comision_sistema

            # actualizando registro en transacciones_derivados
            new_diccs = []
            with open('util/transacciones_derivados.csv', 'r') as leer_derivados:
                diccs = csv.DictReader(leer_derivados)

                for row in diccs:
                    if forward['Fecha Evento'] == row['Fecha Evento']:

                        new_row = {
                            'Fecha Evento': row['Fecha Evento'],
                            'Evento': "Forward Liquidado",
                            'Divisa': row['Divisa'],
                            'Monto pactado': row['Monto pactado'],
                            'Precio Forward': row['Precio Forward'],
                            'Comisión (0.27%)': comision_sistema,
                            'Plazo (Días)': row['Plazo (Días)'],
                            'Fecha Cobro': row['Fecha Cobro'],
                            'Total': total_a_cobrar,
                            'Finalizado': "si"
                            }
                    else:
                        new_row = {
                            'Fecha Evento': row['Fecha Evento'],
                            'Evento': row['Evento'],
                            'Divisa': row['Divisa'],
                            'Monto pactado': row['Monto pactado'],
                            'Precio Forward': row['Precio Forward'],
                            'Comisión (0.27%)': row['Comisión (0.27%)'],
                            'Plazo (Días)': row['Plazo (Días)'],
                            'Fecha Cobro': row['Fecha Cobro'],
                            'Total': row['Total'],
                            'Finalizado': row['Finalizado']
                            }
                    new_diccs.append(new_row)


            # re-agregando registro a derivado
            with open('util/transacciones_derivados.csv', 'w') as op:
              campos = ['Fecha Evento',
              'Evento',
              'Divisa',
              'Monto pactado',
              'Precio Forward',
              'Comisión (0.27%)',
              'Plazo (Días)',
              'Fecha Cobro',
              'Total',
              'Finalizado'
              ]

              output_writer = csv.DictWriter(op, fieldnames=campos)
              output_writer.writeheader()
              for registro in new_diccs:
                output_writer.writerow(registro)


            # agregar moneda extranjera a resumen_derivados
            dicc_forward = []
            with open('util/resumen_derivados.csv', 'r') as derivados_csv:
                diccs = csv.DictReader(derivados_csv)

                existe_divisa = False
                for row in diccs:
                    if forward['Divisa'] == row['Divisa']:
                        existe_divisa = True

                        new_row = {
                        'Divisa': row['Divisa'],
                        'Cantidad': float(row['Cantidad']) + float(forward['Monto pactado']),
                        'Tasa de Cambio': row['Tasa de Cambio'],
                        'Última Actualización': row['Última Actualización'],
                        'Equivalente': row['Equivalente']
                        }
                    else:
                        new_row = {
                        'Divisa': row['Divisa'],
                        'Cantidad': row['Cantidad'],
                        'Tasa de Cambio': row['Tasa de Cambio'],
                        'Última Actualización': row['Última Actualización'],
                        'Equivalente': row['Equivalente']
                        }
                    dicc_forward.append(new_row)

                if not existe_divisa:
                    new_row = {
                    'Divisa': forward['Divisa'],
                    'Cantidad': forward['Monto pactado'],
                    'Tasa de Cambio': get_current_divisa(forward['Divisa']),
                    'Última Actualización': ahorita.strftime("%d/%b/%Y, %H:%M:%S"),
                    'Equivalente': float(forward['Monto pactado']) * get_current_divisa(forward['Divisa'])
                    }
                    new_dicc_forwarddiccs.append(new_row)

            # re-agregando registros a resumen
            with open('util/resumen_derivados.csv', 'w') as op:
              campos = ['Divisa', 'Cantidad', 'Tasa de Cambio', 'Última Actualización', 'Equivalente']
              output_writer = csv.DictWriter(op, fieldnames=campos)
              output_writer.writeheader()
              for registro in dicc_forward:
                output_writer.writerow(registro)

            print(" Se te ha cobrado automáticamente un contrato finalizado.")

            genera_carta("Forward Liquidado", forward, ahorita, tasa_actual)

            print(" Se ha generado un documento con información de la transacción.")
            print(" Lo podrá encontrar como: " + forward['Fecha Evento'].strftime("%d%b%Y_%H%M%S") + '.pdf')
            input(" Presione ENTER para continuar.")
    if opciones_a_cobrar:
        # PENDIENTE ver como funciona una opcion
        input(" Presione ENTER para continuar.")

    if derivados_proximos:
        if len(derivados_proximos) > 1:
            print("\n MENSAJE: Tienes", len(derivados_proximos), "contratos por vencer en los próximos 7 días. Favor de Consultar.")
        else:
            print("\n MENSAJE: Tienes 1 contrato por vencer en los próximos 7 días. Favor de Consultar.")


# imprime info de derivados contratados
def ver_derivados_contratados():
    print("\n Dinero en efectivo:")
    print(" ", moneyfy(get_current_cash()), '\n')

    # guardamos datos de capitales en lista_diccs_der[]
    lista_diccs_der = []
    with open('util/transacciones_derivados.csv', 'r') as derivados_csv:
        diccs_derivados = csv.DictReader(derivados_csv)

        for dicc in diccs_derivados:
            if "Forward" in dicc["Evento"]:
                dicc.pop('Fecha Evento')
                dicc['Monto pactado'] = moneyfy(float(dicc['Monto pactado'])) + " " + dicc['Divisa']
                dicc.pop('Divisa')
                dicc['Precio Forward'] = moneyfy(float(dicc['Precio Forward'])) + " MXN"
                dicc['Comisión (0.27%)'] = moneyfy(float(dicc['Comisión (0.27%)'])) + " MXN"
                dicc.pop('Plazo (Días)')
                dicc.pop('Comisión (0.27%)')
                dicc.pop('Total')
                dicc.pop('Finalizado')
                lista_diccs_der.append(dicc)

    print(tabulate(lista_diccs_der, headers="keys", tablefmt="github"))

    print("\n Valor total efectivo + portafolio de acciones + equivalente de monedas extranjeras:")
    print(" ", moneyfy(get_current_cash() + get_valor_portafolio_capitales() + get_valor_portafolio_derivados()))

    input("\n Presione ENTER para continuar.")


# imprime info de portafolio actual
def ver_portafolio():
    print(" Dinero en efectivo:")
    print(" ", moneyfy(get_current_cash()), '\n')

    # guardamos datos de capitales en lista_diccs[]
    lista_diccs = []
    with open('util/resumen_capitales.csv', 'r') as archivo:
        diccs = csv.DictReader(archivo)

        for dicc in diccs:
            dicc['Precio Unitario Ponderado'] = moneyfy(float(dicc['Precio Unitario Ponderado'])) + " MXN"
            dicc['Total Ponderado'] = moneyfy(float(dicc['Total Ponderado'])) + " MXN"
            lista_diccs.append(dicc)

    # aprovechamos para actualizar tipo de cambio actual
    rows_actualizados = []
    with open('util/resumen_derivados.csv', 'r') as derivados_csv:
        diccs_derivados = csv.DictReader(derivados_csv)

        for dicc in diccs_derivados:
            tipo_cambio_actual = get_current_divisa(dicc['Divisa'])
            new_row = {
            'Divisa': dicc['Divisa'],
            'Cantidad': dicc['Cantidad'],
            'Tasa de Cambio': tipo_cambio_actual,
            'Última Actualización': datetime.now().strftime("%d/%b/%Y, %H:%M:%S"),
            'Equivalente': float(dicc['Cantidad']) * tipo_cambio_actual
            }
            rows_actualizados.append(new_row)


    # re-agregando registros a resumen
    with open('util/resumen_derivados.csv', 'w') as op:
      campos = ['Divisa', 'Cantidad', 'Tasa de Cambio', 'Última Actualización', 'Equivalente']
      output_writer = csv.DictWriter(op, fieldnames=campos)
      output_writer.writeheader()
      for registro in rows_actualizados:
        output_writer.writerow(registro)


    # guardamos datos de capitales en lista_diccs_der[]
    lista_diccs_der = []
    with open('util/resumen_derivados.csv', 'r') as derivados_csv:
        diccs_derivados = csv.DictReader(derivados_csv)

        for dicc in diccs_derivados:
            dicc['Cantidad'] = moneyfy(float(dicc['Cantidad']))
            dicc['Tasa de Cambio'] = moneyfy(float(dicc['Tasa de Cambio']))
            dicc['Equivalente'] = moneyfy(float(dicc['Equivalente']))
            lista_diccs_der.append(dicc)

    print(tabulate(lista_diccs, headers="keys", tablefmt="github", stralign="right"))
    print("\n")
    print(tabulate(lista_diccs_der, headers="keys", tablefmt="github", stralign="right"))

    print("\n Valor total efectivo + portafolio de acciones + equivalente de monedas extranjeras:")
    print(" ", moneyfy(get_current_cash() + get_valor_portafolio_capitales() + get_valor_portafolio_derivados()))

    input("\n Presione ENTER para continuar.")


# Animación interactiva de carga de menu
def show_info(menu):
    print()
    sleep(1)
    print('\t.')
    sleep(1)
    print('\t.')
    sleep(1)
    print('\t.')
    sleep(1)
    print(menu)


# Agrega formato de dinero + separadores de miles a numero
# regresa string formateado
def moneyfy(num):
    return locale.currency(num, grouping=True)


### FUNCIONES PRINCIPALES ###

# Despliega el menu principal
def main_menu():
    print("\nPortafolio Electrónico")
    print("Usuario: Gerardo Anglada")
    sel_menu = True
    las_opciones = "\n MENU PRINCIPAL\n"
    las_opciones += "\t1.- Ver Portafolio\n"
    las_opciones += "\t2.- Mercado de Capitales\n"
    las_opciones += "\t3.- Mercado de Derivados\n"
    las_opciones += "\t4.- Ver ganancias sistema\n"
    las_opciones += "\t 5.- SALIR\n"
    print(las_opciones)
    sleep(1)

    while sel_menu:
        opcion = input(" Seleccione una opción [1-5]: ")
        if opcion == "1":
            print("\n")
            ver_portafolio()

            show_info(las_opciones)
        elif opcion == "2":
            menu_capitales()

            show_info(las_opciones)
        elif opcion == "3":
            menu_derivados()

            show_info(las_opciones)
        elif opcion == "4":
            print(" Dinero acumulado:")
            print("", moneyfy(get_current_comissions()), '\n')
            desglose = input(" ¿Quieres desglose? [Sí/No]: ").lower()
            if desglose[0] == 's':
                lista_diccs = []
                with open('util/transacciones_capitales.csv', 'r') as archivo:
                    diccs = csv.DictReader(archivo)

                    for dicc in diccs:
                        new_dict = {}
                        new_dict["Fecha"] = dicc['Fecha Transacción']
                        new_dict["Evento"] = dicc['Evento']
                        comm = abs(float(dicc['Comisión Sistema (1.7%)']))
                        dicc['Comisión Sistema (1.7%)'] = moneyfy(comm)
                        new_dict["Comisión"] = dicc['Comisión Sistema (1.7%)']
                        lista_diccs.append(new_dict)

                print()
                print(tabulate(lista_diccs, headers="keys", tablefmt="github"))

            show_info(las_opciones)
        elif opcion == "5":
            sel_menu = False
            print(" Saliendo...")
            sleep(1.3)

        else:
            print(" Opción no válida. Pruebe otra opción.")


# sub menu que permite realizar compra y venta de acciones disponibles
def menu_capitales():
    las_opciones = "\n\n MENÚ COMPRA/VENTA ACCIONES\n"
    las_opciones += " Considere que el sistema cobrará una comisión del 1.7%\n"
    las_opciones += " *Por el momento, solo podrás hacer compra/venta de:\n"
    las_opciones += "\ta. Advanced Micro Devices (AMD)\n"
    las_opciones += "\tb. Apple (AAPL)\n"
    las_opciones += "\tc. Amazon (AMZN)\n"
    las_opciones += "\td. AstraZeneca (AZNN)\n"
    las_opciones += "\te. Johnson & Johnson (JNJ)\n"
    las_opciones += "\tf. Netflix (NFLX)\n"
    las_opciones += "\tg. Nvidia Corporation (NVDA)\n"
    las_opciones += "\th. Uber (UBER)\n"
    las_opciones += "\n"
    las_opciones += "\t P.- Ver Portafolio\n"
    las_opciones += "\t M.- Menú Principal\n"
    las_opciones += "\t X.- SALIR\n"
    print(las_opciones)
    sleep(1)

    dicc_empresas = {
        'a': ["AMD", "Advanced Micro Devices Inc."],
        'b': ["AAPL", "Apple Inc."],
        'c': ["AMZN", "Amazon Inc."],
        'd': ["AZNN", "AstraZeneca"],
        'e': ["JNJ", "Johnson & Johnson"],
        'f': ["NFLX", "Netflix Inc."],
        'g': ["NVDA", "Nvidia Corporation"],
        'h': ["UBER", "Uber Technologies Inc."]
    }

    sel_menu = True
    while sel_menu:
        print(" Seleccione de qué empresa [a-h] quieres hacer compra/venta ó [P/M/X].")
        opcion = input("  [a-h] ó [P/M/X]: ").lower()
        switcher = dicc_empresas.get(opcion[0], "ERROR #1308")

        if isinstance(switcher, list):
            sleep(0.3)
            print("\n La acción de", switcher[1], "se encuentra en actualmente en:")
            print("", moneyfy(get_precio_accion(switcher[0])), "MXN.")
            print(" ¿Compra ['C'] o Venta ['V'] de " + switcher[0] + "? ('X' Para regresar)")
            opc_compraventa = input("  [C/V/X]: ").lower()

            if opc_compraventa == 'c':
                compra_accion(switcher[0])
            elif opc_compraventa == 'v':
                vende_accion(switcher[0])
            elif opc_compraventa == 'x':
                pass
            else:
                print(" Opción no válida, regresando a menú principal...")

            sel_menu = False
        elif opcion[0] == "p":
            ver_portafolio()
            show_info(las_opciones)
        elif opcion[0] == "m":
            print(" Regresando a menú principal...")
            sel_menu = False
        elif opcion[0] == "x":
            print(" Saliendo...")
            sleep(1.3)
            sys.exit()
        else:
            print(" Opción no disponible, intente nuevamente.\n")


# sub menu que permite realizar compra y venta de acciones disponibles
def menu_derivados():
    las_opciones = "\n\n MENÚ DERIVADOS\n"
    las_opciones += " El sistema cobrará una comisión del 0.27% durante la liquidación del contrato.\n"
    las_opciones += " *Divisas soportadas:\n"
    las_opciones += "\ta. USD\n"
    las_opciones += "\tb. EUR\n"
    las_opciones += "\tc. CAD\n"
    las_opciones += "\n"
    las_opciones += "\t D.- Ver Derivados Contratados\n"
    las_opciones += "\t P.- Ver Portafolio\n"
    las_opciones += "\t M.- Menú Principal\n"
    las_opciones += "\t X.- SALIR\n"
    print(las_opciones)
    sleep(1)

    dicc_divisas = {
        'a': ["USD", "EEUU"],
        'b': ["EUR", "EUROPE"],
        'c': ["CAD", "CANADA"]
    }

    sel_menu = True
    while sel_menu:
        print(" Seleccione de qué divisa [a-c] quieres hacer compra ó [D/P/M/X].")
        opcion = input("  [a-c] ó [D/P/M/X]: ").lower()
        switcher = dicc_divisas.get(opcion[0], "ERROR #1313")

        if isinstance(switcher, list):
            tipo_cambio_actual = get_current_divisa(switcher[0])
            sleep(0.3)
            print()
            print("\t['F'] Forward")
            print("\t['O'] Opción")
            print("\t['C'] Compra")
            print("\t['V'] Venta")
            print("\t ['X'] CANCELAR")
            print(" El", switcher[0], "se encuentra en actualmente en", tipo_cambio_actual, "MXN.")
            opc_forwardopcion = input("  Su opción: ").lower()

            if opc_forwardopcion[0] == 'f':
                forward_divisa(switcher[0], tipo_cambio_actual)
            elif opc_forwardopcion[0] == 'o':
                opcion_divisa(switcher[0], tipo_cambio_actual)
            elif opc_forwardopcion[0] == 'c':
                compra_divisa(switcher[0], tipo_cambio_actual)
            elif opc_forwardopcion[0] == 'v':
                venta_divisa(switcher[0], tipo_cambio_actual)
            else:
                print(" Opción no válida, regresando a menú principal...")

            sel_menu = False
        elif opcion[0] == "d":
            ver_derivados_contratados()
            show_info(las_opciones)
        elif opcion[0] == "p":
            ver_portafolio()
            show_info(las_opciones)
        elif opcion[0] == "m":
            print(" Regresando a menú principal...")
            sel_menu = False
        elif opcion[0] == "x":
            print(" Saliendo...")
            sleep(1.3)
            sys.exit()
        else:
            print(" Opción no disponible, intente nuevamente.\n")


# AQUI SE CORRE EL PROGRAMA
print("\n\n\n Bienvenido al portafolio electrónico.\n\n")
sleep(0.5)
print(" Para la mejor experiencia, ajuste ahora la pantalla y/o la letra")
print(" para que la siguiente tabla se vea correctamente:\n")
sleep(0.5)
ver_portafolio()
show_info("")
cobrar_derivados()
main_menu()
