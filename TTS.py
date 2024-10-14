import os
import azure.cognitiveservices.speech as speechsdk

def get_speech_output(text):
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(subscription=os.getenv('AZURE_AI_SPEECH'), region=os.getenv('AZURE_AI_REGION'))
    audio_config = speechsdk.AudioConfig(filename="./output.mp3")

    # The language of the voice that speaks.
    speech_config.speech_synthesis_voice_name='en-US-JennyNeural'
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()
    return speech_synthesis_result


if __name__ == "__main__":
    # Get text from the console and synthesize to the default speaker.
    text = "This is a beautiful day to be alive."
    text += "I am so happy to be here. I went to Microsoft Thermal Energy Center. It was a great experience. I learned a lot about how the buildings are getting powered." 
    print(get_speech_output(text))