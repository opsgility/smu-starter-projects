"""
Capstone Project: Multimodal Meeting Assistant
Course 203 - Lesson 10: Capstone Project

Build a meeting assistant that:
1. Transcribes meeting audio with Whisper (word timestamps)
2. Analyzes shared screen/slides with GPT-4o vision
3. Generates a structured meeting report with GPT-4.1
4. Narrates the summary with TTS (gpt-4o-mini-tts)
5. Outputs a complete meeting package: transcript + report JSON + audio

IMPORTANT: OPENAI_API_KEY and OPENAI_BASE_URL are pre-configured in your
environment automatically. Do NOT set them manually.
"""
from openai import OpenAI
from pydantic import BaseModel
import base64
import json
import os
import time

client = OpenAI()

# Input files (provided in lab environment)
MEETING_AUDIO_PATH = "meeting_audio.mp3"
SLIDE_IMAGE_PATH = "meeting_slide.jpg"    # Screenshot of shared screen/slide

# Output files
TRANSCRIPT_PATH = "meeting_transcript.json"
REPORT_PATH = "meeting_report.json"
AUDIO_SUMMARY_PATH = "meeting_summary.mp3"


# -----------------------------------------------------------------------
# Step 1: Audio transcription
# -----------------------------------------------------------------------

class TranscriptSegment(BaseModel):
    text: str
    start: float
    end: float


def transcribe_meeting(audio_path: str) -> dict:
    """
    Exercise 1: Transcribe meeting audio with word-level timestamps.

    Use client.audio.transcriptions.create() with:
    - model="whisper-1"
    - response_format="verbose_json"
    - timestamp_granularities=["word", "segment"]

    Returns:
        Dict with: text (full transcript), words (list), duration (seconds)
    """
    with open(audio_path, "rb") as f:
        # TODO: Call client.audio.transcriptions.create() with verbose_json
        # TODO: Return {"text": ..., "words": [...], "duration": ...}
        pass


# -----------------------------------------------------------------------
# Step 2: Visual analysis
# -----------------------------------------------------------------------

class SlideAnalysis(BaseModel):
    title: str
    key_points: list[str]
    action_items: list[str]
    questions_raised: list[str]


def analyze_slide(image_path: str) -> SlideAnalysis:
    """
    Exercise 2: Analyze a meeting slide or screen capture with GPT-4o.

    Use client.responses.parse() with:
    - model="gpt-4o"
    - Multi-modal input: system message + user message with image
    - text_format=SlideAnalysis

    System prompt: "You are a meeting analyst. Extract key information
    from meeting slides and presentations."

    Returns:
        SlideAnalysis with title, key_points, action_items, questions_raised
    """
    system = "You are a meeting analyst. Extract key information from meeting slides and presentations."

    with open(image_path, "rb") as f:
        b64_data = base64.b64encode(f.read()).decode("utf-8")

    # TODO: Call client.responses.parse() with model="gpt-4o"
    # TODO: Include the image as base64 in the user message content
    # TODO: Use text_format=SlideAnalysis
    # TODO: Return response.output_parsed
    pass


# -----------------------------------------------------------------------
# Step 3: Meeting report generation
# -----------------------------------------------------------------------

class ActionItem(BaseModel):
    task: str
    owner: str
    due_date: str


class MeetingReport(BaseModel):
    meeting_title: str
    date: str
    duration_minutes: float
    executive_summary: str
    key_decisions: list[str]
    action_items: list[ActionItem]
    follow_up_topics: list[str]
    sentiment: str   # "positive", "neutral", "negative", "mixed"


def generate_meeting_report(transcript: str, slide_analysis: SlideAnalysis,
                             duration_seconds: float) -> MeetingReport:
    """
    Exercise 3: Generate a structured meeting report from transcript + slides.

    Use client.responses.parse() with:
    - model="gpt-4.1"
    - Combined input: transcript text + slide analysis JSON
    - text_format=MeetingReport

    System prompt: "You are a professional meeting summarizer. Create
    comprehensive meeting reports with action items and decisions."

    Returns:
        MeetingReport — fully structured meeting summary
    """
    system = """You are a professional meeting summarizer. Create comprehensive meeting
reports with clear action items, key decisions, and executive summaries."""

    context = f"""Meeting transcript:
{transcript}

Slide/visual content analysis:
{json.dumps(slide_analysis.model_dump() if slide_analysis else {}, indent=2)}

Meeting duration: {duration_seconds/60:.1f} minutes"""

    # TODO: Call client.responses.parse() with model="gpt-4.1"
    # TODO: Include system + user messages with transcript and slide data
    # TODO: Use text_format=MeetingReport
    # TODO: Return response.output_parsed
    pass


# -----------------------------------------------------------------------
# Step 4: TTS narration
# -----------------------------------------------------------------------

def narrate_summary(report: MeetingReport, output_path: str = AUDIO_SUMMARY_PATH) -> str:
    """
    Exercise 4: Convert meeting summary to audio with expressive TTS.

    Build a concise spoken summary from the MeetingReport:
    "Meeting: {title}. {executive_summary}. Key decisions: ...
    Action items: ..."

    Use client.audio.speech.create() with:
    - model="gpt-4o-mini-tts"
    - voice="alloy"
    - input=summary_text
    - instructions="Speak professionally and clearly, like a business meeting narrator."

    Returns:
        output_path
    """
    if not report:
        return ""

    # Build spoken summary
    decisions_text = ". ".join(report.key_decisions[:3]) if report.key_decisions else "None recorded."
    actions_text = ". ".join([f"{a.task} — assigned to {a.owner}" for a in report.action_items[:3]])

    summary_text = (
        f"Meeting summary for {report.meeting_title}. "
        f"{report.executive_summary} "
        f"Key decisions: {decisions_text}. "
        f"Action items: {actions_text}."
    )

    instructions = "Speak professionally and clearly, like a business executive summarizing a meeting for busy stakeholders."

    # TODO: Call client.audio.speech.create() with gpt-4o-mini-tts
    # TODO: Use instructions parameter for expressive style
    # TODO: Save via response.stream_to_file(output_path)
    # TODO: Return output_path
    pass


# -----------------------------------------------------------------------
# Step 5: Full pipeline
# -----------------------------------------------------------------------

def run_meeting_assistant(audio_path: str, slide_path: str) -> dict:
    """
    Exercise 5: Orchestrate the full meeting assistant pipeline.

    Steps:
    1. Transcribe audio → get transcript + duration
    2. Analyze slide → get SlideAnalysis (if slide_path exists)
    3. Generate MeetingReport from transcript + slide analysis
    4. Narrate summary with TTS
    5. Save transcript JSON, report JSON, audio file

    Returns:
        Dict with paths to all output files and the report data
    """
    print("Starting meeting assistant pipeline...")
    results = {}

    # Step 1: Transcription
    print("  [1/4] Transcribing audio...")
    # TODO: Call transcribe_meeting(audio_path)
    # TODO: Save transcript to TRANSCRIPT_PATH as JSON
    # TODO: Store in results["transcript_path"]

    # Step 2: Slide analysis
    print("  [2/4] Analyzing slides...")
    slide_analysis = None
    if os.path.exists(slide_path):
        # TODO: Call analyze_slide(slide_path)
        pass

    # Step 3: Report generation
    print("  [3/4] Generating report...")
    # TODO: Call generate_meeting_report(transcript_text, slide_analysis, duration)
    # TODO: Save report to REPORT_PATH as JSON
    # TODO: Store in results["report_path"]

    # Step 4: TTS narration
    print("  [4/4] Narrating summary...")
    # TODO: Call narrate_summary(report, AUDIO_SUMMARY_PATH)
    # TODO: Store in results["audio_path"]

    return results


# -----------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------

if __name__ == "__main__":
    print("Multimodal Meeting Assistant - Capstone")
    print("=" * 60)

    if not os.path.exists(MEETING_AUDIO_PATH):
        print(f"\nNote: Place a meeting recording at '{MEETING_AUDIO_PATH}' to run the full pipeline.")
        print("The pipeline requires: meeting_audio.mp3 (required), meeting_slide.jpg (optional)")
    else:
        results = run_meeting_assistant(MEETING_AUDIO_PATH, SLIDE_IMAGE_PATH)
        print("\nMeeting Assistant Complete!")
        print(f"  Transcript: {results.get('transcript_path', 'N/A')}")
        print(f"  Report:     {results.get('report_path', 'N/A')}")
        print(f"  Audio:      {results.get('audio_path', 'N/A')}")

        # Display report summary
        if os.path.exists(REPORT_PATH):
            with open(REPORT_PATH) as f:
                report_data = json.load(f)
            print(f"\nMeeting: {report_data.get('meeting_title')}")
            print(f"Summary: {report_data.get('executive_summary', '')[:200]}...")
            print(f"Action items: {len(report_data.get('action_items', []))}")
