import subprocess
import time

print("🚀 Starting Bharat News Pipeline...")

steps = [
    ("Fetching News", "fetch_news.py"),         # Step 1
    ("Processing Data", "process_data_india.py"), # Step 2
    ("Launching Server", "app.py")             # Step 3
]

for name, script in steps:
    print(f"\n--- {name} ---")
    try:
        # 'check=True' stops the pipeline if a script crashes
        subprocess.run(["python", script], check=True)
    except subprocess.CalledProcessError:
        print(f"❌ Error in {name}. Stopping pipeline.")
        break
    except KeyboardInterrupt:
        print("\n🛑 Pipeline stopped by user.")
        break