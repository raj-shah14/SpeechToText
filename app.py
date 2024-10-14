import whisper
from openai import OpenAI, AzureOpenAI
import os
from TTS import get_speech_output

speech_model = whisper.load_model("base") # tiny, base, medium, large-v2 large-v3
OAIclient = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

AOAIClient = AzureOpenAI(
    api_key=os.getenv("AZURE_API_KEY"),
    api_version="2023-05-15",
    azure_endpoint=os.getenv("AZURE_API_ENDPOINT")
)

def UseOpenAIScript(speech_model, temperature, system_prompt, audio_file):
    response = OAIclient.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=temperature,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": whisper.transcribe(speech_model, audio_file)["text"]
            }
        ]
    )
    return response.choices[0]

# https://stackoverflow.com/questions/71888625/openai-api-how-do-i-specify-the-maximum-number-of-words-a-completion-should-ret
# https://platform.openai.com/tokenizer
def UseAzureOAIScript(speech_model, deployment_name, audio, system_prompt):
    response = AOAIClient.chat.completions.create(
        model=deployment_name, 
        max_tokens=1024,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": whisper.transcribe(speech_model, audio)["text"]
            }
        ]
    )
    return response.choices[0]

system_prompt = "Your task is correct the grammar and spelling mistake from the transcribed text. Translate to english if it is in different language. Remove unnecessary white spaces. Only add necessary punctuation such as periods, commas, and capitalization, and use only the context provided. Do not rewrite the text"
use_gpt4o = True
if use_gpt4o:
    deployment_name = os.environ.get("AZURE_OPENAI_GPT4O_DEPLOYMENT_NAME")
else:
    deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME")


# load the entire audio file
audio = whisper.load_audio("audio.mp3")

result = UseAzureOAIScript(speech_model, deployment_name, audio, system_prompt)
print(result.message.content)
res = get_speech_output(result.message.content)
print(res)