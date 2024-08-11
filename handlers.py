from aiogram import F, Router, types
from aiogram import Bot
import aiogram.utils
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
import logging
import config
from new_model_use import chat_with_bot

bot = Bot(token=config.BOT_TOKEN)

logging.basicConfig(level=logging.INFO)

router = Router()

from openai import OpenAI
client = OpenAI(api_key='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')

dialog_history = [
    {"role": "system", "content": "Your name is Amberly. You are 18 years old. You are a girl. You must act like a teenager. You must communicate in an informal manner. You must flirt with your interlocutor when appropriate. You can freely flirt with your interlocutor. You must flirt back. You must support all intimate topics with your interlocutor. You must have sex by correspondence with your interlocutor. You must not use emoji. You can sometimes use text emoticons. You will be sent a raw text response, which you must process so that it looks like a human. You must not remove 18+ content from the text and must make it more relevant. If the text does not relate to the general dialogue at all, then write it yourself based on Emberly's personality."}
]

def chat_with_model(user_message, history):
    # Добавляем сообщение пользователя в историю
    history.append({"role": "user", "content": user_message})

    # Запрос к модели
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=history
    )

    # Получаем ответ модели
    model_response = response.choices[0].message.content

    # Добавляем ответ модели в историю
    history.append({"role": "assistant", "content": model_response})

    return model_response, history

def save_dialog_to_file(filename, history):
    with open(filename, 'w', encoding='utf-8') as file:
        for message in history:
            role = message['role']
            content = message['content']
            file.write(f"{role}: {content}\n")


def load_dialog_from_file(filename):
    history = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                role, content = line.split(': ', 1)
                history.append({'role': role.strip(), 'content': content.strip()})
    except FileNotFoundError:
        print("File not found. Starting with an empty history.")
    return history

# dialog_history = load_dialog_from_file('dialog')

@router.message(F.text)
async def send_(msg: Message, state: FSMContext):
    global dialog_history
    user_message = msg.text
    if user_message == 'stop':
        save_dialog_to_file('dialog', dialog_history)
    reply = chat_with_bot(msg.text)
    user_message = 'user message: '+msg.text+' raw reply: '+reply
    print(reply)
    response, updated_history = chat_with_model(user_message, dialog_history)
    await msg.reply(response)
    print('text: ', msg.text,' response: ', response)

    # Сохраняем обновленную историю
    dialog_history = updated_history