from transformers import T5Tokenizer, T5ForConditionalGeneration


class Summarizer:

    def __init__(self):
        pass

    async def summarize(self, text) -> str:
        pass


class T5Summarizer(Summarizer):

    def __init__(self,
                 summ_tokenizer,
                 summ_model):
        super().__init__()
        self.summ_tokenizer = summ_tokenizer
        self.summ_model = summ_model

    async def summarize(self, text):
        input_ids = self.summ_tokenizer.encode(text, return_tensors='pt')
        summary_ids = self.summ_model.generate(input_ids,
                                               max_length=150,
                                               num_beams=2,
                                               repetition_penalty=2.5,
                                               length_penalty=1.0,
                                               early_stopping=True,
                                               no_repeat_ngram_size=2,
                                               use_cache=True)
        return self.summ_tokenizer.decode(summary_ids[0], skip_special_tokens=True)
