"""
PROMPT OPTIMIZER
Enhances prompts for better image generation results
"""

import re

class PromptOptimizer:

    def __init__(self):

        self.style_boosters = {

            "indie": "clean minimalist line art, flat color palette, crisp outlines",

            "comic": "comic book style, cel-shaded, bold black inks",

            "clean": "tidy composition, geometric shapes, no sketchy lines",

            "hand_drawn": "hand-drawn illustration, organic lines, indie aesthetic"

        }

        

        self.negative_boosters = {

            "default": "photorealistic, 3d render, shading, gradients, blurry, messy lines",

            "line_art": "watercolor bleed, oil painting texture, impasto brush strokes",

            "color": "muddy colors, color bleeding, oversaturated"

        }

    

    def optimize_positive_prompt(self, prompt, style="indie"):

        """Add style boosters to positive prompt"""

        style_booster = self.style_boosters.get(style, self.style_boosters["indie"])

        

                                

        optimized = f"{style_booster}, {prompt}"

        

                                                             

        optimized = re.sub(r'(oversized|yellow|hoodie|scar)', r'(\1)', optimized)

        

        return optimized

    

    def optimize_negative_prompt(self, base_negative=None):

        """Build comprehensive negative prompt"""

        negatives = [

            self.negative_boosters["default"],

            self.negative_boosters["line_art"],

            self.negative_boosters["color"]

        ]

        

        if base_negative:

            negatives.append(base_negative)

        

        return ", ".join(negatives)

    

    def add_consistency_constraints(self, prompt, character_name):

        """Add constraints for character consistency"""

        return f"{prompt}, consistent {character_name}"

    

    def build_scene_prompt(self, character_desc, action, background, mood, colors):

        """Build a complete scene prompt from components"""

        prompt = f"""
{character_desc}

Action: {action}
Background: {background}
Mood: {mood}
Colors: {colors}

Clean indie comic style, flat colors, crisp outlines, no gradients.
"""

        return self.optimize_positive_prompt(prompt)

def get_prompt_optimizer():

    return PromptOptimizer()

