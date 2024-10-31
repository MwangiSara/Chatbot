from flask import *
import openai
from decouple import config


app = Flask(__name__)
openai.api_key= config('API_KEY')
#generate a function that helps in connectng GPT to out application
def generate_text(prompt):
    response= openai.ChatCompletion.create(
        model= config('MODEL'), # specifies the model to be used for generating the cpompletion
        messages = [
            {"role":"system","content":"You are suppossed to be a helpful assistant" },
            {"role":"user","content": prompt}
        ],
        max_tokens = 150, # the maximum number of words in response.
        temperature = 0.8 #it controls the randomness of the response. A higher value eg 0.8 makes the output more diverse
    )
    return response.choices[0].message['content'].strip()
# we want to access the content of the first choice in the responses. the responses from API is usually a list of choices, and we're selecting the first one
# .strip(): removes any leading or trailing whitespace from the generated text to clean up the output

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        prompt = request.form['prompt']
        text = generate_text(prompt)
        return render_template("index.html",prompt=prompt,text=text)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
