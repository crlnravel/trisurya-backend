import torch
from transformers import AutoTokenizer, AutoConfig, AutoModelForSequenceClassification


class Classifier:
    TOPICS = ['hukum', 'opendata', 'transportasi']

    def __init__(self):
        pass

    async def predict(self, text) -> str:
        pass


class IndoBertClassifier(Classifier):

    def __init__(self,
                 clf_tokenizer,
                 clf_model):
        super().__init__()
        self.clf_tokenizer = clf_tokenizer
        self.clf_model = clf_model

    async def predict(self, text):
        inputs = self.clf_tokenizer(text, return_tensors="pt")
        outputs = self.clf_model(**inputs)
        logits = outputs.logits

        return Classifier.TOPICS[torch.argmax(logits, dim=1).item()]
