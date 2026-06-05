"""
CHARACTER + STORY FUSION ENGINE (STORYBOARDER)
Combines personality and setting into visual character designs and a 4-panel storyboard script
"""

import json

import re

import sys

import os

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

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config_helper import load_settings, get_output_path

from langchain_ollama import ChatOllama

from langchain_core.output_parsers import StrOutputParser

from langchain_core.prompts import ChatPromptTemplate

print("=" * 70)

print("CHARACTER + STORY FUSION ENGINE (STORYBOARDER) - Fusing identity with space")

print("=" * 70)

settings = load_settings()

fusion_dir = settings.get("outputs", {}).get("fusion_dir", "outputs/fusion")

langchain_settings = settings.get("langchain", {})

print("\nLoading extracted parameters...")

char_path = get_output_path(fusion_dir, "character_personality.json")

story_path = get_output_path(fusion_dir, "story_setting.json")

with open(char_path, "r", encoding="utf-8") as f:

    personality = json.load(f)

with open(story_path, "r", encoding="utf-8") as f:

    setting = json.load(f)

print(f"Loaded configurations for: {personality['character_name']} + {setting['story_name']}")

print("\nConnecting to local Ollama server...")

llm = ChatOllama(

    model=langchain_settings.get("model", "llama3.2"),

    temperature=langchain_settings.get("temperature", 0.4),

    base_url=langchain_settings.get("ollama_url", "http://localhost:11434")

)

print(f"Connected to Ollama: {llm.model}")

def get_cosine_similarity(v1, v2):

    dot = np.dot(v1, v2)

    norm1 = np.linalg.norm(v1)

    norm2 = np.linalg.norm(v2)

    if norm1 > 0 and norm2 > 0:

        return dot / (norm1 * norm2)

    return 0.0

def run_vector_persistence_analysis(candidates, pages, model_name, base_url):

    print("\nRunning vector space persistence analysis...")

    try:

        from langchain_ollama import OllamaEmbeddings

        embeddings_model = OllamaEmbeddings(

            model=model_name,

            base_url=base_url

        )

        

                             

        candidate_texts = [f"{c['name']} {c['description']}" for c in candidates]

        print(f"Embedding {len(candidates)} candidate visual elements...")

        candidate_vecs = embeddings_model.embed_documents(candidate_texts)

        

                        

        page_texts = [f"{p['location']} {p['narrative_progression']}" for p in pages]

        print("Embedding 10 storyboard pages...")

        page_vecs = embeddings_model.embed_documents(page_texts)

        

                                                                        

        print("Clustering and de-duplicating candidates...")

        unique_indices = []

        for i in range(len(candidates)):

            is_duplicate = False

            for uj in unique_indices:

                sim = get_cosine_similarity(candidate_vecs[i], candidate_vecs[uj])

                if sim > 0.85:

                    is_duplicate = True

                    break

            if not is_duplicate:

                unique_indices.append(i)

                

        unique_candidates = [candidates[i] for i in unique_indices]

        unique_vecs = [candidate_vecs[i] for i in unique_indices]

        

                                           

        scored_candidates = []

        for i, c in enumerate(unique_candidates):

            c_vec = unique_vecs[i]

            similarities = []

            for p_vec in page_vecs:

                sim = get_cosine_similarity(c_vec, p_vec)

                similarities.append(sim)

                                                                      

            persistence_score = np.mean(similarities)

            scored_candidates.append((c, persistence_score))

            

                                              

        scored_candidates.sort(key=lambda x: x[1], reverse=True)

        print("\nPersistent Visual Components Ranked by Vector Space Score:")

        for idx, (c, score) in enumerate(scored_candidates):

            print(f"  {idx+1}. {c['name']} ({c['type']}) - Persistence: {score:.4f}")

            

                                                                                           

        selected_candidates = []

        for c, score in scored_candidates:

                                                                      

            if len(selected_candidates) < 3 or (score >= 0.22 and len(selected_candidates) < 5):

                selected_candidates.append(c)

                

                                          

        for idx, c in enumerate(selected_candidates):

            c['component_number'] = idx + 1

            

        return selected_candidates

        

    except Exception as e:

        print(f"Warning: Vector analysis failed ({e}). Falling back to LLM raw candidates order.")

        seen = set()

        selected_candidates = []

        for c in candidates:

            if c['name'].lower() not in seen:

                seen.add(c['name'].lower())

                selected_candidates.append(c)

            if len(selected_candidates) >= 4:

                break

        if len(selected_candidates) < 3:

            selected_candidates = candidates[:3]

        for idx, c in enumerate(selected_candidates):

            c['component_number'] = idx + 1

        return selected_candidates

def fuse_character_and_story(personality, setting):

    """Fuse character and story into a 10-page script and visual components list"""

    

    prompt = ChatPromptTemplate.from_messages([

        ("system", """You are an expert comic book narrative director, storyboard artist, and visual asset planner.
        
        Your task is to perform two tasks:
        1. Write a 10-page Multiverse Crossover Comic Book Script/Storyboard:
           - Page 1 to 10 must follow a chronological story arc where the main character is pulled from their original universe into a new setting.
           - Detail how the character's personality/mood adapts and shifts page-by-page.
           - The events must unfold in accordance with the target setting's theme.
           - Detail the side characters present on each page (adapted to multiverse versions of themselves).
        2. Identify candidate visual elements (characters, environments, props) mentioned in the 10-page script that would make important visual assets. For each, write a highly descriptive visual SDXL prompt (under 60 words) in the indie comic style (flat colors, clean minimalist line art, crisp outlines, no gradients).
        
        COLOR FUSION MANDATE: You must explicitly fuse the character's original signature colors with the target setting's color palette when designing the character's adapted look and any related visual components. In the "character_visual_looks" description and the SDXL prompts ("sdxl_prompt") for character components, you MUST explicitly specify these colors (e.g. Victorian crimson red and navy blue coat with dark green lining, or neon pink and cyan web-patterned jacket) to ensure Stable Diffusion renders them with the correct color schemes.

        AUTHENTIC VISUAL & DIALOGUE STYLE: In the 10-page storyboard script, you must write all dialogue, monologue, and captions in the exact tone, cadence, vocabulary, and style of the target setting's original dialogue (e.g., poetic archaic Victorian dialogue or cynical street-smart cyberpunk jargon). In the candidate visual SDXL prompts, you must write highly cinematic scene setups, framing, and lighting setups drawing direct inspiration from the target story's original cinematographic visualization (e.g. dramatic low-angle views of foggy landscapes, high-contrast neon-noir reflections in rain, etc.).

        To prevent hallucinations and guarantee high-quality descriptive results, follow this detailed example of fusing Spider-Man into Wuthering Heights:
        
        Example Input:
        CHARACTER: Spider-Man
        Core Personality: responsible, witty, self-sacrificing
        Values: protecting the innocent, great power equals great responsibility
        Original Story: Peter Parker becomes Spider-Man after failing to save Uncle Ben.
        Original Character Arc: Shifts from a selfish teenager to a selfless mature hero.
        Signature Colors: red, blue
        
        STORY WORLD: Wuthering Heights
        Location: Yorkshire moors, England
        Mood: gothic, brooding, tragic
        Color Palette: dark green, grey, brown, muted purple, stormy blue
        Theme: destructive obsession, revenge, class barriers
        Dialogue Style & Tone: Formal, dramatic, poetic, and archaic Victorian dialogue.
        Cinematographic Visual Style: High contrast, dark brooding shadows, wide shots of isolated landscapes, low key natural lighting.
        Key Side Characters: Heathcliff, Catherine
        
        Example Output:
        {{
            "character_visual_looks": "Spider-Man wearing a Victorian-era deep crimson red and dark navy blue woolen coat with dark green lining, a black webbed-pattern cloak, messy wind-blown hair, determined face, and gothic brass mechanical web-shooters.",
            "multiverse_adaptation_summary": "As he enters the gothic moors, his quick-witted optimism breaks down into brooding obsession, reflecting the gothic mood while the struggle for responsibility remains.",
            "storyboard_10_pages": [
                {{
                    "page_number": 1,
                    "location": "Yorkshire Moors Boundary",
                    "narrative_progression": "Spider-Man falls from a glowing portal onto the cold, dark Yorkshire Moors. He is disoriented as the stormy winds lash against his Victorian cloak.",
                    "personality_state": "Confused and disoriented, feeling the oppressive weight of the gothic environment.",
                    "side_characters_present": [],
                    "panels_breakdown": [
                        "Panel 1: A cosmic rift tearing open in the dark sky above lonely moors. Caption: 'This isn't Queens.'",
                        "Panel 2: Spider-Man kneeling on wet grass, shivering in the wind. Dialogue: 'Where's the skyline?'"
                    ],
                    "dialogue_and_captions": [
                        "Caption: I was swinging through Manhattan, and then... nothing but wind and heather.",
                        "Spider-Man: Great. My web-shooters won't do much good without skyscrapers."
                    ]
                }}
            ],
            "candidate_visual_elements": [
                {{
                    "name": "Spider-Man Crossover Pose",
                    "type": "character",
                    "description": "Spider-Man standing in a brooding crouch on an old stone wall, wearing his adapted Victorian crimson red and navy blue suit and black webbed cloak.",
                    "sdxl_prompt": "indie comic style illustration, clean minimalist line art, flat color palette, Spider-Man in Victorian crimson red and navy blue wool suit, black webbed cloak, crouching on stone wall, windswept dark moors, stormy sky, consistent Spider-Man"
                }},
                {{
                    "name": "Heathcliff Crossover",
                    "type": "character",
                    "description": "Heathcliff standing intensely, wearing a dark Victorian tailcoat, looking vengeful and brooding.",
                    "sdxl_prompt": "indie comic style illustration, clean minimalist line art, flat color palette, Heathcliff in dark Victorian tailcoat, brooding dark eyes, intense expression, standing near old stone gates, stormy grey sky"
                }},
                {{
                    "name": "Stormy Moors Landscape",
                    "type": "environment",
                    "description": "A desolate windswept moor under a dark, purple stormy sky, with ancient stone ruins and heather.",
                    "sdxl_prompt": "indie comic style background, clean minimalist line art, flat color palette, empty desolate Yorkshire moors, old stone ruins, wild heather, stormy purple clouds, no people"
                }}
            ]
        }}

        Respond ONLY with valid JSON matching the exact schema above. Do not add any text before or after the JSON:
        """),

        ("human", """
        CHARACTER: {character_name}
        Core Personality: {personality_traits}
        Values: {values}
        Flaws: {flaws}
        Motivation: {motivation}
        Original Story: {original_story_summary}
        Original Character Arc: {original_character_arc}
        Signature Colors: {signature_colors}
        
        STORY WORLD: {story_name}
        Era/Time Period: {era}
        Location: {location}
        Mood/Atmosphere: {mood}
        Color Palette: {color_palette}
        Visual Elements: {visual_elements}
        Lighting: {lighting}
        Weather: {weather}
        Theme: {theme}
        Dialogue Style & Tone: {dialogue_style_and_tone}
        Cinematographic Visual Style: {cinematographic_visual_style}
        Key Side Characters: {key_side_characters}
        """)

    ])

    

    chain = prompt | llm | StrOutputParser()

    

    try:

        response = chain.invoke({

            "character_name": personality['character_name'],

            "personality_traits": ', '.join(personality['core_personality_traits']),

            "values": ', '.join(personality['values']),

            "flaws": ', '.join(personality['flaws']),

            "motivation": personality['motivation'],

            "original_story_summary": personality['original_story_summary'],

            "original_character_arc": personality['original_character_arc'],

            "signature_colors": ', '.join(personality.get('signature_colors', ['red', 'blue'])),

            "story_name": setting['story_name'],

            "era": setting['era'],

            "location": setting['location'],

            "mood": setting['mood'],

            "color_palette": ', '.join(setting['color_palette']),

            "visual_elements": ', '.join(setting['visual_elements']),

            "lighting": setting['lighting'],

            "weather": setting.get('weather', 'varies'),

            "theme": setting['theme'],

            "dialogue_style_and_tone": setting.get('dialogue_style_and_tone', 'Authentic dialogue style suitable for the setting.'),

            "cinematographic_visual_style": setting.get('cinematographic_visual_style', 'Cinematic framing, atmospheric lighting, and distinct visual motifs.'),

            "key_side_characters": json.dumps(setting['key_side_characters'])

        })

        json_match = re.search(r'\{.*\}', response, re.DOTALL)

        if json_match:

            fusion = json.loads(json_match.group())

            return fusion

        else:

            raise ValueError("No JSON found")

    except Exception as e:

        print(f"Error during LLM fusion execution: {e}")

        return fallback_fusion(personality, setting)

def fallback_fusion(personality, setting):

    char_name = personality['character_name']

    story_name = setting['story_name']

    loc = setting['location']

    era = setting['era']

    mood = setting['mood']

    palette = ", ".join(setting['color_palette'][:3])

    sig_colors = ", ".join(personality.get('signature_colors', ['red', 'blue']))

    

    looks = f"{char_name} wearing an adapted costume suited for {era} aesthetics, fusing original signature colors ({sig_colors}) with the setting's color palette ({palette})."

    

                                       

    pages = []

    for p_num in range(1, 11):

        pages.append({

            "page_number": p_num,

            "location": loc,

            "narrative_progression": f"Page {p_num} showing {char_name} adapting to the {mood} theme of {story_name}.",

            "personality_state": f"Gradual shift matching page {p_num}.",

            "side_characters_present": [f"Local companion (page {p_num} state)"],

            "panels_breakdown": [f"Panel 1: {char_name} in scene {p_num}"],

            "dialogue_and_captions": [f"Caption: Page {p_num} in the crossover event."]

        })

        

    candidates = [

        {

            "name": f"{char_name} Crossover Pose",

            "type": "character",

            "description": f"{char_name} in an active pose reflecting {mood} style.",

            "sdxl_prompt": f"indie comic style illustration, clean minimalist line art, flat color palette, {looks}, consistent {char_name}"

        },

        {

            "name": "Local Companion",

            "type": "character",

            "description": f"A companion from {loc} adapted for the story.",

            "sdxl_prompt": f"indie comic style illustration, clean minimalist line art, flat color palette, secondary character, local of {loc}, consistent {char_name}"

        },

        {

            "name": f"{loc} Landscape",

            "type": "environment",

            "description": f"The landscape of {loc}.",

            "sdxl_prompt": f"indie comic style background illustration, clean minimalist line art, flat color palette, landscape of {loc}, no people"

        },

        {

            "name": "Setting Prop",

            "type": "prop",

            "description": "An important item from the world.",

            "sdxl_prompt": f"indie comic style illustration, clean minimalist line art, flat color palette, mysterious prop of {loc}, close up"

        }

    ]

    

    return {

        "character_visual_looks": looks,

        "multiverse_adaptation_summary": f"{char_name} blends into the {mood} setting of {story_name}.",

        "storyboard_10_pages": pages,

        "candidate_visual_elements": candidates

    }

print("\nSynthesizing crossover storyboard and candidates...")

fusion_result = fuse_character_and_story(personality, setting)

                                                                         

candidates_list = fusion_result.get("candidate_visual_elements", [])

pages_list = fusion_result.get("storyboard_10_pages", [])

import numpy as np

persistent_components = run_vector_persistence_analysis(

    candidates_list, 

    pages_list, 

    langchain_settings.get("model", "llama3.2"),

    langchain_settings.get("ollama_url", "http://localhost:11434")

)

                                                           

fusion_result["components"] = persistent_components

if "candidate_visual_elements" in fusion_result:

    del fusion_result["candidate_visual_elements"]

print("\nPERSISTENT COMPONENT ASSETS SELECTED:")

print("-" * 50)

for c in fusion_result["components"]:

    print(f"  Asset {c['component_number']} ({c['type']}): {c['name']}")

    print(f"    SDXL Prompt: {c['sdxl_prompt'][:60]}...")

                                                      

output_path = get_output_path(fusion_dir, "fusion_complete.json")

with open(output_path, "w", encoding="utf-8") as f:

    json.dump({

        "personality": personality,

        "setting": setting,

        "fusion": fusion_result

    }, f, indent=2)

print(f"\nSaved components configuration to: {output_path}")

                                                             

style_settings = settings.get("style", {})

negative_prompt = ", ".join(style_settings.get("negative_terms", [

    "photorealistic", "3D render", "shading", "gradients", "blurry", "messy lines"

]))

style_desc = ", ".join(style_settings.get("positive_terms", [

    "clean minimalist line art", "flat color palette", "crisp continuous outlines", "cel-shaded with no gradients"

]))

prompt_output = {

    "positive_prompt": fusion_result['character_visual_looks'],

    "negative_prompt": negative_prompt,

    "style": style_desc,

    "character_name": personality['character_name'],

    "story_world": setting['story_name']

}

sdxl_prompt_path = get_output_path(fusion_dir, "sdxl_prompt.json")

with open(sdxl_prompt_path, "w", encoding="utf-8") as f:

    json.dump(prompt_output, f, indent=2)

print(f"Saved SDXL prompt configuration to: {sdxl_prompt_path}")

print("=" * 70)

