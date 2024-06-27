from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
import ast

mdl_name = "distilbert-base-cased-distilled-squad"
my_pipeline = pipeline('question-answering', model=mdl_name, tokenizer=mdl_name)


def answer_question(question, context):
    text = "{" + "'question': '" + question + "','context': '" + context + "'}"

    di = ast.literal_eval(text)
    response = my_pipeline(di)
    return response

context = 'Taipei is in Taiwan. Now, we are at Taipei.'
question = 'What country are we in?'

ans = answer_question(question, context)

print(ans)