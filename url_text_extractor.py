from newspaper import Article
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

def extract_text_from_url(url):
    try:
        # Download and parse the article
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

if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/Apple_Inc."
    extracted_text = extract_text_from_url(url)
    print("Extracted Text:\n")
    print(extracted_text[:2000])  # Print first 2000 characters for brevity

    if extracted_text:
        summarized_text = summarize_text(extracted_text)
        print("\nSummarized Text:\n")
        print(summarized_text)
