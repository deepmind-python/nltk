import spacy
# Load the English model
nlp = spacy.load('en_core_web_sm')

# Function to recognize intent
def recognize_intent(text):
    doc = nlp(text)
    # Here you can define your intents based on the entities or patterns
    intents = {
               'greeting': ['hello', 'hi', 'hey'],

               'goodbye': ['bye', 'goodbye'],


               }
    for token in doc:
        for intent_i, keywords in intents.items():
            if token.text.lower() in keywords:
                return intent_i
    return 'unknown'

# Example usage
user_input = 'Hello, how are you?'

intent = recognize_intent(user_input)
print(f'Intent recognized: {intent}')







