from src.text_utils import WordCloudGenerator

WORDS_PER_PRIMARY_SEGMENT = 200
WORDS_PER_SECONDARY_SEGMENT = 500


def group_segments_by_word_count(segments: list[dict]) -> list[list[dict]]:
    word_count = 0
    grouped_segments = []
    group = []
    for segment in segments:
        num_words = len(segment["text"].split(" "))
        if word_count + num_words <= WORDS_PER_PRIMARY_SEGMENT:
            word_count += num_words
            group.append(segment)
        else:
            grouped_segments.append(group)
            group = []
            word_count = 0
    if group:
        grouped_segments.append(group)
    return grouped_segments


def add_idx_to_segments(segments: list[dict]) -> list[dict]:
    segments_with_idx = []
    for idx, segment in enumerate(segments):
        segment["idx"] = idx
        segments_with_idx.append(segment)
    return segments_with_idx


def group_segments_by_topic(segments: list[dict]) -> list[list[dict]]:
    if not segments:
        return []

    grouped_segments = []

    prev_topic = segments[0]["topic_id"]
    group = [segments[0]]
    word_count = len(segments[0]["text"].split(" "))
    for segment in segments[1:]:
        topic = segment["topic_id"]
        num_words = len(segment["text"].split(" "))

        if (topic == prev_topic) and (
            (word_count + num_words) <= WORDS_PER_SECONDARY_SEGMENT
        ):
            word_count += num_words
            group.append(segment)
        else:
            grouped_segments.append(group)
            group = [segment]
            prev_topic = topic
            word_count = len(segment["text"].split(" "))
    if group:
        grouped_segments.append(group)
    return grouped_segments


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


def filter_segments_by_topic_id(
    segments: list[dict], topic_id_list: list[int]
) -> list[dict]:
    filtered_segments = []
    for segment in segments:
        if segment["topic_id"] in topic_id_list:
            filtered_segments.append(segment)
    return filtered_segments


def merge_segments_in_group(group: list[dict]) -> dict:
    merged_segment = {}
    merged_text = ""
    # merged_words = []
    # no_speech_probs = []
    for segment in group:
        merged_text += segment["text"]
        # merged_words.append(segment["words"])
        # no_speech_probs.append(segment["no_speech_prob"])
    merged_segment["text"] = merged_text
    merged_segment["start"] = float(group[0]["start"])
    merged_segment["end"] = float(group[-1]["end"])
    # merged_segment["words"] = merged_words
    # merged_segment["no_speech_prob"] = no_speech_probs
    merged_segment["topic_id"] = segment.get("topic_id", None)
    merged_segment["topic_tags"] = segment.get("topic_tags", None)
    return merged_segment


def add_wordcloud_to_segments(
    segments: list[dict], wc_generator: WordCloudGenerator
) -> list[dict]:
    for segment in segments:
        wc_path = wc_generator.generate_word_cloud(segment["text"])
        segment["wordcloud_img_path"] = wc_path
    return segments
