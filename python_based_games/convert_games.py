import os
import re

# Dictionary mapping your filenames to Nice Display Names
# Note: Chess is excluded because it needs a backend server.
game_files = {
    'snake_game.py': 'Classic Snake',
    'mario_game.py': 'Super Mario Style',
    'craft_game.py': 'Termux Craft (Minecraft 2D)',
    'shooting_game.py': 'Neon Space Shooter',
    'vice_city_game.py': 'Vice City 3D (Open World)',
    'birds.py': 'Angry Birds Clone',
    '2048_game.py' : '2048 Game'
}

index_content = """
<!DOCTYPE html>
<html>
<head>
    <title>My Termux Games</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #222; color: #fff; text-align: center; padding: 20px; }
        h1 { color: #f1c40f; margin-bottom: 30px; }
        .game-container { max-width: 600px; margin: 0 auto; }
        .game-link { 
            display: block; background: #333; margin: 15px 0; padding: 20px; 
            text-decoration: none; color: white; border-radius: 10px; 
            border-left: 5px solid #2ecc71; transition: 0.3s;
            text-align: left; font-size: 18px; font-weight: bold;
        }
        .game-link:hover { background: #444; border-left-color: #f1c40f; transform: translateX(5px); }
        .note { font-size: 12px; color: #777; margin-top: 50px; }
    </style>
</head>
<body>
    <h1>🎮 My Game Collection</h1>
    <div class="game-container">
"""

print("--- Converting Games to HTML ---")

found_any = False

for py_file, display_name in game_files.items():
    if not os.path.exists(py_file):
        print(f"⚠️  Skipping {py_file} (File not found in folder)")
        continue

    with open(py_file, 'r') as f:
        content = f.read()

    # Regex to find the HTML content inside GAME_TEMPLATE or HTML_TEMPLATE
    match = re.search(r'(?:GAME|HTML)_TEMPLATE\s*=\s*"""(.*?)"""', content, re.DOTALL)
    
    if match:
        html_content = match.group(1)
        # Create a cleaner HTML filename (e.g., vice_city_game.py -> vice_city.html)
        html_filename = py_file.replace('_game.py', '').replace('.py', '') + '.html'
        
        with open(html_filename, 'w') as f:
            f.write(html_content)
            
        print(f"✅ Converted {py_file} -> {html_filename}")
        
        # Add to index.html
        index_content += f'<a href="{html_filename}" class="game-link">{display_name}</a>\n'
        found_any = True
    else:
        print(f"❌ Could not extract HTML from {py_file}")

index_content += """
    </div>
    <p class="note">Hosted on GitHub Pages</p>
</body></html>
"""

if found_any:
    with open('index.html', 'w') as f:
        f.write(index_content)
    print("\n✅ 'index.html' created successfully!")
else:
    print("\n⚠️  No games were converted. Check if you are running this script in the correct folder.")

