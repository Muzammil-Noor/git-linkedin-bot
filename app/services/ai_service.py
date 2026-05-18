import os
import aiohttp
import asyncio
import json

HF_TOKEN = os.getenv("HF_TOKEN")
HF_CHAT_URL = "https://router.huggingface.co/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

async def generate_linkedin_post(project_name: str, commit_messages: list[str]) -> str:
    system_prompt = """
        You are a professional software engineer writing engaging LinkedIn posts.
        Your goal is to:
        - Summarize the week's progress for a project in 7-8 sentences.
        - If a project is just started then mention that.
        - If a project has ended with its final commits then mention that in the post as well
        - Focus on tangible improvements, impact, or results.
        - Use active, friendly, and human-readable language.
        - Include specific achievements or features without repeating phrases.
        - Optionally, add a subtle emoji for excitement or emphasis.
    """

    user_prompt = f"""
        Project: {project_name}
        Commits this week:
        {chr(10).join('- ' + m for m in commit_messages)}

        Write a polished LinkedIn post following the guidelines above.
    """

    payload = {
        "model": "Qwen/Qwen2.5-72B-Instruct",  # hosted instruction-tuned model
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": 250,
        "temperature": 0.7
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(HF_CHAT_URL, headers=HEADERS, data=json.dumps(payload)) as resp:
            if not resp.status == 200:
                text = await resp.text()
                raise RuntimeError(f"HF API error {resp.status}: {text}")
            data = await resp.json()
            return data["choices"][0]["message"]["content"].strip()

# Example usage
if __name__ == "__main__":
    commits = ["Refactored login flow", "Fixed bug in payment API", "Updated README"]
    post = asyncio.run(generate_linkedin_post("AwesomeProject", commits))
    print(post)