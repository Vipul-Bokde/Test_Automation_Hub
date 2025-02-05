// CSVUtilities.java
package utilities;

import com.opencsv.CSVReader;
import com.opencsv.CSVWriter;
import com.opencsv.exceptions.CsvException;

import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class CSVUtilities implements AutoCloseable {

    private static final String ENCRYPTED_FILE_PATH = "src/main/java/testdata/TestData.enc";
    private static final String TEMP_FILE_PATH = "src/main/java/testdata/temp.csv";
    private static final String SECRET_KEY = System.getenv("SECRET_TEST_DATA_KEY");

    public CSVUtilities() {
        try {
            decryptFile(ENCRYPTED_FILE_PATH, TEMP_FILE_PATH);
        } catch (Exception e) {
            throw new RuntimeException("Error initializing CSVUtilities: " + e.getMessage(), e);
        }
    }

    private void decryptFile(String inputPath, String outputPath) throws Exception {
        if (SECRET_KEY == null || SECRET_KEY.isEmpty()) {
            throw new RuntimeException("SECRET_TEST_DATA_KEY environment variable is not set.");
        }

        byte[] encryptedData = Files.readAllBytes(Paths.get(inputPath));
        byte[] decryptedData = decrypt(encryptedData);
        Files.write(Paths.get(outputPath), decryptedData);
    }

    private byte[] decrypt(byte[] encryptedData) throws Exception {
        Cipher cipher = Cipher.getInstance("AES");
        SecretKeySpec keySpec = new SecretKeySpec(SECRET_KEY.getBytes(), "AES");
        cipher.init(Cipher.DECRYPT_MODE, keySpec);
        return cipher.doFinal(encryptedData);
    }

    public Map<String, String> readData() {
        Map<String, String> dataMap = new HashMap<>();
        try (CSVReader reader = new CSVReader(new FileReader(TEMP_FILE_PATH))) {
            List<String[]> rows = reader.readAll();
            if (rows.size() < 2) {
                return dataMap; // Handle empty or header-only CSV
            }
            String[] headerRow = rows.get(0);
            String[] valueRow = rows.get(1);

            for (int i = 0; i < Math.min(headerRow.length, valueRow.length); i++) {
                dataMap.put(headerRow[i], valueRow[i]);
            }
        } catch (IOException | CsvException e) {
            throw new RuntimeException("Error reading CSV file: " + e.getMessage(), e);
        }
        return dataMap;
    }

    public void writeData(String key, String value) throws Exception {
        try {
            List<String[]> rows;
            try (CSVReader reader = new CSVReader(new FileReader(TEMP_FILE_PATH))) {
                rows = reader.readAll();
            }

            boolean keyExists = false;
            for (String[] row : rows) {
                if (row.length > 0 && row[0].equalsIgnoreCase(key)) {
                    if (row.length > 1) {
                        row[1] = value;
                    } else {
                        String[] newRow = {key, value};
                        rows.add(newRow);
                    }
                    keyExists = true;
                    break;
                }
            }

            if (!keyExists) {
                rows.add(new String[]{key, value});
            }

            try (CSVWriter writer = new CSVWriter(new FileWriter(TEMP_FILE_PATH))) {
                writer.writeAll(rows);
            }

            encryptFile(TEMP_FILE_PATH, ENCRYPTED_FILE_PATH);
        } catch (IOException | CsvException e) {
            throw new RuntimeException("Error writing to CSV file: " + e.getMessage(), e);
        }
    }

    private void encryptFile(String inputPath, String outputPath) throws Exception {
        byte[] fileData = Files.readAllBytes(Paths.get(inputPath));
        byte[] encryptedData = encrypt(fileData);
        Files.write(Paths.get(outputPath), encryptedData);
    }

    private byte[] encrypt(byte[] data) throws Exception {
        Cipher cipher = Cipher.getInstance("AES");
        SecretKeySpec keySpec = new SecretKeySpec(SECRET_KEY.getBytes(), "AES");
        cipher.init(Cipher.ENCRYPT_MODE, keySpec);
        return cipher.doFinal(data);
    }

    @Override
    public void close() {
        new File(TEMP_FILE_PATH).delete();
    }
}
