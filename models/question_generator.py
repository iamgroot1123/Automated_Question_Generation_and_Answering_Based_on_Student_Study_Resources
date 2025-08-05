import json
import os
from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch

# Load the model and tokenizer
model_name = "valhalla/t5-small-qg-prepend"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

input_json = "../data/extracted_text.json"
output_json = "../data/generated_questions.json"


def generate_question_answer(text, max_length=64):
    input_text = "generate question: " + text.strip().replace("\n", " ")
    inputs = tokenizer.encode(input_text, return_tensors="pt", truncation=True)
    outputs = model.generate(inputs, max_length=max_length, num_return_sequences=1)
    question = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Use simple sentence slicing for the answer
    answer = text.strip().split(".")[0].strip() + "."

    return question, answer


def generate_mcq_options(correct_answer):
    distractors = [
        "Not mentioned in text",
        "None of the above",
        "All of the above"
    ]
    options = [correct_answer] + distractors
    return options


def generate_questions_from_paragraphs():
    if not os.path.exists(input_json):
        print(f"[✗] Missing input: {input_json}")
        return

    with open(input_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    generated = []
    for idx, para_text in enumerate(data):
        context = para_text.strip()
        if not context:
            continue

        question, answer = generate_question_answer(context)
        options = generate_mcq_options(answer)

        generated.append({
            "id": idx + 1,
            "context": context,
            "mcq": {
                "question": question,
                "options": options,
                "answer": answer
            },
            "short_answer": {
                "question": question,
                "answer": answer
            }
        })

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(generated, f, indent=4)

    print(f"[✓] Generated questions for {len(generated)} paragraph(s).")


if __name__ == "__main__":
    generate_questions_from_paragraphs()
