import csv


def best_ifo(ticker):
    # actualizando portafolio de transacciones con FIFO
    new_diccs = []
    cont_fifo = 0
    cont_lifo = 0
    precio_ponderado_fifo = 0.0
    precio_ponderado_lifo = 0.0

    with open('../util/transacciones_detalles.csv', 'r') as leer_trans:
        diccs = csv.DictReader(leer_trans)

        # sacar precio ponderado con FIFO
        for row in diccs:
            if ticker in row['Evento'] and row['Vendido'] == "no" and cont_fifo == 0:
                cont_fifo += 1
            elif ticker in row['Evento'] and row['Vendido'] == "no":
                print("entra")
                precio_ponderado_fifo += float(row["Precio Unitario (MXN)"])
                cont_fifo += 1


    print(precio_ponderado_fifo)
    precio_ponderado_fifo /= (cont_fifo - 1)
    print("FIFO =", precio_ponderado_fifo)

    with open('../util/transacciones_detalles.csv', 'r') as leer_trans:
        diccs = csv.DictReader(leer_trans)

        cont_lifo = cont_fifo - 1

        # sacar precio ponderado con LIFO
        for row in diccs:
            if ticker in row['Evento'] and row['Vendido'] == "no" and cont_lifo > 0:
                precio_ponderado_lifo += float(row["Precio Unitario (MXN)"])
                cont_lifo -= 1

    precio_ponderado_lifo /= (cont_fifo - 1)
    print("LIFO =", precio_ponderado_lifo)

    # ver cual accion venderá
    if precio_ponderado_fifo > precio_ponderado_lifo:
        print("mejor fifo")
        existe = False

        # actualizando valores
        with open('../util/transacciones_detalles.csv', 'r') as leer_trans:
            diccs = csv.DictReader(leer_trans)

            for row in diccs:
                if ticker in row['Evento'] and row['Vendido'] == "no" and existe == False:
                    existe = True

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
                print("Error 304: Si vendiste, debe haber una accion", ticker, "no vendida.")

    # lifo es mejor
    else:
        print("mejor lifo")
        cont = cont_fifo - 1
        # actualizando valores
        with open('../util/transacciones_detalles.csv', 'r') as leer_trans:
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

                print(cont)
                new_diccs.append(new_row)

    # agregando registro a transacciones
    with open('../util/transacciones_detalles.csv', 'w') as op:
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


def nettea_esto(ticker):
    cont = 0
    precio_ponderado = 0.0

    with open('../util/transacciones_detalles.csv', 'r') as leer_trans:
        list_diccs = csv.DictReader(leer_trans)
        for dicc in list_diccs:
            if "Compra " + ticker in dicc["Evento"] and dicc["Vendido"] == "no":
                cont += 1
                precio_ponderado += float(dicc["Precio Unitario (MXN)"])

    return precio_ponderado / cont if cont > 0 else 0


print(nettea_esto("AAPL"))

best_ifo("AAPL")
