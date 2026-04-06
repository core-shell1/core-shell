import uuid
import time
from typing import Optional

# 서버 메모리 기반 세션 저장소
# {session_id: {"messages": [...], "last_active": timestamp, "created_at": timestamp}}
SESSIONS: dict = {}

SESSION_TTL = 86400  # 24시간 (초 단위)
MAX_HISTORY = 20     # 세션당 최대 메시지 수


def create_session() -> str:
    """새 세션 생성 후 session_id 반환."""
    session_id = str(uuid.uuid4())
    now = time.time()
    SESSIONS[session_id] = {
        "messages": [],
        "last_active": now,
        "created_at": now,
    }
    return session_id


def get_session(session_id: str) -> Optional[dict]:
    """
    세션 조회. 없거나 만료된 경우 None 반환.
    유효한 경우 last_active 갱신.
    """
    session = SESSIONS.get(session_id)
    if session is None:
        return None

    # TTL 체크
    if time.time() - session["last_active"] > SESSION_TTL:
        del SESSIONS[session_id]
        return None

    session["last_active"] = time.time()
    return session


def add_message(session_id: str, role: str, content: str) -> bool:
    """
    세션에 메시지 추가.
    20턴 초과 시 가장 오래된 항목 제거 (FIFO).
    세션이 없으면 False 반환.
    """
    session = SESSIONS.get(session_id)
    if session is None:
        return False

    session["messages"].append({"role": role, "content": content})
    session["last_active"] = time.time()

    # MAX_HISTORY 초과 시 앞에서 제거
    if len(session["messages"]) > MAX_HISTORY:
        session["messages"] = session["messages"][-MAX_HISTORY:]

    return True


def get_history(session_id: str) -> list:
    """
    세션 히스토리 반환.
    Claude API에 넘길 때는 최근 10턴만 사용 권장.
    세션 없으면 빈 리스트 반환.
    """
    session = SESSIONS.get(session_id)
    if session is None:
        return []
    return session["messages"]


def get_or_create_session(session_id: Optional[str]) -> tuple[str, bool]:
    """
    session_id가 있으면 기존 세션 반환,
    없거나 만료됐으면 새 세션 생성.
    Returns: (session_id, is_new)
    """
    if session_id:
        session = get_session(session_id)
        if session is not None:
            return session_id, False

    new_id = create_session()
    return new_id, True


def cleanup_expired() -> int:
    """
    만료된 세션 삭제.
    APScheduler가 1시간마다 호출.
    삭제된 세션 수 반환.
    """
    now = time.time()
    expired = [
        sid for sid, session in SESSIONS.items()
        if now - session["last_active"] > SESSION_TTL
    ]
    for sid in expired:
        del SESSIONS[sid]
    return len(expired)


def active_session_count() -> int:
    """현재 활성 세션 수 반환."""
    return len(SESSIONS)
