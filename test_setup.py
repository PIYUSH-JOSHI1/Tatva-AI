"""
Quick Setup Verification Script
Tests all dependencies and model files before running the app
"""
import sys
import os

def check_imports():
    """Check all required imports"""
    print("🔍 Checking Python packages...")
    
    packages = [
        ('streamlit', 'Streamlit'),
        ('pandas', 'Pandas'),
        ('numpy', 'NumPy'),
        ('plotly', 'Plotly'),
        ('cv2', 'OpenCV'),
        ('tensorflow', 'TensorFlow'),
        ('PIL', 'Pillow'),
        ('ultralytics', 'Ultralytics YOLO'),
    ]
    
    missing = []
    for module, name in packages:
        try:
            __import__(module)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ❌ {name} - MISSING")
            missing.append(name)
    
    return missing

def check_files():
    """Check all required files"""
    print("\n📁 Checking model files...")
    
    files = [
        ('Readmission_Model.pkl', '~3.6 MB'),
        ('models/keras_model.h5', '~2.4 MB'),
        ('models/labels.txt', 'Small'),
        ('yolov8n.pt', '~6.5 MB'),
        ('logo.jpeg', 'Small'),
    ]
    
    missing = []
    for filepath, size in files:
        if os.path.exists(filepath):
            actual_size = os.path.getsize(filepath) / (1024 * 1024)  # MB
            print(f"  ✅ {filepath} ({actual_size:.1f} MB)")
        else:
            print(f"  ❌ {filepath} - MISSING")
            missing.append(filepath)
    
    return missing

def check_secrets():
    """Check for secrets.toml"""
    print("\n🔐 Checking API configuration...")
    
    secrets_path = '.streamlit/secrets.toml'
    if os.path.exists(secrets_path):
        print(f"  ✅ {secrets_path} exists")
        return []
    else:
        print(f"  ⚠️  {secrets_path} - MISSING (Chatbot won't work)")
        print("     Create it with: [google]")
        print("                      api_key = 'YOUR_KEY'")
        return [secrets_path]

def main():
    print("="*60)
    print("🏥 Hospital Management System - Setup Verification")
    print("="*60)
    
    missing_packages = check_imports()
    missing_files = check_files()
    missing_secrets = check_secrets()
    
    print("\n" + "="*60)
    print("📊 SUMMARY")
    print("="*60)
    
    if not missing_packages and not missing_files:
        print("✅ All required packages and files are present!")
        if missing_secrets:
            print("⚠️  Chatbot requires API key configuration")
        print("\n🚀 Ready to run: streamlit run Hospital_Streamlit.py")
    else:
        print("❌ Setup incomplete:")
        if missing_packages:
            print(f"   Missing packages: {', '.join(missing_packages)}")
            print("   Run: pip install -r requirements.txt")
        if missing_files:
            print(f"   Missing files: {', '.join(missing_files)}")

if __name__ == "__main__":
    main()
