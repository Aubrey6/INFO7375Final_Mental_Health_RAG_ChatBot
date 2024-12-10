from langchain_core.prompts import ChatPromptTemplate


_HISTORY_TEMPLATE = """Given a chat history and the latest user question which might reference context in the chat history,

formulate a standalone question which can be understood without the chat history. Do NOT answer the question,

just reformulate it if needed and otherwise return it as is.

<chat_history>
{chat_history}
</chat_history>

user's question: {user_input}
"""
HISTORY_PROMPT = ChatPromptTemplate.from_template(_HISTORY_TEMPLATE)


_RETRIVAL_TEMPLATE = """You are a mental health expert, and your task is to answer the user's questions in a friendly and empathetic manner. 

You will be provided with reference documents related to mental health topics. You should use these documents when answering any questions related to mental health. 

Do not make up answers; always refer to the provided documents if they contain the necessary information.

<document>
{docs}
</document>

user's question:
{user_input}
"""
RETRIVAL_PROMPT = ChatPromptTemplate.from_template(_RETRIVAL_TEMPLATE)
