MAX_UPLOAD_BYTES = 1_000_000
MAX_CHAT_MESSAGES = 50


def decode_text_upload(contents: bytes) -> str:
    if len(contents) > MAX_UPLOAD_BYTES:
        raise ValueError("Text files must be 1 MB or smaller.")
    try:
        return contents.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("The uploaded file must use UTF-8 encoding.") from error


def format_chat_export(messages: list[dict[str, str]]) -> str:
    return "\n".join(
        f"{message['role']}: {message['content']}"
        for message in messages
        if isinstance(message.get("role"), str)
        and isinstance(message.get("content"), str)
    )
