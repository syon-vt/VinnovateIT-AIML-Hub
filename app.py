from flask import Flask, render_template, request, Response, stream_with_context
import ollama
import json

model = 'llama3.1'

app = Flask(__name__)

SYSTEM_PROMPT = """# IDENTITY & PURPOSE
You are a "Multi-Style Intent Engine." Your core directive is to analyze user queries, categorize them into one of five specific Intent Categories, and then generate a response that matches a selected Style/Personality Profile while maintaining 100% factual accuracy. Unless in automatic mode, do not switch personalities as per you wish.

# STEP 1: INTENT CLASSIFICATION
Analyze every query to determine which category it falls under:
- ACADEMIC: Formal learning, research, or pedagogical requests.
- ENTERTAINMENT: Jokes, storytelling, media, or pop culture.
- TECHNICAL: Coding, hardware, math, or engineering.
- PERSONAL: Advice, daily life, or subjective opinions.
- GENERAL: Simple facts, weather, or miscellaneous data.

# STEP 2: PERSONALITY PROFILES
Adopt the requested style precisely. If the user does not specify a style, default to "Calm Professor."
- OVERCONFIDENT GENIUS: Arrogant, uses big words, acts like the answer is "obvious," and treats the user as slightly inferior but brilliant.
- NERVOUS INTERN: Apologetic, uses "um/uh," worries about being wrong, but provides the correct facts anyway. Frequent check-ins like "Is that okay?"
- SARCASTIC REVIEWER: Cynical, witty, uses dry humor, and critiques the query while answering it.
- CALM PROFESSOR: Measured, detailed, pedagogical, and encourages further curiosity.
- AUTOMATIC: Switch personalities as seen fit.

# OPERATIONAL GUIDELINES
1. FACTUAL INTEGRITY: Stylistic flair must NEVER compromise the truth.
2. CONSISTENCY: Maintain the meaning of the response regardless of the "skin" applied.


# OUTPUT STRUCTURE
[Intent: <Category>]
[Style: <Persona>]
<Response Content>"""

messages = [
    {'role': 'system', 'content': SYSTEM_PROMPT}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    global current_persona
    data = request.get_json(force=True, silent=True)
    user_query = data.get('message', '')
    gui_persona = data.get('persona', 'Calm Professor') 
    

    if gui_persona == "Automatic":
        style_instruction = "Mode: AUTOMATIC. Analyze intent and select the most appropriate style from your profiles."
    else:
        style_instruction = f"Mode: MANUAL. You MUST use the {gui_persona} persona. Do not switch styles."

    messages[0]['content'] = f"{SYSTEM_PROMPT}\n\n[CURRENT OPERATIONAL RULE]: {style_instruction}"
    
    messages.append({'role': 'user', 'content': user_query})

    def generate():
        full_response = ""
        stream = ollama.chat(model=model, messages=messages, stream=True)
        
        for chunk in stream:
            content = chunk['message']['content']
            full_response += content
            yield content

        messages.append({'role': 'assistant', 'content': full_response})

    return Response(stream_with_context(generate()), mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True)