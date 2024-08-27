from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("Falconsai/text_summarization")
model = AutoModelForSeq2SeqLM.from_pretrained("Falconsai/text_summarization")

max_length = 200


def get_summary(text):
    inputs = tokenizer(text, return_tensors="pt",
                       max_length=512, truncation=True)
    summary_ids = model.generate(inputs["input_ids"], max_length=max_length, min_length=200, length_penalty=3.0,
                                 num_beams=3, temperature=0.2, repetition_penalty=2.0, early_stopping=False, do_sample=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary
