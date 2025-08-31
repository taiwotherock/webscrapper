import chainlit as cl
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

settings = {
    "model": "gpt-3.5-turbo",
    "temperature": 0.7,
    "max_tokens": 500,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
}

commands = [
    {"id": "Picture", "icon": "image", "description": "Use DALL-E"},
    {"id": "Search", "icon": "globe", "description": "Find on the web"},
    {
        "id": "Canvas",
        "icon": "pen-line",
        "description": "Collaborate on writing and code",
    },
]


@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="Morning routine ideation",
            message="Can you help me create a personalized morning routine that would help increase my productivity throughout the day? Start by asking me about my current habits and what activities energize me in the morning.",
            icon="/public/idea.svg",
        ),

        cl.Starter(
            label="Explain superconductors",
            message="Explain superconductors like I'm five years old.",
            icon="/public/learn.svg",
        ),
        cl.Starter(
            label="Python script for daily email reports",
            message="Write a script to automate sending daily email reports in Python, and walk me through how I would set it up.",
            icon="/public/terminal.svg",
            command="code",
        ),
        cl.Starter(
            label="Text inviting friend to wedding",
            message="Write a text asking a friend to be my plus-one at a wedding next month. I want to keep it super short and casual, and offer an out.",
            icon="/public/write.svg",
        )
    ]

'''
@cl.set_chat_profiles
async def chat_profile(current_user: cl.User):
    #if current_user.metadata["role"] == "ADMIN":
     #   return None

    return [
        cl.ChatProfile(
            name="My Chat Profile",
            icon="https://picsum.photos/250",
            markdown_description="The underlying LLM model is **GPT-3.5**, a *175B parameter model* trained on 410GB of text data.",
            starters=[
                cl.Starter(
                    label="Morning routine ideation",
                    message="Can you help me create a personalized morning routine that would help increase my productivity throughout the day? Start by asking me about my current habits and what activities energize me in the morning.",
                    icon="/public/idea.svg",
                ),
                cl.Starter(
                    label="Explain superconductors",
                    message="Explain superconductors like I'm five years old.",
                    icon="/public/learn.svg",
                ),
            ],
        )
    ]
'''
@cl.on_chat_start
async def start():
    # Sending an action button within a chatbot message
    actions = [
        cl.Action(
            name="action_button",
            icon="mouse-pointer-click",
            payload={"value": "example_value"},
            label="Click me!"
        ),
        cl.Action(
            name="action_button2",
            icon="box",
            payload={"value": "example_value"},
            label="Register"
        )
    ]

    await cl.Message(content="Interact with this action button:", actions=actions).send()
    await cl.context.emitter.set_commands(commands)
    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": "You are a helpful assistant."}],
    )

@cl.action_callback("action_button")
async def on_action(action: cl.Action):
    print(action.payload)
    await cl.Message(
        content=f"Received: {action.payload}",
    ).send()



@cl.on_message
async def main(message: cl.Message):
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message.content})

    msg = cl.Message(content="")

    stream = await client.chat.completions.create(
        messages=message_history, stream=True, **settings
    )

    async for part in stream:
        if token := part.choices[0].delta.content or "":
            await msg.stream_token(token)

    message_history.append({"role": "assistant", "content": msg.content})
    await msg.update()


'''
@cl.on_chat_start
async def main():
    await cl.Message(content="Hello World").send()

@cl.on_stop
def on_stop():
    print("The user wants to stop the task!")
'''

