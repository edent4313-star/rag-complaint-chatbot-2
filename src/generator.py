'''from transformers import pipeline

generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-large"
)

def generate(prompt):

    result = generator(
        prompt,
        max_new_tokens=150
    )

    return result[0]["generated_text"]'''


# Load the model and tokenizer
'''model_name = "google/flan-t5-large"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def generate_answer(prompt):
    # Use truncation=True and max_length to fit the model's capacity
    inputs = tokenizer(
        prompt, 
        return_tensors="pt", 
        truncation=True, 
        max_length=512
    )
    
    outputs = model.generate(
        **inputs, 
        max_new_tokens=256
    )
    
    return tokenizer.decode(outputs[0], skip_special_tokens=True)'''

from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL = "Qwen/Qwen2.5-0.5B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(
    MODEL,
    torch_dtype="auto",
    device_map="cpu" 
)

'''def generate_answer(prompt):
    inputs = tokenizer(
        prompt, 
        return_tensors="pt", 
        truncation=True, 
        max_length=512
    ).to(model.device) # Ensure inputs are on the same device as the model

    # For CausalLM, we usually use max_new_tokens
    outputs = model.generate(
        **inputs, 
        max_new_tokens=512,
        do_sample=True,
        temperature=0.7
    )
    
    # CausalLM returns the prompt + the answer, so we decode and skip the prompt
    answer = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
    return answer'''

def generate_answer(question):
    messages = [
        {"role": "system", "content": "You are a helpful banking complaint analyst."},
        {"role": "user", "content": question}
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=2048
    ).to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=300,
        temperature=0.7,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id
    )

    response = tokenizer.decode(
        outputs[0][inputs.input_ids.shape[1]:],
        skip_special_tokens=True
    )

    return response

