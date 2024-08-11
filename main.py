from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration

# Загрузите токенизатор и модель
tokenizer = BlenderbotTokenizer.from_pretrained('facebook/blenderbot-400M-distill')
model = BlenderbotForConditionalGeneration.from_pretrained('facebook/blenderbot-400M-distill')

def chat_with_bot(user_input):
    # Токенизируйте входное сообщение
    inputs = tokenizer([user_input], return_tensors='pt')
    
    # Сгенерируйте ответ
    reply_ids = model.generate(inputs['input_ids'], max_length=150, num_beams=5, early_stopping=True)
    
    # Декодируйте ответ
    reply = tokenizer.decode(reply_ids[0], skip_special_tokens=True)
    
    return reply

if __name__ == "__main__":
    print("Привет! Я BlenderBot. Чем могу помочь?")
    while True:
        user_input = input("Вы: ")
        if user_input.lower() in ['выход', 'exit']:
            print("Пока!")
            break
        
        response = chat_with_bot(user_input)
        print(f"Бот: {response}")
