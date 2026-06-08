"""
MASTER PIPELINE SCRIPT
Runs everything from character extraction to comic generation
"""

import subprocess

import sys

import os

import time

if sys.stdout.encoding != 'utf-8':

    try:

        sys.stdout.reconfigure(encoding='utf-8')

    except:

        pass

if sys.stderr.encoding != 'utf-8':

    try:

        sys.stderr.reconfigure(encoding='utf-8')

    except:

        pass

print("=" * 70)

print("INDIE COMIC GENERATOR - MASTER PIPELINE - Orchestrating multi-modal generation")

print("=" * 70)

start_time = time.time()

                                                                                 

def check_ollama():
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    result = sock.connect_ex(('localhost', 11434))
    sock.close()
    return result == 0

def ensure_ollama_running():
    import time
    import subprocess
    
    if check_ollama():
        print("Ollama is running.")
        return True
        
    print("⚠️ Ollama daemon is not running. Attempting to start Ollama automatically...")
    try:
        if sys.platform == "win32":
            CREATE_NO_WINDOW = 0x08000000
            subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=CREATE_NO_WINDOW)
        else:
            subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
        for attempt in range(15):
            time.sleep(1)
            if check_ollama():
                print("✅ Ollama server started and connected successfully!")
                return True
            print(f"   Waiting for Ollama to initialize... (attempt {attempt+1}/15)")
    except Exception as e:
        print(f"❌ Failed to auto-start Ollama: {e}")
        
    print("\nError: Ollama daemon is not running.")
    print("   Please make sure Ollama is installed and run 'ollama serve' in your terminal.")
    print("   Then come back and run this script again.")
    sys.exit(1)

print("\nChecking dependencies...")
ensure_ollama_running()

                                                                         

print("\nChecking local LLM model...")

result = subprocess.run(["ollama", "list"], capture_output=True, text=True)

if "llama3.2" not in result.stdout:

    print("Warning: Llama 3.2 model not found locally. Triggering Ollama download...")

    subprocess.run(["ollama", "pull", "llama3.2"])

print("Llama 3.2 is available.")

                                                            

print("\n" + "=" * 70)
print("STEP 1: Running Initial Parameters Extraction")
print("=" * 70)

os.chdir("langchain_code")
print("🎭 Step 1A: Running Character Personality Extractor...")
result = subprocess.run([sys.executable, "character_extractor.py"])
if result.returncode != 0:
    print("Error: Character extraction failed.")
    sys.exit(1)

print("\n🌍 Step 1B: Running Story Setting Extractor...")
result = subprocess.run([sys.executable, "story_extractor.py"])
if result.returncode != 0:
    print("Error: Story extraction failed.")
    sys.exit(1)
os.chdir("..")

print("\n" + "=" * 70)
print("STEP 2: Verifying GPU/CUDA environments")
print("=" * 70)

import torch
if not torch.cuda.is_available():
    print("Warning: CUDA acceleration is not active. Image generation will be extremely slow.")
    response = input("Continue anyway? (y/n): ")
    if response.lower() != 'y':
        print("Exiting...")
        sys.exit(0)

print("\n" + "=" * 70)
print("STEP 3: Image Generation Pipeline Configuration")
print("=" * 70)

print("Choose the image generation pipeline model to use:")
print("  1. SDXL Base Pipeline (Recommended)")
print("  2. Stable Diffusion v1.5 Pipeline")
print("  3. SDXL + LoRA Pipeline")
choice = input("Enter choice [1, 2, or 3, default is 1]: ").strip()
if not choice:
    choice = "1"

print("\nGenerate character sheet reference and component assets first? (y/n, default is y): ", end="")
gen_assets = input().strip().lower()
if gen_assets != 'n':
    print("\nExecuting Component Assets Generation...")
    if choice == '2':
        os.chdir("sd15_code")
        subprocess.run([sys.executable, "run_sd15_pipeline.py"])
    elif choice == '3':
        os.chdir("lora_code")
        subprocess.run([sys.executable, "run_lora_pipeline.py"])
    else:
        os.chdir("sdxl_code")
        subprocess.run([sys.executable, "run_sdxl_pipeline.py"])
    os.chdir("..")

print("\n" + "=" * 70)
print("STEP 4: Page-by-Page Storyboard and Panel Generation Loop")
print("=" * 70)

for page_num in range(1, 11):
    print(f"\n==========================================")
    print(f"🎬 PROCESSING PAGE {page_num} OF 10")
    print(f"==========================================")
    
    # 1. Run Fusion Engine for this page
    os.chdir("langchain_code")
    result = subprocess.run([sys.executable, "fusion_engine.py", "--page", str(page_num)])
    if result.returncode != 0:
        print(f"Error: Storyboard fusion failed for Page {page_num}.")
        sys.exit(1)
        
    # 2. Run Emotion Recognition Engine for this page
    result = subprocess.run([sys.executable, "emotion_recognition_engine.py", "--page", str(page_num)])
    if result.returncode != 0:
        print(f"Error: Emotion recognition failed for Page {page_num}.")
        sys.exit(1)
    os.chdir("..")
    
    # 3. Generate Panel Images for this page
    print(f"\n🎨 Drawing panels and compiling layout for Page {page_num}...")
    if choice == '2':
        os.chdir("sd15_code")
        result = subprocess.run([sys.executable, "generate_panels.py", "--page", str(page_num)])
    elif choice == '3':
        os.chdir("lora_code")
        result = subprocess.run([sys.executable, "generate_panels.py", "--page", str(page_num)])
    else:
        os.chdir("sdxl_code")
        result = subprocess.run([sys.executable, "generate_panels.py", "--page", str(page_num)])
    os.chdir("..")
    
    if result.returncode != 0:
        print(f"Error: Image generation failed for Page {page_num}.")
        sys.exit(1)
        
    print(f"\n✅ Page {page_num} completed successfully!")
    
    # Pause and prompt user
    if page_num < 10:
        val = input(f"\n[Press Enter to proceed to Page {page_num+1}, or type 'exit' to quit]: ").strip().lower()
        if val == 'exit':
            print("Exiting loop...")
            break

print("\n" + "=" * 70)
print("MASTER PIPELINE COMPLETE")
print("=" * 70)

elapsed_time = time.time() - start_time
print(f"\nTotal elapsed time: {elapsed_time:.2f} seconds")
print("\nDONE")
print("=" * 70)

