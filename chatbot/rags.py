from langchain.chains.base import Chain
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import PromptTemplate

from chatbot import prompts


class RAGBase:
    def __init__(
            self,
            llm: BaseChatModel,
            chain: Chain,
            check_is_rag_prompt: str = prompts.CHECK_IS_RAG_PROMPT,
            check_is_query_prompt: str = prompts.CHECK_IS_QUERY_PROMPT,
    ):
        """
        Base Trisurya RAG class
        :param llm: LLM model used for the RAG
        :param chain: LLM chain
        :param prompt: base prompt for RAG
        :param check_is_rag_prompt: str
        """
        self.llm = llm
        self.chain = chain
        self.check_is_rag_format = PromptTemplate.from_template(template=check_is_rag_prompt)
        self.check_is_query_format = PromptTemplate.from_template(template=check_is_query_prompt)

        self._response = ''

    async def _is_rag(self) -> bool:
        """
        RAG method for checking whether the LLM got the result from the database or from its
        own knowledge.
        :return is_rag: bool
        """

        # Creating question based on the input result.
        q_is_rag = await self.check_is_rag_format.aformat(input=self._response)

        # Tell the llm to decide whether the result came from the database or not
        llm_answer_is_rag = await self.llm.ainvoke(q_is_rag)

        # Creating question based on the input result.
        q_is_query = await self.check_is_query_format.aformat(input=self._response)

        # Check whether the answer is a query or a normal text
        llm_answer_is_query = await self.llm.ainvoke(q_is_query)

        confirming_answers = ['yes', 'iya', 'ya', '\nyes', '\niya', '\nya']
        confirming_in_query = [1, "1"]

        print(llm_answer_is_rag)
        print("#####")
        print(llm_answer_is_query)

        return (llm_answer_is_rag.content.lower() not in confirming_answers) and (
                    llm_answer_is_query.content not in confirming_in_query)

    async def generate_response(
            self,
            q,
            formatter: PromptTemplate = None,
    ) -> dict[str, any]:
        """
        Querying a response from RAG.
        :param q: given input or question
        :param formatter:
        :return: response from chain if and only if the is_rag returns True, returns empty dict otherwise.
        """

        if formatter is None:
            self._response = await self.chain.ainvoke(input=q)
        else:
            formatted_q = await formatter.aformat(question=q)
            self._response = await self.chain.ainvoke(input=formatted_q)

        print("#### BEFORE IS_RAG")

        if await self._is_rag():
            print("#### AFTER IS_RAG")
            return self._response
        print("#### AFTER IS_RAG")

        return {}


class Neo4jRAG(RAGBase):
    def __init__(
            self,
            llm: BaseChatModel,
            chain: Chain,
            check_is_rag_prompt: str = prompts.CHECK_IS_RAG_PROMPT
    ):
        super().__init__(llm, chain, check_is_rag_prompt)


class PostgreRAG(RAGBase):
    def __init__(
            self,
            llm: BaseChatModel,
            chain: Chain,
            check_is_rag_prompt: str = prompts.CHECK_IS_RAG_PROMPT
    ):
        super().__init__(llm, chain, check_is_rag_prompt)
