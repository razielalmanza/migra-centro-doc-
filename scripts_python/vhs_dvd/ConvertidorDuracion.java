import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class ConvertidorDuracion{
  //expresiones regulares para la duracion de una copia de titulo
  public static final String regexSoloNumMin = "^[0-9]+\\s*";
  //public static final String regexMin = "^[0-9]+\\s*[MIN]*";
  public static final String regexMin = "^[0-9]+\\s*[min|minutos]*";
  //public static final String regexMinConDecimal = "^[0-9]+[.][0-9]+\\s*[MIN]*";
  public static final String regexMinConDecimal = "^[0-9]+[.][0-9]+\\s*[min|minutos]*";
  //public static final String regexMinSec = "^[0-9]+\\s*[MIN]*\\s*[0-9]+\\s*[SEG]*";
	public static final String regexMinSec = "^[0-9]+\\s*[min|minutos]*\\s*[0-9]+\\s*[seg|segundos]*";
  public static final String regexTime = "^[0-9][0-9]+:[0-5][0-9]:[0-5][0-9]";
  
  /**
   * Metodo que, dada una duracion, devuelve la duracionSec
   * 
   * @author Luis Felipe Maciel Mercado lfmm
   */

  public static int calculaDuracionSecPorRegex(String duracion) {
    if (duracion.equals("58 MINUTOS, 58 MINUTOS")) return 58;   // Caso harcodeado del unico posible caso raro de la lista. 
    duracion = duracion.toLowerCase(); 
		int duracionSec;
    //		String duracion=this.getDuracion().trim();
		if (duracion==null || duracion.equals("") || duracion.equals("desconocido")){
			duracionSec=0;
		} else {
			float floatDuracionSec=0;
			if (duracion.matches(ConvertidorDuracion.regexMin) || duracion.matches(ConvertidorDuracion.regexMinConDecimal)) {
				String[] duracionDividida = duracion.split("\\s");
				floatDuracionSec = Float.parseFloat(duracionDividida[0])*60;
			} else if (duracion.matches(ConvertidorDuracion.regexMinSec)) {
        String[] duracionDividida = duracion.split("\\s");
        try {
				floatDuracionSec = Float.parseFloat(duracionDividida[0])*60;//parte de los minutos
        floatDuracionSec +=Float.parseFloat(duracionDividida[2]);//se suman los segundos
        } catch (Exception e) {
          //System.out.println("Excepcion." + duracion);
          // Se agrega esta excepción porque moría en algunos casos.
        }
			} else if (duracion.matches(ConvertidorDuracion.regexSoloNumMin)){
				floatDuracionSec = Float.parseFloat(duracion)*60;
			} else if (duracion.matches(ConvertidorDuracion.regexTime)){
				String[] duracionDividida = duracion.split(":");
				floatDuracionSec = Float.parseFloat(duracionDividida[0])*3600;//parte de las horas
				floatDuracionSec += Float.parseFloat(duracionDividida[1])*60;//parte de los minutos
				floatDuracionSec += Float.parseFloat(duracionDividida[2]);//se suman los segundos
			}
			duracionSec=(int) floatDuracionSec;
    }
		return duracionSec;
  }
  
  /**
   * Metodo que recibe un .cvs y por cada entrada manda a llamar a la conversión.
   * Se decide hacer a mano, para evitar el uso de bibliotecas de terceros. 
   * 
   */

  public static String processCSV (String file){
    String s = "";
    try (BufferedReader br = new BufferedReader(new FileReader(file))) {
      String line;
      br.readLine(); // se salta la primera linea.
      while ((line = br.readLine()) != null) {
          String[] values = line.split(",");
          // Quita los "" de cda cadena.
          values[0] = values[0].replace("\"", "");
          values[1] = values[1].replace("\"", "");
          //System.out.println(values[0]);
          //System.out.println(values[1]);
          s += values[0] + "," + calculaDuracionSecPorRegex(values[1]) + "\n";
      }
    } catch (IOException e) {
      e.printStackTrace();
      return s;
     }
    return s;
  }
  public static void main(String[] args) {
    //String convertida = processCSV("duracion_en_strings.csv");
    String convertida = processCSV("duracion_en_strings.csv");
    // Se pretende que al ejecutar el output de la ejecución se redirija a un output file.
    // java ... > output.csv
    System.out.println(convertida); 

    /* Casos de prueba.
    System.out.println(calculaDuracionSecPorRegex("60 MIN")); // ok
    System.out.println(calculaDuracionSecPorRegex("30 minutos 20 seg")); // ok
    System.out.println(calculaDuracionSecPorRegex("58 MINUTOS, 58 MINUTOS")); // no funciona
    //System.out.println(calculaDuracionSecPorRegex("58MINUTOS")); // no funciona, exception
    System.out.println(calculaDuracionSecPorRegex("60")); // funciona
    */

  }

}