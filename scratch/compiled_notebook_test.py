
# --- CELL 0 ---
# ============================================================
# 0. Universal Cloud / Local Setup & GPU Acceleration Check
# ============================================================
import os
import sys
import torch

_IN_KAGGLE = os.path.exists("/kaggle/working")
_IN_CLOUD = _IN_KAGGLE

if _IN_CLOUD:
    print("[Kaggle] Detected Kaggle Environment. Setting up repo paths...")
    _repo = "/kaggle/working/Indie-Comic"
    if not os.path.exists(_repo):
        import subprocess
        subprocess.run(["git", "clone", "--depth", "1", "https://github.com/Cyberpunk-San/Indie-Comic.git", _repo], check=True)
    if _repo not in sys.path:
        sys.path.append(_repo)
    _pipeline_dir = os.path.join(_repo, "indie_comic_pipeline")
    if _pipeline_dir not in sys.path:
        sys.path.append(_pipeline_dir)
    setup_file = f"{_repo}/indie_comic_pipeline/colab_setup.py"
    if os.path.exists(setup_file):
        exec(open(setup_file).read(), globals())
else:
    print("[Env] Detected Local Jupyter / Python Environment.")
    if os.getcwd() not in sys.path:
        sys.path.append(os.getcwd())
    _local_pipe = os.path.join(os.getcwd(), "indie_comic_pipeline")
    if os.path.exists(_local_pipe) and _local_pipe not in sys.path:
        sys.path.append(_local_pipe)

# Verify CUDA GPU availability & TF32 acceleration
if torch.cuda.is_available():
    print(f"[GPU] GPU Detected: {torch.cuda.get_device_name(0)}")
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True
    try:
        torch.set_float32_matmul_precision('high')
    except Exception:
        pass
    DRY_RUN = False
else:
    print("[CPU] No CUDA GPU detected. Running in fast deterministic DRY-RUN mock mode.")
    DRY_RUN = True

# --- CELL 1 ---
# ============================================================
# 1. MDCP Master Pipeline & Attention Manager Configuration
# ============================================================
from integrated_pipeline import IntegratedComicPipeline
from core.advanced_attention import AdvancedAttentionManager
from core.layout_engine import MangaFlowLayoutEngine
from comic_exporter import ComicExporter
from PIL import Image

print("Initializing MDCP Master Pipeline...")
pipeline = IntegratedComicPipeline(dry_run=DRY_RUN, skip_backends=DRY_RUN)

# Configure output paths
output_dir = os.path.join(os.getcwd(), "outputs", "comics")
panels_dir = os.path.join(os.getcwd(), "outputs", "panels_50")
os.makedirs(output_dir, exist_ok=True)
os.makedirs(panels_dir, exist_ok=True)

pipeline.panels_dir = panels_dir
pipeline.panel_engine.output_dir = panels_dir
pipeline.text_integrator.output_dir = panels_dir

print("[OK] MDCP Pipeline initialized successfully!")

# --- CELL 2 ---
# ============================================================
# 2. Embedded 50-Beat High-Voltage Thriller Story Generator
# ============================================================

AUTO_STORY_PROMPT = "Cyberpunk Overdrive Saga: The Awakening of the Eclipse Blade"
AUTO_CHARACTER_NAME = "Kaelen Vane"
AUTO_STORY_WORLD = "Neo-Aethelgard Orbital Spire & Shattered Seabed"

# 50 Ultra-Detailed Dramatic Thriller Beats
DRAMATIC_50_BEATS = [
    # Act I – Re-entry & Planetary Siege (1-10)
    ("Orbital Drop", "Cybernetic warrior Kaelen Vane falls from low Earth orbit, atmospheric friction igniting fiery plasma trails around his armored chassis", "Entering atmosphere!", "extreme low-angle tilt", "blazing orange/fire red", "plummeting downward at Mach 25 engulfed in atmospheric friction flames"),
    ("Crater Impact", "Impact creates a colossal kilometer-wide crater, shattering city bedrock into soaring shockwave monoliths", "KABOOM!", "wide panoramic crater view", "smoldering ash & magma orange", "braced in center of crater with energy shockwaves radiating outward"),
    ("Swarm Awakening", "Ten thousand crimson optic combat mechs emerge from the dust rim, surrounding the impact zone", "Target located. Eliminate!", "high-angle wide vantage", "gunmetal grey & ominous red", "rising from crater dust as thousand laser targeting grids lock on"),
    ("Railgun Storm", "Hyper-velocity railgun slugs rain down, cutting through atmospheric dust in blue tracer arcs", "Bullet-time dodge!", "tracking bullet-time macro", "electric cyan & deep navy", "twisting torso in mid-air as railgun slugs pass within inches of visor"),
    ("Mach Sprint", "Kaelen ignites suit thrusters, sprinting faster than sound across crumbling concrete", "Too slow!", "kinetic side profile blur", "violet speed motion & neon blue", "sprinting horizontally with shockwave rings forming behind heels"),
    ("Facade Vertical Run", "Sprinting straight up the vertical glass wall of a 100-story skyscraper while windows implode", "Going vertical!", "extreme upward dutch angle", "glass shatter reflections & silver", "vertical sprint up glass building while pressure wave shatters facade"),
    ("Jet Cleave", "Leaping off the skyscraper peak and delivering a jet-assisted kick slicing an enemy gunship in two", "Slice!", "impact freeze-frame mid-air", "fiery explosion flare", "flying side-kick cleaving jet fuselage cleanly in half"),
    ("Missile Surfing", "Landing directly onto a supersonic cruise missile, riding it through dense flak cannon fire", "Riding the payload!", "over-shoulder aerial tracking", "smoke trail & stormy sky", "standing balanced on missile nose cone steering with magnetic boots"),
    ("Nuclear Burst Dive", "Backflipping through the radiant fireball of a tactical warhead, armored cape burning with plasma", "Clear the zone!", "wide nuclear silhouette", "blinding nuclear white & gold", "inverting body in mid-air against towering mushroom cloud"),
    ("Flagship Touchdown", "Crashing onto the flight deck of the colossal flagship Superion, armor cracking steel plates", "Touchdown.", "low-angle landing impact", "dark steel & electric sparks", "three-point superhero landing sending lightning arcs through deck"),

    # Act II – Total War & Colossus Rampage (11-20)
    ("Drone Swarm Storm", "Sky turns black as 50,000 kamikaze attack drones descend upon the flagship deck", "They just keep coming!", "extreme wide sky shot", "black swarm against violent storm", "drawing dual plasma katanas as sky darkens with drone cloud"),
    ("Blade Tempest", "Spinning into a 360-degree whirlwind of plasma slashes, bisecting hundreds of drones per second", "Whirlwind slash!", "radial action blur", "electric blue blade arcs", "blade tempest leaving cloud of cut drone debris and spark showers"),
    ("Gravity Rupture", "Gravitational field distorts, causing entire city quadrants to fold 90 degrees sideways", "Reality bending!", "dutch angle warping tilt", "twisted concrete & purple void", "leaning into gravitational vector as skyscrapers fold sideways around him"),
    ("Train Javelin", "Ripping a multi-ton maglev train off its rails and hurling it like a massive javelin", "Take this!", "dynamic full body heave", "metallic shine & electric arcs", "heaving maglev engine overhead with plasma energy pulsing in arms"),
    ("Titan Emergence", "A 300-meter gargantuan enemy Titan mech rises from the burning ocean horizon", "It's colossal!", "extreme worm-eye view", "dark silhouette against crimson sunset", "looking up from ground level at 300-meter mechanical leg stepping down"),
    ("Skyscraper Throw", "Gripping a 50-story building foundation and launching the entire structure into the Titan's chest", "Heads up!", "epic scale wide shot", "shattering glass & dust cloud", "ripping building foundation and hurling it straight at mech torso"),
    ("Beam Collision", "Chest energy reactor beam collides with Titan's laser, splitting the clouds above in half", "MAX POWER!", "center beam collision split", "blinding crimson & celestial gold", "bracing feet in crater as two massive energy beams lock in struggle"),
    ("Seabed Shockwave", "Impact shockwave parts the entire surrounding ocean, exposing raw ancient seabed", "Force ripple!", "extreme wide ocean panorama", "sea spray & deep ocean blue", "shockwave ring expanding outward pushing ocean wall 100 meters high"),
    ("Freefall Combat", "Brutal hand-to-hand combat while falling through 30,000 feet of cloud layers", "Claw for claw!", "vertical downward tracking", "cloud wisps & speed lines", "exchanging lightning fists with enemy champion while plummeting downward"),
    ("Planetary Faultline", "Titan slammed into the mantle, creating a new deep canyon rift across the continent", "IMPACT ZERO!", "satellite perspective", "cracked earth & fiery fissure", "smoke column rising from newly formed kilometer-deep continental fault"),

    # Act III – Chrono Rupture & Dimensional Void (21-30)
    ("Chrono Lock", "Time stops completely in mid-air, suspending falling raindrops and bullets like crystal spheres", "Chrono lock activated.", "macro static freeze-frame", "monochrome grayscale with vivid hero", "walking calmly past frozen bullet trails and mid-air explosion shrapnel"),
    ("Flash Afterimages", "Moving at hyper-speeds, creating a complete 360-degree ring of afterimages around the target", "Omnipresent!", "multi-shadow ring composition", "cyan afterimage trails", "speed afterimages surrounding bewildered enemy from all angles"),
    ("Infinite Legion", "Enemy replicates infinitely, forming an endless army covering the horizon", "We are infinite!", "extreme wide legion vista", "crimson eyes & dark steel", "countless identical enemy clones marching forward in locked formation"),
    ("Dimensional Portal Combat", "Slashes tear open space, fighting simultaneously across multiple dimensional rift portals", "Rift burst!", "split portal multi-pane", "dimensional purple & void gold", "punching through spatial rift and striking enemy in another dimension"),
    ("Stratosphere Upper-Cut", "Delivering a kinetic uppercut launching the enemy commander straight into orbit", "Up you go!", "upward tracking streak", "shockwave ring skyward", "uppercut launching enemy through upper atmosphere into space"),
    ("Orbital Array Duel", "Battling across solar panels of an orbital space station in zero-gravity with Earth below", "Zero-G duel!", "deep space view with Earth curve", "deep space black & blue Earth glow", "leaping between space station solar wings in zero gravity"),
    ("Meteor Re-Entry", "Catching a giant falling meteor and riding it back down toward Earth at re-entry velocity", "Riding the meteor!", "extreme descent tracking", "flaming meteor friction tail", "standing atop burning meteor surface driving it downward like a sled"),
    ("Lunar Cleave", "Enemy slash cuts a massive slice through the Moon, visible from Earth's surface", "The Moon... split!", "lunar space wide shot", "glowing white moon slash", "crescent moon splitting with glowing energy crack across lunar crust"),
    ("Debris Firestorm", "Glowing moon fragments rain down upon Earth in an apocalyptic meteor shower", "Rain of fire!", "global perspective view", "fiery streak trails", "giant lunar rock chunks falling through burning atmosphere"),
    ("Atmospheric Ignition", "The entire global atmosphere ignites into a swirling plasma storm canopy", "The sky is burning!", "horizon wide panorama", "swirling plasma violet & orange", "looking up at sky burning with electric plasma aurora waves"),

    # Act IV – Event Horizon & Dragon Titan Apocalypse (31-40)
    ("Black Hole Singularity", "An artificial black hole singularity opens above the shattered metropolis", "Event Horizon!", "vortex center composition", "pitch black core & light lensing", "gravitational lensing bending light around dark black singularity core"),
    ("City Upward Lift", "Entire city blocks are ripped from the ground and sucked upward into the singularity", "Metropolis lifted!", "vertical soaring wide shot", "shattered skyscrapers in gravity", "buildings and roads breaking apart floating up into gravitational core"),
    ("Mid-Air Rescue", "Sprinting across falling debris in mid-air to rescue falling civilians in an energy shield", "Got you all!", "multi-focus kinetic action", "golden aura glow & blue sky", "catching falling citizens in forcefield while dashing across debris"),
    ("Dragon Titan Unfold", "Enemy boss transforms into a colossal mechanical Dragon Titan of destruction", "Final mechanical evolution!", "epic low-angle creature reveal", "dark steel & glowing plasma scales", "robotic dragon roaring with massive wings unfolding across storm sky"),
    ("Dogfight Through Clouds", "Supersonic aerial combat weaving between the Dragon Titan's wings through lightning clouds", "Dogfight!", "kinetic aerial tracking", "cloud streaks & jet streams", "weaving between dragon's mechanical jaws in high-speed flight"),
    ("Lightning Bolt Capture", "Reaching into a thunderstorm with bare hand and catching a natural lightning bolt", "Hold the storm!", "high-contrast electric flash", "blinding electric blue & white", "hand grasping jagged lightning bolt as raw electricity arcs over armor"),
    ("Lightning Spear Throw", "Hurling the compressed lightning bolt like a javelin through the Dragon Titan's core", "SMITE!", "impact beam pass", "pure white lightning trail", "lightning spear piercing straight through Dragon Titan's chest reactor"),
    ("Mountain Range Crash", "Dragon Titan crashes into a mountain range, obliterating a granite peak into dust", "Crash landing!", "wide mountain impact", "rock dust explosion & ash", "dragon mech plowing through mountain peak sending boulders flying"),
    ("Magma Geyser Eruption", "Planetary crust ruptures, fountains of molten magma erupting from fissure trenches", "Planetary core rupture!", "magma landscape panorama", "molten orange & ash black", "lava erupting from subterranean cracks underfoot into night sky"),
    ("Cosmic Core Siphon", "Enemy boss absorbs planetary core energy into a radiant cosmic god form", "Absorbing planet core!", "cosmic energy halo", "blinding planetary core light", "boss floating in center of planet-wide energy siphon halo"),

    # Act V – Overdrive Zenith & Dimensional Slash Dawn (41-50)
    ("Extinction Beam", "Enemy fires a planetary beam so colossal it is visible from deep space", "Extinction Beam!", "deep space view of Earth", "golden energy beam in space", "colossal energy beam erupting from planet surface out into cosmos"),
    ("Barrier Energy Lock", "Hero's shield collides with the extinction beam, world shaking from raw force", "I will NOT fall!", "center clash explosion", "gold vs crimson shockwave", "pushing forward step-by-step against overwhelming energy column"),
    ("Memory Flash", "A serene one-second memory of why he fights flashes in warm peaceful light", "Remember why...", "soft nostalgic warm glow", "vivid warm memory highlight", "close-up of eyes reflecting quiet peaceful dawn memory"),
    ("Suit Overdrive 1000%", "Overclocking suit reactor beyond 1000% safety limit, energy veins bursting through armor", "OVERDRIVE 1000%!", "intense power aura close-up", "white-hot energy veins", "suit armor cracking as core glows with supernovic intensity"),
    ("Mach 1000 Strike", "Rockets forward at Mach 1000, slicing straight through the center of the extinction beam", "FINAL STRIKE!", "hyper-speed line motion", "blinding white kinetic streak", "single white streak cutting straight through enemy's giant beam"),
    ("Reality Fabric Tear", "Ultimate katana slash tears open the fabric of space-time itself", "Dimensional Slash!", "reality crack line", "cosmic void fracture", "space tearing along sword edge revealing starfield behind spatial tear"),
    ("Absolute Silence", "Sound cuts to complete silence, background instantly turning to pitch black", "...", "stark high-contrast silhouette", "pure black background with white rim", "frozen instant after slash, zero sound, absolute stillness"),
    ("Decisive Slash Mark", "Single gold slash line ignites across the enemy Titan's chest as sword is sheathed", "It is done.", "extreme close-up sword sheath", "single thin gold slash line", "sheathing blade click as golden line ignites across boss torso"),
    ("Gold Dust Disintegration", "Enemy Titan dissolves into millions of brilliant golden light motes floating into sky", "Disintegrating...", "dissolving particle effect", "glowing golden dust particles", "boss shattering into sparkling golden light drifting into sky"),
    ("Triumphant Dawn", "Kaelen stands victorious on the ruined skyscraper edge watching the peaceful sunrise", "The dawn of a new era.", "panoramic golden sunrise", "glowing golden morning sun", "hero standing on edge of ruined skyscraper facing rising golden sun"),
]

def build_50_panel_story_config():
    panels = []
    for idx in range(50):
        p_id = idx + 1
        beat_name, scene_desc, dialogue_text, camera_type, color_pal, action_mechanics = DRAMATIC_50_BEATS[idx]
        
        panels.append({
            "panel": p_id,
            "panel_id": p_id,
            "beat_name": beat_name,
            "emotion_beat": beat_name,
            "scene_description": f"{scene_desc}. Style: {AUTO_STORY_PROMPT}. Palette: {color_pal}.",
            "camera_angle": camera_type,
            "action_intensity": 0.6 + (p_id % 5) * 0.08,
            "characters": [
                {
                    "id": AUTO_CHARACTER_NAME.lower().replace(" ", "_"),
                    "name": AUTO_CHARACTER_NAME,
                    "pose": {
                        "body": f"{action_mechanics} in {AUTO_STORY_WORLD}",
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
                    "actor": AUTO_CHARACTER_NAME.lower().replace(" ", "_"),
                    "verb": beat_name,
                    "target": scene_desc,
                    "mechanics": action_mechanics,
                    "impact": f"Extreme thriller beat #{p_id:02d}: {beat_name}",
                    "reaction": f"Environmental shift in {color_pal}",
                    "timing": f"Frame #{p_id:02d} freeze moment"
                }
            ],
            "environment": {
                "location": AUTO_STORY_WORLD,
                "time": "dynamic progression",
                "dominant_color_palette": color_pal,
                "light_source": f"dramatic {color_pal} illumination"
            },
            "camera": f"{camera_type}, dramatic perspective"
        })
        
    return {
        "title": "Cyberpunk_50_Panel_Saga",
        "character_name": AUTO_CHARACTER_NAME,
        "story_world": AUTO_STORY_WORLD,
        "panels": panels,
        "recurring_motif": "glowing kinetic energy aura"
    }

story_config = build_50_panel_story_config()
print(f"[OK] Constructed 50-beat dramatic story configuration! ({len(story_config['panels'])} panels)")

# --- CELL 3 ---
# ============================================================
# 3. Execute 50-Panel MDCP Pipeline Loop
# ============================================================
print("[Run] Executing MDCP Pipeline Run for 50 dramatic panels...")
results = pipeline.run(
    prompt=AUTO_STORY_PROMPT,
    character_name=AUTO_CHARACTER_NAME,
    story_world=AUTO_STORY_WORLD,
    panel_count=50,
    _prebuilt_story=story_config,
    story_mode="literal"
)

generated_panels = results.get("panels", [])
print(f"[OK] Generated {len(generated_panels)} panel assets via MDCP framework!")

# --- CELL 4 ---
# ============================================================
# 4. MangaFlow High-Density Page Layout Assembly (2500x3750, 5x10 grid)
# ============================================================
layout_engine = MangaFlowLayoutEngine(
    page_width=2500,
    page_height=3750,
    gutter_width=16,
    margin=60,
    bg_color="white"
)
pipeline.layout_engine = layout_engine

print("[Layout] Assembling 50 panels onto single high-density comic page canvas...")
single_page_image = layout_engine.layout_page(
    panels=generated_panels,
    page_num=1,
    text_integrator=pipeline.text_integrator
)

page_output_path = os.path.join(output_dir, "single_page_50_panels.png")
single_page_image.save(page_output_path)
print(f"[OK] Saved High-Res Single-Page Canvas (2500x3750) to: {page_output_path}")

# Also save standard display scale (1000x1500)
display_img = single_page_image.resize((1000, 1500), Image.Resampling.LANCZOS)
display_path = os.path.join(output_dir, "single_page_50_panels_display.png")
display_img.save(display_path)
print(f"[OK] Saved Display Scale (1000x1500) to: {display_path}")

# --- CELL 5 ---
# ============================================================
# 5. Multi-Format Export (CBZ, PDF, Web HTML)
# ============================================================
exporter = ComicExporter(output_dir=output_dir)
page_record = [{"page_num": 1, "page_image": single_page_image, "panels": generated_panels}]

cbz_file = exporter.export_cbz(page_record, title="50_Panel_Comic_Special")
pdf_file = exporter.export_pdf(page_record, title="50_Panel_Comic_Special")
html_file = os.path.join(output_dir, "web_comic_50_panels.html")
exporter.export_web_comic(page_record, html_file)

print("=" * 80)
print("SUMMARY OF EXPORTED 50-PANEL ASSETS:")
print(f" - High-Res Canvas (2500x3750): {page_output_path}")
print(f" - Display Scale (1000x1500):  {display_path}")
print(f" - CBZ Archive:               {cbz_file}")
print(f" - PDF Document:              {pdf_file}")
print(f" - Web Reader HTML:           {html_file}")
print("=" * 80)

# --- CELL 6 ---
# ============================================================
# 6. Inline Jupyter Visualization
# ============================================================
from IPython.display import display

print("[Display] 50-Panel Single-Page Comic Layout:")
display(display_img)
