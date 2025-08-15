#!/usr/bin/env python3
"""
PySpark Java Compatibility Handler

This script addresses the common Java version compatibility issues with PySpark,
specifically the UnsupportedClassVersionError that occurs when Spark is compiled
with a newer Java version than the runtime supports.

Error addressed:
- java.lang.UnsupportedClassVersionError: org/apache/spark/launcher/Main 
  has been compiled by a more recent version of the Java Runtime (class file version 61.0), 
  this version of the Java Runtime only recognizes class file versions up to 55.0
"""

import os
import sys
import subprocess
import re
from typing import Optional, Tuple


def get_java_version() -> Optional[Tuple[int, str]]:
    """
    Get the current Java version.
    
    Returns:
        Tuple of (major_version, full_version_string) or None if Java not found
    """
    try:
        result = subprocess.run(['java', '-version'], 
                              capture_output=True, text=True)
        version_output = result.stderr
        
        # Parse version from output like "openjdk version "11.0.20""
        version_match = re.search(r'"(\d+)\.(\d+)\.(\d+)', version_output)
        if version_match:
            major = int(version_match.group(1))
            if major == 1:  # Handle older format like "1.8.0"
                major = int(version_match.group(2))
            return major, version_output.strip()
        
        # Try alternate format for newer Java versions
        version_match = re.search(r'"(\d+)', version_output)
        if version_match:
            major = int(version_match.group(1))
            return major, version_output.strip()
            
    except (subprocess.SubprocessError, FileNotFoundError):
        pass
    
    return None


def check_java_compatibility() -> bool:
    """
    Check if the current Java version is compatible with PySpark.
    
    Returns:
        True if compatible, False otherwise
    """
    java_info = get_java_version()
    if not java_info:
        print("❌ Java not found. Please install Java 8, 11, or 17.")
        print("   Download from: https://adoptium.net/")
        return False
    
    major_version, full_version = java_info
    print(f"☕ Found Java version: {major_version}")
    print(f"   Full version: {full_version}")
    
    # PySpark typically supports Java 8, 11, and 17
    supported_versions = [8, 11, 17]
    if major_version in supported_versions:
        print(f"✅ Java {major_version} is supported by PySpark")
        return True
    else:
        print(f"⚠️  Java {major_version} may not be fully supported by PySpark")
        print(f"   Recommended versions: {', '.join(map(str, supported_versions))}")
        return False


def set_java_home_if_needed():
    """
    Set JAVA_HOME environment variable if not already set.
    """
    if 'JAVA_HOME' not in os.environ:
        try:
            # Try to find Java home
            result = subprocess.run(['java', '-XshowSettings:properties', '-version'], 
                                  capture_output=True, text=True)
            
            for line in result.stderr.split('\n'):
                if 'java.home' in line:
                    java_home = line.split('=')[1].strip()
                    os.environ['JAVA_HOME'] = java_home
                    print(f"🔧 Set JAVA_HOME to: {java_home}")
                    break
        except subprocess.SubprocessError:
            print("⚠️  Could not automatically set JAVA_HOME")


def configure_spark_with_compatible_java():
    """
    Configure Spark session with Java compatibility settings.
    """
    try:
        from pyspark.sql import SparkSession
        from pyspark.conf import SparkConf
        
        # Configure Spark with compatibility settings
        conf = SparkConf()
        conf.set("spark.sql.adaptive.enabled", "true")
        conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
        
        # Set driver and executor Java options for compatibility
        java_info = get_java_version()
        if java_info and java_info[0] >= 11:
            # Add JVM options for Java 11+ compatibility
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
            conf.set("spark.driver.extraJavaOptions", java_opts_str)
            conf.set("spark.executor.extraJavaOptions", java_opts_str)
            
        spark = SparkSession.builder \
            .appName("JavaCompatibilityDemo") \
            .config(conf=conf) \
            .getOrCreate()
            
        print("✅ Spark session created successfully!")
        return spark
        
    except ImportError:
        print("❌ PySpark not installed. Install with: pip install pyspark")
        return None
    except Exception as e:
        print(f"❌ Failed to create Spark session: {str(e)}")
        return None


def demo_pyspark_usage(spark):
    """
    Demonstrate basic PySpark usage.
    """
    if not spark:
        return
        
    try:
        # Create a simple DataFrame
        data = [("Alice", 25), ("Bob", 30), ("Charlie", 35)]
        columns = ["name", "age"]
        
        df = spark.createDataFrame(data, columns)
        
        print("\n📊 Demo DataFrame:")
        df.show()
        
        print("📈 DataFrame with age filter:")
        df.filter(df.age > 25).show()
        
        spark.stop()
        print("✅ Spark session stopped successfully")
        
    except Exception as e:
        print(f"❌ Error during PySpark demo: {str(e)}")


def main():
    """
    Main function to check Java compatibility and demonstrate PySpark usage.
    """
    print("🚀 PySpark Java Compatibility Checker")
    print("=" * 50)
    
    # Check Java compatibility
    if not check_java_compatibility():
        print("\n💡 To fix Java version issues:")
        print("   1. Install a compatible Java version (8, 11, or 17)")
        print("   2. Set JAVA_HOME environment variable")
        print("   3. Use a PySpark version compatible with your Java version")
        sys.exit(1)
    
    # Set JAVA_HOME if needed
    set_java_home_if_needed()
    
    print("\n🔧 Attempting to create Spark session...")
    spark = configure_spark_with_compatible_java()
    
    if spark:
        demo_pyspark_usage(spark)
    else:
        print("\n🔍 Troubleshooting tips:")
        print("   1. Ensure PySpark version matches your Java version")
        print("   2. Check if JAVA_HOME is set correctly")
        print("   3. Try using a different PySpark version:")
        print("      - Java 8: PySpark 2.x or 3.0-3.3")
        print("      - Java 11: PySpark 3.0+")
        print("      - Java 17: PySpark 3.3+")


if __name__ == "__main__":
    main()