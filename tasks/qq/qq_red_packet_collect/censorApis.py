import requests
from chat_local import getLinearSentiment, getAbsSentiment


def censorReply(reply, moderate=True):
    url = "http://127.0.0.1:8932/filter"
    response = requests.get(url, params={"text": reply, "moderate": moderate})
    response = response.json()
    reply = response["response"]
    return reply


def censorReplyAbsSentiment(
    reply, moderate=True, sentiment_abs_level=0.6, censored_sentiment_threshold=0.8
):
    sentiment = getAbsSentiment(reply)

    if sentiment > sentiment_abs_level:
        reply = censorReply(reply)
        censored_sentiment = getAbsSentiment(reply)
        if censored_sentiment > censored_sentiment_threshold:
            return None
    return reply


# however these sentiment based function will not work very well since the positive/negative flag is not working properly for sentence like "操你妈" -> ("positive", 0.8)


def censorReplyLinearSentiment(reply, moderate=True, sentiment_level=-0.9):
    sentiment = getLinearSentiment(reply)

    if sentiment < sentiment_level:
        reply = censorReply(reply)
    return reply


def censorReplySentimentDelta(reply, moderate=True, sentiment_delta_level=0.5):
    reply2 = censorReply(reply)

    sentiment = getLinearSentiment(reply)
    sentiment2 = getLinearSentiment(reply2)

    sentiment_delta = sentiment2 - sentiment
    if sentiment_delta < sentiment_delta_level:  # is that good?
        return reply
    else:
        return reply2
