import os
import sys
from dotenv import load_dotenv
from utils.config_loader import load_config
from core.logger import LOGGER
from core.exceptions import CustomException
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings


logger_obj = LOGGER.get_logger(__name__)


class ModelLoader:
    def __init__(self):
        load_dotenv()
        self._validate_environment_variables()
        self.config = load_config()
        logger_obj.info("config.yaml loaded successfully", config_keys=list(self.config.keys()))

    def _validate_environment_variables(self):
        required_variables = ["GOOGLE_API_KEY", "GROQ_API_KEY", "PINECONE_API_KEY"]

        self.api_keys = {key: os.getenv(key) for key in required_variables}
        missing = {k for k,v in self.api_keys.items() if not v}

        if missing:
            logger_obj.error("Missing necessary environment variables", missing_vars=missing)
            raise CustomException("Missing necessary environment variables", sys)
        logger_obj.info("Environment variables validated", available_keys=[k for k in self.api_keys if self.api_keys[k]])

    def load_embedding_models(self):
        try:
            model_name = self.config["embedding_model"]["model_name"]
            embedding_model = GoogleGenerativeAIEmbeddings(model=model_name)
            logger_obj.info("Embedding model successfully loaded.")
            return embedding_model
        except Exception as e:
            logger_obj.error("Error while loading embedding model", error=str(e))
            raise CustomException("Error while loading embedding model", sys)

    def load_chat_model(self, provider="google", model_name="gemini-3-pro-preview"):
        try:
            temperature = self.config["llm"][provider]["temperature"]
            max_output_tokens = self.config["llm"][provider]["max_output_tokens"]
            if provider == "google":
                chat_model = ChatGoogleGenerativeAI(model=model_name, temperature=temperature, max_output_tokens=max_output_tokens)
                logger_obj.info(f"{provider.title()}'s {model_name} chat model successfully loaded")
                return chat_model
            logger_obj.error(f"For a chat model {provider.title()} is not valid")
            raise CustomException(f"For a chat model {provider.title()} is not valid", sys)
        except Exception as e:
            logger_obj.error(f"Error while loading {provider.title()}'s {model_name} chat model", error=str(e))
            raise CustomException(f"Error while loading {provider.title()}'s {model_name} chat model", sys)
