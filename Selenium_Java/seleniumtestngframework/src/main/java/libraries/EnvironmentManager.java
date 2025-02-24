package libraries;

import utilities.CSVUtilities;

import java.util.HashMap;
import java.util.Map;

public class EnvironmentManager {

	private static Map<String, String> environment;

	static {
		loadEnvironmentsFromCSV();
	}

	private static void loadEnvironmentsFromCSV() {
		environment = new HashMap<>();
		try (CSVUtilities csvUtils = new CSVUtilities()) {
			Map<String, String> data = csvUtils.readData();
			if (data != null) {
				for (Map.Entry<String, String> entry : data.entrySet()) {
					environment.put(entry.getKey().toLowerCase(), entry.getValue()); // Case-insensitive key
				}
			} else {
				System.err.println("Error reading environment data from CSV. Using default values.");
			}
		} catch (Exception e) {
			System.err.println("Error initializing CSVUtilities: " + e.getMessage());

		}
	}

	public static String getEnvironmentUrl(String envName) {
		if (envName == null) {
			envName = System.getenv("ENV_NAME");
		}

		if (envName == null) {
			System.err.println("ENV_NAME environment variable is not set and no envName was provided.");
			return null;
		}

		envName = envName.toLowerCase();

		if (environment.containsKey(envName)) {
			return environment.get(envName);
		} else {
			System.err.println("Environment '" + envName + "' not found.");
			return null;
		}
	}

	public static String getEnvironmentUrl() {
		return getEnvironmentUrl(null);
	}
}