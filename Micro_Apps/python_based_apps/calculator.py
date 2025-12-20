from flask import Flask, render_template_string, request

app = Flask(__name__)

# This HTML string defines how the calculator looks in your browser
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Termux Python Calculator</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #222; margin: 0; }
        .calculator { background: #333; padding: 20px; border-radius: 15px; box-shadow: 0px 0px 20px rgba(0,0,0,0.5); }
        input[type="text"] { width: 100%; height: 50px; font-size: 24px; text-align: right; margin-bottom: 15px; border-radius: 5px; border: none; padding: 5px; box-sizing: border-box; }
        .buttons { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; }
        button { padding: 20px; font-size: 18px; border: none; border-radius: 5px; cursor: pointer; background: #555; color: white; }
        button:active { background: #777; }
        .operator { background: #f39c12; color: white; }
        .equal { background: #2ecc71; grid-column: span 2; }
        .clear { background: #e74c3c; grid-column: span 2; }
    </style>
</head>
<body>

<div class="calculator">
    <form method="POST">
        <input type="text" name="expression" value="{{ result }}" readonly>
        
        <div class="buttons">
            <button type="submit" name="btn" value="C" class="clear">C</button>
            <button type="submit" name="btn" value="/" class="operator">/</button>
            <button type="submit" name="btn" value="*" class="operator">&times;</button>
            
            <button type="submit" name="btn" value="7">7</button>
            <button type="submit" name="btn" value="8">8</button>
            <button type="submit" name="btn" value="9">9</button>
            <button type="submit" name="btn" value="-" class="operator">-</button>
            
            <button type="submit" name="btn" value="4">4</button>
            <button type="submit" name="btn" value="5">5</button>
            <button type="submit" name="btn" value="6">6</button>
            <button type="submit" name="btn" value="+" class="operator">+</button>
            
            <button type="submit" name="btn" value="1">1</button>
            <button type="submit" name="btn" value="2">2</button>
            <button type="submit" name="btn" value="3">3</button>
            <button type="submit" name="btn" value="=" class="equal">=</button>
            
            <button type="submit" name="btn" value="0" style="grid-column: span 2;">0</button>
            <button type="submit" name="btn" value=".">.</button>
        </div>
    </form>
</div>

</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    current_result = ""
    
    if request.method == 'POST':
        # Get the previous expression and the button pressed
        expression = request.form.get('expression', '')
        pressed = request.form.get('btn', '')

        if pressed == 'C':
            current_result = ""
        elif pressed == '=':
            try:
                # Provide a restricted scope for eval for safety
                allowed_names = {"abs": abs, "round": round}
                # Evaluate the python math expression
                current_result = str(eval(expression, {"__builtins__": None}, allowed_names))
            except Exception:
                current_result = "Error"
        else:
            # If the previous result was Error, clear it before adding new numbers
            if expression == "Error":
                current_result = pressed
            else:
                current_result = expression + pressed
                
    return render_template_string(HTML_TEMPLATE, result=current_result)

if __name__ == '__main__':
    # '0.0.0.0' allows you to access it from other devices on the same wifi if needed
    # Port 5000 is standard for Flask
    app.run(host='0.0.0.0', port=5000, debug=True)

