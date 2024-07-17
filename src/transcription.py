import stable_whisper
from whisper.model import Whisper

WORDS_PER_CHUNK = 1500


def load_stable_whisper_model(model_name: str) -> Whisper:
    model = stable_whisper.load_model(model_name)
    return model


def get_transcript_from_result_dict(result_dict: dict) -> str:
    transcript = result_dict["text"].strip()
    return transcript


def group_segments_by_word_count(segments: list[dict]) -> list[list[dict]]:
    word_count = 0
    grouped_segments = []
    group = []
    for segment in segments:
        num_words = len(segment["text"].split(" "))
        if word_count + num_words <= WORDS_PER_CHUNK:
            word_count += num_words
            group.append(segment)
        else:
            grouped_segments.append(group)
            group = []
            word_count = 0
    return grouped_segments


def group_segments_by_topic(segments: list[dict]) -> list[list[dict]]:
    grouped_segments = []
    group = []

    for segment in segments:
        topic_id = segment["topic_id"]


def merge_segments_secondary(segments: list[dict]) -> list[list[dict]]:
    grouped_segments = group_segments_by_topic(segments)
    merged_segments = []
    for group in grouped_segments:
        merged_segment = merge_segments_in_group(group)
        merged_segments.append(merged_segment)
    return merged_segments


def merge_segments_primary(segments: list[dict]) -> list[dict]:
    grouped_segments = group_segments_by_word_count(segments)
    merged_segments = []
    for group in grouped_segments:
        merged_segment = merge_segments_in_group(group)
        merged_segments.append(merged_segment)
    return merged_segments


def filter_segments_by_duration(
    segments: list[dict], duration_threshold: float = 2
) -> list[dict]:
    filtered_segments = []
    for segment in segments:
        if (segment["end"] - segment["start"]) < duration_threshold:
            continue
        filtered_segments.append(segment)
    return filtered_segments


def merge_segments_in_group(group: list[dict]) -> dict:
    merged_segment = {}
    merged_text = ""
    merged_words = []
    no_speech_probs = []
    for segment in group:
        merged_text += segment["text"]
        merged_words.append(segment["words"])
        no_speech_probs.append(segment["no_speech_prob"])
    merged_segment["text"] = merged_text
    merged_segment["start"] = group[0]["start"]
    merged_segment["end"] = group[-1]["end"]
    merged_segment["words"] = merged_words
    merged_segment["no_speech_prob"] = no_speech_probs
    return merged_segment
