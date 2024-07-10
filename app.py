from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import logging

app = Flask(__name__)
CORS(app)

# Enable logging
logging.basicConfig(level=logging.DEBUG)

# Load the model and tokenizer
model_name = "gpt2"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Create a text generation pipeline
text_generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_text():
    try:
        data = request.get_json()
        app.logger.debug(f"Request JSON: {data}")
        
        prompt = data.get('prompt', '')
        
        if not prompt:
            app.logger.error("No prompt provided")
            return jsonify({"error": "No prompt provided"}), 400

        app.logger.debug(f"Received Prompt: {prompt}")

        # Generate text using the pipeline
        generated_text = text_generator(prompt, max_length=100, num_return_sequences=1)
        
        # Debugging: log the generated text
        app.logger.debug(f"Generated Text: {generated_text}")

        return jsonify({"generated_text": generated_text[0]['generated_text']})
    
    except Exception as e:
        app.logger.error(f"Error: {e}")
        return jsonify({"error": "An error occurred during text generation"}), 500

if __name__ == '__main__':
    app.run(debug=True)
