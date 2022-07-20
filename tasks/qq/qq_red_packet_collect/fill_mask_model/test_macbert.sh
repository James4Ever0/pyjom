curl https://api-inference.huggingface.co/models/hfl/chinese-macbert-base \
	-X POST \
	-d '{"inputs": "我感冒了，今天天气[MASK]"}' \
	-H "Authorization: Bearer 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"
