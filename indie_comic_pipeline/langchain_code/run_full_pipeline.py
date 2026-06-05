"""
RUN FULL LANGCHAIN PIPELINE
Executes character extraction, story extraction, and fusion in sequence
"""

import subprocess

import sys

import os

print("=" * 70)

print("RUNNING FULL LANGCHAIN PIPELINE - Sequential LLM extraction")

print("=" * 70)

                                                                          

current_dir = os.path.dirname(os.path.abspath(__file__))

                                           

print("\n" + "=" * 70)

print("STEP 1/3: Character Personality Extraction")

print("=" * 70)

result = subprocess.run([sys.executable, "character_extractor.py"], cwd=current_dir)

if result.returncode != 0:

    print("Error: Character extraction failed")

    sys.exit(1)

                                                    

print("\n" + "=" * 70)

print("STEP 2/3: Story Setting Extraction")

print("=" * 70)

result = subprocess.run([sys.executable, "story_extractor.py"], cwd=current_dir)

if result.returncode != 0:

    print("Error: Story extraction failed")

    sys.exit(1)

                                                                   

print("\n" + "=" * 70)

print("STEP 3/3: Fusion Engine")

print("=" * 70)

result = subprocess.run([sys.executable, "fusion_engine.py"], cwd=current_dir)

if result.returncode != 0:

    print("Error: Fusion failed")

    sys.exit(1)

print("\n" + "=" * 70)

print("FULL PIPELINE COMPLETE")

print("=" * 70)

print("\nOutput files:")

print("   - ../outputs/fusion/character_personality.json")

print("   - ../outputs/fusion/story_setting.json")

print("   - ../outputs/fusion/fusion_complete.json")

print("   - ../outputs/fusion/sdxl_prompt.json")

print("\nNext: Run SDXL generation with:")

print("   python ../sdxl_code/generate_character.py")

print("=" * 70)

