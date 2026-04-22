"""Generate fixtures for the Multimodal Meeting Assistant capstone.

- meeting_audio.mp3: TTS-generated ~30s fake meeting clip
- meeting_slide.jpg: PIL-rendered slide with title + bullets + actions

Idempotent.
"""
import os
from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont

MEETING_TEXT = (
    "Hello everyone. This is the Q4 product planning meeting. Our target launch date "
    "is December fifteenth. The allocated budget is fifty thousand dollars, and Sarah "
    "will serve as the team lead on this project. Action item one: Sarah will own "
    "the detailed launch plan and deliver a draft by end of week. Action item two: "
    "We need to schedule a stakeholder review session. That concludes today's meeting. "
    "Thank you all for attending."
)


def make_audio() -> None:
    if os.path.exists("meeting_audio.mp3"):
        print("[fixtures] meeting_audio.mp3 exists, skipping")
        return
    client = OpenAI()
    response = client.audio.speech.create(model="tts-1", voice="alloy", input=MEETING_TEXT)
    response.stream_to_file("meeting_audio.mp3")
    print("[fixtures] wrote meeting_audio.mp3")


def _load_font(size: int) -> ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibri.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def make_slide() -> None:
    if os.path.exists("meeting_slide.jpg"):
        print("[fixtures] meeting_slide.jpg exists, skipping")
        return
    W, H = 1280, 720
    img = Image.new("RGB", (W, H), (248, 248, 252))
    draw = ImageDraw.Draw(img)
    title_font = _load_font(52)
    body_font = _load_font(34)
    action_font = _load_font(28)

    draw.text((60, 40), "Q4 Product Planning", fill=(20, 30, 80), font=title_font)
    bullets = [
        "- Launch date: December 15",
        "- Budget: $50,000",
        "- Team lead: Sarah",
    ]
    y = 150
    for bullet in bullets:
        draw.text((80, y), bullet, fill=(30, 30, 30), font=body_font)
        y += 60

    draw.text((60, 470), "Action Items:", fill=(130, 20, 20), font=body_font)
    actions = [
        "- Sarah owns launch plan (due EOW)",
        "- Schedule stakeholder review session",
    ]
    y = 530
    for a in actions:
        draw.text((80, y), a, fill=(80, 30, 30), font=action_font)
        y += 45

    img.save("meeting_slide.jpg", quality=88)
    print("[fixtures] wrote meeting_slide.jpg")


if __name__ == "__main__":
    make_audio()
    make_slide()
