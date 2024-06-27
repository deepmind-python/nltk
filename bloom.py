from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained('bigscience/bloom-1b1')
tokenizer = AutoTokenizer.from_pretrained('bigscience/bloom-1b1')

prompt = (
    "What is the meaning of life?"
)
input_ids = tokenizer(prompt, return_tensors="pt").input_ids
gen_tokens = model.generate(
    input_ids,
    do_sample=True,
    temperature=0.9,
    max_length=1024,
)
gen_text = tokenizer.batch_decode(gen_tokens)[0]

print(gen_text)
