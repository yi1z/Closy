from paddlespeech.cli.asr.infer import ASRExecutor


def speech_to_text(filename: str):
    asr = ASRExecutor()
    result = asr(audio_file=filename)
    return result


if __name__ == '__main__':
    filename = input("Enter the filename: ")
    print(speech_to_text(filename))
