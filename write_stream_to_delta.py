#!/usr/bin/env python3
"""
PySpark Delta Lake Streaming Script

This script addresses the specific error in write_stream_to_delta.py:
- Java version compatibility issues
- Delta Lake configuration
- Proper error handling for PySpark startup failures

Original error:
java.lang.UnsupportedClassVersionError: org/apache/spark/launcher/Main 
has been compiled by a more recent version of the Java Runtime (class file version 61.0), 
this version of the Java Runtime only recognizes class file versions up to 55.0
"""

import os
import sys
import subprocess
from typing import Optional


def check_java_compatibility():
    """Check Java version compatibility for PySpark Delta Lake."""
    try:
        result = subprocess.run(['java', '-version'], 
                              capture_output=True, text=True)
        java_version = result.stderr
        print(f"Java version info: {java_version}")
        
        # Extract major version
        import re
        version_match = re.search(r'"(\d+)\.(\d+)\.(\d+)', java_version)
        if version_match:
            major = int(version_match.group(1))
            if major == 1:  # Handle format like "1.8.0"
                major = int(version_match.group(2))
            return major
        
        # Try newer format
        version_match = re.search(r'"(\d+)', java_version)
        if version_match:
            return int(version_match.group(1))
            
    except (subprocess.SubprocessError, FileNotFoundError):
        print("❌ Java not found")
        return None
    
    return None


def configure_spark_with_delta_pip(builder):
    """
    Configure Spark with Delta Lake using pip packages.
    This function mimics the original configure_spark_with_delta_pip mentioned in the error.
    """
    try:
        # Configure for Delta Lake with proper Java compatibility
        builder = builder.config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
                        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        
        # Add Java compatibility options for Java 11+
        java_version = check_java_compatibility()
        if java_version and java_version >= 11:
            java_opts = [
                "--add-opens=java.base/java.lang=ALL-UNNAMED",
                "--add-opens=java.base/java.lang.invoke=ALL-UNNAMED",
                "--add-opens=java.base/java.lang.reflect=ALL-UNNAMED",
                "--add-opens=java.base/java.io=ALL-UNNAMED",
                "--add-opens=java.base/java.net=ALL-UNNAMED",
                "--add-opens=java.base/java.nio=ALL-UNNAMED",
                "--add-opens=java.base/java.util=ALL-UNNAMED",
                "--add-opens=java.base/java.util.concurrent=ALL-UNNAMED",
                "--add-opens=java.base/java.util.concurrent.atomic=ALL-UNNAMED",
                "--add-opens=java.base/sun.nio.ch=ALL-UNNAMED",
                "--add-opens=java.base/sun.nio.cs=ALL-UNNAMED",
                "--add-opens=java.base/sun.security.action=ALL-UNNAMED",
                "--add-opens=java.base/sun.util.calendar=ALL-UNNAMED"
            ]
            
            java_opts_str = " ".join(java_opts)
            builder = builder.config("spark.driver.extraJavaOptions", java_opts_str) \
                           .config("spark.executor.extraJavaOptions", java_opts_str)
        
        return builder
        
    except Exception as e:
        print(f"❌ Error configuring Delta Lake: {str(e)}")
        raise


def safe_spark_session_creation():
    """
    Safely create a Spark session with proper error handling.
    """
    try:
        from pyspark.sql import SparkSession
        
        print("🔧 Creating Spark session with Delta Lake support...")
        
        # Check Java compatibility first
        java_version = check_java_compatibility()
        if not java_version:
            raise RuntimeError("Java not found. Please install Java 8, 11, or 17.")
        
        if java_version not in [8, 11, 17]:
            print(f"⚠️  Warning: Java {java_version} may not be fully compatible with PySpark")
            print("Recommended versions: Java 8, 11, or 17")
        
        # Create builder
        builder = SparkSession.builder.appName("DeltaLakeStreaming")
        
        # Configure with Delta Lake
        builder = configure_spark_with_delta_pip(builder)
        
        # Create session
        spark = builder.getOrCreate()
        
        print("✅ Spark session created successfully!")
        return spark
        
    except ImportError as e:
        print(f"❌ Missing dependency: {str(e)}")
        print("Install required packages:")
        print("  pip install pyspark delta-spark")
        raise
        
    except Exception as e:
        print(f"❌ Failed to create Spark session: {str(e)}")
        
        # Provide specific troubleshooting based on error type
        error_str = str(e)
        if "UnsupportedClassVersionError" in error_str:
            print("\n🔍 Java Version Compatibility Issue Detected!")
            print("Solutions:")
            print("1. Install compatible Java version:")
            print("   - For PySpark 3.3+: Use Java 11 or 17")
            print("   - For PySpark 3.0-3.2: Use Java 8 or 11")
            print("2. Set JAVA_HOME environment variable")
            print("3. Use compatible PySpark version")
            
        elif "JAVA_GATEWAY_EXITED" in error_str:
            print("\n🔍 Java Gateway Exit Issue Detected!")
            print("Solutions:")
            print("1. Check Java version compatibility")
            print("2. Ensure JAVA_HOME is set correctly")
            print("3. Check for conflicting Java installations")
            print("4. Try restarting your terminal/IDE")
            
        raise


def demo_delta_streaming():
    """
    Demonstrate Delta Lake streaming functionality.
    """
    try:
        spark = safe_spark_session_creation()
        
        # Create sample data for streaming demo
        from pyspark.sql.types import StructType, StructField, StringType, IntegerType
        from pyspark.sql.functions import col, current_timestamp
        
        # Define schema
        schema = StructType([
            StructField("id", IntegerType(), True),
            StructField("name", StringType(), True),
            StructField("value", IntegerType(), True)
        ])
        
        # Create sample DataFrame
        data = [(1, "Alice", 100), (2, "Bob", 200), (3, "Charlie", 300)]
        df = spark.createDataFrame(data, schema)
        df = df.withColumn("timestamp", current_timestamp())
        
        print("📊 Sample data for Delta streaming:")
        df.show()
        
        # Write to Delta format (simulating streaming write)
        delta_path = "/tmp/delta-table"
        print(f"💾 Writing to Delta table at: {delta_path}")
        
        df.write.format("delta").mode("overwrite").save(delta_path)
        
        # Read back from Delta
        delta_df = spark.read.format("delta").load(delta_path)
        print("📖 Reading from Delta table:")
        delta_df.show()
        
        print("✅ Delta Lake operations completed successfully!")
        
        spark.stop()
        
    except Exception as e:
        print(f"❌ Error in Delta streaming demo: {str(e)}")
        raise


def main():
    """
    Main function to demonstrate the fix for the PySpark Delta streaming issue.
    """
    print("🚀 PySpark Delta Lake Streaming Fix")
    print("=" * 50)
    
    try:
        demo_delta_streaming()
        
    except Exception as e:
        print(f"\n❌ Failed to run Delta streaming demo: {str(e)}")
        print("\n💡 Complete troubleshooting checklist:")
        print("1. ☑️  Install compatible Java (8, 11, or 17)")
        print("2. ☑️  Set JAVA_HOME environment variable")
        print("3. ☑️  Install PySpark: pip install pyspark")
        print("4. ☑️  Install Delta Lake: pip install delta-spark")
        print("5. ☑️  Ensure versions are compatible:")
        print("   - Java 8: PySpark 2.x-3.3, Delta 0.8-2.x")
        print("   - Java 11: PySpark 3.0+, Delta 1.0+")
        print("   - Java 17: PySpark 3.3+, Delta 2.0+")
        
        sys.exit(1)


if __name__ == "__main__":
    main()