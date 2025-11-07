package com.devsecops.vulnerable;

import org.springframework.web.bind.annotation.*;
import javax.servlet.http.HttpServletRequest;
import java.sql.*;
import java.io.*;
import java.util.*;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*")  // VULNERABILITY: Allow all origins
public class VulnerableController {

    // VULNERABILITY: Hardcoded credentials
    private static final String DB_PASSWORD = "admin123";
    private static final String API_KEY = "sk-1234567890abcdef";

    @GetMapping("/health")
    public Map<String, String> health() {
        Map<String, String> response = new HashMap<>();
        response.put("status", "UP");
        response.put("version", "1.0.0");
        return response;
    }

    // VULNERABILITY: SQL Injection
    @GetMapping("/users")
    public List<Map<String, Object>> getUsers(@RequestParam String username) throws SQLException {
        List<Map<String, Object>> results = new ArrayList<>();
        Connection conn = DriverManager.getConnection("jdbc:h2:mem:testdb", "sa", "");
        
        // Unsafe concatenation - SQL Injection vulnerability
        Statement stmt = conn.createStatement();
        ResultSet rs = stmt.executeQuery("SELECT * FROM users WHERE username = '" + username + "'");
        
        while (rs.next()) {
            Map<String, Object> row = new HashMap<>();
            row.put("id", rs.getInt("id"));
            row.put("username", rs.getString("username"));
            row.put("email", rs.getString("email"));
            results.add(row);
        }
        
        conn.close();
        return results;
    }

    // VULNERABILITY: Path Traversal
    @GetMapping("/file")
    public String readFile(@RequestParam String filename) throws IOException {
        // No validation - allows path traversal
        File file = new File(filename);
        Scanner scanner = new Scanner(file);
        StringBuilder content = new StringBuilder();
        
        while (scanner.hasNextLine()) {
            content.append(scanner.nextLine()).append("\n");
        }
        scanner.close();
        
        return content.toString();
    }

    // VULNERABILITY: Command Injection
    @PostMapping("/ping")
    public String ping(@RequestParam String host) throws IOException {
        // Unsafe command execution
        Process process = Runtime.getRuntime().exec("ping -c 4 " + host);
        BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
        StringBuilder output = new StringBuilder();
        String line;
        
        while ((line = reader.readLine()) != null) {
            output.append(line).append("\n");
        }
        
        return output.toString();
    }

    // VULNERABILITY: Sensitive data exposure
    @GetMapping("/config")
    public Map<String, String> getConfig() {
        Map<String, String> config = new HashMap<>();
        config.put("database_password", DB_PASSWORD);
        config.put("api_key", API_KEY);
        config.put("environment", "production");
        return config;
    }

    // VULNERABILITY: XXE (XML External Entity)
    @PostMapping("/xml")
    public String parseXml(@RequestBody String xmlData) {
        try {
            javax.xml.parsers.DocumentBuilderFactory factory = 
                javax.xml.parsers.DocumentBuilderFactory.newInstance();
            // XXE vulnerability - external entities enabled by default
            javax.xml.parsers.DocumentBuilder builder = factory.newDocumentBuilder();
            org.w3c.dom.Document doc = builder.parse(
                new org.xml.sax.InputSource(new StringReader(xmlData))
            );
            return "XML parsed successfully";
        } catch (Exception e) {
            return "Error: " + e.getMessage();
        }
    }

    // VULNERABILITY: No authentication/authorization
    @DeleteMapping("/users/{id}")
    public String deleteUser(@PathVariable int id) {
        // Anyone can delete any user - no auth check
        return "User " + id + " deleted";
    }

    // VULNERABILITY: Information disclosure through error messages
    @GetMapping("/debug")
    public String debug(HttpServletRequest request) {
        StringBuilder info = new StringBuilder();
        info.append("System Properties:\n");
        System.getProperties().forEach((key, value) -> 
            info.append(key).append(" = ").append(value).append("\n")
        );
        return info.toString();
    }
}
