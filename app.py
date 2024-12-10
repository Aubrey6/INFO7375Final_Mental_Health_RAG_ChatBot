import os
import streamlit as st
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from Prompts import RETRIVAL_PROMPT, HISTORY_PROMPT
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import HumanMessage, AIMessage


load_dotenv()
embedding = OpenAIEmbeddings(
    model='text-embedding-3-small',
    api_key=os.getenv("OPENAI_API_KEY"),
)
vector_store = FAISS.load_local(
    f'./vector_store/',
    embedding,
    allow_dangerous_deserialization=True
)


def load_llm(llm_model):
    try:
        if llm_model == 'gpt-4o-mini':
            llm = ChatOpenAI(
                model="gpt-4o-mini",
                api_key=os.getenv("OPENAI_API_KEY"),
                stream_options={"include_usage": True}
            )
        elif llm_model == "gpt-3.5-turbo":
            llm = ChatOpenAI(
                model="gpt-3.5-turbo",
                api_key=os.getenv("OPENAI_API_KEY"),
                stream_options={"include_usage": True}
            )
        else:
            llm = ChatOpenAI(
                model="Llama3.2",
                api_key=os.getenv("Llama_API_KEY"),
                base_url=os.getenv("Llama_URL"),
                stream_options={"include_usage": True}
            )
        return {'statu': 'success', 'llm_model': llm}
    except Exception as e:
        return {'statu': 'error', 'description': e}


def query(user_input, llm_model):
    llm_res = load_llm(llm_model)
    if llm_res['statu'] == 'error':
        return llm_res
    else:
        llm = llm_res['llm_model']
    if len(st.session_state.chat_history) > 1:
        question_gen = HISTORY_PROMPT | llm | StrOutputParser()
        history = st.session_state.chat_history[:-1] if len(st.session_state.chat_history) < 4 else st.session_state.chat_history[-5:-1]
        print(f'history: {history}')
        chunks = question_gen.stream({
            "chat_history": history,
            "user_input": user_input
        })
        user_input = ''
        for chunk in chunks:
            if chunk:
                user_input += chunk
        print(f'new_user_input: {user_input}')
    doc = vector_store.similarity_search(user_input, k=2)
    docs = [d.page_content for d in doc]
    chain = RETRIVAL_PROMPT | llm | StrOutputParser()
    response = chain.stream({
        "docs": docs,
        "user_input": user_input
    })
    return response


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(page_title="Mental Health QA System", page_icon="🚀")
st.title("Mental Health Chatbot")

llm_model = st.selectbox("Select LLM Model", ["gpt-3.5-turbo", "gpt-4o-mini", "Llama3.2"])

user_input = ''
for i in range(len(st.session_state.chat_history)):
    message = st.session_state.chat_history[i]
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.write(message.content)
    else:
        with st.chat_message("assistant"):
            st.write(message.content)

if not user_input:
    user_input = st.chat_input("Ask any question to me...")
if user_input is not None and user_input != (" " * len(user_input)):
    st.session_state.chat_history.append(HumanMessage(user_input))
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        ai_output = st.write_stream(query(user_input, llm_model))
    st.session_state.chat_history.append(AIMessage(ai_output))
else:
    print("It's a Empty Input!")
