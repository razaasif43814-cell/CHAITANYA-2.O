# ================================
# MAIN ASSISTANT FILE (STABLE)
# ================================

from Frontend.GUI import (
    GraphicalUserInterface,
    SetAssistantStatus,
    ShowTextToScreen,
    TempDirectoryPath,
    SetMicrophoneStatus,
    AnswerModifier,
    QueryModifier,
    GetMicrophoneStatus,
    GetAssistantStatus
)

from Backend.Model import FirstLayerDMM
from Backend.RealtimeSearchEngine import RealtimeSearchEngine
from Backend.Automation import Automation
from Backend.SpeechToText import SpeechRecognition
from Backend.Chatbot import Assistantname, ChatBot, Username
from Backend.TextToSpeech import TextToSpeech

from asyncio import run
from time import sleep
import subprocess
import threading
import json
import os


# ================================
# CHAT LOG FUNCTIONS
# ================================

def ShowDefaultChatIfNoChats():

    try:

        with open(r'Data\ChatLog.json', "r", encoding='utf-8') as file:
            content = file.read()

        if len(content) < 5:

            with open(TempDirectoryPath('Database.data'), 'w', encoding="utf-8") as file:
                file.write("")

            with open(TempDirectoryPath('Responses.data'), 'w', encoding="utf-8") as file:
                file.write("Hello! How can I help you?")

    except FileNotFoundError:
        pass


def ReadChatLogJson():

    try:

        with open(r'Data\ChatLog.json', 'r', encoding="utf-8") as file:
            return json.load(file)

    except:
        return []


def ChatLogIntegration():

    json_data = ReadChatLogJson()

    formatted_chatlog = ""

    for entry in json_data:

        if entry["role"] == "user":
            formatted_chatlog += f"{Username}: {entry['content']}\n"

        elif entry["role"] == "assistant":
            formatted_chatlog += f"{Assistantname}: {entry['content']}\n"

    with open(TempDirectoryPath('Database.data'), 'w', encoding="utf-8") as file:
        file.write(AnswerModifier(formatted_chatlog))


def ShowChatsOnGUI():

    try:

        with open(TempDirectoryPath('Database.data'), "r", encoding="utf-8") as file:

            data = file.read()

            if data:

                with open(TempDirectoryPath('Responses.data'), "w", encoding="utf-8") as file:
                    file.write(data)

    except:
        pass


# ================================
# INITIAL SETUP
# ================================

def InitialExecution():

    SetMicrophoneStatus("False")

    ShowTextToScreen("")

    ShowDefaultChatIfNoChats()

    ChatLogIntegration()

    ShowChatsOnGUI()


InitialExecution()


# ================================
# MAIN EXECUTION FUNCTION
# ================================

def MainExecution():

    try:

        TaskExecution = False
        ImageExecution = False
        ImageGenerationQuery = ""

        SetAssistantStatus("Listening...")

        Query = SpeechRecognition()

        if not Query:
            SetAssistantStatus("Idle")
            SetMicrophoneStatus("True")
            return

        ShowTextToScreen(f"{Username} : {Query}")

        SetAssistantStatus("Thinking...")

        Decision = FirstLayerDMM(Query)

        print("\n[DEBUG] Query:", Query)
        print("[DEBUG] Decision:", Decision, "\n")


        G = any("general" in i.lower() for i in Decision)
        R = any("realtime" in i.lower() for i in Decision)


        Merged_query = " and ".join(
            [" ".join(i.split()[1:]) for i in Decision]
        )


        function = ["open", "close", "play", "search"]

        for queries in Decision:

            if any(x in queries.lower() for x in ["generate", "create", "make"]):

                ImageGenerationQuery = " ".join(queries.split()[1:])
                ImageExecution = True


            if not TaskExecution:

                if any(queries.lower().startswith(func) for func in function):

                    run(Automation(list(Decision)))
                    TaskExecution = True


        if ImageExecution:

            with open(r"Frontend\Files\ImageGeneration.data", "w", encoding="utf-8") as file:
                file.write(f"{ImageGenerationQuery},True")

            subprocess.Popen(
                ['python', r'Backend\ImageGeneration.py'],
                shell=False
            )


        Answer = ""

        if G and R:

            SetAssistantStatus("Searching...")
            Answer = RealtimeSearchEngine(QueryModifier(Merged_query))

        else:

            for Queries in Decision:

                if "general" in Queries.lower():

                    SetAssistantStatus("Thinking...")

                    QueryFinal = Queries.lower().replace("general", "").strip()

                    print("[DEBUG] Sending to ChatBot:", QueryFinal)

                    Answer = ChatBot(QueryModifier(QueryFinal))

                    print("[DEBUG] ChatBot Answer:", Answer)


                elif "realtime" in Queries.lower():

                    SetAssistantStatus("Searching...")

                    QueryFinal = Queries.lower().replace("realtime", "").strip()

                    Answer = RealtimeSearchEngine(QueryModifier(QueryFinal))


                elif "exit" in Queries.lower():

                    Answer = "Okay, Bye!"

                    ShowTextToScreen(f"{Assistantname}: {Answer}")

                    TextToSpeech(Answer)

                    os._exit(0)


        # Fallback protection
        if not Answer or Answer.strip() == "":
            Answer = "Sorry, I could not generate a response."


        ShowTextToScreen(f"{Assistantname}: {Answer}")

        SetAssistantStatus("Answering...")

        TextToSpeech(Answer)

        SetAssistantStatus("Idle")

        # 🔥 IMPORTANT FIX: Reactivate microphone
        SetMicrophoneStatus("True")


    except Exception as e:

        print("[MainExecution ERROR]:", e)

        SetAssistantStatus("Error")

        SetMicrophoneStatus("True")

# ================================
# ASSISTANT BACKGROUND THREAD
# ================================

def AssistantThread():

    print("[INFO] Assistant thread started")

    while True:

        try:

            if GetMicrophoneStatus() == "True":

                print("[INFO] Microphone active")

                SetMicrophoneStatus("False")

                MainExecution()

            elif GetAssistantStatus() == "Exit":

                print("[INFO] Assistant exiting")

                break

            sleep(0.1)

        except Exception as e:

            print("[AssistantThread ERROR]:", e)

            SetMicrophoneStatus("True")

            sleep(1)

# ================================
# GUI THREAD (MAIN THREAD ONLY)
# ================================

def StartGUI():

    try:

        print("[INFO] Starting GUI")

        GraphicalUserInterface()

    except Exception as e:

        print("[GUI ERROR]:", e)


# ================================
# PROGRAM ENTRY POINT
# ================================

if __name__ == "__main__":

    print("[INFO] Starting Assistant System")

    # Start assistant logic in background thread
    assistant_thread = threading.Thread(
        target=AssistantThread,
        daemon=True
    )

    assistant_thread.start()

    # Run GUI in MAIN THREAD (IMPORTANT)
    StartGUI()