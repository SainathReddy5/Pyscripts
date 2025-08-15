# PySpark Java Compatibility Solutions

This repository contains Python scripts to diagnose and fix common PySpark Java compatibility issues, particularly the `UnsupportedClassVersionError` that occurs when there's a Java version mismatch.

## The Problem

When running PySpark applications, you might encounter this error:

```
Error: LinkageError occurred while loading main class org.apache.spark.launcher.Main
        java.lang.UnsupportedClassVersionError: org/apache/spark/launcher/Main has been compiled by a more recent version of the Java Runtime (class file version 61.0), this version of the Java Runtime only recognizes class file versions up to 55.0
```

This error occurs when:
- Spark JARs were compiled with Java 17 (class file version 61.0)
- Your runtime environment only has Java 11 or older (supports up to class file version 55.0)

## Java Version Mapping

| Java Version | Class File Version | PySpark Compatibility |
|--------------|-------------------|----------------------|
| Java 8       | 52.0              | PySpark 2.x - 3.3   |
| Java 11      | 55.0              | PySpark 3.0+         |
| Java 17      | 61.0              | PySpark 3.3+         |

## Solutions

### 1. Environment Validation Script

Use `pyspark_env_validator.py` to diagnose your environment:

```bash
python pyspark_env_validator.py
```

This script will:
- ✅ Check Java installation and version
- ✅ Validate JAVA_HOME environment variable
- ✅ Test PySpark installation
- ✅ Attempt to create a Spark session
- ✅ Generate a detailed environment report

### 2. Java Compatibility Handler

Use `pyspark_java_compatibility.py` for a comprehensive compatibility check:

```bash
python pyspark_java_compatibility.py
```

Features:
- 🔍 Automatic Java version detection
- ⚙️ Spark session configuration with compatibility settings
- 🛠️ Automatic JAVA_HOME setup
- 📊 PySpark functionality demonstration

### 3. Delta Lake Streaming Fix

Use `write_stream_to_delta.py` to fix the specific Delta Lake streaming issue:

```bash
python write_stream_to_delta.py
```

This script addresses:
- ✅ Java gateway exit issues
- ✅ Delta Lake configuration with Java compatibility
- ✅ Proper error handling and troubleshooting

## Quick Fixes

### Option 1: Install Compatible Java Version

```bash
# Install Java 11 (recommended for most PySpark versions)
# Ubuntu/Debian
sudo apt update
sudo apt install openjdk-11-jdk

# macOS
brew install openjdk@11

# Set JAVA_HOME
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64  # Linux
export JAVA_HOME=/opt/homebrew/opt/openjdk@11         # macOS
```

### Option 2: Use Compatible PySpark Version

```bash
# For Java 8
pip install pyspark==3.3.4

# For Java 11
pip install pyspark==3.4.1

# For Java 17
pip install pyspark==3.5.0
```

### Option 3: Docker Solution

Use a pre-configured Docker environment:

```dockerfile
FROM openjdk:11-jre-slim

RUN pip install pyspark==3.4.1 delta-spark

COPY your_script.py /app/
WORKDIR /app

CMD ["python", "your_script.py"]
```

## Environment Setup

### 1. Set Environment Variables

```bash
# Add to ~/.bashrc or ~/.zshrc
export JAVA_HOME=/path/to/your/java/installation
export SPARK_HOME=/path/to/spark  # if using standalone Spark
export PYSPARK_PYTHON=python3
```

### 2. Install Required Packages

```bash
# Basic PySpark
pip install pyspark

# With Delta Lake
pip install pyspark delta-spark

# Development dependencies
pip install pyspark[sql] jupyter
```

## Troubleshooting

### Common Issues and Solutions

1. **JAVA_GATEWAY_EXITED Error**
   - Check Java version compatibility
   - Verify JAVA_HOME is set correctly
   - Ensure no conflicting Java installations

2. **UnsupportedClassVersionError**
   - Install compatible Java version
   - Use matching PySpark version
   - Set JAVA_HOME to correct Java installation

3. **Delta Lake Issues**
   - Install delta-spark package
   - Use compatible versions (see compatibility matrix)
   - Configure Spark with Delta extensions

### Compatibility Matrix

| PySpark Version | Java 8 | Java 11 | Java 17 | Delta Lake |
|----------------|--------|---------|---------|------------|
| 2.4.x          | ✅     | ❌      | ❌      | 0.6-0.8    |
| 3.0.x          | ✅     | ✅      | ❌      | 0.7-1.0    |
| 3.1.x          | ✅     | ✅      | ❌      | 1.0-1.2    |
| 3.2.x          | ✅     | ✅      | ❌      | 1.2-2.0    |
| 3.3.x          | ✅     | ✅      | ✅      | 2.0-2.2    |
| 3.4.x          | ✅     | ✅      | ✅      | 2.2-2.4    |
| 3.5.x          | ❌     | ✅      | ✅      | 2.4+       |

## Additional Resources

- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)
- [Delta Lake Documentation](https://docs.delta.io/)
- [Java Downloads](https://adoptium.net/)
- [PySpark Installation Guide](https://spark.apache.org/docs/latest/api/python/getting_started/install.html)

## Contributing

Feel free to contribute improvements to these scripts or add new compatibility solutions!