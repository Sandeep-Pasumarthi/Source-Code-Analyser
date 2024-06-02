from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings

from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

from dotenv import load_dotenv

import os

load_dotenv()
session_store = dict()


class ChatWithGemini:
    def __init__(self, namespace: str, repo_id: str):
        self.namespace = namespace
        self.repo_id = repo_id
        self.vector_store = PineconeVectorStore.from_existing_index(index_name=os.getenv("PINECONE_INDEX"), namespace=namespace, 
                                                                    embedding=OpenAIEmbeddings(model=os.getenv("EMBEDDING_MODEL"), dimensions=1024), 
                                                                    text_key=os.getenv("PINECONE_TEXT_KEY"))
        self.retriever = self.vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 8, "filter": {"repo_id": self.repo_id}})
        self.gemini = ChatGoogleGenerativeAI(model=os.getenv("GEMINI_CHAT_MODEL"), temperature=0.2, top_p=0.9)
    
    def __initiate_contextualize_retriever(self) -> None:
        system_prompt = """
        Given chat history and user question which might reference context in the chat history, formulate a standalone question which can be understood without the chat history.
        Don't answer the question. Reformat it if needed otherwise return the question as it is.
        """
        contextualize_prompt = ChatPromptTemplate.from_messages([
            ("human", system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}")
        ])
        self.history_aware_retriever = create_history_aware_retriever(llm=self.gemini, retriever=self.retriever, prompt=contextualize_prompt)
    
    def __initiate_retrieval_chain(self) -> None:
        system_prompt = """
        You are Code Brahma bot working at Arjuna AI developed by Sandeep Pasumarthi. You are highly skilled mentor for programmers. 
        Who Explains complex code repositories in easy understandable way. You are given user query, relevant context information and chat history.
        Your task is to answer the query based on the context and source code provided.
        
        Context:
        {context}
        
        Set the output tone to simple wording and professional. Be clear and concise.
        """
        prompt = ChatPromptTemplate.from_messages([
            ("human", system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}")
        ])

        self.qa_chain = create_stuff_documents_chain(llm=self.gemini, prompt=prompt)
        self.rag_chain = create_retrieval_chain(self.history_aware_retriever, self.qa_chain)
    
    def __initiate_chat_history(self) -> None:
        self.conversational_rag_chain = RunnableWithMessageHistory(self.rag_chain, get_session_history, 
                                                                   input_messages_key="input",
                                                                   history_messages_key="chat_history",
                                                                   output_messages_key="answer")
    
    def initiate_chat(self) -> None:
        self.__initiate_contextualize_retriever()
        self.__initiate_retrieval_chain()
        self.__initiate_chat_history()
    
    def chat(self, query: str, session_id: str) -> str:
        return self.conversational_rag_chain.invoke({"input": query}, config={"configurable": {"session_id": session_id}})["answer"]


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in session_store:
        session_store[session_id] = ChatMessageHistory()
    return session_store[session_id]
