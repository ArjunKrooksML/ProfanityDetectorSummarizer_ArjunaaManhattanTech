from transformers import pipeline
import torch

try:
    generator = pipeline(
        "text-generation",
        model="mistralai/Mistral-7B-Instruct-v0.1",
        torch_dtype=torch.bfloat16,
        device_map="auto",
    )
except Exception as e:
    print(f"Error loading model: {e}")
    print("Please ensure you have run 'huggingface-cli login'.")
    generator = None


def sum_mist(nsfw_results, abusive_segments, ocr_results=None):
    if generator is None:
        return "Model could not be loaded. Please check your setup."

    prompt = "You are a video moderation assistant. Summarize the content moderation results. Format clearly in bullet points. Give a few insights extra from your side based on the input.\n\n"

    # NSFW section
    prompt += "• NSFW Detections:\n"
    if nsfw_results:
        for item in nsfw_results:
            prompt += f"  - At {item['timestamp']:.2f}s: {item['label']} detected (score: {item['score']:.2f})\n"
    else:
        prompt += "  - None\n"

    # Abuse section
    prompt += "\n• Abusive Speech:\n"
    if abusive_segments:
        for seg in abusive_segments:
            start = seg.get("start", None)
            end = seg.get("end", None)
            text = seg.get("text", "")
            if start is not None and end is not None:
                prompt += f"  - Between {start:.2f}s and {end:.2f}s: \"{text}\"\n"
            else:
                prompt += f"  - \"{text}\"\n"
    else:
        prompt += "  - None\n"

 
    if ocr_results:
        prompt += "\n• On-Screen Text Detected (OCR):\n"
        for ocr in ocr_results:
            prompt += f"  - At {ocr['timestamp']:.2f}s: \"{ocr['text']}\"\n"
    else:
        prompt += "\n• On-Screen Text Detected (OCR): None\n"

    formatted_prompt = f"<s>[INST] {prompt} [/INST]"

    sequences = generator(
        formatted_prompt,
        max_new_tokens=200,
        do_sample=True,
        top_k=10,
        num_return_sequences=1,
        eos_token_id=generator.tokenizer.eos_token_id,
    )

    if sequences and sequences[0]:
        full_text = sequences[0]['generated_text']
        return full_text.split("[/INST]")[-1].strip()

    return "Failed to generate summary."
