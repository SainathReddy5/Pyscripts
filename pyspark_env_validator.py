#!/usr/bin/env python3
"""
PySpark Environment Setup and Validation Utility

This utility helps diagnose and fix common PySpark environment issues,
particularly Java version compatibility problems.
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class PySparkEnvironmentValidator:
    """Validates and fixes PySpark environment setup."""
    
    def __init__(self):
        self.issues = []
        self.fixes = []
        
    def check_java_installation(self) -> bool:
        """Check if Java is installed and get version info."""
        try:
            result = subprocess.run(['java', '-version'], 
                                  capture_output=True, text=True)
            
            if result.returncode != 0:
                self.issues.append("Java not found in PATH")
                self.fixes.append("Install Java from https://adoptium.net/")
                return False
                
            version_output = result.stderr
            print(f"☕ Java installation found:")
            print(f"   {version_output.strip()}")
            
            # Parse version
            import re
            version_match = re.search(r'"(\d+)\.(\d+)\.(\d+)', version_output)
            if version_match:
                major = int(version_match.group(1))
                if major == 1:  # Handle format like "1.8.0"
                    major = int(version_match.group(2))
                
                if major not in [8, 11, 17]:
                    self.issues.append(f"Java {major} may not be compatible with PySpark")
                    self.fixes.append("Install Java 8, 11, or 17 for best compatibility")
                    
                return True
            
            # Try newer version format
            version_match = re.search(r'"(\d+)', version_output)
            if version_match:
                major = int(version_match.group(1))
                if major not in [8, 11, 17]:
                    self.issues.append(f"Java {major} may not be compatible with PySpark")
                    self.fixes.append("Install Java 8, 11, or 17 for best compatibility")
                return True
                
        except FileNotFoundError:
            self.issues.append("Java not found")
            self.fixes.append("Install Java from https://adoptium.net/")
            return False
        except Exception as e:
            self.issues.append(f"Error checking Java: {str(e)}")
            return False
            
        return True
    
    def check_java_home(self) -> bool:
        """Check if JAVA_HOME is set correctly."""
        java_home = os.environ.get('JAVA_HOME')
        
        if not java_home:
            self.issues.append("JAVA_HOME environment variable not set")
            self.fixes.append("Set JAVA_HOME to your Java installation directory")
            return False
            
        java_home_path = Path(java_home)
        if not java_home_path.exists():
            self.issues.append(f"JAVA_HOME points to non-existent directory: {java_home}")
            self.fixes.append("Update JAVA_HOME to correct Java installation path")
            return False
            
        java_bin = java_home_path / "bin" / "java"
        if not java_bin.exists():
            java_bin = java_home_path / "bin" / "java.exe"  # Windows
            
        if not java_bin.exists():
            self.issues.append(f"Java executable not found in JAVA_HOME/bin")
            self.fixes.append("Verify JAVA_HOME points to a valid Java installation")
            return False
            
        print(f"☑️  JAVA_HOME is set to: {java_home}")
        return True
    
    def check_pyspark_installation(self) -> bool:
        """Check if PySpark is installed."""
        try:
            import pyspark
            version = pyspark.__version__
            print(f"🐍 PySpark {version} is installed")
            
            # Check version compatibility
            major_version = int(version.split('.')[0])
            if major_version < 3:
                self.issues.append(f"PySpark {version} is quite old")
                self.fixes.append("Consider upgrading to PySpark 3.x for better Java compatibility")
                
            return True
            
        except ImportError:
            self.issues.append("PySpark not installed")
            self.fixes.append("Install PySpark: pip install pyspark")
            return False
    
    def check_delta_lake(self) -> bool:
        """Check if Delta Lake is available."""
        try:
            import delta
            print(f"🔺 Delta Lake is available")
            return True
        except ImportError:
            self.issues.append("Delta Lake not installed")
            self.fixes.append("Install Delta Lake: pip install delta-spark")
            return False
    
    def test_spark_session_creation(self) -> bool:
        """Test if Spark session can be created."""
        try:
            from pyspark.sql import SparkSession
            
            builder = SparkSession.builder.appName("EnvironmentTest")
            
            # Add Java compatibility options
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
            
            spark = builder.getOrCreate()
            
            # Test basic operation
            data = [1, 2, 3, 4, 5]
            rdd = spark.sparkContext.parallelize(data)
            result = rdd.collect()
            
            spark.stop()
            
            print("✅ Spark session test passed")
            return True
            
        except Exception as e:
            error_str = str(e)
            self.issues.append(f"Spark session creation failed: {error_str}")
            
            if "UnsupportedClassVersionError" in error_str:
                self.fixes.append("Java version compatibility issue - install compatible Java version")
            elif "JAVA_GATEWAY_EXITED" in error_str:
                self.fixes.append("Java gateway issue - check JAVA_HOME and Java installation")
            else:
                self.fixes.append("Check PySpark installation and Java configuration")
                
            return False
    
    def generate_environment_report(self) -> Dict:
        """Generate a comprehensive environment report."""
        report = {
            "java_info": {},
            "python_info": {},
            "pyspark_info": {},
            "environment_vars": {},
            "issues": self.issues,
            "fixes": self.fixes
        }
        
        # Python info
        report["python_info"] = {
            "version": sys.version,
            "executable": sys.executable,
            "platform": sys.platform
        }
        
        # Java info
        try:
            result = subprocess.run(['java', '-version'], 
                                  capture_output=True, text=True)
            report["java_info"]["version_output"] = result.stderr.strip()
        except:
            report["java_info"]["version_output"] = "Not found"
        
        # Environment variables
        spark_vars = ['JAVA_HOME', 'SPARK_HOME', 'PYSPARK_PYTHON', 'PYSPARK_DRIVER_PYTHON']
        for var in spark_vars:
            report["environment_vars"][var] = os.environ.get(var, "Not set")
        
        # PySpark info
        try:
            import pyspark
            report["pyspark_info"]["version"] = pyspark.__version__
            report["pyspark_info"]["location"] = pyspark.__file__
        except ImportError:
            report["pyspark_info"]["status"] = "Not installed"
        
        return report
    
    def validate_environment(self) -> bool:
        """Run full environment validation."""
        print("🔍 PySpark Environment Validation")
        print("=" * 50)
        
        all_good = True
        
        # Check Java
        if not self.check_java_installation():
            all_good = False
        
        if not self.check_java_home():
            all_good = False
            
        # Check PySpark
        if not self.check_pyspark_installation():
            all_good = False
            
        # Check Delta Lake (optional)
        self.check_delta_lake()
        
        # Test Spark session
        if not self.test_spark_session_creation():
            all_good = False
        
        return all_good
    
    def print_summary(self):
        """Print validation summary."""
        print("\n" + "=" * 50)
        print("📋 VALIDATION SUMMARY")
        print("=" * 50)
        
        if not self.issues:
            print("✅ No issues found! Your PySpark environment is ready.")
        else:
            print("❌ Issues found:")
            for i, issue in enumerate(self.issues, 1):
                print(f"   {i}. {issue}")
                
            print("\n💡 Suggested fixes:")
            for i, fix in enumerate(self.fixes, 1):
                print(f"   {i}. {fix}")
    
    def auto_fix_java_home(self):
        """Attempt to automatically set JAVA_HOME."""
        if os.environ.get('JAVA_HOME'):
            return  # Already set
            
        try:
            # Try to find Java home automatically
            result = subprocess.run(['java', '-XshowSettings:properties', '-version'], 
                                  capture_output=True, text=True)
            
            for line in result.stderr.split('\n'):
                if 'java.home' in line:
                    java_home = line.split('=')[1].strip()
                    os.environ['JAVA_HOME'] = java_home
                    print(f"🔧 Automatically set JAVA_HOME to: {java_home}")
                    break
        except:
            pass


def main():
    """Main function for environment validation."""
    validator = PySparkEnvironmentValidator()
    
    # Try to auto-fix JAVA_HOME
    validator.auto_fix_java_home()
    
    # Run validation
    success = validator.validate_environment()
    
    # Print summary
    validator.print_summary()
    
    # Generate detailed report
    report = validator.generate_environment_report()
    
    # Save report to file
    report_file = "/tmp/pyspark_environment_report.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Detailed report saved to: {report_file}")
    
    if success:
        print("\n🎉 Environment validation successful!")
        sys.exit(0)
    else:
        print("\n⚠️  Environment validation failed. Please address the issues above.")
        sys.exit(1)


if __name__ == "__main__":
    main()