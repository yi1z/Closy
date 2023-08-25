from paddlespeech.cli.asr.infer import ASRExecutor


# convert speech to text
def speech_to_text(filename: str):
    asr = ASRExecutor()
    result = asr(filename)
    return result
