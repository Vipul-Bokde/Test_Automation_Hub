package utilities;

import java.util.HashMap;
import java.util.Map;

import org.testng.Assert;

public class DataProvider {
	private static Map<String, String> allTestData = new HashMap<>();

    static {
        try (CSVUtilities csv = new CSVUtilities()) {
            allTestData = csv.readData();
            if (allTestData == null) {
                Assert.fail("Failed to load test data. Check CSV file and setup.");
            }
        } catch (RuntimeException e) {
            System.err.println("Error loading test data: " + e.getMessage());
            e.printStackTrace();
            Assert.fail("Test data loading error: " + e.getMessage());
        }
    }

    public static Map<String, String> getData(String... keys) {
        Map<String, String> requestedData = new HashMap<>();

        for (String key : keys) {
            String value = allTestData.get(key);

            if (value == null) {
                Assert.fail("Data not found for key '" + key + "'. Available keys are: " + allTestData.keySet());
                return null;
            }
            requestedData.put(key, value);
        }
        return requestedData;
    }
}
