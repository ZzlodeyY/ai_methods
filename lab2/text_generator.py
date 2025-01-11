from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

def load_tokenizer_and_model(model_name_or_path="sberbank-ai/rugpt3small_based_on_gpt2"):
    tokenizer = GPT2Tokenizer.from_pretrained(model_name_or_path)
    model = GPT2LMHeadModel.from_pretrained(model_name_or_path).cuda()
    return tokenizer, model

def generate_text(
    model, tokenizer, prompt, max_length=50, repetition_penalty=5.0,
    top_k=5, top_p=0.95, temperature=1.0, num_beams=10, no_repeat_ngram_size=3
    ):
    input_ids = tokenizer.encode(prompt, return_tensors="pt").cuda()
    with torch.no_grad():
        output = model.generate(
            input_ids,
            max_length=max_length,
            repetition_penalty=repetition_penalty,
            do_sample=True,
            top_k=top_k,
            top_p=top_p,
            temperature=temperature,
            num_beams=num_beams,
            no_repeat_ngram_size=no_repeat_ngram_size,
        )
    return tokenizer.decode(output[0], skip_special_tokens=True)
