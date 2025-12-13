import os
import re

# 1. SETUP THE INDEX HTML HEADER
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
            display: flex; justify-content: space-between; align-items: center;
        }
        .game-link:hover { background: #444; border-left-color: #f1c40f; transform: translateX(5px); }
        .arrow { color: #777; }
        .note { font-size: 12px; color: #777; margin-top: 50px; }
    </style>
</head>
<body>
    <h1>🎮 My Game Collection</h1>
    <div class="game-container">
"""

print("--- 🔄 Auto-Detecting and Converting Games ---")

# 2. SCAN FOLDER FOR ALL PYTHON FILES
files = [f for f in os.listdir('.') if f.endswith('.py')]
files.sort() # Sort alphabetically

count = 0

for py_file in files:
    # Skip this script itself
    if py_file == "convert_games.py":
        continue

    with open(py_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 3. LOOK FOR THE HTML TEMPLATE
    # We allow GAME_TEMPLATE, HTML_TEMPLATE, or just TEMPLATE
    match = re.search(r'(?:GAME|HTML)?_?TEMPLATE\s*=\s*"""(.*?)"""', content, re.DOTALL)
    
    if match:
        html_content = match.group(1)
        
        # Determine new filename (e.g., snake_game.py -> snake_game.html)
        html_filename = py_file.replace('.py', '.html')
        
        # Generate a nice display name
        # 1. Remove .py
        # 2. Replace underscores with spaces
        # 3. Capitalize every word
        display_name = py_file.replace('.py', '').replace('_', ' ').title()
        
        # Special fix for specific names if you want them prettier
        display_name = display_name.replace("Game", "").strip() # Remove redundant "Game"
        if display_name == "Game 2048": display_name = "2048 Puzzle"

        # Write the HTML file
        with open(html_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        print(f"✅ Found & Converted: {display_name} ({html_filename})")
        
        # Add to index
        index_content += f'<a href="{html_filename}" class="game-link"><span>{display_name}</span> <span class="arrow">▶</span></a>\n'
        count += 1
    else:
        # File exists but has no HTML template (likely a utility script or chess_game.py)
        print(f"⚠️  Skipped {py_file} (No HTML template found)")

# 4. FINISH INDEX HTML
index_content += """
    </div>
    <p class="note">Hosted on GitHub Pages • Auto-Generated</p>
</body></html>
"""

if count > 0:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(index_content)
    print(f"\n🎉 Success! {count} games added to index.html.")
else:
    print("\n❌ No compatible game files found.")

