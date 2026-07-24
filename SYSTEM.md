# SelectSum: System Overview

## Motivation

Summarizing long speech-based videos (lectures, podcasts, interviews) with a large language model is expensive and produces monolithic output that is hard to navigate. A user interested in only a few topics covered in a 90-minute video should not have to pay the cost of processing the entire transcript.

SelectSum solves this with **topic-based selective summarization**: it automatically segments and labels a video by topic, visualizes each segment, and lets the user request summaries only for the segments they care about. This is the official implementation of the paper *"SelectSum: Topic-Based Selective Summarization of Speech-Based Videos"* (MMM 2025).

---

## System Overview

The system has two phases:

1. **Processing** — runs once per video; produces a set of labeled, visually enriched segments.
2. **Interaction** — the user filters segments by topic and triggers on-demand LLM summarization for selected segments only.

```
Video (YouTube URL or local file)
        │
        ▼
  Audio Extraction  ──►  Transcription  ──►  Primary Merging (~100 words/segment)
                                                        │
                                                        ▼
                                              Topic Modeling (BERTopic)
                                                        │
                                                        ▼
                                          Secondary Merging (~800 words, by topic)
                                                        │
                              ┌─────────────────────────┤
                              ▼                         ▼
                     Keyframe Extraction         Wordcloud Generation
                              │                         │
                              └─────────┬───────────────┘
                                        ▼
                              Interactive Web UI
                                        │
                              (User selects topics)
                                        │
                                        ▼
                            On-Demand Summarization
                         (trim clip → local LLM → output)
```

---

## Pipeline Stages

### 1. Video Ingest
A video enters the system either via a YouTube URL (downloaded with `yt-dlp`) or a local file upload through the Reflex web UI.

### 2. Audio Extraction
`ffmpeg` strips the audio track to a WAV file for transcription.

### 3. Transcription
`stable-whisper` (a word-timestamp-aware Whisper wrapper) transcribes the audio into a sequence of text segments with start/end times.

### 4. Primary Segment Merging
Transcription segments are merged into chunks of approximately **100 words**. Smaller chunks give BERTopic enough resolution to detect distinct topics without overwhelming it with noise.

### 5. Topic Modeling
`BERTopic` assigns a topic to each primary chunk:
- Embeddings are generated with `sentence-transformers` (`BAAI/bge-base-en-v1.5`).
- UMAP reduces the embedding dimensionality.
- KeyBERTInspired extracts the top-5 keywords that represent each topic.

### 6. Secondary Segment Merging
Primary chunks with the same topic are re-merged into larger segments of approximately **800 words**. This produces the final display segments — large enough to summarize meaningfully, still topically coherent.

### 7. Wordcloud Generation
`YAKE` extracts keywords from each segment's text; `wordcloud` renders them into an image weighted by relevance. These images give a quick visual sense of segment content.

### 8. Keyframe Extraction
OpenCV uniformly samples **6 frames** from each segment's time range in the original video, providing visual context alongside the text.

---

## User Interaction

The Reflex web app presents all segments as cards. Each card shows:
- A wordcloud image
- Six keyframe thumbnails
- The segment's topic label

**Topic chips** at the top of the page let the user show or hide segments by topic. Clicking "Summarize" on a card:
1. Trims the video to that segment's time range (ffmpeg).
2. Sends the segment transcript to a locally running OpenAI-compatible LLM server (via the `instructor` library for structured output).
3. Displays the trimmed clip alongside a structured summary: title + bullet points.

Only the segments the user actually requests are ever sent to the LLM, keeping inference costs proportional to user intent.

---

## Key Files

| Path | Responsibility |
|---|---|
| `TaSeSum/TaSeSum.py` | App entry point; `IndexState.process_video()` orchestrates the full pipeline |
| `TaSeSum/state.py` | Shared state classes: `CommonState`, `Segment`, `SummaryFields` |
| `TaSeSum/components/topic_chips.py` | Topic filter UI and filtering logic |
| `TaSeSum/components/summary_card.py` | Per-segment card; triggers `generate_summary()` |
| `TaSeSum/components/download.py` | YouTube URL input |
| `TaSeSum/components/upload.py` | Local file upload |
| `src/transcription.py` | stable-whisper model loader |
| `src/audio_utils.py` | ffmpeg audio extraction |
| `src/video_utils.py` | `VideoReader`, keyframe sampling, video trimming |
| `src/segment_utils.py` | Primary/secondary merging; attaches keyframes and wordclouds |
| `src/topic_modelling.py` | BERTopic topic assignment |
| `src/text_utils.py` | YAKE keyword extraction and wordcloud generation |
| `src/summarization.py` | LLM call via instructor; returns structured `SummaryResponse` |
| `src/downloading.py` | yt-dlp video download |

---

## Technology Stack

| Library | Role |
|---|---|
| [Reflex](https://reflex.dev) | Python-based reactive web framework |
| yt-dlp | YouTube video download |
| ffmpeg-python | Audio extraction and video trimming |
| stable-whisper | Whisper transcription with word-level timestamps |
| BERTopic | Neural topic modeling |
| sentence-transformers | Text embeddings (`BAAI/bge-base-en-v1.5`) |
| UMAP | Dimensionality reduction for embeddings |
| YAKE | Unsupervised keyword extraction |
| wordcloud | Keyword visualization |
| opencv-python | Video frame reading and keyframe sampling |
| instructor + openai | Structured output from a local OpenAI-compatible LLM |
