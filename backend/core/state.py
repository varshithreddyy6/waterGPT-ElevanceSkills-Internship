from utils.rag_engine import RAGEngine
from utils.sentiment import SentimentAnalyzer
from utils.translator import Translator
from utils.image_handler import ImageHandler
from utils.gemini_vision_handler import GeminiVisionHandler
from utils.updater import KnowledgeUpdater
from utils.research_engine import ResearchEngine


rag = RAGEngine()
sentiment_analyzer = SentimentAnalyzer()
translator = Translator()
image_handler = ImageHandler()
gemini_vision = GeminiVisionHandler()
updater = KnowledgeUpdater(rag=rag)
research_engine = ResearchEngine()