from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class SentimentAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze(self, text):
        scores = self.analyzer.polarity_scores(text or "")
        compound = scores["compound"]

        if compound >= 0.05:
            sentiment = "positive"
        elif compound <= -0.05:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        return {
            "sentiment": sentiment,
            "score": compound,
            "details": scores,
        }

    def get_response_tone(self, sentiment):
        tones = {
            "positive": "Respond in an enthusiastic and encouraging tone.",
            "negative": (
                "Respond with empathy and understanding. "
                "Be supportive and helpful."
            ),
            "neutral": "Respond in a clear, informative, and professional tone.",
        }

        return tones.get(sentiment, tones["neutral"])