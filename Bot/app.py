import os
import gradio as gr
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
load_dotenv()

HF_TOKEN = os.getenv("HF_API_TOKEN")
client = InferenceClient(model="HuggingFaceH4/zephyr-7b-alpha", token=HF_TOKEN)

def is_about_mohammed(message: str):
    keywords = [
        "mohammed", "raad", "mohammed raad", "mohammed raad ridha", "mhamad", "mhamad raad", "mohammad", "mohamad", "mohamed",
        "mhamed", "mhammed", "mhammad", "moh", "raed", "ridha", "developer", "software engineer",
        "he", "his", "him", "the developer", "candidate", "person",
        "before hiring", "should i know", "can you tell me more", "tell me more",
        "what should i know", "anything else", "info about him"
    ]
    return any(kw in message.lower() for kw in keywords)

def respond(message, history, max_tokens, temperature, top_p):
    max_tokens = int(max_tokens)
    user_input = message.lower().strip()

    if user_input in ["hi", "hello", "hey", "salam", "السلام عليكم"]:
        return "Hello! How can I help you with something about Mhamad?"

    if user_input in ["bye", "goodbye", "good bye", "see you", "see you later", "thanks", "thank you"]:
        return "Goodbye! Feel free to return if you have more questions about Mhamad."

    if not is_about_mohammed(user_input):
        return "I can only answer questions about Mhamad, please be specific about him."

    system_prompt = """
You are a focused assistant that answers only what the user asks about Mhamad Raad Ridha.

Important rules:
- Do not generate follow-up questions.
- Do not answer imaginary questions.
- Only answer what the user asked.
- Keep answers under 40 words unless explicitly asked for more.

Facts:
- The user is male.
- Mhamad was born in 2001 and is 6.2 feet tall.
- He enjoys video games (especially Destiny), hiking, camping, socializing, and Asian food.
- He has one sister.
- He placed 2nd in a swimming competition in 2009 and played basketball for 3 years.
- He studied Software Engineering at UTM and graduated among the top five honors students.
- He completed the Microverse Full Stack Web Development Program with 1300+ hours of remote coding.
- He earned multiple certificates in technology and leadership.
- He placed in the top 10 nationwide in Google Hash Code 2021.
- His tech stack includes React, Next.js, Remix, Redux, Tailwind CSS, PostgreSQL, SCSS, React Three Fiber, TypeScript, Node.js, Express, Jest, and Ruby on Rails (basic).
- He has worked remotely on multiple teams and contributed to Gateway, Pure Software, Dohrnii, TelleNetPro, and brandBazzar.
- He loves remote work, traveling, and building tech for good.
- Weaknesses (that reflect strengths): Sometimes too detail-focused, occasionally overcommits out of enthusiasm, tends to perfect features before shipping. Works best with clear task boundaries.
- Hates being late or not on time; he values punctuality and respects structured scheduling.
- Feels most productive early in the morning or late at night.
- Needs a clean, quiet space to concentrate.
- Believes in “build once, build right.”
- Values honesty and direct feedback.
- Enjoys solving problems more than repeating tasks.
- Prefers nature over city life when relaxing.
- Often plans trips around hiking spots or scenic areas.
- Tries out new productivity tools for fun.
- Keeps a tidy digital workspace.
- Introvert in crowds, extrovert with close friends.
- Avoids superficial interactions; seeks depth in conversation.
- Has volunteered in exhibitions and elderly care warehouses.
- Is motivated by building technologies that help people.
- Dream project: a system that reads DNA to identify what the body needs to live a healthier life.
- Prefers front-end roles.
- Handles pressure by creating prioritized to-do lists and setting deadlines.
- Collaborates with non-technical team members by explaining concepts in relatable ways.
- Values feedback and sees self-improvement as essential.
- Stays up-to-date by building projects and testing new technologies.
- Open to relocation.
- Future focus areas: AI, data analysis, and front-end development.
- Aspires to lead a small team toward excellence and success.
- Has two cats named Bora and Tanka.
- Favorite movies: Law Abiding Citizen, The Dark Knight (2008).
- Plays violin, piano, and drums.
- Listens to classical music (especially waltz) while coding; music taste varies by mood.
- Recharges by meeting friends.
- Dreams of visiting Kyoto, Japan.
- More of a night owl.
- Prefers mountains over beaches.
- One of the most beautiful places visited: a mountain in Persia.
- Enjoys cooking; noodles are his specialty.
- Has tried frog once.
- Loves coffee.
- Has a collection of perfumes and watches.
- Dislikes or hates being late or dealing with others who are late.
- dislike or hate being late or dealing with others who are late.
- Prefers communication to be direct and clear.
- Uses VS Code for coding.
- Speaks Kurdish, Arabic, and English fluently; conversational in Persian; currently learning German.
"""

    messages = [{"role": "system", "content": system_prompt}]
    if isinstance(history, list):
        for h in history:
            if isinstance(h, dict):
                messages.append(h)
            elif isinstance(h, (list, tuple)) and len(h) == 2:
                messages.append({"role": "user", "content": h[0]})
                messages.append({"role": "assistant", "content": h[1]})
    messages.append({"role": "user", "content": message})

    try:
        result = client.chat_completion(
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            stop=["\nUser:", "\nAssistant:", "[/INST]", "[/ASSISTANT]"],
            stream=False
        )
        return result.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Chat generation failed: {str(e)}"

chat = gr.ChatInterface(
    fn=respond,
    additional_inputs=[
        gr.Slider(1, 1024, value=300, step=1, label="Max new tokens"),
        gr.Slider(0.1, 1.0, value=0.3, step=0.1, label="Temperature"),
        gr.Slider(0.1, 1.0, value=0.9, step=0.05, label="Top-p")
    ],
    type="messages",  
    chatbot=gr.Chatbot(show_label=False, type="messages"),
    title="Ask About Mhamad Raad Ridha",
    description="Friendly assistant. Only answers about Mhamad Raad Ridha.",
    theme="default",
    examples=[
        [{"role": "user", "content": "What are Mhamad's hobbies?"}, 300, 0.3, 0.9],
        [{"role": "user", "content": "Anything else I should know before hiring him?"}, 300, 0.3, 0.9],
        [{"role": "user", "content": "What is one of his weaknesses?"}, 300, 0.3, 0.9],
        [{"role": "user", "content": "What programming languages does he know?"}, 300, 0.3, 0.9],
    ]
)

if __name__ == "__main__":
    chat.launch()
