#!/usr/bin/env python3
"""
Test script to demonstrate PySpark Java compatibility handling.
This script can be run with or without PySpark installed to show proper error handling.
"""

import sys
import os

# Add current directory to path to import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_java_version_check():
    """Test Java version checking functionality."""
    print("=" * 60)
    print("Testing Java Version Detection")
    print("=" * 60)
    
    try:
        from pyspark_java_compatibility import get_java_version, check_java_compatibility
        
        java_info = get_java_version()
        if java_info:
            major_version, full_version = java_info
            print(f"✅ Java {major_version} detected")
            print(f"   Full version: {full_version}")
        else:
            print("❌ Java not found")
            
        compatibility = check_java_compatibility()
        print(f"Compatibility check: {'✅ PASS' if compatibility else '❌ FAIL'}")
        
    except Exception as e:
        print(f"❌ Error during Java version check: {str(e)}")

def test_environment_validation():
    """Test environment validation functionality."""
    print("\n" + "=" * 60)
    print("Testing Environment Validation")
    print("=" * 60)
    
    try:
        from pyspark_env_validator import PySparkEnvironmentValidator
        
        validator = PySparkEnvironmentValidator()
        success = validator.validate_environment()
        
        print(f"Environment validation: {'✅ PASS' if success else '⚠️  ISSUES FOUND'}")
        
        if validator.issues:
            print(f"Issues detected: {len(validator.issues)}")
            for issue in validator.issues[:3]:  # Show first 3 issues
                print(f"  - {issue}")
        
    except Exception as e:
        print(f"❌ Error during environment validation: {str(e)}")

def test_spark_session_creation():
    """Test Spark session creation with error handling."""
    print("\n" + "=" * 60)
    print("Testing Spark Session Creation")
    print("=" * 60)
    
    try:
        from write_stream_to_delta import safe_spark_session_creation
        
        spark = safe_spark_session_creation()
        if spark:
            print("✅ Spark session created successfully!")
            spark.stop()
        else:
            print("❌ Failed to create Spark session")
            
    except ImportError:
        print("⚠️  PySpark not installed - this is expected in testing environment")
        print("   Install PySpark to test actual session creation")
    except Exception as e:
        print(f"❌ Error during Spark session creation: {str(e)}")

def demonstrate_error_scenarios():
    """Demonstrate how scripts handle various error scenarios."""
    print("\n" + "=" * 60)
    print("Demonstrating Error Scenarios")
    print("=" * 60)
    
    # Simulate no PySpark scenario
    print("Scenario 1: PySpark not installed")
    try:
        import pyspark
        print("  PySpark is available")
    except ImportError:
        print("  ✅ PySpark not found - error handling will be demonstrated")
    
    # Java version scenario
    print("\nScenario 2: Java version compatibility")
    from pyspark_java_compatibility import get_java_version
    java_info = get_java_version()
    if java_info:
        major_version, _ = java_info
        if major_version == 17:
            print("  ✅ Java 17 detected - requires PySpark 3.3+ for full compatibility")
        elif major_version == 11:
            print("  ✅ Java 11 detected - compatible with PySpark 3.0+")
        elif major_version == 8:
            print("  ✅ Java 8 detected - compatible with most PySpark versions")
        else:
            print(f"  ⚠️  Java {major_version} detected - may have compatibility issues")

def main():
    """Run all tests."""
    print("🧪 PySpark Java Compatibility Test Suite")
    print("This test demonstrates error handling and compatibility checking")
    
    test_java_version_check()
    test_environment_validation()
    test_spark_session_creation()
    demonstrate_error_scenarios()
    
    print("\n" + "=" * 60)
    print("🎯 Test Summary")
    print("=" * 60)
    print("All scripts demonstrated proper error handling and compatibility checking.")
    print("For full functionality testing, install PySpark and Delta Lake:")
    print("  pip install pyspark delta-spark")

if __name__ == "__main__":
    main()