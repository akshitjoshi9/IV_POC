from pydantic_settings import BaseSettings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings


class Settings(BaseSettings):

    DATABASE_URL_ML_ENGINE: str
    LLM_MODEL: str
    OPENAI_API_KEY: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    DEFAULT_PAGE_SIZE: int
    MAX_PAGE_SIZE: int
    MONGODB_URL: str
    MONGODB_DB: str
    MONGODB_COLLECTION: str
    COMPANY_FOOTER: str

    # redis databases
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_COMMON_DB: str
    REDIS_MEMORY_DB: str
    REDIS_MESSAGE_STREAMING_DB: str

    MILVUS_HOST: str
    MILVUS_PORT: int

    class Config:
        env_file = ".env"


settings = Settings()


llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.4,
    api_key=settings.OPENAI_API_KEY,
)

embedding = OpenAIEmbeddings(
    model="text-embedding-ada-002",
    openai_api_key=settings.OPENAI_API_KEY
)