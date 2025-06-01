from watchdog.observers import Observer

from backend.core import run_llm
import streamlit as st

st.header("Ai conventional chat ")

prompt = st.text_input("Prompt",placeholder="enter your prompt...")

if "chat_answer_history" not in st.session_state:
    st.session_state["chat_answer_history"] = []

if "user_prompt_history" not in st.session_state:
    st.session_state["user_prompt_history"] = []

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []



# def crete_source_string(source_urls: set[str]) -> set:
#     if not source_urls:
#         return ""
#     source_list = list(source_urls)
#     source_list.sort()
#     source_string = "sources:\n"
#     for i, source in enumerate(source_list):
#         source_string += f"{i+1}.{source}\n"
#     return source_string


if prompt:
    with st.spinner("Generating response.."):
        generate_response = run_llm(query=prompt, chat_history=st.session_state["chat_history"])

    formatted_response = (
        f"{generate_response['result']} \n\n"
    )

    st.session_state["user_prompt_history"].append(prompt)
    st.session_state["chat_answer_history"].append(formatted_response)

    st.session_state["chat_history"].append({
        "user": prompt,
        "assistant": generate_response["result"]
    })


if st.session_state["chat_answer_history"]:
    for generate_response, user_query in zip(st.session_state["chat_answer_history"],st.session_state["user_prompt_history"]):
       st.chat_message("user").write(user_query)
       st.chat_message("assistant").write(generate_response)
