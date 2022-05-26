package bancooo;
import java.util.*;

public class Cliente {
    private int id;
    private static int contid = 0, tarjetaNum = 0, aContid=0;
    private String nombre, apellido, direccion;
    private Fecha fechaNacimiento;
    private String telefono, password, matricula;
    private ArrayList < TCredito > listaTC = new ArrayList < > ();

    public Cliente(String nombre, String apellido, String direccion, int dia, int mes, int anio, String telefono){
        contid++;
        id = contid;
        this.nombre = nombre;
        this.apellido = apellido;
        this.direccion = direccion;
        fechaNacimiento = new Fecha(dia, mes, anio);
        this.telefono = telefono;
        password="1";
        matricula="C"+id;
    }
    public Cliente(String nombre, String apellido, String direccion, int dia, int mes, int anio, String telefono, String password){
        contid++;
        id = contid;
        this.nombre = nombre;
        this.apellido = apellido;
        this.direccion = direccion;
        fechaNacimiento = new Fecha(dia, mes, anio);
        this.telefono = telefono;
        this.password=password;
        matricula="A"+id;
    }

    public Cliente(int tarjetaNum){
        contid--;
    }
    public Cliente(){

    }

    public void removeTarjeta(int pos) {
        listaTC.remove(pos);
    }

    public void setTCredito(TCredito tc) {
        listaTC.add(tc);
    }
    public void setNom(String nom) {
        this.nombre = nom;
    }
    public void setAp(String ap) {
        this.apellido = ap;
    }
    public void setDir(String direccion) {
        this.direccion = direccion;
    }
    public void setTel(String telefono) {
        this.telefono = telefono;
    }
    public void setMatricula(String matricula) {
        this.matricula = matricula;
    }
    public String getNom() {
        return nombre;
    }
    public String getAp(){
      return apellido;
    }
    public String getDir(){
      return direccion;
    }
    public String getTel(){
      return telefono;
    }
    public int getID() {
        return id;
    }
    public int getDias() {
        return fechaNacimiento.getDia();
    }
    public int getMeses() {
        return fechaNacimiento.getMes();
    }
    public int getAnios() {
        return fechaNacimiento.getAnno();
    }
    public String getMat() {
        return matricula;
    }
    public String getPass(){
      return password;
    }

    public double getBalanceTarjeta(int posicion) {
        return listaTC.get(posicion - 1).getBalance();
    }

    public void setNuevoSaldo(int posicion, double saldo) {
        listaTC.get(posicion - 1).setBalance(saldo);
    }

    public void printCliente() {
        System.out.printf("\nId: %d\nMatricula: %s\nNombre: %s, %s\nDireccion: %s\nTelefono: %s\n", id, matricula, apellido, nombre, direccion, telefono);
        System.out.println("Fecha de Nacimiento: "+fechaNacimiento.FormatoFecha2());
        if (listaTC.size() > 0)
            for (int cont = 0; cont < listaTC.size(); cont++)
                listaTC.get(cont).printTarjeta();
        else
            System.out.println("El cliente no tiene asignada tarjetas de crédito \n");
    }

    public void printTarjetas() {
        for (int cont = 0; cont < listaTC.size(); cont++) {
            listaTC.get(cont).printTarjeta();
        }
    }

    public void printNoTarjetas() {
        for (int cont = 0; cont < listaTC.size(); cont++) {
            System.out.println(listaTC.get(cont).getNumero());
        }
    }

    public boolean pickTarjeta(int opcion) {
        TCredito tarjeta;
        Scanner lector = new Scanner(System.in);
        boolean valid = false;

        if (listaTC.size() > 0) {
            System.out.println("Ingrese el número de la tarjeta");
            String num = lector.nextLine();
            for (int i = 0; i < listaTC.size(); i++) {
                if (num.equals(listaTC.get(i).getNumero())) {
                    tarjeta = listaTC.get(i);

                    switch(opcion){
                      case 1: //retiros
                        valid = (tarjeta.pickPin(1));
                        break;
                      case 2: //pagos
                        valid = (tarjeta.pickPin(2));
                        break;
                      case 3: //compras
                        valid = (tarjeta.pickPin(3));
                         break;
                      case 4: //edo. cuenta
                        valid = (tarjeta.pickPin(4));
                        break;
                      default:
                        System.out.println("Selcciona una opción válida");
                      break;
                    }

                }

                else {
                    System.out.println("No se encontró tarjeta.");
                    valid = false;
                }
            }
        }
        else {
            System.out.println("El cliente no tiene asignada tarjetas de crédito \n");
            valid = false;
        }
        return valid;
    }

    public String fileTarjeta() {
        TCredito tarjeta;
        String val="9";
        if (listaTC.size() > 0){
            for (int cont = 0; cont < listaTC.size(); cont++){
              switch (listaTC.get(cont).getTipoTC()) {
                  case CLASICA:
                      val="1/2/"+listaTC.get(cont).getNumero()+"/"+listaTC.get(cont).getPin()+"/"+listaTC.get(cont).getMese()+"/"+listaTC.get(cont).getAnios()+"/1/"+listaTC.get(cont).getBalance();
                      break;
                  case ORO:
                      val="1/2/"+listaTC.get(cont).getNumero()+"/"+listaTC.get(cont).getPin()+"/"+listaTC.get(cont).getMese()+"/"+listaTC.get(cont).getAnios()+"/2/"+listaTC.get(cont).getBalance();
                      break;
                  case PLATINO:
                      val="1/2/"+listaTC.get(cont).getNumero()+"/"+listaTC.get(cont).getPin()+"/"+listaTC.get(cont).getMese()+"/"+listaTC.get(cont).getAnios()+"/3/"+listaTC.get(cont).getBalance();
                      break;
                  case BLACK:
                      val="1/2/"+listaTC.get(cont).getNumero()+"/"+listaTC.get(cont).getPin()+"/"+listaTC.get(cont).getMese()+"/"+listaTC.get(cont).getAnios()+"/4/"+listaTC.get(cont).getBalance();
                      break;
                  default:
                      System.out.println("Opcion no valida. Elija entre 1 y 4.\n");
                      break;
              } //switch
            }
            return val;
        }
        else{
            return val;
        }
    }

    public void getCard() {
        TCredito card;
        Scanner stdIn = new Scanner(System.in);
        if (listaTC.size() > 0) {

            System.out.println("Ingrese los numeros de la tarjeta: ");
            String cardNumber = stdIn.nextLine();
            for (int i = 0; i < listaTC.size(); i++) {
                if (cardNumber.equals(listaTC.get(i).getNumero())) {
                    card = listaTC.get(i);
                    card.pickPin(2);

                } else {
                    System.out.println("Alguno de los datos es incorrecto, intente otra vez");
                    System.out.println();
                }
            }

        } else {
            System.out.println("El cliente no tiene una tarjeta\n");
        }
    }

}
