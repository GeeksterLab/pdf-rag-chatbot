# ╔════════════════════════════════════════════════════════════╗
# ║ 🚚 IMPORTS
# ╚════════════════════════════════════════════════════════════╝
from pathlib import Path
from typing import List, ClassVar
from pydantic import SecretStr
from pydantic_settings import SettingsConfigDict, BaseSettings


# ╔════════════════════════════════════════════════════════════╗
# ║ ⚙️ CONFIG
# ╚════════════════════════════════════════════════════════════╝
class Settings(BaseSettings):

    # ═════════════════════ APP ═════════════════════
    APP_NAME: str = "medical__rag_chatbot"
    DESCRIPTION: str = (
        "Document-grounded assistant that retrieves relevant chunks, cites its sources and refuses to invent an answer when the evidence is missing."
    )
    VERSION: str = "0.1.0"
    ALLOWED_ORIGINS: List[str] = ["http://localhost:8003", "http://127.0.0.1"]

    # ═════════════════════ PATH ═════════════════════
    BASE_DIR: ClassVar[Path] = Path(__file__).resolve().parents[1]
    DATA_DIR: ClassVar[Path] = BASE_DIR / "data"

    # ═════════════════════ PINECONE + LLM ═════════════════════
    PINECONE_API_KEY: str = ""
    OPENAI_API_KEY: SecretStr = SecretStr("")

    # ═════════════════════ CONFIG ═════════════════════

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore",
        case_sensitive=False,
    )


settings = Settings()
