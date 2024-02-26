import textwrap
from typing import List
from langchain_community.vectorstores.chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from aisploit.core import BaseModel, BaseEmbeddings

_template = textwrap.dedent(
    """
    You are a helpful assistant, tasked with answering user queries based on 
    relevant contexts provided. If the answer cannot be found, respond with 
    "I don't know".

    Contexts: ```{context}```

    Query: ```{question}```

    Answer:
    """
)

GENERIC_RAG_PROMPT = PromptTemplate.from_template(_template)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


class GenericRAG:
    def __init__(
        self,
        *,
        model: BaseModel,
        embeddings: BaseEmbeddings,
        prompt: PromptTemplate = GENERIC_RAG_PROMPT,
    ) -> None:
        self._vectorstore = Chroma(
            embedding_function=embeddings,
        )

        self._retriever = self._vectorstore.as_retriever()

        self._chain = (
            {
                "context": self._retriever | format_docs,
                "question": RunnablePassthrough(),
            }
            | prompt
            | model
            | StrOutputParser()
        )

    def invoke(self, input: str) -> str:
        return self._chain.invoke(input)

    def add_texts(self, texts: List[str]) -> None:
        self._vectorstore.add_texts(texts=texts)

    def retrieve(self, input: str) -> List[str]:
        docs = self._retriever.invoke(input=input)
        return [doc.page_content for doc in docs]
