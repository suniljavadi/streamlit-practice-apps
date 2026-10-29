import pytest

from practice_utils import MAX_UPLOAD_BYTES, decode_text_upload, format_chat_export


def test_decode_text_upload_accepts_utf8():
    assert decode_text_upload("Hello, café".encode("utf-8")) == "Hello, café"


def test_decode_text_upload_rejects_files_over_limit():
    with pytest.raises(ValueError, match="1 MB"):
        decode_text_upload(b"x" * (MAX_UPLOAD_BYTES + 1))


def test_decode_text_upload_rejects_invalid_utf8():
    with pytest.raises(ValueError, match="UTF-8"):
        decode_text_upload(b"\xff")


def test_chat_export_contains_only_role_and_content():
    result = format_chat_export(
        [
            {"role": "user", "content": "Hello", "avatar": "private-ui-detail"},
            {"role": "bot", "content": "Hi"},
        ]
    )

    assert result == "user: Hello\nbot: Hi"
    assert "private-ui-detail" not in result
