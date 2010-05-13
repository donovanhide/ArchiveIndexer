import org.python.core.PyException;
import org.python.util.PythonInterpreter;
import java.util.*;

public class Main {
    public static void main(String[] args) throws PyException{
	Properties props=new Properties();
    PythonInterpreter.initialize(System.getProperties(),props,args);
    PythonInterpreter intrp = new PythonInterpreter();
	intrp.exec("import archiveindexer");
	intrp.exec("archiveindexer.main()");
    }
}