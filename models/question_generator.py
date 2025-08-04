import json
from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch

# Load model only once (efficient!)
model_name = "valhalla/t5-small-qg-hl"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

def generate_question(context):
    # Highlighting a key sentence to focus QG (simplified here)
    input_text = "generate question: " + context.strip().replace("\n", " ")
    inputs = tokenizer.encode(input_text, return_tensors="pt", truncation=True)

    outputs = model.generate(inputs, max_length=64, num_beams=4, early_stopping=True)
    question = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return question

def generate_questions_from_paragraphs(input_json="../data/extracted_text.json", output_json="../data/generated_questions.json"):
    with open(input_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    paragraphs = data["paragraphs"]
    all_qas = []

    for i, para in enumerate(paragraphs):
        try:
            question = generate_question(para)
            short_answer = para.split(".")[0] + "."  # naive answer from first sentence
            fill_blank = para.replace(short_answer, short_answer.replace("is", "_____"), 1)

            qa_item = {
                "id": i+1,
                "context": para,
                "mcq": {
                    "question": question,
                    "options": [
                        short_answer,
                        "None of the above",
                        "Not mentioned in text",
                        "All of the above"
                    ],
                    "answer": short_answer
                },
                "short_answer": {
                    "question": question,
                    "answer": short_answer
                },
                "fill_in_blank": {
                    "question": fill_blank,
                    "answer": short_answer
                }
            }
            all_qas.append(qa_item)

        except Exception as e:
            print(f"[!] Skipped para {i}: {e}")

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(all_qas, f, indent=4, ensure_ascii=False)

    print(f"[✓] Generated questions for {len(all_qas)} paragraphs.")

# Example usage
if __name__ == "__main__":
    generate_questions_from_paragraphs()
