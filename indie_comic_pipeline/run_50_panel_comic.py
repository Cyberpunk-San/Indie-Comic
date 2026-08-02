#!/usr/bin/env python
"""
50-PANEL HIGH-DENSITY SINGLE PAGE COMIC GENERATOR (MDCP-Powered)
==================================================================
Generates 50 distinct dramatic comic panel images using the core Multi-Level 
Diffusion Consistency Prior (MDCP) framework (IntegratedComicPipeline, AdvancedAttentionManager, 
PanelEngine, MangaFlowLayoutEngine, ComicExporter).

Features the extreme 50-beat action progression (Orbital Drop -> Impact -> Swarm -> Time Stop -> Black Hole -> Absolute Cinema Victory) arranged on a single high-density comic page canvas (2500x3750, 5x10 grid).
"""

import os
import sys
import time
import argparse
import logging
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
log = logging.getLogger("pipeline.run_50_panel")

from integrated_pipeline import IntegratedComicPipeline
from core.layout_engine import MangaFlowLayoutEngine
from core.text_image_integrator import TextImageIntegrator
from comic_exporter import ComicExporter


EXTREME_50_BEATS = [
    # Act I – Re-entry & Assault (1-10)
    ("Orbital Drop", "Hero crashes from orbit through burning atmosphere with fiery re-entry plasma", "Entering atmosphere!", "extreme low-angle tilt", "blazing orange/fire red", "plummeting downward engulfed in atmospheric friction flames"),
    ("Impact", "Creates a kilometer-wide crater as ground shatters into giant shockwave boulders", "Boom!", "wide panoramic crater", "smoldering ash & magma orange", "hero braced in center of massive smoking crater"),
    ("Awakening", "Enemy army of thousands of cyber-mechs already waiting around crater rim", "Surround the target!", "high-angle wide", "gunmetal grey & red eyes", "standing up in crater dust as thousands of red optics lock on"),
    ("Sniper Rain", "Hundreds of hyper-velocity railgun shots incoming from all directions", "Dodge!", "tracking bullet-time", "cyan energy tracer lines", "twisting torso in mid-air as railgun slugs streak past inches away"),
    ("Mach Sprint", "Hero runs faster than bullets, creating sonic boom shockwaves behind", "Too slow!", "kinetic side profile tracking", "violet speed motion blur", "sprinting horizontally at Mach 5 with feet barely touching ground"),
    ("Wall Run", "Hero runs vertically straight up a collapsing glass skyscraper", "Going up!", "extreme vertical tilt", "glass shatter reflections", "vertical sprint up glass facade while windows explode outward"),
    ("Jet Kick", "Hero kicks a flying supersonic enemy fighter jet clean in half", "Break!", "impact freeze-frame", "fiery explosion flare", "extended flying side-kick cleaving jet fuselage in half"),
    ("Missile Surf", "Hero surfs on the back of a soaring cruise missile through anti-air fire", "Ride it!", "over-shoulder aerial tracking", "smoke trail & cloud sky", "standing balanced on missile nose cone steering with boots"),
    ("Explosion Dive", "Hero backflips cleanly through a massive nuclear explosion fireball", "Clear skies!", "wide explosion silhouette", "blinding nuclear white & orange", "inverting body in mid-air backflip against mushroom cloud"),
    ("Landing", "Hero lands heavily onto the deck of the enemy colossal flagship", "Touchdown.", "low-angle landing impact", "dark steel & electric sparks", "three-point superhero landing cracking the armored deck plate"),

    # Act II – Total War (11-20)
    ("Swarm", "10,000 attack drones swarm the flagship simultaneously in a dark cloud", "They just keep coming!", "extreme wide sky shot", "black swarm against storm sky", "drawing dual plasma swords as sky fills with drone cloud"),
    ("Sword Storm", "Hero cuts hundreds of drones in seconds with a vortex of blade slashes", "Slash!", "radial action blur", "electric blue blade arcs", "spinning in 360-degree blade tempest leaving bisected drone parts"),
    ("Gravity Crush", "Gravity distorts as an entire city quadrant folds sideways in distortion field", "Reality bending!", "dutch angle warping tilt", "twisted concrete & purple warp", "leaning into gravitational tilt as buildings bend 90 degrees"),
    ("Train Throw", "Hero lifts a multi-ton magnetic bullet train and hurls it like a spear", "Catch this!", "dynamic full body angle", "metallic shine & electric arcs", "heaving train engine over head with veins pulsing in arms"),
    ("Titan Arrives", "A colossal 300-meter enemy Titan mech emerges from the burning horizon", "It's massive!", "extreme low-angle worm-eye view", "dark silhouette against fiery red", "looking up from ground level at 300m towering mech leg"),
    ("Building Throw", "Hero grips and throws a 50-story skyscraper directly at the Titan mech", "Heads up!", "epic scale wide shot", "shattering glass & dust cloud", "both hands ripping skyscraper foundation and tossing it forward"),
    ("Laser Clash", "Hero's chest beam collides with Titan's laser, splitting storm clouds above", "Power maxed!", "center beam collision split", "blinding crimson & gold flare", "bracing feet in crater as two massive energy beams lock together"),
    ("Shockwave", "Impact shockwave parts the entire ocean, revealing raw seabed below", "Force ripple!", "extreme wide ocean panorama", "sea spray & dark blue abyss", "shockwave ring expanding outwards pushing ocean water away"),
    ("Freefall Fight", "Brutal combat while falling several kilometers through upper cloud layer", "Claw for claw!", "vertical downward tracking", "cloud wisps & altitude lines", "exchanging rapid punches with enemy colossus while tumbling in freefall"),
    ("Ground Slam", "Titan slammed into Earth, creating a massive new canyon across the landscape", "Impact zero!", "high-altitude satellite view", "cracked earth & dust shockwave", "smoke column rising from newly formed kilometer-deep faultline"),

    # Act III – Impossible (21-30)
    ("Time Stop", "Everything freezes in mid-air except the hero, raindrops suspended like glass", "Chrono lock.", "macro static freeze-frame", "monochrome grayscale with color hero", "hero walking calmly past frozen bullets and mid-air explosion debris"),
    ("Flash Steps", "Hero creates thousands of glowing afterimages surrounding the enemy from all sides", "Omnipresent!", "multi-shadow ring composition", "cyan afterimage trails", "speed afterimages forming complete ring around stunned enemy"),
    ("Clone Army", "Enemy multiplies infinitely into a dark legion covering the horizon", "Infinite legion!", "extreme wide army vista", "crimson eyes legion", "countless identical enemy clones marching forward in locked formation"),
    ("Portal Combat", "Combat ruptures space, fighting across multiple dimensional portals at once", "Rift burst!", "split portal multi-pane", "dimensional purple/gold rifts", "punching through spatial rift and hitting enemy on other side"),
    ("Space Launch", "Hero delivers a punch so powerful it launches the enemy boss straight into orbit", "Up you go!", "upward tracking shot", "shockwave ring skyward", "uppercut launching enemy through stratosphere into space"),
    ("Orbital Chase", "Battle rages across satellite arrays in zero-gravity space above Earth", "Zero-G duel!", "orbital space view with Earth below", "deep space black & blue Earth curve", "leaping between solar panels of space station pursuing boss"),
    ("Meteor Ride", "Hero latches onto a giant falling meteor and rides it back down to Earth", "Re-entry speed!", "extreme descent tracking", "flaming meteor friction tail", "standing atop burning meteor surface driving it downward"),
    ("Moon Slice", "Enemy cuts part of the moon in half with an apocalyptic energy blade", "The moon... split!", "lunar space wide shot", "glowing white moon slash", "crescent moon splitting with glowing crack across lunar surface"),
    ("Debris Rain", "Massive glowing moon fragments bombard Earth in an apocalyptic meteor shower", "Rain of fire!", "global perspective view", "fiery streak trails", "giant lunar rock chunks falling through burning sky"),
    ("Sky Collapse", "The global atmosphere ignites into a canopy of swirling plasma storm", "The sky is burning!", "horizon panorama", "swirling plasma violet & orange", "looking up at sky burning with electric plasma aurora"),

    # Act IV – Apocalypse (31-40)
    ("Black Hole", "An artificial black hole singularity opens above the crumbling city", "Event horizon!", "vortex center composition", "black center & gravitational distortion", "gravitational lensing bending light around dark black core"),
    ("City Falling", "An entire metropolis is ripped from the ground and sucked upward into singularity", "City lifted!", "vertical soaring wide shot", "shattered skyscrapers in gravity", "buildings and roads breaking apart floating up into black hole"),
    ("Rescue", "Hero sprints in mid-air catching hundreds of falling civilians before impact", "Got you all!", "multi-focus kinetic action", "heroic aura glow", "catching civilians in energy field while dashing through air"),
    ("Dragon Mech", "Enemy transforms into a colossal mechanical dragon of destruction", "Final evolution!", "epic low angle creature reveal", "dark steel & glowing plasma scales", "robotic dragon roaring with mechanical wings unfolding"),
    ("Dogfight", "Supersonic aerial combat between hero and dragon mech through storm clouds", "Dogfight!", "kinetic aerial tracking", "cloud streaks & jet streams", "weaving between dragon's mechanical jaws in high-speed flight"),
    ("Lightning Grab", "Hero reaches up and catches a bolt of natural lightning with bare hand", "Hold the storm!", "high-contrast electric flash", "blinding electric blue & white", "hand grasping jagged lightning bolt as electricity arcs over suit"),
    ("Lightning Spear", "Hero hurls the compressed lightning bolt like a javelin through the dragon mech", "Smite!", "impact beam pass", "white lightning trail", "lightning spear piercing through dragon mech's chest core"),
    ("Dragon Crash", "Dragon mech crashes through mountain range, shattering peak into rubble", "Crash landing!", "wide mountain impact", "rock dust explosion", "dragon mech plowing through granite peak sending boulders flying"),
    ("Volcano Burst", "Ground erupts everywhere into fountains of molten lava and magma geysers", "Planetary rupture!", "magma landscape panorama", "molten orange & ash black", "lava erupting from subterranean cracks underfoot"),
    ("Final Form", "Enemy boss absorbs the planet's core energy into a radiant cosmic form", "Absorbing core!", "cosmic energy aura", "blinding planetary core light", "boss floating in center of planet-wide energy siphon halo"),

    # Act V – Absolute Cinema (41-50)
    ("Planet Beam", "Enemy fires a planetary beam so massive it's visible from deep space", "Extinction beam!", "deep space view of Earth", "golden beam shooting into space", "colossal energy beam erupting from Earth out into cosmos"),
    ("Energy Clash", "Hero's final barrier collides with planet beam, world shaking from force", "I won't fall!", "center clash explosion", "gold vs crimson shockwave", "hero pushing forward against overwhelming energy column"),
    ("Flashback", "One-second emotional memory of why hero fights flashes in peaceful light", "Remember why...", "soft nostalgic warm glow", "vivid warm memory highlight", "close-up of hero's eyes reflecting quiet peaceful dawn memory"),
    ("Last Charge", "Hero overclocks suit beyond 1000% safety limits, energy veins erupting", "OVERDRIVE!", "intense power aura close-up", "white-hot energy veins", "suit armor cracking as core glows with supernovic light"),
    ("Mach 1000", "Fastest attack yet, hero rockets forward at Mach 1000 cutting through beam", "Final Strike!", "hyper-speed line motion", "blinding white kinetic streak", "single streak cutting straight through enemy's giant beam"),
    ("Dimension Cut", "Hero's ultimate sword slash tears the fabric of reality itself open", "Dimensional Slash!", "reality crack line", "cosmic void fracture", "space tearing along sword edge revealing starfield behind tear"),
    ("Silence", "Everything goes completely quiet and silent, background fading to black", "...", "stark high-contrast silhouette", "pure black background with white rim", "frozen instant after slash, zero sound, absolute stillness"),
    ("One Strike", "Single decisive slash mark appears across the enemy colossus's chest", "It is done.", "extreme close-up sword sheath", "single thin gold slash line", "hero sheathing sword click as gold line ignites on boss"),
    ("Enemy Falls", "The enemy colossus disintegrates into millions of brilliant floating light motes", "Disintegration...", "dissolving particle effect", "glowing golden dust particles", "boss shattering into sparkling golden light drifting into sky"),
    ("Victory", "Hero stands triumphant on ruined skyline watching the peaceful sunrise", "The dawn.", "panoramic golden sunrise", "glowing golden morning sun", "hero standing on edge of ruined skyscraper facing rising sun")
]


def build_50_dramatic_story_config(
    story_prompt: str = "Extreme Cyberpunk Action Saga",
    character_name: str = "Wanderer",
    story_world: str = "Earth & Orbit Battlefield",
    custom_beats: list = None
) -> dict:
    """
    Decomposes a story into 50 distinct dramatic visual beats, ensuring each frame
    has a unique camera perspective, dramatic lighting, kinetic physical action,
    dialogue beat, and emotional intensity.
    """
    TOTAL_PANELS = 50

    if custom_beats and len(custom_beats) == TOTAL_PANELS:
        raw_beats = custom_beats
    else:
        raw_beats = EXTREME_50_BEATS

    panels = []
    for idx in range(TOTAL_PANELS):
        p_id = idx + 1
        beat_name, scene_desc, dialogue_text, camera_type, color_pal, action_mechanics = raw_beats[idx]
        
        panels.append({
            "panel": p_id,
            "panel_id": p_id,
            "beat_name": beat_name,
            "emotion_beat": beat_name,
            "scene_description": f"{scene_desc}. Style: {story_prompt}. Palette: {color_pal}.",
            "camera_angle": camera_type,
            "action_intensity": 0.5 + (p_id % 5) * 0.1,
            "characters": [
                {
                    "id": character_name.lower().replace(" ", "_"),
                    "name": character_name,
                    "pose": {
                        "body": f"{action_mechanics} in {story_world}",
                        "head": "facing focal point",
                        "arms": "in dynamic kinetic posture",
                        "legs": "braced for action"
                    },
                    "expression": {
                        "emotion": beat_name,
                        "eyes": "intense focused gaze",
                        "mouth": "set in firm determination"
                    },
                    "dialogue": {
                        "text": dialogue_text,
                        "tone": "dramatic",
                        "bubble": "speech"
                    }
                }
            ],
            "actions": [
                {
                    "actor": character_name.lower().replace(" ", "_"),
                    "verb": beat_name,
                    "target": scene_desc,
                    "mechanics": action_mechanics,
                    "impact": f"Extreme action beat #{p_id:02d}: {beat_name}",
                    "reaction": f"Environmental shift in {color_pal}",
                    "timing": f"Frame #{p_id:02d} freeze moment"
                }
            ],
            "environment": {
                "location": story_world,
                "time": "dynamic progression",
                "dominant_color_palette": color_pal,
                "light_source": f"dramatic {color_pal} illumination"
            },
            "camera": f"{camera_type}, dramatic perspective"
        })

    return {
        "title": story_prompt[:30].replace(" ", "_"),
        "character_name": character_name,
        "story_world": story_world,
        "panels": panels,
        "recurring_motif": "glowing kinetic energy aura"
    }


def run_50_panel_generation(
    prompt: str = "Extreme Cyberpunk Action Saga",
    character_name: str = "Wanderer",
    story_world: str = "Earth & Orbit Battlefield",
    dry_run: bool = False,
    custom_beats: list = None
) -> dict:
    """
    Executes the 50-panel high-density single page comic generator through the MDCP
    IntegratedComicPipeline system.
    """
    log.info("=" * 80)
    log.info("🚀 STARTING MDCP 50-PANEL SINGLE-PAGE HIGH-DENSITY COMIC GENERATOR")
    log.info(f"   Prompt: '{prompt}'")
    log.info(f"   Character: '{character_name}' | World: '{story_world}'")
    log.info(f"   Mode: {'DRY-RUN (Mock)' if dry_run else 'FULL RUN (GPU/MDCP)'}")
    log.info("=" * 80)

    output_dir = os.path.join(PROJECT_ROOT, "outputs", "comics")
    panels_dir = os.path.join(PROJECT_ROOT, "outputs", "panels_50")
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    Path(panels_dir).mkdir(parents=True, exist_ok=True)

    # 1. Initialize master integrated MDCP pipeline
    pipeline = IntegratedComicPipeline(dry_run=dry_run, skip_backends=dry_run)
    pipeline.panels_dir = panels_dir
    pipeline.panel_engine.output_dir = panels_dir
    pipeline.text_integrator.output_dir = panels_dir

    # 2. Build 50 dramatic beats story configuration
    story_config = build_50_dramatic_story_config(
        story_prompt=prompt,
        character_name=character_name,
        story_world=story_world,
        custom_beats=custom_beats
    )

    # 3. Configure MangaFlow layout engine for 2500x3750 single-page 50-panel canvas
    layout_engine = MangaFlowLayoutEngine(
        page_width=2500,
        page_height=3750,
        gutter_width=16,
        margin=60,
        bg_color="white"
    )
    pipeline.layout_engine = layout_engine

    # 4. Execute the MDCP pipeline run with pre-built dramatic story config
    log.info("Running MDCP pipeline execution loop for 50 dramatic panels...")
    results = pipeline.run(
        prompt=prompt,
        character_name=character_name,
        story_world=story_world,
        panel_count=50,
        _prebuilt_story=story_config,
        story_mode="literal"
    )

    generated_panels = results.get("panels", [])
    log.info(f"✅ Generated {len(generated_panels)} MDCP panel assets.")

    # 5. Assemble all 50 panels on a single page (5x10 grid)
    log.info("Assembling all 50 panels onto a single high-density comic page canvas (2500x3750, 5x10 grid)...")
    single_page_image = layout_engine.layout_page(
        panels=generated_panels,
        page_num=1,
        text_integrator=pipeline.text_integrator
    )

    # Save 50-panel high-density single page image
    page_output_path = os.path.join(output_dir, "single_page_50_panels.png")
    single_page_image.save(page_output_path)
    log.info(f"🎉 50-Panel Single-Page Comic saved to: {page_output_path}")

    # Also save standard display scale (1000x1500)
    display_img = single_page_image.resize((1000, 1500), Image.Resampling.LANCZOS)
    display_path = os.path.join(output_dir, "single_page_50_panels_display.png")
    display_img.save(display_path)
    log.info(f"🖼️ Display scale (1000x1500) saved to: {display_path}")

    # Export CBZ, PDF, and Web HTML
    exporter = ComicExporter(output_dir=output_dir)
    page_record = [{"page_num": 1, "page_image": single_page_image, "panels": generated_panels}]

    cbz_file = exporter.export_cbz(page_record, title="50_Panel_Comic_Special")
    pdf_file = exporter.export_pdf(page_record, title="50_Panel_Comic_Special")
    html_file = os.path.join(output_dir, "web_comic_50_panels.html")
    exporter.export_web_comic(page_record, html_file)

    log.info("=" * 80)
    log.info("SUMMARY OF EXPORTED MDCP 50-PANEL ASSETS:")
    log.info(f" - High-Res Page Image (2500x3750): {page_output_path}")
    log.info(f" - Display Page Image (1000x1500):  {display_path}")
    log.info(f" - CBZ Archive:                      {cbz_file}")
    log.info(f" - PDF Document:                     {pdf_file}")
    log.info(f" - Web HTML Reader:                  {html_file}")
    log.info("=" * 80)

    return {
        "page_image": single_page_image,
        "page_path": page_output_path,
        "display_path": display_path,
        "cbz_path": cbz_file,
        "pdf_path": pdf_file,
        "html_path": html_file,
        "panels": generated_panels
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="50-Panel Single-Page Comic Generator (MDCP)")
    parser.add_argument("--story", type=str, default="Extreme Cyberpunk Action Saga", help="Custom story prompt")
    parser.add_argument("--character", type=str, default="Wanderer", help="Character name")
    parser.add_argument("--world", type=str, default="Earth & Orbit Battlefield", help="Story world environment")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Run in dry-run mode (default: True)")
    parser.add_argument("--full-run", action="store_false", dest="dry_run", help="Run full GPU MDCP generation")

    args = parser.parse_args()
    run_50_panel_generation(
        prompt=args.story,
        character_name=args.character,
        story_world=args.world,
        dry_run=args.dry_run
    )
