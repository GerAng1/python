def opcion_divisa(divisa, tipo_cambio):
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

    print(" Elija '1' para comprar un 'Call' (donde Ud. tendrá la opción de comprar)")
    print(" Elija '2' para comprar un 'Put' (donde Ud. tendrá la opción de vender)")
    print(" (Cualquier otra tecla lo regresará al menú principal)")
    ans = input(" [1/2]: ")

    if ans == 1:
        tipo_opcion = "comprar"
        tipo_opcion2 = "Call"
    elif ans == 2:
        tipo_opcion = "vender"
        tipo_opcion2 = "Put"
    else:
        return

    while (monto != confirma_monto):
        print("\n Ingrese el monto de " + divisa + " que quiere " + tipo_opcion + ".")
        monto_sucio = input("  (Núm. entero): ")

        error = True
        while error:
            try:
                monto = int(monto_sucio.replace(",",""))
                error = False
            except:
                monto_sucio = input(" No se ingresó un número entero. Intente nuevamente: ")

        print("\n Ingresó " + moneyfy(monto) + " " + divisa + ". Reingrese el valor para confirmar.")
        confirma_monto_sucio = input("  Confirme el monto: ")

        error = True
        while error:
            try:
                confirma_monto = int(confirma_monto_sucio.replace(",",""))
                error = False
            except:
                confirma_monto_sucio = input(" No se ingresó un número entero. Intente nuevamente: ")

        if monto != confirma_monto:
            print("\n Montos no coincidieron, intente nuevamente.\n")

        sleep(1)

    print("\n Ingrese el plazo que desee.")
    error = True
    while error:
        try:
            plazo = int(input("  (Núm. de días): "))
            error = False
        except:
            print(" No se ingresó un número entero. Intente nuevamente.")

    fin_plazo = (timestamp_hoy + timedelta(days = plazo)).strftime("%d/%b/%Y")
    print("\n La fecha de cobro sería el:", fin_plazo)

    precio_ejercicio = tipo_cambio * ((1 + t_interes_mex * plazo / 360) / (1 + t_usada * plazo / 360))

    print("\n El precio de ejercicio para el final del plazo será de:", moneyfy(precio_ejercicio), divisa)
    print(" La prima para la Opción Americana (ejerces cuando quieras) es de 12 centavos por cada", divisa)
    print(" La prima para la Opción Europea (ejerces solo al final del plazo) es de 6 centavos por cada", divisa)


    print(" La prima que tendrá que pagar en este momento sería de:")
    print("\t", moneyfy(monto * .12), "MXN para la Prima Americana ")
    print("\t", moneyfy(monto * .06), "MXN para la Prima Europea")

    print(" Elija:")
    print("\t'1' para elegir su", tipo_opcion2, "tipo Americano.")
    print("\t'2' para elegir su", tipo_opcion2, "tipo Europeo.")
    print(" (Cualquier otra tecla cancelará la operación y regresará al menú principal)")
    ans = input(" [1/2]: ")

    if ans == 1:
        tipo_opcion3 = "Americano"
    elif ans == 2:
        tipo_opcion3 = "Europeo"
    else:
        return

    # Actualización de archivo transacciones_derivados.csv
    dicc_forward = [{
    'Fecha Evento': timestamp_hoy.strftime("%d/%b/%Y, %H:%M:%S"),
    'Evento': "Prima Opción " + tipo_opcion2 + tipo_opcion3 + " Liquidado",
    'Divisa': divisa,
    'Monto pactado': monto,
    'Precio Forward': precio_ejercicio,
    'Comisión (0.27%)': 0.0,
    'Plazo (Días)': plazo,
    'Fecha Cobro': fin_plazo,
    'Total': monto * ,
    'Finalizado': "no"
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
      for registro in dicc_forward:
        output_writer.writerow(registro)

    sleep(1)
    genera_carta("Prima Opción " + tipo_opcion2 + tipo_opcion3 + " Liquidado", dicc_forward[0], timestamp_hoy, tipo_cambio)
    print(" ¡Enhorabuena! Se ha generado una carta para confirmar la adquisión.")
    print(" Lo podrá encontrar como: " + timestamp_hoy.strftime("%d%b%Y_%H%M%S") + '.pdf')
    input(" Presione ENTER para continuar.")
    sleep(1)

    print()
    print(" *Experimental* ¿Te gustaría usar datos históricos para cobrar ahora mismo tu contrato?")
    print(" (Se tomarán los tipos de cambio de un año atrás)")
    print()
    speedup_ans = input("  [Sí/No]: ").lower()

    if speedup_ans[0] == 's':
        speedup(timestamp_hoy.strftime("%d/%b/%Y, %H:%M:%S"))
    else:
        print(" Favor de regresar el", fin_plazo, "para la finalización del contrato.")
