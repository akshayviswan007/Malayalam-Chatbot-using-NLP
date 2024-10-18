from googletrans import Translator

translator = Translator()
malayalam_text = "ആരാണ് വിനായക്"
translated_text = translator.translate(malayalam_text, src='ml', dest='en').text
print(translated_text)
