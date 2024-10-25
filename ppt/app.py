import streamlit as st
import ollama
from pkg.ppt_gen import data_helper
from pkg.llm import generate_ppt_stream
from pkg.ppt_gen import pptx_helper
import json
import os

st.title("Yuan PPT Writer")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "prompt_history" not in st.session_state:
    st.session_state.prompt_history = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
template = st.radio("选择模板",("绚烂","青春","水冷","商务灰","商务红"))
mode = template +".pptx"
current_work_path = os.path.join(os.getcwd(), "icons", "template_background",mode)

# Accept user input
if prompt := st.chat_input("以“人工智能未来发展”为主题，生成一个ppt"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"): st.markdown(prompt)

    # Display assistant response in chat message container
    responses =""
    with st.chat_message("assistant"):
        responses = st.write_stream(generate_ppt_stream.generate_outline_from_api(prompt))
        # responses = st.write_stream(generate_ppt_stream.generate_body_stream_from_api(res))
        progress_bar = st.progress(0,"正在制作PPT...")
        prompt_ppt = responses
        try:
            data = data_helper.cleaned_slide_data(prompt_ppt)
        except json.decoder.JSONDecodeError:
            st.write("json格式有误，尝试修复...")
            prompt_ppt = generate_ppt_stream.fix_json(prompt_ppt)
            try:
                data = data_helper.cleaned_slide_data(prompt_ppt)
            except json.decoder.JSONDecodeError:
                st.write("修复失败，请重新提问。")
            else:
                progress_bar.progress(0.5,text="内容生成成功，正在制作PPT，正在生成PPT...")
                file_path = pptx_helper.generate_powerpoint_presentation(data,current_work_path,template)
                file_name = data["title"]+".pptx"
                progress_bar.progress(1.0,text="PPT制作完成!")
                st.download_button(label="下载PPT",
                                        data=file_path,
                                        file_name=file_name,
                                        mime="presentation/vnd.openxmlformats-officedocument.presentationml.presentation")
            
        else:
            progress_bar.progress(0.5,text="内容生成成功，正在制作PPT，正在生成PPT...")
            file_path = pptx_helper.generate_powerpoint_presentation(data,current_work_path,template)
            file_name = data["title"]+".pptx"
            progress_bar.progress(1.0,text="PPT制作完成!")
            st.download_button(label="下载PPT",
                                    data=file_path,
                                    file_name=file_name,
                                    mime="presentation/vnd.openxmlformats-officedocument.presentationml.presentation")
     
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": responses})



