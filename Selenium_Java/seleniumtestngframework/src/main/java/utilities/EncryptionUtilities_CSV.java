package utilities;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.nio.file.Files;
import java.nio.file.Paths;

public class EncryptionUtilities_CSV {

	private static final String SECRET_KEY = System.getenv("SECRET_TEST_DATA_KEY");
	
	// Check if the environment variable is set
    static {
        if (SECRET_KEY == null || SECRET_KEY.isEmpty()) {
            System.out.println("Error: SECRET_TEST_DATA_KEY environment variable is not set.");
            System.exit(1); // Exit if the key is not found
        }
    }

	public static void encryptFile(String inputPath, String outputPath) throws Exception {
	    System.out.println("Starting encryption...");
	    byte[] fileData = Files.readAllBytes(Paths.get(inputPath));
	    byte[] encryptedData = encrypt(fileData);
	    
	    // Check if encrypted data is generated
	    if (encryptedData != null && encryptedData.length > 0) {
	        Files.write(Paths.get(outputPath), encryptedData);
	        System.out.println("Encrypted file written successfully to: " + outputPath);
	    } else {
	        System.out.println("Encryption failed: no data to write.");
	    }
	}

	// Decrypt file
	public static void decryptFile(String inputPath, String outputPath) throws Exception {
		byte[] encryptedData = Files.readAllBytes(Paths.get(inputPath));
		byte[] decryptedData = decrypt(encryptedData);
		Files.write(Paths.get(outputPath), decryptedData);
	}
	
	// Encrypt method using AES
	private static byte[] encrypt(byte[] data) throws Exception {
		Cipher cipher = Cipher.getInstance("AES");
		SecretKeySpec keySpec = new SecretKeySpec(SECRET_KEY.getBytes(), "AES");
		cipher.init(Cipher.ENCRYPT_MODE, keySpec);
		return cipher.doFinal(data);
	}
	
	// Decrypt method using AES
	private static byte[] decrypt(byte[] encryptedData) throws Exception {
		Cipher cipher = Cipher.getInstance("AES");
		SecretKeySpec keySpec = new SecretKeySpec(SECRET_KEY.getBytes(), "AES");
		cipher.init(Cipher.DECRYPT_MODE, keySpec);
		return cipher.doFinal(encryptedData);
	}

	public static void main(String[] args) throws Exception {
		
		String inputPath = ConfigReader.getProperty("inputPath");
        String outputPath = ConfigReader.getProperty("outputPath");
		// Encrypt
		encryptFile(inputPath, outputPath);
		System.out.println("TestData encrypted successfully.");

		// Decrypt (for testing)
		decryptFile(outputPath, inputPath);
		System.out.println("TestData decrypted successfully.");
	}
}
