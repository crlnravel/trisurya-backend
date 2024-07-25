from langchain_community.chains.graph_qa.cypher import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import PromptTemplate
from langchain_experimental.sql import SQLDatabaseChain
from langchain_openai import ChatOpenAI
from transformers import AutoConfig, AutoTokenizer, AutoModelForSequenceClassification, T5Tokenizer, \
    T5ForConditionalGeneration

from chatbot import prompts
from chatbot.chatbot import TrisuryaChatbot, Bahasa
from chatbot.classifiers import IndoBertClassifier
from chatbot.rags import Neo4jRAG, PostgreRAG
from chatbot.summarizers import T5Summarizer
from config import Config

llm = ChatOpenAI(api_key=Config.OPENAI_KEY, temperature=0, model="gpt-4o-mini")
rel_db = SQLDatabase.from_uri(Config.POSTGRE_URL)

CYPHER_GENERATION_PROMPT = PromptTemplate(
    input_variables=["schema", "question"], template=prompts.CYPHER_GENERATION_TEMPLATE
)

graph_db = Neo4jGraph(
    url=Config.NEO4J_URL,
    username=Config.NEO4J_USERNAME,
    password=Config.NEO4J_PASSWORD,
)

chain = GraphCypherQAChain.from_llm(llm,
                                    graph=graph_db,
                                    verbose=True,
                                    cypher_prompt=CYPHER_GENERATION_PROMPT)

db_chain = SQLDatabaseChain.from_llm(llm, rel_db, verbose=True)

lang_translator_format = PromptTemplate.from_template(template=prompts.LANG_PROMPT)
is_found_format = PromptTemplate.from_template(template=prompts.CHECK_IS_RAG_PROMPT)
law_llm_format = PromptTemplate.from_template(prompts.LLM_LAW_PROMPT)
nonlaw_llm_format = PromptTemplate.from_template(prompts.LLM_NONLAW_PROMPT)
trl_back_format = PromptTemplate.from_template(prompts.REV_LANG_PROMPT)

graph_rag = Neo4jRAG(
    llm,
    chain
)

relational_rag = PostgreRAG(
    llm,
    db_chain
)

fallback_prompt = {
    'law': law_llm_format,
}


clf_config = AutoConfig.from_pretrained('indobert-base-p1-finetuned_config')
clf_tokenizer = AutoTokenizer.from_pretrained('indobert-base-p1-finetuned_tokenizer')
clf_model = AutoModelForSequenceClassification.from_pretrained(
    'indobert-base-p1-finetuned_trainer',
    config=clf_config,
)

classifier = IndoBertClassifier(
    clf_tokenizer,
    clf_model
)

summ_tokenizer = T5Tokenizer.from_pretrained("panggi/t5-small-indonesian-summarization-cased")
summ_model = T5ForConditionalGeneration.from_pretrained("panggi/t5-small-indonesian-summarization-cased")

summarizer = T5Summarizer(
    summ_tokenizer,
    summ_model
)

cb = TrisuryaChatbot(
    llm,
    graph_rag,
    relational_rag,
    classifier,
    summarizer,
    fallback_prompt=fallback_prompt,
)


async def generate_response(q, lang: Bahasa):
    return await cb.generate(q, lang)
