import pandas as pd
import streamlit as st
from utils import dataframe_agent

st.title("csv数据分析智能工具")

with st.sidebar:
    api_key =  st.text_input("请输入OPENAI_API秘钥", type="password")

def gen_chart(ai_response):
    output_type = list(ai_response.keys())[0]
    output_data = ai_response[output_type]
    #with st.expander("ai回答"):
    #st.write("AI输出：")
    #st.write(output_data)

    if output_type == "answer":
        #st.write(output_data)
        st.chat_message("ai").write(output_data)
    elif output_type == "table":
        st.chat_message("ai").write("数据如下：")
        st.dataframe(pd.DataFrame(output_data["data"], columns=output_data["columns"]))
    elif output_type == "bar" or output_type == "line" or output_type == "scatter":
        df_data = pd.DataFrame(output_data["data"], columns=output_data["columns"])
        df_data.set_index(output_data["columns"][0], inplace=True)
        if output_type == "bar":
            st.chat_message("ai").write("条形图如下：")
            st.bar_chart(df_data)
        elif output_type == "line":
            st.chat_message("ai").write("折线图如下：")
            st.line_chart(df_data)
        elif output_type == "scatter":
            st.chat_message("ai").write("散点图如下：")
            st.scatter_chart(df_data)

upload_file = st.file_uploader("请上传需要分析的csv文件", type=["csv"])
if upload_file :
    if "df" not in st.session_state or st.session_state["file_name"] != upload_file.name:
        st.session_state["file_name"] = upload_file.name
        st.session_state["df"] = pd.read_csv(upload_file)

if "df" in st.session_state:
    with st.expander("原始数据"):
        st.dataframe(st.session_state["df"])

    query = st.text_area("请输入你的问题，如数据提取请求，可视化要求（支持散点图、折线图、条形图）")
    button = st.button("生成回答")

    if button:
        if not api_key:
            st.info("请输入你的OPENAI API秘钥")
            st.stop()
        if not query :
            st.info("请输入你的问题")
            st.stop()

        with st.spinner("AI正在思考中，请稍等 ..."):
            res = dataframe_agent(openai_api_key=api_key, df = st.session_state["df"], query=query)

        if "res_list" in st.session_state:
            st.session_state["query"].append(query)
            st.session_state["res_list"].append(res)
        else:
            st.session_state["res_list"] = [res]
            st.session_state["query"] = [query]

        gen_chart(res)

        if "res_list" in st.session_state and len(st.session_state["res_list"])>1:
            with st.expander("历史问答"):
                for i in range(len(st.session_state["res_list"])-2,-1,-1):
                    res = st.session_state["res_list"][i]
                    question = st.session_state["query"][i]
                    #st.write(question)
                    st.chat_message("human").write(question)
                    gen_chart(res)
                    st.divider()
                    
