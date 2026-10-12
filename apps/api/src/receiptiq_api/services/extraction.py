import base64
from pathlib import Path

from anthropic import Anthropic

from ..config import settings
from ..schemas import ReceiptCreate

PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "extract_receipt_v1.md"
MODEL = "claude-opus-4-7"

_client = Anthropic(api_key=settings.anthropic_api_key)


def extract(image_bytes: bytes) -> ReceiptCreate:
    prompt = PROMPT_PATH.read_text()
    image_b64 = base64.standard_b64encode(image_bytes).decode()

    _response = _client.messages.create(
        model=MODEL,
        max_tokens=2048,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image_b64,
                        },
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ],
    )
    raise NotImplementedError("parse model JSON output into ReceiptCreate")
