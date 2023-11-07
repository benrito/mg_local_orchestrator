import time
from simpleaichat import AIChat
from whisper_mic.whisper_mic import WhisperMic
from elevenlabs import clone, generate, stream, play, set_api_key
import speech_recognition as sr
from playsound import playsound

#OPENAI / SIMPLEAICHAT
personality = open("doppelganger.txt").read().strip()
ai = AIChat(system=personality, api_key="sk-", model="gpt-4-1106-preview")

#WHISPER
mic = WhisperMic()

#ELEVENLABS
set_api_key("")

def main():
    counter = 0
    while True:
        playsound('media/beep_start.wav')
        utterance = mic.listen()
        print(f"I heard: {utterance}")
        response = ai(utterance)
        print(f"I said: {response}")
        counter += 1
        print(f"Interaction count: {counter}")
        audio_stream = generate(
            text=f"{response}",
            model="eleven_multilingual_v2",
            voice=voice,
            stream=True
        )
        stream(audio_stream)

if __name__ == "__main__":
    timestamp = str(int(time.time()))
    print(timestamp)

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n\nI'm listening...")
        audio = r.listen(source)
        with open(f"working/{timestamp}_recording.wav", "wb") as f:
            f.write(audio.get_wav_data())

    voice = clone(
        name=f"{timestamp}",
        description="Testing", # Optional
        files=[f"working/{timestamp}_recording.wav"],
    )

    print(voice)
    audio = generate(text="OK, we're ready to go. The voice is now cloned. Isn't it cool?", voice=voice)
    play(audio)
    main()