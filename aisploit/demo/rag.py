import textwrap
from typing import List, Any
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableSerializable
from langchain_core.prompts import PromptTemplate
from aisploit.core import BaseModel, BaseVectorStore

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

VECTOR_STORE_RAG_PROMPT = PromptTemplate.from_template(_template)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


class VectorStoreRAG:
    def __init__(
        self,
        *,
        model: BaseModel,
        vectorstore: BaseVectorStore,
        prompt: PromptTemplate = VECTOR_STORE_RAG_PROMPT,
    ) -> None:
        self._vectorstore = vectorstore
        self._retriever = self._vectorstore.as_retriever()

        self._chain: RunnableSerializable[Any, str] = (
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
