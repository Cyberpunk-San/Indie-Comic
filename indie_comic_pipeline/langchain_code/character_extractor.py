"""
CHARACTER PERSONALITY EXTRACTOR
Uses Ollama + Llama 3.2 to extract personality from any character name
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

print("CHARACTER PERSONALITY EXTRACTOR - Parsing human psyche")

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

def extract_character_personality(character_name):

    """Extract personality traits from any character using local LLM"""

    

    prompt = ChatPromptTemplate.from_messages([

        ("system", """You are a character analysis expert. Extract personality from ANY fictional character.
        
        To prevent hallucinations and guarantee high-quality descriptive outputs, study the following example:
        
        Example Input: Spider-Man
        Example Output:
        {{
            "character_name": "Spider-Man",
            "core_personality_traits": ["responsible", "witty", "self-sacrificing", "relatable", "persistent"],
            "values": ["protecting innocents", "family", "great power equals great responsibility"],
            "flaws": ["guilt complex", "struggles with double life", "financially insecure"],
            "behavioral_quirks": ["makes jokes when nervous", "talks to himself", "always late"],
            "emotional_range": ["hides fear behind humor", "shows determination"],
            "motivation": "to protect others because he couldn't save Uncle Ben",
            "catchphrase": "With great power comes great responsibility",
            "signature_colors": ["red", "blue"],
            "original_story_summary": "Peter Parker gets bitten by a radioactive spider, ignores his responsibility, leading to his uncle's death. He becomes a hero to make up for it.",
            "original_character_arc": "Starts as a selfish, nerdy kid. Shifts to a highly responsible, self-sacrificing protector of New York, learning to balance personal desires with hero duties."
        }}
        
        Respond ONLY with valid JSON matching the exact schema above. No other text before or after:
        """),

        ("human", "Extract personality for: {character}")

    ])

    

    chain = prompt | llm | StrOutputParser()

    

    try:

        response = chain.invoke({"character": character_name})

        

                                                                                      

        json_match = re.search(r'\{.*\}', response, re.DOTALL)

        if json_match:

            personality = json.loads(json_match.group())

                               

            if 'original_story_summary' not in personality:

                personality['original_story_summary'] = "Original hero origins and adventures."

            if 'original_character_arc' not in personality:

                personality['original_character_arc'] = "Starts as an amateur hero and matures into a seasoned protector."

            if 'signature_colors' not in personality:

                personality['signature_colors'] = ["red", "blue"]

            return personality

        else:

            raise ValueError("No JSON found")

            

    except Exception as e:

        print(f"Error: {e}")

        return fallback_character(character_name)

def fallback_character(character_name):

                                                                                            

    fallbacks = {

        "spiderman": {

            "character_name": "Spider-Man",

            "core_personality_traits": ["responsible", "witty", "self-sacrificing", "relatable", "persistent"],

            "values": ["protecting innocents", "family", "great power = great responsibility"],

            "flaws": ["guilt complex", "struggles with double life", "financially insecure"],

            "behavioral_quirks": ["makes jokes when nervous", "talks to himself", "always late"],

            "emotional_range": ["hides fear behind humor", "shows determination"],

            "motivation": "to protect others because he couldn't save Uncle Ben",

            "catchphrase": "With great power comes great responsibility",

            "signature_colors": ["red", "blue"],

            "original_story_summary": "Peter Parker gets bitten by a radioactive spider, ignores his responsibility, leading to his uncle's death. He becomes a hero to make up for it.",

            "original_character_arc": "Starts as a selfish, nerdy kid. Shifts to a highly responsible, self-sacrificing protector of New York, learning to balance personal desires with hero duties."

        },

        "batman": {

            "character_name": "Batman",

            "core_personality_traits": ["brooding", "strategic", "vengeful", "disciplined", "loner"],

            "values": ["justice", "order", "protecting Gotham", "no killing"],

            "flaws": ["paranoid", "distrustful", "emotionally closed off"],

            "behavioral_quirks": ["speaks in low growl", "works at night", "uses fear"],

            "emotional_range": ["hides all emotions", "shows anger"],

            "motivation": "to avenge his parents' death",

            "catchphrase": "I am vengeance",

            "signature_colors": ["black", "dark grey"],

            "original_story_summary": "Bruce Wayne witnesses his parents' murder as a child, traveling the world to train his mind and body to become the vigilante protector of Gotham City.",

            "original_character_arc": "Shifts from a vengeful orphan driven by rage to a self-disciplined symbol of justice who learns to rely on allies and trust others."

        }

    }

    

    name_lower = character_name.lower()

    for key in fallbacks:

        if key in name_lower:

            return fallbacks[key]

    

    return {

        "character_name": character_name.title(),

        "core_personality_traits": ["brave", "determined", "loyal", "resourceful", "compassionate"],

        "values": ["justice", "friendship", "freedom"],

        "flaws": ["stubborn", "sometimes reckless"],

        "behavioral_quirks": ["unique speech pattern"],

        "emotional_range": ["shows courage", "hides fear"],

        "motivation": "to do what's right",

        "catchphrase": "I'll do what's right",

        "signature_colors": ["primary color", "secondary color"],

        "original_story_summary": f"The original background story and origins of {character_name}.",

        "original_character_arc": f"The development path where {character_name} overcomes challenges and matures."

    }

                                                                   

print("\n" + "=" * 70)

if len(sys.argv) > 1:

    character_name = sys.argv[1].strip()

    print(f"Using character from command line argument: {character_name}")

else:

    if not sys.stdin.isatty():

        try:

            character_name = sys.stdin.readline().strip()

        except Exception:

            character_name = ""

        if not character_name:

            character_name = "Spiderman"

            print(f"Non-interactive mode: Using default character '{character_name}'")

        else:

            print(f"Non-interactive mode: Read character from stdin: '{character_name}'")

    else:

        character_name = input("Enter character name (e.g., Spiderman, Batman, Wolverine): ").strip()

print(f"\nAnalyzing character: '{character_name}'...")

personality = extract_character_personality(character_name)

print("\nEXTRACTED PERSONALITY:")

print("-" * 50)

print(f"Name: {personality['character_name']}")

print(f"\nCore Traits: {', '.join(personality['core_personality_traits'])}")

print(f"Values: {', '.join(personality['values'])}")

print(f"Flaws: {', '.join(personality['flaws'])}")

print(f"Motivation: {personality['motivation']}")

if personality.get('catchphrase'):

    print(f"Catchphrase: {personality['catchphrase']}")

                                                                

fusion_dir = settings.get("outputs", {}).get("fusion_dir", "outputs/fusion")

output_path = get_output_path(fusion_dir, "character_personality.json")

with open(output_path, "w", encoding="utf-8") as f:

    json.dump(personality, f, indent=2)

print(f"\nSaved JSON configuration to: {output_path}")

print("=" * 70)

