"""
STORY SETTING EXTRACTOR
Uses Ollama + Llama 3.2 to extract setting details from any story
No API key required - runs completely locally
"""

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

import json

import re

from langchain_ollama import ChatOllama

from langchain_core.output_parsers import StrOutputParser

from langchain_core.prompts import ChatPromptTemplate

print("=" * 70)

print("STORY SETTING EXTRACTOR - Parsing geographical settings")

print("=" * 70)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config_helper import load_settings, get_output_path

settings = load_settings()

langchain_settings = settings.get("langchain", {})

                                                                                       

print("\nConnecting to local Ollama server...")

llm = ChatOllama(

    model=langchain_settings.get("model", "llama3.2"),

    temperature=langchain_settings.get("temperature", 0.3),

    base_url=langchain_settings.get("ollama_url", "http://localhost:11434")

)

print(f"Connected to Ollama: {llm.model}")

def extract_story_setting(story_name):

    """Extract setting details from any story using local LLM"""

    

    prompt = ChatPromptTemplate.from_messages([

        ("system", """You are a setting analysis expert. Extract world details from any story.
        
        To prevent hallucinations and guarantee high-quality descriptive outputs, study the following example:
        
        Example Input: Wuthering Heights
        Example Output:
        {{
            "story_name": "Wuthering Heights",
            "era": "Victorian era, late 1700s-1800s",
            "location": "Yorkshire moors, England",
            "environment_description": "windswept moors, wild heather, stormy skies, isolated stone manor",
            "mood": "gothic, tragic, passionate, brooding",
            "color_palette": ["dark green", "grey", "brown", "muted purple", "stormy blue"],
            "visual_elements": ["stone walls", "graveyards", "storm clouds", "candles", "old books"],
            "lighting": "dim, candlelit, stormy natural light",
            "weather": "stormy, windy, foggy",
            "theme": "destructive passion, social class barriers, and obsessive cycles of revenge",
            "dialogue_style_and_tone": "Formal, dramatic, poetic, and archaic Victorian dialogue.",
            "cinematographic_visual_style": "High contrast, dark brooding shadows, wide shots of isolated landscapes, low key natural lighting.",
            "key_side_characters": [
                {{
                    "name": "Heathcliff",
                    "default_personality": "brooding, intense, vengeful, passionate yet cruel"
                }},
                {{
                    "name": "Catherine Earnshaw",
                    "default_personality": "spirited, volatile, rebellious, torn between status and love"
                }}
            ]
        }}
        
        Respond ONLY with valid JSON matching the exact schema above. No other text before or after:
        """),

        ("human", "Describe the setting of: {story}")

    ])

    

    chain = prompt | llm | StrOutputParser()

    

    try:

        response = chain.invoke({"story": story_name})

        json_match = re.search(r'\{.*\}', response, re.DOTALL)

        if json_match:

            setting = json.loads(json_match.group())

                               

            if 'theme' not in setting:

                setting['theme'] = "The struggle of survival and identity in a unique world."

            if 'dialogue_style_and_tone' not in setting:

                setting['dialogue_style_and_tone'] = "Authentic dialogue style suitable for the setting."

            if 'cinematographic_visual_style' not in setting:

                setting['cinematographic_visual_style'] = "Cinematic framing, atmospheric lighting, and distinct visual motifs."

            if 'key_side_characters' not in setting:

                setting['key_side_characters'] = [

                    {"name": "Local Companion", "default_personality": "Helpful, knowledgeable guide."},

                    {"name": "Local Adversary", "default_personality": "Hostile, suspicious of outsiders."}

                ]

            return setting

        else:

            raise ValueError("No JSON found")

    except Exception as e:

        print(f"Error: {e}")

        return fallback_story(story_name)

def fallback_story(story_name):

                                                                                   

    fallbacks = {

        "wuthering heights": {

            "story_name": "Wuthering Heights",

            "era": "Victorian era, late 1700s-1800s",

            "location": "Yorkshire moors, England",

            "environment_description": "windswept moors, wild heather, stormy skies, isolated stone manor",

            "mood": "gothic, tragic, passionate, brooding",

            "color_palette": ["dark green", "grey", "brown", "muted purple", "stormy blue"],

            "visual_elements": ["stone walls", "graveyards", "storm clouds", "candles", "old books"],

            "lighting": "dim, candlelit, stormy natural light",

            "weather": "stormy, windy, foggy",

            "theme": "destructive passion, social class barriers, and obsessive cycles of revenge",

            "dialogue_style_and_tone": "Formal, dramatic, poetic, and archaic Victorian dialogue.",

            "cinematographic_visual_style": "High contrast, dark brooding shadows, wide shots of isolated landscapes, low key natural lighting.",

            "key_side_characters": [

                {"name": "Heathcliff", "default_personality": "brooding, intense, vengeful, passionate yet cruel"},

                {"name": "Catherine Earnshaw", "default_personality": "spirited, volatile, rebellious, torn between status and love"}

            ]

        },

        "harry potter": {

            "story_name": "Harry Potter",

            "era": "1990s alternate magical",

            "location": "Hogwarts Castle, Scotland",

            "environment_description": "magical castle, moving staircases, forbidden forest, black lake",

            "mood": "magical, mysterious, adventurous",

            "color_palette": ["burgundy", "gold", "forest green", "dark brown"],

            "visual_elements": ["wands", "floating candles", "owls", "cauldrons", "house crests"],

            "lighting": "warm torchlight, magical glow",

            "weather": "variable, sometimes stormy",

            "theme": "the power of love, choice versus destiny, and overcoming darkness",

            "dialogue_style_and_tone": "Modern British English with magical terminology, school slang, and formal tones for authority figures.",

            "cinematographic_visual_style": "Warm, gold and amber tones inside Hogwarts, deep shadows in the forbidden forest, cinematic tracking shots, and magical particles.",

            "key_side_characters": [

                {"name": "Hermione Granger", "default_personality": "intellectual, rule-abiding, loyal, highly logical"},

                {"name": "Ron Weasley", "default_personality": "brave, humorous, loyal, occasionally insecure, strategic"}

            ]

        },

        "cyberpunk": {

            "story_name": "Cyberpunk",

            "era": "dystopian future",

            "location": "Night City, megacity",

            "environment_description": "neon-lit streets, flying cars, holographic ads, constant rain",

            "mood": "gritty, high-energy, dangerous",

            "color_palette": ["neon pink", "cyan", "purple", "black", "yellow"],

            "visual_elements": ["cyberware", "holograms", "drones", "neon signs", "flying cars"],

            "lighting": "neon glow, screen reflections",

            "weather": "constant rain, fog",

            "theme": "dehumanization by megacorporations, high tech low life, survival, and rebellion",

            "dialogue_style_and_tone": "Gritty street slang, cybernetic jargon, cynical one-liners, and formal corporate speak.",

            "cinematographic_visual_style": "High contrast neon-noir lighting, rain-slicked pavement reflections, low-angle tracking shots of skyscrapers, holographic glare, and cybernetic HUD overlays.",

            "key_side_characters": [

                {"name": "Johnny Silverhand", "default_personality": "rebellious, charismatic, cynical, anti-corporate rockerboy"},

                {"name": "Jackie Welles", "default_personality": "loyal, ambitious, warm-hearted, street-smart solo"}

            ]

        }

    }

    

    name_lower = story_name.lower()

    for key in fallbacks:

        if key in name_lower:

            return fallbacks[key]

    

    return {

        "story_name": story_name.title(),

        "era": "fantasy era",

        "location": "fantasy world",

        "environment_description": "beautiful landscape with unique features",

        "mood": "adventurous and mysterious",

        "color_palette": ["emerald green", "golden amber", "deep purple", "silver"],

        "visual_elements": ["ancient ruins", "magical crystals", "floating islands", "mystical creatures"],

        "lighting": "golden hour, magical glow",

        "weather": "pleasant, occasional mist",

        "theme": "light versus shadow, discovering ancient mysteries",

        "dialogue_style_and_tone": "Formal and archaic fantasy dialogue.",

        "cinematographic_visual_style": "Bright, colorful fantasy lighting, wide scenic landscape shots, and magical glows.",

        "key_side_characters": [

            {"name": "Elven Guide", "default_personality": "Wise, silent, knows the ancient paths."},

            {"name": "Goblin Thief", "default_personality": "Greedy, mischievous, but easily frightened."}

        ]

    }

                                                                                 

print("\n" + "=" * 70)

if len(sys.argv) > 1:

    story_name = sys.argv[1].strip()

    print(f"Using story/setting from command line argument: {story_name}")

else:

    if not sys.stdin.isatty():

        try:

            story_name = sys.stdin.readline().strip()

        except Exception:

            story_name = ""

        if not story_name:

            story_name = "Cyberpunk"

            print(f"Non-interactive mode: Using default story/setting '{story_name}'")

        else:

            print(f"Non-interactive mode: Read story/setting from stdin: '{story_name}'")

    else:

        story_name = input("Enter story/setting (e.g., Wuthering Heights, Harry Potter, Cyberpunk): ").strip()

print(f"\nAnalyzing setting: '{story_name}'...")

setting = extract_story_setting(story_name)

print("\nEXTRACTED SETTING:")

print("-" * 50)

print(f"Story: {setting['story_name']}")

print(f"Location: {setting['location']}")

print(f"Era: {setting['era']}")

print(f"Mood: {setting['mood']}")

print(f"Colors: {', '.join(setting['color_palette'])}")

print(f"Weather: {setting.get('weather', 'varies')}")

print(f"\nEnvironment: {setting['environment_description'][:100]}...")

                                                                    

fusion_dir = settings.get("outputs", {}).get("fusion_dir", "outputs/fusion")

output_path = get_output_path(fusion_dir, "story_setting.json")

with open(output_path, "w", encoding="utf-8") as f:

    json.dump(setting, f, indent=2)

print(f"\nSaved JSON configuration to: {output_path}")

print("=" * 70)

