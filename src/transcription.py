import stable_whisper
from whisper.model import Whisper


def load_stable_whisper_model(model_name: str) -> Whisper:
    model = stable_whisper.load_model(model_name)
    return model


def get_transcript_from_result_dict(result_dict: dict) -> str:
    transcript = result_dict["text"].strip()
    return transcript
