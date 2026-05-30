from utils.rag_engine import RAGEngine
from utils.sentiment import SentimentAnalyzer
from utils.translator import Translator
from utils.image_handler import ImageHandler
from utils.updater import KnowledgeUpdater


rag = RAGEngine()
sentiment_analyzer = SentimentAnalyzer()
translator = Translator()
image_handler = ImageHandler()
updater = KnowledgeUpdater(rag=rag)