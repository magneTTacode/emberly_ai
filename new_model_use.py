from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration

# Загрузите токенизатор и модель
tokenizer = BlenderbotTokenizer.from_pretrained('fine-tuned-blenderbot')
model = BlenderbotForConditionalGeneration.from_pretrained('fine-tuned-blenderbot')

def chat_with_bot(user_input):
    inputs = tokenizer([user_input], return_tensors='pt')
    reply_ids = model.generate(inputs['input_ids'], max_length=128, num_beams=5, early_stopping=True)
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
