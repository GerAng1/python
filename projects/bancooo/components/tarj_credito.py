from tarjeta import Tarjeta


class TCredito(Tarjeta):
    def __init__(self, no_tarjeta, nip, tipoTC, balance=0.0):
        super().__init__(self, no_tarjeta, nip)
        self.balance = balance
        self.tipoTC = tipoTC

    def set_tipoTC(tipoTC):
        self.tipoTC = tipoTC

    def set_Balance(balance):
        this.balance = balance

    def get_no_tarjeta():
        return self.no_tarjeta

    def get_tipoTC():
        return self.tipoTC

    def get_balance():
        return self.balance


    def type_nip(opcion):
        intentos = 3;
        while (intentos > 0):
            if intentos > 1:
                nip = input("Ingrese su NIP actual. Tiene", intentos, "intentos: ")
            else:
                nip = input("Ingrese su NIP actual. ÚLTIMO INTENTO: ")

            if (nip == get_nip() && opcion == 1):
                self.retiros()
            elif (nip == get_nip() && opcion == 2):
                monto = float(input("Monto a pagar: "))
                self.pagos(monto)
            elif (nip == get_nip() && opcion == 3):
                monto = float(input("Monto a cobrar: "))
                self.compras(monto)
            elif (nip == get_nip() && opcion == 4):
                print_tarjeta()
            else:
                print("NIP incorrecto, intente nuevamente.\n")
                intentos -= 1


    def pagos(cantidad):
            self.balance -= cantidad
            print("Pago exitoso.")
            print(f"Nuevo balance: ${self.balance:,} MXN.")
        }
    }

    def compras(cantidad):
        if(cantidad + balance) > tipoTC.getLimite())
            System.out.println("Fondos insuficientes.\n");

        else{
            balance -= cantidad;
            System.out.println("Transaccion exitosa.");
            System.out.println("Nuevo balance: " + balance);
        }
    }

    @Override
    public void retiros() {
        Scanner lector = new Scanner(System.in);
        boolean err = true;
        double cantidad;

        while (err) {
            try {
                System.out.print("Ingrese la cantidad a retirar: ");
                cantidad = lector.nextDouble();

                if ((cantidad + balance) > tipoTC.getLimite()) {
                    System.out.println("Fondos insuficientes");
                    err = true;
                }

                else {
                    balance -= cantidad;
                    System.out.println("Retiro exitoso");
                    System.out.println("Nuevo balance: " + balance);

                    err = false;
                }

            }
            catch (InputMismatchException ime) {
                System.err.println("Error: No se pueden teclear letras");
                lector.nextLine();
            }
        }
    }

    @Override
    public void printTipo() {
        switch (tipoTC) {
            case CLASICA:
                System.out.println("Tipo de Tarjeta: CLASICA");
                break;
            case ORO:
                System.out.println("Tipo de Tarjeta: ORO");
                break;
            case PLATINO:
                System.out.println("Tipo de Tarjeta: PLATINO");
                break;
            case BLACK:
                System.out.println("Tipo de Tarjeta: BLACK");
                break;
            default:
                System.out.println("No existe");
        }

        System.out.printf("Tasa de interes mensual: %.2f%nTasa de interes anual: %.2f%n",
            tipoTC.TIM(), tipoTC.TIA());
    }

    @Override
    public void printTarjeta() {
        System.out.printf("\nTarjeta de Crédito: %s\nSaldo: %.2f\nLimite Credito: %.2f\n", numero, balance, tipoTC.getLimite());
        printTipo();
        System.out.printf("Fecha de Expedición: %s\nFecha de Expiración: %s\n\n",
            fechaExpe.FormatoFecha(), fechaExpi.FormatoFecha());
    }

}
