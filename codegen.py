from transformers import AutoTokenizer, AutoModelForCausalLM
codegen_tkn = AutoTokenizer.from_pretrained("Salesforce/codegen-350M-mono")
mdl = AutoModelForCausalLM.from_pretrained("Salesforce/codegen-350M-mono")

def codegen(intent):
# give input as text which reflects intent of the program.
     #text = " write a function which takes 2 numbers as input and returns the larger of the two"
     input_ids = codegen_tkn(intent, return_tensors="pt").input_ids
     gen_ids = mdl.generate(input_ids, max_length=256)
     response = codegen_tkn.decode(gen_ids[0], skip_special_tokens=True)
     return response

intent = " write a function which takes 2 numbers as input and returns the larger of the two"

ans = codegen(intent)

print(ans)