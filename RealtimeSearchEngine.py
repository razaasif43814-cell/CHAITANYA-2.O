from groq import Groq
from dotenv import dotenv_values
from json import load, dump
import datetime

env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")

client = Groq(api_key=GroqAPIKey)

def RealtimeInformation():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")

    data = f"please use this real-time information if needed,\n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} hours :{minute} minutes :{second} seconds.\n"
    return data 

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

def RealtimeSearchEngine(Query):
    try:
        # load previous messages if exist
        try:
            with open(r"Data\SearchLog.json", "r") as f:
                messages = load(f)
        except FileNotFoundError:
            messages = []
            with open(r"Data\SearchLog.json", "w") as f:
                dump([], f)

        messages.append({"role": "user", "content": f"{Query}"})

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",   # ✅ updated model
            messages=[{"role": "system", "content": RealtimeInformation()}] + messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=False   # ✅ no streaming
        )

        Answer = completion.choices[0].message.content
        Answer = Answer.replace("</s>", "")

        messages.append({"role": "assistant", "content": Answer})

        with open(r"Data\SearchLog.json", "w") as f:
            dump(messages, f, indent=4)

        return AnswerModifier(Answer)
    
    except Exception as e:
        print(f"Error in RealtimeSearchEngine: {e}")
        return "[ERROR] RealtimeSearchEngine is unavailable. Please try again later."

if __name__ == "__main__":
    while True:
        prompt = input("Enter your query: ")
        print(RealtimeSearchEngine(prompt))
