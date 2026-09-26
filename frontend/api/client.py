import os
from typing import Any

import requests


class APIError(RuntimeError):
    """Readable error returned by the LegalEase FastAPI service."""


def api_base_url() -> str:
    return os.getenv("API_BASE_URL", "http://127.0.0.1:8001").rstrip("/")


def _request(
    method: str,
    path: str,
    payload: dict[str, Any] | None = None,
    timeout: int = 95,
) -> requests.Response:
    try:
        response = requests.request(
            method,
            f"{api_base_url()}{path}",
            json=payload,
            timeout=timeout,
        )
    except requests.Timeout as exc:
        raise APIError("The LegalEase service took too long to respond. Please try again.") from exc
    except requests.ConnectionError as exc:
        raise APIError(
            "Unable to reach the LegalEase service. Start the FastAPI backend and check API_BASE_URL in .env."
        ) from exc
    except requests.RequestException as exc:
        raise APIError("The request could not be sent to the LegalEase service.") from exc

    if not response.ok:
        try:
            detail = response.json().get("detail", "")
        except (ValueError, AttributeError):
            detail = ""
        if response.status_code == 503:
            message = detail or "The AI provider is not configured. Check the backend .env settings."
        elif response.status_code == 502:
            message = detail or "The AI provider could not complete the request. Please retry."
        elif response.status_code == 422:
            message = detail or "Some submitted fields are invalid. Review the form and try again."
        else:
            message = detail or f"The service returned an error (HTTP {response.status_code})."
        raise APIError(str(message))
    return response


def _post(path: str, payload: dict[str, Any], timeout: int = 95) -> requests.Response:
    return _request("POST", path, payload, timeout)


def get_ai_provider() -> dict[str, Any]:
    return _request("GET", "/api/settings/ai-provider", timeout=10).json()


def set_ai_provider(provider: str) -> dict[str, Any]:
    if provider not in {"groq", "gemini"}:
        raise ValueError("Unsupported AI provider")
    return _request(
        "PUT",
        "/api/settings/ai-provider",
        {"provider": provider},
        timeout=10,
    ).json()


def generate_document(
    document_type: str,
    party_one: str,
    party_two: str,
    effective_date: str,
    key_terms: str,
) -> dict[str, str]:
    result = _post(
        "/api/documents/generate",
        {
            "document_type": document_type,
            "party_one": party_one,
            "party_two": party_two,
            "effective_date": effective_date,
            "key_terms": key_terms,
        },
    ).json()
    if not isinstance(result.get("document"), str) or not result["document"].strip():
        raise APIError("The AI returned an empty draft. Please try again.")
    return result


def assist(kind: str, text: str) -> str:
    if kind not in {"summary", "explain"}:
        raise ValueError("Unsupported AI action")
    result = _post(f"/api/ai/{kind}", {"text": text}).json()
    answer = result.get("result")
    if not isinstance(answer, str) or not answer.strip():
        raise APIError("The AI returned an empty response. Please try again.")
    return answer


def export_document(file_format: str, text: str) -> tuple[bytes, str]:
    if file_format not in {"pdf", "docx", "txt"}:
        raise ValueError("Unsupported export format")
    response = _post(f"/api/exports/{file_format}", {"text": text}, timeout=30)
    return response.content, response.headers.get("Content-Type", "application/octet-stream")
