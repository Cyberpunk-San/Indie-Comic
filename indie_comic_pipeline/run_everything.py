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

    result = sock.connect_ex(('localhost', 11434))

    sock.close()

    return result == 0

print("\nChecking dependencies...")

              

if not check_ollama():

    print("Error: Ollama daemon is not running.")

    print("   Please open a new terminal and run: ollama serve")

    print("   Then come back and run this script again.")

    sys.exit(1)

print("Ollama is running.")

                                                                         

print("\nChecking local LLM model...")

result = subprocess.run(["ollama", "list"], capture_output=True, text=True)

if "llama3.2" not in result.stdout:

    print("Warning: Llama 3.2 model not found locally. Triggering Ollama download...")

    subprocess.run(["ollama", "pull", "llama3.2"])

print("Llama 3.2 is available.")

                                                            

print("\n" + "=" * 70)

print("STEP 1: Running LangChain Pipeline")

print("=" * 70)

os.chdir("langchain_code")

result = subprocess.run([sys.executable, "run_full_pipeline.py"])

if result.returncode != 0:

    print("Error: LangChain pipeline step failed.")

    sys.exit(1)

                                                     

print("\n" + "=" * 70)

print("STEP 2: Verifying GPU/CUDA environments for SDXL")

print("=" * 70)

os.chdir("..")

            

import torch

if not torch.cuda.is_available():

    print("Warning: CUDA acceleration is not active. SDXL running on CPU will be extremely slow.")

    response = input("Continue anyway? (y/n): ")

    if response.lower() != 'y':

        print("Exiting...")

        sys.exit(0)

                                                          

print("\n" + "=" * 70)

print("STEP 3: Executing SDXL Image Generation Pipeline")

print("=" * 70)

os.chdir("sdxl_code")

result = subprocess.run([sys.executable, "run_sdxl_pipeline.py"])

if result.returncode != 0:

    print("Error: SDXL pipeline step failed.")

    sys.exit(1)

                                       

print("\n" + "=" * 70)

print("MASTER PIPELINE COMPLETE")

print("=" * 70)

elapsed_time = time.time() - start_time

print(f"\nTotal elapsed time: {elapsed_time:.2f} seconds")

print("\nOutput files:")

print("   Character: outputs/characters/character_reference.png")

print("   Components: outputs/comics/component_1.png through component_N.png")

print("   Component Sheet: outputs/comics/component_sheet_horizontal.png and component_sheet_grid_2x2.png")

print("\nDONE")

print("=" * 70)

