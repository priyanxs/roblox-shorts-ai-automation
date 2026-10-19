import os
import json
import random

BASE_DIR = "/Users/priyanxs/Downloads/automation"
HISTORY_FILE = os.path.join(BASE_DIR, "used_topics.json")

TOPICS = {
    "roblox": [
        {
            "category": "HORROR_LORE",
            "topic": "The Tragic Lore of Figure in DOORS",
            "angle": "Why Figure is completely blind and was once a normal human researcher trapped inside the hotel who mutated from the greenhouse toxins.",
            "hook": "Did you know the scariest monster in Roblox DOORS was actually human?",
            "voice": "en-US-ChristopherNeural"
        },
        {
            "category": "MYTHS_HACKERS",
            "topic": "The 2012 April Fools Hack That Broke Roblox",
            "angle": "How hackers took over the entire Roblox website in 2012, giving everyone infinite Robux, posting banned banners, and crashing the platform for 3 days.",
            "hook": "This is the single most terrifying day in Roblox history!",
            "voice": "en-US-GuyNeural"
        },
        {
            "category": "RARE_ECONOMY",
            "topic": "The 50 Million Robux Dominus Empyreus",
            "angle": "Only 9 exist in the entire universe. A single hat worth more than a real-life luxury mansion, and why its billionaire owners will never sell.",
            "hook": "This single Roblox hat is worth more than a real Lamborghini!",
            "voice": "en-US-ChristopherNeural"
        },
        {
            "category": "BLOX_FRUITS_SECRETS",
            "topic": "The Hidden Kitsune Shrine Sea Event",
            "angle": "How to spawn the secret Kitsune Island in Sea 3 during a full moon, collect 25 azure embers, and craft the legendary fox lamp weapon.",
            "hook": "Only 1% of Blox Fruits players know how to find the Kitsune Island!",
            "voice": "en-US-GuyNeural"
        },
        {
            "category": "BROOKHAVEN_CONSPIRACY",
            "topic": "The Secret Underground Agency in Brookhaven",
            "angle": "How to access the hidden Agency bunker under the cinema by flipping secret light switches and decoding the hidden wall numbers.",
            "hook": "Brookhaven has a dark secret hiding beneath the town cinema!",
            "voice": "en-US-ChristopherNeural"
        },
        {
            "category": "IMPOSSIBLE_OBBIES",
            "topic": "The 1000-Stage Tower of Hell Glitch Jump",
            "angle": "How pro speedrunners use a 60 FPS camera flick to wrap around 4.5 stud walls and skip entire sections without touching coils.",
            "hook": "Speedrunners use this illegal camera trick to beat any Roblox obby!",
            "voice": "en-US-GuyNeural"
        },
        {
            "category": "MYTHS_HACKERS",
            "topic": "The Legend of John Doe and March 18",
            "angle": "Why millions of players panicked on March 18th thinking account #2 was an evil hacker, but the truth was just an old testing bot.",
            "hook": "Remember when everyone thought John Doe would delete Roblox?",
            "voice": "en-US-GuyNeural"
        },
        {
            "category": "HORROR_LORE",
            "topic": "Apeirophobia Level 7 Collapse Secret",
            "angle": "The terrifying story of the endless ocean of ventilation shafts and how looking at the monster too long crashes your client.",
            "hook": "This Roblox horror game is so scary it was banned in 3 countries!",
            "voice": "en-US-ChristopherNeural"
        },
        {
            "category": "BEDWARS_BLADEBALL",
            "topic": "The Blade Ball Infinite Deflection Curve",
            "angle": "How pro players spin their sensitivity to 100 to curve the ball around blockers and hit 200 mph deflections.",
            "hook": "This impossible Blade Ball spin trick is completely undefeated!",
            "voice": "en-US-GuyNeural"
        },
        {
            "category": "RARE_ECONOMY",
            "topic": "The Deleted Account With 100 Rare Items",
            "angle": "The tragic story of Minish, one of the richest traders who got banned permanently, locking away millions in lost items forever.",
            "hook": "Roblox banned the richest player alive and locked away millions forever!",
            "voice": "en-US-ChristopherNeural"
        },
        {
            "category": "BLOX_FRUITS_SECRETS",
            "topic": "Awakening Dough V2 Without Getting Killed",
            "angle": "How using the Buddha glitch on Dough King allows solo players to dodge the spike barrage and unlock the deadliest PvP combos.",
            "hook": "Top Blox Fruits players use this secret trick to awaken Dough V2 effortlessly!",
            "voice": "en-US-GuyNeural"
        },
        {
            "category": "HORROR_LORE",
            "topic": "The Mimic Chapter 4 Book 2 Secret Ending",
            "angle": "The hidden Japanese folklore behind the blind witch Kintoru and how walking backward through the bamboo forest unlocks the true ending.",
            "hook": "The secret true ending of The Mimic will give you absolute nightmares!",
            "voice": "en-US-ChristopherNeural"
        },
        {
            "category": "MYTHS_HACKERS",
            "topic": "The 1x1x1x1 Legend Created By Roblox CEO",
            "angle": "How Telamon actually invented 1x1x1x1 as a fictional lore character for an official Roblox event, but players believed it was real for a decade.",
            "hook": "The truth about Roblox's most feared hacker 1x1x1x1 was an official lie!",
            "voice": "en-US-ChristopherNeural"
        },
        {
            "category": "BROOKHAVEN_CONSPIRACY",
            "topic": "The Abandoned Hospital Zombie Room in Brookhaven",
            "angle": "The secret code under the operating table that opens the basement lab where biohazard experiments took place before the town was built.",
            "hook": "There is a secret zombie bunker hidden inside Brookhaven hospital!",
            "voice": "en-US-GuyNeural"
        },
        {
            "category": "MURDER_MYSTERY_2",
            "topic": "The Nikilis Scythe and The Rarest Knife in MM2",
            "angle": "The story of the Nikilis Scythe, given only to the game creator, and how a developer glitch briefly gave it to a random player.",
            "hook": "Only one person in the world owns this impossible Murder Mystery 2 godly!",
            "voice": "en-US-ChristopherNeural"
        }
    ],
    "minecraft": [
        {
            "category": "PRO_SURVIVAL_TRICKS",
            "topic": "Mace + Wind Charge One-Shotting The Warden",
            "angle": "How falling from 50 blocks with the new heavy mace generates over 500 damage, instantly obliterating the Warden in a single hit.",
            "hook": "You can now one-shot the Warden in Minecraft with this insane combo!",
            "voice": "en-US-GuyNeural"
        },
        {
            "category": "DARK_LORE_CREEPYPASTA",
            "topic": "The Horrifying Secret Hidden Inside Disc 11",
            "angle": "When you put Disc 11 into a spectrograph, you can see a terrifying face and the player breathing heavily while running from an unknown beast.",
            "hook": "Mojang hid a terrifying secret inside Minecraft Music Disc 11!",
            "voice": "en-US-ChristopherNeural"
        },
        {
            "category": "ILLEGAL_GLITCHES",
            "topic": "Breaking The Nether Roof With Dark Oak Saplings",
            "angle": "How growing 4 dark oak saplings at bedrock level forces leaf blocks through indestructible bedrock, creating an instant escape.",
            "hook": "Mojang tried to patch this bedrock breaking glitch for 10 years!",
            "voice": "en-US-GuyNeural"
        },
        {
            "category": "MOB_PSYCHOLOGY",
            "topic": "Why Iron Golems Offer Poppies to Villagers",
            "angle": "Iron Golems are a tribute to the anime Castle in the Sky, showing that these brutal killing machines are actually gentle protectors.",
            "hook": "The real reason Iron Golems hand flowers to baby villagers will shock you!",
            "voice": "en-US-ChristopherNeural"
        },
        {
            "category": "ANCIENT_SECRETS",
            "topic": "The Deleted Ruby Dimension Notch Cancelled",
            "angle": "Before emeralds existed, rubies were fully coded into Minecraft, but Notch scrapped them because Dinnerbone was red-green colorblind.",
            "hook": "Minecraft almost replaced Emeralds with this deleted ancient gem!",
            "voice": "en-US-GuyNeural"
        },
        {
            "category": "SCARY_SEEDS",
            "topic": "The Corrupted Ancient City at Coordinate 0 0",
            "angle": "A rare world seed where an Ancient City spawned directly inside a lava ocean, creating an eerie glowing underworld.",
            "hook": "This is the single rarest and creepiest Minecraft seed ever found!",
            "voice": "en-US-ChristopherNeural"
        },
        {
            "category": "SPEEDRUNNER_HACKS",
            "topic": "Finding Bastions in 30 Seconds with F3 Pie Chart",
            "angle": "How speedrunners use Shift+F3 to read Minecraft's internal block entity pie chart and locate piglin bastions through solid walls.",
            "hook": "Speedrunners use this legal cheat code to find Nether Bastions instantly!",
            "voice": "en-US-GuyNeural"
        },
        {
            "category": "DARK_LORE_CREEPYPASTA",
            "topic": "The Origin of Herobrine in 2010",
            "angle": "The original 4chan post where a player in singleplayer saw another player staring back at him in the fog with no username.",
            "hook": "This is the real true story of how Herobrine was born!",
            "voice": "en-US-ChristopherNeural"
        },
        {
            "category": "REDSTONE_BLACK_MAGIC",
            "topic": "The Wireless Sculk Sensor Radio Transmitter",
            "angle": "How amethyst resonance frequencies allow wireless redstone signals across thousands of blocks with zero delay.",
            "hook": "You can now build wireless WiFi inside Minecraft without any mods!",
            "voice": "en-US-GuyNeural"
        },
        {
            "category": "ILLEGAL_GLITCHES",
            "topic": "The Invincible End Portal Wither Cage",
            "angle": "How spawning the Wither directly under the Bedrock fountain in the End traps it forever, giving you an infinite automatic obsidian farm.",
            "hook": "How to trap the Wither forever and get infinite free items!",
            "voice": "en-US-GuyNeural"
        },
        {
            "category": "MOB_PSYCHOLOGY",
            "topic": "Why Creepers Are Terrified of Cats",
            "angle": "Creepers are silent stalkers that fear being spotted. Cats have acute senses that detect Creepers before they explode, causing panic in their code.",
            "hook": "The shocking psychological reason why Creepers run away from cats!",
            "voice": "en-US-ChristopherNeural"
        },
        {
            "category": "ANCIENT_SECRETS",
            "topic": "The Secret Notch Apple Recipe Removed Forever",
            "angle": "Back in version 1.8, crafting an Enchanted Golden Apple required 8 blocks of solid gold. Mojang removed it to make hardcore survival brutal.",
            "hook": "Remember when you could craft this overpowered god item in Minecraft?",
            "voice": "en-US-GuyNeural"
        },
        {
            "category": "PRO_SURVIVAL_TRICKS",
            "topic": "Surviving 1000-Block Falls With Powder Snow",
            "angle": "How a single bucket of powder snow negates all kinetic fall damage in Minecraft, making water buckets completely obsolete.",
            "hook": "Stop using water buckets! This block cancels all fall damage 10x better!",
            "voice": "en-US-GuyNeural"
        },
        {
            "category": "DARK_LORE_CREEPYPASTA",
            "topic": "The Mystery of the Desert Well at Midnight",
            "angle": "Why desert wells spawn in the middle of nowhere with no structures around, and the eerie sound files that Mojang associated with them.",
            "hook": "The mysterious Desert Well in Minecraft hides a terrifying secret!",
            "voice": "en-US-ChristopherNeural"
        },
        {
            "category": "SPEEDRUNNER_HACKS",
            "topic": "The Blind Travel Portal Calculator Trick",
            "angle": "How entering a Nether Portal at specific coordinates mathematically guarantees you exit inside an End Portal stronghold in the Overworld.",
            "hook": "Speedrunners use this portal math trick to spawn directly at the End Portal!",
            "voice": "en-US-GuyNeural"
        }
    ]
}

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {"roblox": [], "minecraft": []}

def save_history(history):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2)

def get_next_topic(niche):
    history = load_history()
    niche_history = history.get(niche, [])
    pool = TOPICS.get(niche, [])
    
    # Exclude the last 10 used topics to ensure variety
    available = [t for t in pool if t["topic"] not in niche_history[-10:]]
    if not available:
        available = pool
        niche_history = []
        
    chosen = random.choice(available)
    niche_history.append(chosen["topic"])
    history[niche] = niche_history
    save_history(history)
    
    return chosen
