from flask import Flask, request, jsonify, send_from_directory, render_template
from transformers import pipeline
from googletrans import Translator
from newspaper import Article
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

# Use T5 model
qa_pipeline = pipeline("text2text-generation", model="t5-large")
translator = Translator()

def extract_text_from_url(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        return f"Error: {str(e)}"

def summarize_text(text, sentence_count=5):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentence_count)
    return ' '.join(str(sentence) for sentence in summary)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data['question']
    pdf_text = data.get('pdfText', '')
    url = data.get('url', '')

    if url:
        web_text = extract_text_from_url(url)
        print("Extracted web text:", web_text)  # Print first 1000 characters for debugging
        web_text = summarize_text(web_text)
        print("Summarized Text: ", web_text)
        if 'Error' in web_text:
            return jsonify({'error': 'Failed to extract text from URL'}), 500
    else:
        web_text = pdf_text

    try:
        # Translate the question from Malayalam to English
        malayalam_question = translator.translate(question, src='ml', dest='en').text
        print("Translated question to English:", malayalam_question)
        # Perform question answering
        input_text = f"question: {malayalam_question} context: {web_text}"
        answer = qa_pipeline(input_text)[0]['generated_text']
        print("Answer:", answer)
        # Translate the answer from English to Malayalam
        malayalam_answer = translator.translate(answer, src='en', dest='ml').text
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Translation or QA failed'}), 500

    return jsonify({'answer': malayalam_answer})

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    malayalam_text = data['malayalamText']

    # Translate Malayalam text to English
    english_translation = translator.translate(malayalam_text, src='ml', dest='en').text

    return jsonify({'translation': english_translation})

if __name__ == '__main__':
    app.run(debug=True)
