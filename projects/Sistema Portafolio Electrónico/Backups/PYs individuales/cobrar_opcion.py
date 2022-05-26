for opcion in opciones_a_cobrar:
    tasa_actual = get_current_divisa(opcion['Divisa'])
    # actualizando registro en transacciones_derivados

    cobrar_americano = False
    if "Americano" in  opcion['Evento']:
        print(" Esta Opción aún no llega a su plazo de vencimiento.")
        print(" El precio de ejercicio establecido fue de:", opcion['Precio Forward'])
        print(" El precio actual de", opcion['Divisa'], "es de:", moneyfy(tasa_actual))
        print(" ¿Desea ejercer su opción en este momento? (Prima pagada fue de:" + moneyfy(opcion['Total']) + ")")
        respuesta_americano = input("  [Sí/No]: ").lower()

        respuesta_valida = False
        while not respuesta_valida:
            if respuesta_americano[0] == 's':
                respuesta_valida = True
                cobrar_americano = True
            elif respuesta_americano[0] == 'n':
                print(" Gracias por usar este sistema.")
                respuesta_valida = True
                sleep(1)
            else:
                respuesta_americano = input(" Respuesta no válida, digite 'S' para 'Sí' o 'N' para 'No': ").lower()

    if "Europeo" in opcion['Evento'] or cobrar_americano:
        new_diccs = []
        with open('util/transacciones_derivados.csv', 'r') as leer_derivados:
            diccs = csv.DictReader(leer_derivados)

            for row in diccs:
                if opcion['Fecha Evento'] == row['Fecha Evento']:

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

    # continuamos con validacion de si ejerce
    cobrar_europeo = False
    if "Europeo" in  opcion['Evento']:
        print(" El precio de ejercicio establecido fue de:", opcion['Precio Forward'])
        print(" El precio actual de", opcion['Divisa'], "es de:", moneyfy(tasa_actual))

        print(" ¿Desea ejercer su opción? (Prima pagada fue de:" + moneyfy(opcion['Total']) + ")")
        respuesta_europeo = input("  [Sí/No]: ").lower()

        respuesta_valida = False
        while not respuesta_valida:
            if respuesta_europeo[0] == 's':
                respuesta_valida = True
                cobrar_europeo = True
            elif respuesta_europeo[0] == 'n':
                print(" Gracias por usar este sistema.")
                respuesta_valida = True
                sleep(1)
            else:
                respuesta_europeo = input(" Respuesta no válida, digite 'S' para 'Sí' o 'N' para 'No': ").lower()

    if cobrar_americano or cobrar_europeo:
        # si estamos aquí, aceptó ejercer su opcion
        # agregar contrato a transacciones_derivados
        tipo_opcion2 = "Call" if "Call" in opcion['Evento'] else "Put"
        tipo_opcion3 = "Americano" if "Americano" in opcion['Evento'] else "Europeo"

        dicc_opcion = [{
        'Fecha Evento': ahorita.strftime("%d/%b/%Y, %H:%M:%S"),
        'Evento': "Opción " + tipo_opcion2 + tipo_opcion3 + " Liquidado",
        'Divisa': opcion['Divisa'],
        'Monto pactado': opcion['Monto Pactado'],
        'Precio Forward': opcion['Precio Forward'],
        'Comisión (0.27%)': opcion['Comisión (0.27%)'],
        'Plazo (Días)': opcion['Plazo (Días)'],
        'Fecha Cobro': opcion['Fecha Cobro'],
        'Total': float(opcion['Monto Pactado']) * float(opcion['Precio Forward']),
        'Finalizado': "si"
        }]

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
          for registro in dicc_opcion:
            output_writer.writerow(registro)


        # agregar moneda extranjera a resumen_derivados
        dicc_opcion = []
        with open('util/resumen_derivados.csv', 'r') as derivados_csv:
            diccs = csv.DictReader(derivados_csv)

            existe_divisa = False
            for row in diccs:
                if opcion['Divisa'] == row['Divisa']:
                    existe_divisa = True

                    signo = 1 if tipo_opcion2 == "Call" else -1

                    new_row = {
                    'Divisa': row['Divisa'],
                    'Cantidad': float(row['Cantidad']) + (float(opcion['Monto pactado']) * signo),
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
                dicc_opcion.append(new_row)

            if not existe_divisa:
                new_row = {
                'Divisa': opcion['Divisa'],
                'Cantidad': opcion['Monto pactado'],
                'Tasa de Cambio': tasa_actual,
                'Última Actualización': ahorita.strftime("%d/%b/%Y, %H:%M:%S"),
                'Equivalente': float(opcion['Monto pactado']) * tasa_actual
                }
                dicc_opcion.append(new_row)

        # re-agregando registros a resumen
        with open('util/resumen_derivados.csv', 'w') as op:
          campos = ['Divisa', 'Cantidad', 'Tasa de Cambio', 'Última Actualización', 'Equivalente']
          output_writer = csv.DictWriter(op, fieldnames=campos)
          output_writer.writeheader()
          for registro in dicc_opcion:
            output_writer.writerow(registro)

        print(" Se te ha cobrado un contrato finalizado.")

        genera_carta_derivado("Opción " + tipo_opcion2 + tipo_opcion3 + " Liquidado", opcion, ahorita, tasa_actual)

        print(" Se ha generado un documento con información de la transacción.")
        print(" Lo podrá encontrar como: " + opcion['Fecha Evento'].strftime("%d%b%Y_%H%M%S") + '.pdf')
        input(" Presione ENTER para continuar.")
