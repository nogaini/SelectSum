from bertopic import BERTopic
from bertopic.representation import KeyBERTInspired


def load_topic_model() -> BERTopic:
    representation_model = KeyBERTInspired()
    topic_model = BERTopic(representation_model=representation_model)
    return topic_model


def add_topic_to_segments(
    segments: list[dict], topic_model: BERTopic
) -> tuple[list[dict], dict[int, list[str]]]:
    segments_with_topics = []
    docs = [segment["text"].strip() for segment in segments]
    topics, _ = topic_model.fit_transform(docs)
    topic_dict = get_topic_dict(topic_model)

    for topic_id, segment in zip(topics, segments):
        segment_with_topic = segment
        segment_with_topic["topic_id"] = topic_id
        segment_with_topic["topic_tags"] = " | ".join(topic_dict[topic_id][:5])
        segments_with_topics.append(segment_with_topic)
    return segments_with_topics, topic_dict


def get_topic_dict(topic_model) -> dict[int]:
    topics_dict = topic_model.get_topics()
    topics_dict_wo_prob = {}
    for topic_id in topics_dict:
        topic_prob_list = topics_dict[topic_id]
        topics = [x[0] for x in topic_prob_list]
        topics_dict_wo_prob[topic_id] = topics
    return topics_dict_wo_prob
