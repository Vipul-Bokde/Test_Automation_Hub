// PageMethodExecutor.java (Original Version - No Sheet Handling)
package utilities;

import org.testng.Assert;
import java.lang.reflect.Method;
import java.util.HashMap;
import java.util.Map;

public class PageMethodExecutor {

    public void executePageMethod(Object pageObject, String methodName, String... keys) {
        Map<String, String> data = new HashMap<>();

        if (keys.length > 0) {
            data = DataProvider.getData(keys);
            if (data == null) return;
        }

        Object[] args = new Object[keys.length];
        for (int i = 0; i < keys.length; i++) {
            if (keys.length > 0) {
                args[i] = data.get(keys[i]);
            }
        }

        try {
            Class<?> pageClass = pageObject.getClass();
            Method method;

            if (keys.length > 0) {
                method = pageClass.getMethod(methodName, getParameterTypes(args));
            } else {
                try {
                    method = pageClass.getMethod(methodName);
                } catch (NoSuchMethodException noArgsException) {
                    try {
                        method = pageClass.getMethod(methodName, getParameterTypes(args));
                    } catch (NoSuchMethodException withArgsException) {
                        Assert.fail("Method '" + methodName + "' not found in " + pageObject.getClass().getSimpleName() + " or incorrect parameters. Check if you are passing the arguments or not.");
                        withArgsException.printStackTrace();
                        return;
                    }
                }
            }

            method.invoke(pageObject, args);

        } catch (NoSuchMethodException e) {
            Assert.fail("Method '" + methodName + "' not found in " + pageObject.getClass().getSimpleName() + " or incorrect parameters.");
            e.printStackTrace();
        } catch (Exception e) {
            Assert.fail("Error invoking method '" + methodName + "' on " + pageObject.getClass().getSimpleName() + ": " + e.getMessage());
            e.printStackTrace();
        }
    }

    private Class<?>[] getParameterTypes(Object[] args) {
        Class<?>[] types = new Class<?>[args.length];
        for (int i = 0; i < args.length; i++) {
            if (args[i] != null) {
                types[i] = args[i].getClass();
            } else {
                types[i] = String.class; // Default for nulls
            }
        }
        return types;
    }
}