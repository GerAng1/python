import components



public class BancoOO {
  static ArrayList < Cliente > listaClientes = new ArrayList < Cliente > ();

  public static void main(String[] args) {
    System.out.print("\033[H\033[2J");
    System.out.flush();
    try {
      Runtime.getRuntime().exec("cls");
    } catch (final Exception e) {}
    System.out.println("\nPara Una Mejor Experiencia, " +
      "tenga la terminal en Pantalla Completa...\n");

    System.out.println("SISTEMA DE ALTA DE CLIENTES");
    Cliente c = new Cliente();
    TCredito tc = new TCredito();
    //Cliente
    File archivo = null;
    int cont = -1;
    try {
      String datosLeidos = "";
      String renglon[] = new String[10];
      //abre archivo & lo guarda en arreglo
      archivo = new File("HojaClientes.csv");
      FileReader lector = new FileReader(archivo);
      BufferedReader br = new BufferedReader(lector);

      while ((datosLeidos = br.readLine()) != null) {
        renglon = datosLeidos.split("/");
        if (renglon[1].charAt(0) == '1') {
          if (renglon[8].charAt(0) == 'C') {
            c = new Cliente(renglon[2], renglon[3], renglon[4], Integer.parseInt(renglon[5]), Integer.parseInt(renglon[6]), Integer.parseInt(renglon[7]), renglon[8]);
            listaClientes.add(c);
            cont++;
          } else {
            c = new Cliente(renglon[2], renglon[3], renglon[4], Integer.parseInt(renglon[5]), Integer.parseInt(renglon[6]), Integer.parseInt(renglon[7]), renglon[8], renglon[10]);
            listaClientes.add(c);
            cont++;
          }
        } else {
          switch (renglon[6]) {
          case "1":
            tc = new TCredito(renglon[2], Integer.parseInt(renglon[3]), Integer.parseInt(renglon[4]), Integer.parseInt(renglon[5]), TipoTC.CLASICA, Double.parseDouble(renglon[7]));
            break;
          case "2":
            tc = new TCredito(renglon[2], Integer.parseInt(renglon[3]), Integer.parseInt(renglon[4]), Integer.parseInt(renglon[5]), TipoTC.ORO, Double.parseDouble(renglon[7]));
            break;
          case "3":
            tc = new TCredito(renglon[2], Integer.parseInt(renglon[3]), Integer.parseInt(renglon[4]), Integer.parseInt(renglon[5]), TipoTC.PLATINO, Double.parseDouble(renglon[7]));
            break;
          case "4":
            tc = new TCredito(renglon[2], Integer.parseInt(renglon[3]), Integer.parseInt(renglon[4]), Integer.parseInt(renglon[5]), TipoTC.BLACK, Double.parseDouble(renglon[7]));
            break;
          default:
            System.out.println("Opcion no valida. Elija entre 1 y 4.\n");
            break;
          } //switch
          listaClientes.get(cont).setTCredito(tc);
        }
      }
      lector.close();
    } catch (Exception E) {
      System.out.println("Error en crear arreglo");
    }

    menu();
  } //fin Main

  public static void menu() {
    Scanner lc = new Scanner(System.in);
    String lasOpciones;
    boolean selMenu = true, err = true, err2 = true, val = false, found = false;
    String resp;
    int opcion, tryP = 3;
    String matricula, password, matC;

    lasOpciones = "\n MENU\n";
    lasOpciones += "\t1.- Retiros\n";
    lasOpciones += "\t2.- Pagar Tarjeta\n";
    lasOpciones += "\t3.- Compras\n";
    lasOpciones += "\t4.- Estado de Cuentas\n";
    lasOpciones += "\t5.- Administracion de Cuentas\n";
    lasOpciones += "\t6.- Salir\n";
    lasOpciones += "";
    lasOpciones += "Elija la opcion que quiera: ";

    System.out.print(lasOpciones);

    while (err) {
      try {
        do {
          opcion = lc.nextInt();
          lc.nextLine();

          switch (opcion) {
          case 1:
            retirosMenu();
            selMenu = true;
            break;

          case 2:
            pagos();
            selMenu = true;
            break;

          case 3:
            compras();
            selMenu = true;
            break;

          case 4:
            estadoCuenta();
            break;

          case 5:
            while (err2 == true) {
              try {
                System.out.print("Este menu solo esta disponible para administradores. Ingrese su Matricula: ");
                matricula = lc.nextLine();
                if (matricula.charAt(0) == 'A') {
                  for (int cont = 0; cont < listaClientes.size(); cont++) {
                    if (listaClientes.get(cont).getMat().equals(matricula)) {
                      while (val == false && tryP > 0) {
                        System.out.println("Administrador " + matricula + ", escriba su contrasenia. Tiene " + tryP + " intento(s).");
                        password = lc.nextLine();

                        if (listaClientes.get(cont).getPass().equals(password)) {
                          System.out.println("Contrasenia es correcta. Bienvenido(a) " + listaClientes.get(cont).getNom() + ".");
                          val = true;
                        } else {
                          System.out.println("Contrasenia es incorrecta.");
                          tryP--;
                        }
                      }
                      found = true;
                    }
                  }

                  if (found) {

                  } else {
                    System.out.println("No existe ningun usuario con esa matricula");
                  }
                } else {
                  System.out.println("Usted no es un administrador. No tiene acceso a este menu.");
                }
                err2 = false;
              } catch (InputMismatchException ime) {
                System.err.println("Error: No se pueden teclear letras. \n");
                lc.nextLine();
              }
            }
            if (val) {
              menu2();
            } else {
              menu();
            }
            selMenu = true;
            break;
          case 6:
            System.out.println("Adios\n");
            finisher();
            System.exit(0);
            break;
          default:
            System.out.print("Opcion no existe, elige entre 1 y 6: ");
            selMenu = false;
            break;
          }
        } while (selMenu == false);
      } //fin try
      catch (InputMismatchException ime) {
        System.err.println("Error: No se pueden teclear letras. \n");
        lc.nextLine();
        System.out.print("Seleccione entre 1 y 5: ");
      }
    } //fin err
  } //fin Menu

  public static void menu2() {
    Scanner lc = new Scanner(System.in);
    String modificacionC;
    char mod;
    boolean selMenu = true;

    System.out.printf("%nAdministracion de Cuentas%n" +
      "\t a. Alta Cliente%n" +
      "\t b. Baja Cliente%n" +
      "\t c. Modificacion Datos Personales%n" +
      "\t d. Agregar Tarjeta a Cliente%n" +
      "\t e. Imprimir Datos%n" +
      "\t f. Regresar a Menu%n" +
      "\t g. Salir%n%n" +
      "Teclee la letra que quiera: ");

    while (selMenu) {
      modificacionC = lc.nextLine();
      mod = modificacionC.charAt(0);
      switch (mod) {
      case 'a':
      case 'A':
        aC();
        selMenu = false;
        break;
      case 'b':
      case 'B':
        bC();
        selMenu = false;
        break;
      case 'c':
      case 'C':
        mDC();
        selMenu = false;
        break;
      case 'd':
      case 'D':
        aTCE();
        selMenu = false;
        break;
      case 'e':
      case 'E':
        iD();
        selMenu = false;
        break;
      case 'f':
      case 'F':
        menu();
        selMenu = false;
        break;
      case 'g':
      case 'G':
        System.out.println("Adios\n");
        finisher();
        System.exit(0);
        break;
      default:
        System.out.print("Opcion no existe, elige entre 'a' y 'g': ");
        selMenu = true;
        break;
      }
    }
  } //fin MENU2

  public static void retirosMenu() {
    Cliente cliente;
    Scanner lc = new Scanner(System.in);
    boolean err = true;
    while (err) {
      try {
        System.out.println("Ingrese su ID");
        int id = lc.nextInt();
        if (id > 0) {
          for (int cont = 0; cont < listaClientes.size(); cont++) {
            if (listaClientes.get(cont).getID() == id) {
              listaClientes.get(cont).pickTarjeta(1);
            }
          }
        } else {
          System.out.println("El ID no existe");
        }
        err = false;
      } catch (InputMismatchException ime) {
        System.err.println("Error: No se pueden teclear letras. \n");
        lc.nextLine();
      }
    }
    menu();
  } //fin RETIROS

  public static void pagos() {
    Cliente cliente;
    Scanner lc = new Scanner(System.in);
    boolean err = true;
    while (err) {
      try {
        System.out.println("Ingrese su ID");
        int id = lc.nextInt();
        if (id > 0) {
          for (int cont = 0; cont < listaClientes.size(); cont++) {
            if (listaClientes.get(cont).getID() == id) {
              listaClientes.get(cont).pickTarjeta(2);
              err = false;
            }
          }
        } else {
          System.out.println("El ID no existe");
        }
        err = false;
      } catch (InputMismatchException ime) {
        System.err.println("Error: No se pueden teclear letras. \n");
        lc.nextLine();
      }
    }
    menu();
  }

  public static void compras() {
    Cliente cliente;
    Scanner lc = new Scanner(System.in);
    boolean err = true;
    while (err) {
      try {
        System.out.println("Ingrese su ID");
        int id = lc.nextInt();
        if (id > 0) {
          for (int cont = 0; cont < listaClientes.size(); cont++) {
            if (listaClientes.get(cont).getID() == id) {
              listaClientes.get(cont).pickTarjeta(3);
              err = false;
            }
          }
        } else {
          System.out.println("El ID no existe");
        }
        err = false;
      } catch (InputMismatchException ime) {
        System.err.println("Error: No se pueden teclear letras. \n");
        lc.nextLine();
      }
    }
    menu();
  } //fin COMPRAS

  public static void estadoCuenta() {
    Cliente cliente;
    Scanner lc = new Scanner(System.in);
    boolean err = true;
    while (err) {
      try {
        System.out.println("Ingrese su ID");
        int id = lc.nextInt();
        if (id > 0) {
          for (int cont = 0; cont < listaClientes.size(); cont++) {
            if (listaClientes.get(cont).getID() == id) {
              listaClientes.get(cont).pickTarjeta(4);
              err = false;
            }
          }
        } else {
          System.out.println("El ID no existe");
        }
        err = false;
      } catch (InputMismatchException ime) {
        System.err.println("Error: No se pueden teclear letras. \n");
        lc.nextLine();
      }
    }
    menu();
  }

  public static void aC() {
    Scanner lc = new Scanner(System.in);
    String ansCard, ans, pre;
    boolean err = true;
    boolean val = false;

    Cliente c = new Cliente();
    String nom, ap, direccion, calle, numero, colonia, ciudad;
    int dia, mes, anio, prev = 0;
    int telefono1;
    int telefono2;
    String telefono, telefono1S = "", telefono2S = "", password, matricula;

    while (err) {
      try {
        do {
          System.out.print("\nNombre(s) del Cliente: ");
          nom = lc.nextLine();

          System.out.print("Apellido(s) del Cliente: ");
          ap = lc.nextLine();

          System.out.println("Direccion del Cliente(no teclee comas por favor)");
          System.out.print("Calle: ");
          calle = lc.nextLine();
          System.out.print("Numero(sin el #): ");
          numero = lc.nextLine();
          System.out.print("Colonia: ");
          colonia = lc.nextLine();
          System.out.print("Ciudad: ");
          ciudad = lc.nextLine();
          direccion = calle + ", #" + numero + ", " + colonia + ", " + ciudad;

          System.out.print("Dia de Nacimiento: ");
          dia = lc.nextInt();
          lc.nextLine();

          System.out.print("Mes de Nacimiento: ");
          mes = lc.nextInt();
          lc.nextLine();

          System.out.print("Año de Nacimiento: ");
          anio = lc.nextInt();

          do {
            System.out.print("Escriba los primeros 5 digitos de su numero de telefono movil, incluyendo el codigo LADA de su ciudad:");
            telefono1 = lc.nextInt();
            telefono1S = "" + telefono1;
            if (telefono1S.length() == 5) {
              val = true;
            } else {
              System.out.print("No escribio un numero de 5 digitos. Vuelva a intentar.");
            }
          } while (val == false);
          val = false;
          do {
            System.out.print("Escriba los ultimos 5 digitos de su numero de telefono movil:");
            telefono2 = lc.nextInt();
            telefono2S = "" + telefono2;
            if (telefono2S.length() == 5) {
              val = true;
            } else {
              System.out.print("No escribio un numero de 5 digitos. Vuelva a intentar.");
              val = false;
            }
          } while (val == false);
          lc.nextLine();

          telefono = telefono1S + telefono2S;

          do {
            System.out.printf("Este cliente es un cliente normal o un administrador(puede acceder al menu de administracion)? [N/A]: ");
            pre = lc.nextLine();
            if (pre.equalsIgnoreCase("N")) {
              c = new Cliente(nom, ap, direccion, dia, mes, anio, telefono);
              System.out.printf("Se ha creado al Cliente %s con el folio %d y matricula %s.%n%n", nom, c.getID(), c.getMat());
            } else if (pre.equalsIgnoreCase("A")) {
              System.out.print("Escriba la contraseña del administrador: ");
              password = lc.nextLine();
              c = new Cliente(nom, ap, direccion, dia, mes, anio, telefono, password);
              System.out.printf("Se ha creado al Cliente %s con el folio %d y matricula %s.%n%n", nom, c.getID(), c.getMat());
            } else {
              System.out.println("Respuesta no válida. Seleccione 'N' o 'A'.");
            }

          } while (!pre.equalsIgnoreCase("n") && !pre.equalsIgnoreCase("a"));

          //System.out.printf("Se ha creado al Cliente %s con el folio %d.%n%n", nom, c.getID());

          do {
            System.out.print("Desea agregarle una tarjeta ahora? [Y/N]: ");
            ansCard = lc.nextLine();

            if (ansCard.equalsIgnoreCase("Y"))
              aTC(c);

            else if (ansCard.equalsIgnoreCase("N"))
              listaClientes.add(c);

            else
              System.out.println("Respuesta no válida. Seleccione 'N' o 'Y'.");
          } while (!ansCard.equalsIgnoreCase("y") && !ansCard.equalsIgnoreCase("n"));

          System.out.printf("Quieres agregar un cliente nuevo? [Y/N]: ");
          ans = lc.nextLine();
        } while (ans.equalsIgnoreCase("Y"));

        err = false;
      } //fin try
      catch (InputMismatchException ime) {
        System.err.println("Error: No se pueden teclear letras ni en la fecha de nacimiento ni el numero telefonico. \n");
        lc.nextLine();
      } catch (ArithmeticException ae) {
        System.err.println("ArithmeticException: " + ae.getMessage());
        c = new Cliente(prev);
        lc.nextLine();
      }
    } //fin err

    menu2();
  } //fin Agregar CLIENTE

  public static void aTC(Cliente client) {
    Scanner lc = new Scanner(System.in);
    int typeCard;
    boolean selCard, err = true;

    TCredito tc = new TCredito();
    String numero;
    int month, year;
    int nip;

    System.out.println("\n Tajetas Disponibles:\n");

    for (TipoTC t: TipoTC.values())
      System.out.printf("La TIIE de la %s es: %.2f%% %n" +
        "Su Tasa Mensual es: %.2f%% %n" +
        "Su Tasa Anual es: %.2f%% %n" +
        "%n", t, t.TIIE(), t.TIM(), t.TIA());

    System.out.printf("Seleccione la opcion de la tarjeta que desea: %n%n" +
      "1: Clásica: \t\t\t 2: Oro \t\t\t 3: Platinum \t\t\t 4: Black%n" +
      "Limite: $7,500 \t\t\t Limite: $15,000\t\t" +
      " Limite: $45,000\t\t Limite: $100,000%n" +
      "Anualidad: $699 \t\t Anualidad: $959 \t\t Anualidad:1,999 \t\t Anualidad:4,599 %n%n");

    while (err) {
      try {
        do {
          System.out.print("Seleccione [1, 2, 3 o 4]: ");
          typeCard = lc.nextInt();
          lc.nextLine();

          if (typeCard > 4 || typeCard < 1) {
            System.out.println("Esa opción no es válida \n");
            selCard = false;
          } else {
            //generar numero de tarjeta de 16 digitos de manera aleatoria
            long numeroLong = (long)(Math.random() * 10000000000000000L);
            numero = Long.toString(numeroLong);
            System.out.println("El numero de tarjeta asignado es: " + numero);

            System.out.println("Fecha de expedicion? [MM AAAA]: ");
            month = lc.nextInt();
            year = lc.nextInt();

            System.out.println("Inserte un NIP de 4 digitos: ");
            nip = lc.nextInt();

            switch (typeCard) {
            case 1:
              tc = new TCredito(numero, nip, month, year, TipoTC.CLASICA);
              System.out.println("Su tarjeta Clasica ha quedado registrada.\n");
              selCard = true;
              break;
            case 2:
              tc = new TCredito(numero, nip, month, year, TipoTC.ORO);
              System.out.println("Su tarjeta Oro ha quedado registrada\n");
              selCard = true;
              break;
            case 3:
              tc = new TCredito(numero, nip, month, year, TipoTC.PLATINO);
              System.out.println("Su tarjeta Platino ha quedado registrada\n");
              selCard = true;
              break;
            case 4:
              tc = new TCredito(numero, nip, month, year, TipoTC.BLACK);
              System.out.println("Su tarjeta BLACK ha quedado registrada\n");
              selCard = true;
              break;
            default:
              System.out.println("Opcion no valida. Elija entre 1 y 4.\n");
              selCard = false;
              break;
            } //switch
          } //else
        } while (selCard == false);

        client.setTCredito(tc);

        listaClientes.add(client);

        err = false;
      } //fin try //fin try
      catch (ArithmeticException ex) {
        System.err.println("Error: Fecha no existe. \n");
      } catch (InputMismatchException ime) {
        System.err.println("Error: No se pueden teclear letras. \n");
        lc.nextLine();
      }
    } //fin err
  } //fin de addTarejta

  public static void bC() {
    Scanner lc = new Scanner(System.in);
    String ans;
    boolean idfound = true;
    int opcion, sel = -1;

    if (listaClientes.isEmpty())
      System.out.println("\n No hay clientes registrados, regresando al Menu...\n");

    else {
      try {
        System.out.println("Si se sabe el ID del cliente a dar de baja, escribalo, " +
          "si no, escriba 0 para imprimir todos los clientes, o -1 para regresar a menu.");

        while (idfound) {
          opcion = lc.nextInt();
          lc.nextLine();

          if (opcion == -1) {
            System.out.println("Regresnado a Menu...\n");
            idfound = false;
          } else if (opcion == 0) {
            for (int cont = 0; cont < listaClientes.size(); cont++)
              System.out.println("ID: " + listaClientes.get(cont).getID() +
                " Nombre: " + listaClientes.get(cont).getNom());

            System.out.print("\nDigite el Id del Cliente que quiere dar de baja: ");
            idfound = true;
          } else if (opcion > 0) {
            for (int cont = 0; cont < listaClientes.size(); cont++) {
              if (listaClientes.get(cont).getID() == opcion) {
                listaClientes.get(cont).printCliente();

                System.out.println("\n DAR DE BAJA CLIENTE? [Y/N]");
                ans = lc.nextLine();

                if (ans.equalsIgnoreCase("Y")) {
                  listaClientes.remove(cont);
                  System.out.println("Cliente ha sido eliminado.\n");
                  sel = 1;
                } else {
                  System.out.print("\nDigite el Id del Cliente que quiere dar de baja: ");
                  sel = 2;
                }
              } else
                sel = 3;
            }

            switch (sel) {
            case 1:
              idfound = false;
              break;
            case 2:
              idfound = true;
              break;
            case 3:
              System.out.println("No se encontro el Id de ese cliente, intente de nuevo.");
              idfound = true;
              break;
            }
          } else {
            System.out.println("\nEl Id no existe");

            System.out.print("Digite el Id del Cliente que quiere dar de baja: ");
            idfound = true;
          }
        } //fin while idfound
      } //fin try
      catch (InputMismatchException ime) {
        System.err.println("Error: No se pueden teclear letras. \n");
        lc.nextLine();
      }
    }

    menu2();
  } //fin baja de cliente

  public static void mDC() {
    Scanner lc = new Scanner(System.in);
    String newDir, newTel, newTel1S = "", newTel2S = "", calle, numero, colonia, ciudad;
    String toModify;
    int opcion, position = -1;
    int newTel1, newTel2;
    char change;
    boolean idfound = true, sel = true, found = false, val = false;

    if (listaClientes.isEmpty())
      System.out.println("\n No hay clientes registrados, regresando al Menu...\n");

    else {
      //while(err){
      try {
        System.out.print("Si se sabe el ID del cliente a modificar, escribalo, " +
          "si no, escriba 0 para imprimir todos los clientes, o -1 para regresar al menu: ");

        while (idfound) {
          opcion = lc.nextInt();
          lc.nextLine();

          if (opcion == -1) {
            System.out.println("Regresando a menu...");
            idfound = false;
          } else if (opcion == 0) {
            for (int cont = 0; cont < listaClientes.size(); cont++)
              System.out.println("ID: " + listaClientes.get(cont).getID() +
                " Nombre: " + listaClientes.get(cont).getNom());

            System.out.print("\nDigite el Id del Cliente que quiere modificar: ");
            idfound = true;
          } else if (opcion > 0) {
            for (int cont = 0; cont < listaClientes.size(); cont++) {
              if (listaClientes.get(cont).getID() == opcion) {
                listaClientes.get(cont).printCliente();
                position = cont;

                System.out.print("\n¿Que quiere modificar?\n" +
                  "d. Direccion\n" +
                  "t. Telefono\n" +
                  "Escriba la primera letra de lo que quiere modificar: ");

                while (sel) {
                  toModify = lc.nextLine();
                  change = toModify.charAt(0);
                  switch (change) {
                  case 'd':
                  case 'D':
                    System.out.println("Escriba la nueva direccion del cliente (no teclee comas por favor): ");
                    System.out.print("Calle: ");
                    calle = lc.nextLine();
                    System.out.print("Numero(sin el #): ");
                    numero = lc.nextLine();
                    System.out.print("Colonia: ");
                    colonia = lc.nextLine();
                    System.out.print("Ciudad: ");
                    ciudad = lc.nextLine();
                    newDir = calle + ", #" + numero + ", " + colonia + ", " + ciudad;
                    listaClientes.get(position).setDir(newDir);
                    sel = false;
                    break;
                  case 'T':
                  case 't':
                    while (val == false) {
                      System.out.print("Escriba los primeros 5 digitos de su numero de telefono movil, incluyendo el codigo LADA de su ciudad:");
                      newTel1 = lc.nextInt();
                      newTel1S = "" + newTel1;
                      if (newTel1S.length() == 5) {
                        val = true;
                      } else {
                        System.out.print("No escribio un numero de 5 digitos. Vuelva a intentar.");
                        val = false;
                      }
                    }
                    lc.nextLine();
                    val = false;
                    while (val == false) {
                      System.out.print("Escriba los primeros 5 digitos de su numero de telefono movil, incluyendo clave de su ciudad (55, por ejemplo):");
                      newTel2 = lc.nextInt();
                      newTel2S = "" + newTel2;
                      if (newTel2S.length() == 5) {
                        val = true;
                      } else {
                        System.out.print("No escribio un numero de 5 digitos. Vuelva a intentar.");
                        val = false;
                      }
                    }
                    lc.nextLine();
                    newTel = newTel1S + newTel2S;
                    listaClientes.get(position).setTel(newTel);
                    sel = false;
                    break;
                  default:
                    System.out.print("Opcion no existe, vuelva a intentar: ");
                    sel = true;
                    break;
                  } //fin switch
                } //fin del while del switch
                found = true;
              }

              if (found)
                idfound = false;

              else {
                System.out.println("No se encontro el Id de ese cliente, intente de nuevo.");
                idfound = true;
              }
            }
          } else {
            System.out.println("\nEl Id no existe.");

            System.out.print("Digite el Id del Cliente que quiere modificar: ");
            idfound = true;
          }
        } //fin while idfound
      } //fin try
      // }//fin while
      catch (InputMismatchException ime) {
        System.err.println("Error: No se pueden teclear letras. \n");
        lc.nextLine();
      }
    }

    menu2();
  } //fin modificar datos cliente

  public static void aTCE() {
    Scanner lc = new Scanner(System.in);
    int typeCard, opcion, position = 0;
    boolean selCard, found = false, idfound = true, err = true;

    TCredito tc = new TCredito();
    String numero;
    int month, year;
    int nip;

    if (listaClientes.isEmpty())
      System.out.println("\n No hay clientes registrados, regresando al Menu...\n");

    else {
      try {
        System.out.println("Si se sabe el ID del cliente a agregar tarjeta nueva, " +
          "escribalo, si no, escriba 0 para imprimir todos los clientes, o -1 para regresar al menu.");

        while (idfound) {
          opcion = lc.nextInt();

          if (opcion == -1) {
            System.out.println("Regresando a menu...");
            idfound = false;
          } else if (opcion == 0) {
            for (int cont = 0; cont < listaClientes.size(); cont++)
              System.out.println("ID: " + listaClientes.get(cont).getID() +
                " Nombre: " + listaClientes.get(cont).getNom());

            System.out.print("\nDigite el Id del Cliente que quiere agregar tarjeta: ");
            idfound = true;
          } else if (opcion > 0) {
            for (int cont = 0; cont < listaClientes.size(); cont++) {
              if (listaClientes.get(cont).getID() == opcion) {
                System.out.println("\nID: " + listaClientes.get(cont).getID() +
                  " Nombre: " + listaClientes.get(cont).getNom());
                position = cont;
                found = true;
              }
            }
            if (found)
              idfound = false;

            else {
              System.out.println("No se encontro el Id de ese cliente, intente de nuevo.");
              idfound = true;
            }
          } else {
            System.out.println("\nEl Id no existe");

            System.out.print("Digite el Id del Cliente que quiere agregar tarjeta: ");
            idfound = true;
          }
        } //fin while idfound
      } //fin try
      catch (InputMismatchException ime) {
        System.err.println("Error: No se pueden teclear letras. \n");
        lc.nextLine();
      }

      System.out.println("\n Tajetas Disponibles:\n");

      for (TipoTC t: TipoTC.values())
        System.out.printf("La TIIE de la %s es: %.2f%% %n" +
          "Su Tasa Mensual es: %.2f%% %n" +
          "Su Tasa Anual es: %.2f%% %n" +
          "%n", t, t.TIIE(), t.TIM(), t.TIA());

      System.out.printf("Seleccione la opcion de la tarjeta que desea: %n%n" +
        "1: Clásica: \t\t\t 2: Oro \t\t\t 3: Platinum \t\t\t 4: Black%n" +
        "Limite: $7,500 \t\t\t Limite: $15,000\t\t" +
        " Limite: $45,000\t\t Limite: $100,000%n" +
        "Anualidad: $699 \t\t Anualidad: $959 \t\t Anualidad:1,999 \t\t Anualidad:4,599 %n%n");

      while (err) {
        try {
          do {
            System.out.print("Seleccione [1, 2, 3 o 4]: ");
            typeCard = lc.nextInt();
            lc.nextLine();

            if (typeCard > 4 || typeCard < 1) {
              System.out.println("Esa opción no es válida \n");
              selCard = false;
            } else {
              //generar numero de tarjeta de 16 digitos de manera aleatoria
              long numeroLong = (long)(Math.random() * 10000000000000000L);
              numero = Long.toString(numeroLong);
              System.out.println("El numero de tarjeta asignado es: " + numero);

              System.out.println("Fecha de expedicion? [MM AAAA]: ");
              month = lc.nextInt();
              year = lc.nextInt();

              System.out.println("Teclee un NIP de 4 digitos: ");
              nip = lc.nextInt();
              lc.nextLine();

              switch (typeCard) {
              case 1:
                tc = new TCredito(numero, nip, month, year, TipoTC.CLASICA);
                System.out.println("Su tarjeta Clasica ha quedado registrada.\n");
                selCard = true;
                break;
              case 2:
                tc = new TCredito(numero, nip, month, year, TipoTC.ORO);
                System.out.println("Su tarjeta Oro ha quedado registrada\n");
                selCard = true;
                break;
              case 3:
                tc = new TCredito(numero, nip, month, year, TipoTC.PLATINO);
                System.out.println("Su tarjeta Platino ha quedado registrada\n");
                selCard = true;
                break;
              case 4:
                tc = new TCredito(numero, nip, month, year, TipoTC.BLACK);
                System.out.println("Su tarjeta BLACK ha quedado registrada\n");
                selCard = true;
                break;
              default:
                System.out.println("Opcion no valida. Elija entre 1 y 4.\n");
                selCard = false;
                break;
              } //switch
            } //else
          } while (selCard == false);

          listaClientes.get(position).setTCredito(tc);
          err = false;
        } //fin try //fin try
        catch (ArithmeticException ex) {
          System.err.println("Error: Fecha no existe. \n");
        } catch (InputMismatchException ime) {
          System.err.println("Error: No se pueden teclear letras. \n");
          lc.nextLine();
        }
      } //fin err
    }

    menu2();
  } //fin de addTarjeta

  public static void iD() {
    Scanner lc = new Scanner(System.in);
    int id;
    boolean idfound = true, err = true, found = false;

    if (listaClientes.isEmpty()) {
      System.out.println("\nNo hay Clientes registrados, regresando al Menu...\n");
    } else {
      System.out.println("Si se sabe el ID del cliente a imprimir, escribalo, " +
        "si no, escriba 0 para imprimir todos los clientes, o -1 para regresar a menu.");

      while (err) {
        try {
          while (idfound) {
            id = lc.nextInt();
            lc.nextLine();

            if (id == -1) {
              System.out.println("Regresando a menu...\n");
              idfound = false;
            } else if (id == 0) {
              for (int cont = 0; cont < listaClientes.size(); cont++)
                System.out.println("ID: " + listaClientes.get(cont).getID() +
                  " Nombre: " + listaClientes.get(cont).getNom());

              System.out.println("\nDigite el Id del Cliente que quiere imprimir: ");
              idfound = true;
            } else if (id > 0) {
              for (int cont = 0; cont < listaClientes.size(); cont++) {
                if (listaClientes.get(cont).getID() == id) {
                  listaClientes.get(cont).printCliente();
                  found = true;
                }

              }
              if (found)
                idfound = false;

              else {
                System.out.println("No se encontro el Id de ese cliente, intente de nuevo.");
                idfound = true;
              }
            } else {
              System.out.println("\nEl Id no existe");

              System.out.print("Digite el Id del Cliente que quiere imprimir: ");
              idfound = true;
            }
          } //fin while idfound
          err = false;
        } //fin try//fin try
        catch (InputMismatchException ime) {
          System.err.println("Error: No se pueden teclear letras. \n");
          lc.nextLine();
          System.out.print("Digite el Id del Cliente que quiere imprimir: ");
        }
      } //fin err
    }
    menu2();
  } //fin imprimir datos

  public static void finisher() {
    File archivo = null;
    try {
      //Para agregar datos
      FileWriter fw = new FileWriter("HojaClientes.csv");
      BufferedWriter bw = new BufferedWriter(fw);
      PrintWriter pw = new PrintWriter(bw);
      String texto;

      pw.print("");

      for (int cont = 0; cont < listaClientes.size(); cont++) {
        pw.print("1/1/" + listaClientes.get(cont).getNom() + "/" + listaClientes.get(cont).getAp() + "/" + listaClientes.get(cont).getDir() + "/" + listaClientes.get(cont).getDias() + "/" +
          listaClientes.get(cont).getMeses() + "/" + listaClientes.get(cont).getAnios() + "/" + listaClientes.get(cont).getTel() + "/" + listaClientes.get(cont).getMat() + "/" +
          listaClientes.get(cont).getPass());
        texto = listaClientes.get(cont).fileTarjeta();
        if (texto.charAt(0) == '9') {

        } else {
          pw.println();
          pw.print(texto);
        }
        pw.println();
      }

      pw.flush();
      pw.close();

      System.out.println("Clientes guardados");
    } catch (Exception E) {
      System.out.println("Error al guardar nuevo empleado");
    }
  }
} //fin de la clase
