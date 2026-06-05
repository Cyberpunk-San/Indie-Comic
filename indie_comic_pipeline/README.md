# Local AI Indie Comic Generator Pipeline

A local, multi-modal pipeline that takes a character name and a setting name, extracts character personality and story world parameters using a local LLM, dynamically plans 4 critical story components/assets (main character pose, secondary character, background environment, and key props), and renders consistent indie-comic-style assets using Stable Diffusion XL (SDXL).

---

## Architecture Overview

```
                                  +------------------------------------+
                                  | User Input: Character & Setting    |
                                  +------------------------------------+
                                                    |
                                                    v
                                  +------------------------------------+
                                  | LANGCHAIN EXTRACTION PHASE (LLM)   |
                                  | 1. character_extractor.py          |
                                  |    - Personality traits & values   |
                                  | 2. story_extractor.py              |
                                  |    - Era, mood, colors, weather    |
                                  +------------------------------------+
                                                    |
                                                    v
                                  +------------------------------------+
                                  | FUSION & COMPONENT PHASE (LLM)     |
                                  | 3. fusion_engine.py                |
                                  |    - Dynamic visual looks design   |
                                  |    - 4 Visual components & prompts |
                                  +------------------------------------+
                                                    |
                                                    v
                                  +------------------------------------+
                                  | SDXL IMAGE GENERATION PHASE        |
                                  | 4. generate_character.py           |
                                  |    - Renders reference character   |
                                  | 5. generate_components.py          |
                                  |    - Renders 4 separate assets     |
                                  |    - Assembles component sheets    |
                                  |    - Computes CV consistency       |
                                  +------------------------------------+
```

---

## How It Works

### Phase 1: Text & Storyboard Generation (LangChain + Ollama)
1. **Character Extractor**: Queries a local Llama 3.2 instance to extract psychological parameters (personality traits, values, flaws, motivations) from the character name. Visual looks are deliberately excluded in this step to keep the character's design flexible.
2. **Story Extractor**: Queries Llama 3.2 to extract the target world details (era, primary locations, mood, signature color palette, weathering, lighting).
3. **Fusion & Storyboarder**: Merges the character's personality with the setting. The LLM acts as a visual director, designing the character's outfit and style to match the setting, and planning exactly 4 story-specific components: a main character pose, a secondary character/extra person, a background environment (empty setting), and a key prop/item, along with detailed prompts for each.

### Phase 2: Visual rendering (Stable Diffusion XL)
1. **Prompt Optimizer**: Applies standard indie-comic modifiers (minimalist line-art, flat colors, crisp continuous outlines, cel-shaded details) to the LLM-generated prompts, and injects negative keywords to prevent realistic shading or 3D renders.
2. **Character Reference Generation**: Loads the designed visual looks and generates a master reference profile at 1024x1024.
3. **Component Generation**: Loads the story component prompts and loops over them using a Karras scheduler to render the individual visual assets.
4. **Component Compilation**: Glues the individual components into horizontal strips and 2x2 component sheet configurations.
5. **Consistency Checker**: Compares the colors (HSV histograms) and layouts (normalized cross-correlation of grayscale textures) of the main character pose component against the character reference profile, logging similarity percentages to check visual consistency.

---

## Getting Started

### Prerequisites
1. **Ollama**: Install from [Ollama.com](https://ollama.com) and verify Llama 3.2 is pulled:
   ```bash
   ollama pull llama3.2
   ```
2. **Python Environment**: Ensure you are running python in the provided virtual environment:
   ```bash
   .\venv\Scripts\activate
   ```
3. **Model Weights**: Ensure your SDXL model is placed in the designated directories or configured in `config/settings.yaml`.

---

## Execution Guide

### End-to-End Execution
To run the entire pipeline from start to finish, run the master orchestrator script from the root directory:
```bash
python run_everything.py
```

### Running Steps Manually

1. **Run the LangChain extractor pipeline**:
   ```bash
   python langchain_code/run_full_pipeline.py
   ```
   This will prompt you for the character and story setting name, query the local LLM, and output storyboard files into `outputs/fusion/`.

2. **Generate the character reference image**:
   ```bash
   python sdxl_code/generate_character.py
   ```

3. **Generate the visual component layouts**:
   ```bash
   python sdxl_code/generate_components.py
   ```
   This reads the story components, renders the asset images, compiles them into component sheets, and evaluates main character consistency.
