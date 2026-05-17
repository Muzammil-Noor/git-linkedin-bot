import os
from huggingface_hub import InferenceClient

HF_TOKEN = os.getenv("HF_TOKEN")

client = InferenceClient(HF_TOKEN)

async def generate_linkedin_post(project_name: str, commit_messages: list[str]) -> str:
    prompt = f"""
    You are a professional software engineer summarizing work for LinkedIn.
    Project: {project_name}
    Commits this week:
    {chr(10).join('- ' + m for m in commit_messages)}

    Write a polished LinkedIn post (1-3 sentences) highlighting progress, improvements, and impact.
    """

    # Use a summarization/generation model
    # You can swap 'google/flan-t5-large' with any text-generation model
    response = client.text_generation(
        model="google/flan-t5-large",
        inputs=prompt,
        parameters={
            "max_new_tokens": 250,
            "temperature": 0.7
        }
    )

    # response is a dict with 'generated_text'
    return response.generated_text