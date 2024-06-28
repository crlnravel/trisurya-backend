import time
from enum import Enum

from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import PromptTemplate

from chatbot import prompts
from chatbot.classifiers import Classifier
from chatbot.rags import RAGBase
from chatbot.summarizers import Summarizer


class Bahasa(Enum):
    INDONESIA = 'indonesia', '\nindonesia'
    JAWA = 'jawa', '\njawa'
    SUNDA = 'sunda', '\nsunda'
    BALI = 'bali', '\nbali'


class TrisuryaChatbot:

    def __init__(
            self,
            llm: BaseChatModel,
            graph_rag: RAGBase,
            relational_rag: RAGBase,
            classifier: Classifier,
            summarizer: Summarizer,
            fallback_prompt: dict[str, PromptTemplate] = None,
    ):
        self.llm = llm
        self.graph_rag = graph_rag
        self.relational_rag = relational_rag
        self.fallback_prompt = fallback_prompt or {}
        self.classifier = classifier
        self.summarizer = summarizer

        self._response = None
        self._progress = 0
        self._process_txt = ""
        self._progress_bar = None

    async def _translate(self, lang: Bahasa, reverse=False):

        if not self._response:
            raise Exception("The response is still empty")

        if reverse:
            tl_prompt_format = PromptTemplate.from_template(prompts.LANG_PROMPT)
        else:
            tl_prompt_format = PromptTemplate.from_template(prompts.REV_LANG_PROMPT)

        tl_prompt = await tl_prompt_format.aformat(input=self._response, lang=lang.value)

        self._response = await self.llm.ainvoke(tl_prompt)

    async def generate(self, q, lang: Bahasa, q1: str = '', q2: str = '', q3: str = ''):

        # set default value for response
        self._response = q

        # TRANSLATION LAYER
        await self._translate(lang)

        # SUMMARIZATION LAYER
        summary = ''

        if q1 != '' or q2 != '' or q3 != '':
            summary = await self.summarizer.summarize(q1 + q2 + q3)

        self._response = summary + q

        # CLASSIFICATION LAYER
        topic = await self.classifier.predict(self._response)

        # RAG LAYER
        if topic == 'law':
            rag_ans = await self.graph_rag.generate_response(self._response)
        else:
            rag_ans = await self.relational_rag.generate_response(
                self._response,
                PromptTemplate.from_template(prompts.POSTGRE_PROMPT)
            )

        # RAG FILTER LAYER
        # Check whether the rag gave the appropriate response

        # Enter fallback prompt and ask the LLM for the information
        if len(rag_ans) == 0:

            if topic in self.fallback_prompt:
                formatted = await self.fallback_prompt[topic].aformat(input=self._response)
            else:
                formatted = await (PromptTemplate
                                   .from_template(prompts.LLM_NONLAW_PROMPT)
                                   .aformat(input=self._response))
            self._response = (await self.llm.ainvoke(formatted)).content
        else:
            self._response = rag_ans['result']

        # BACK TRANSLATION LAYER
        if lang != Bahasa.INDONESIA:
            await self._translate(lang, reverse=True)

        if len(rag_ans) == 0:
            self._response += (". \nCatatan: Informasi ini masih perlu dipastikan "
                               "kebenarannya karena belum terdaftar di database kami.")

        return self._response
