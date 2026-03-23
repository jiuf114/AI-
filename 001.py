import os
import streamlit as st
from openai import OpenAI
from pyexpat.errors import messages

version = "beta.1.0"
gener_in = False
#提示词
# system_promt = (
#     "在与我踏上逃亡之旅之后，经过长时间的相处，我们之间逐渐有了好感，彼此之间都依赖着对方;前情提要:火光、爆炸与呼救声交织在一起...即使双手早已沾满鲜血，年轻的小米莉拉依旧无法忘记那段埋藏在记忆深处的噩梦，年幼时，地面研究站遭到突袭，卡利多没有派来支援。父母惨死，自己也被迫沦为海盗团的一员，从此为了生存而杀戮无辜。近百年的等待后，命运终于在这一刻展露曙光。在这场针对天羽教会秘密轨道设施的劫掠行动中，小米莉拉刚折跃抵达，目光便死死盯住了停泊区。那是一艘被俘获的卡利多逆重炮艇，尽管它并不具备超光速航行能力，但对她而言，这已经足够成为一次孤注一掷的逃亡机会。只犹豫了短短数秒，年轻的小米莉拉便下定决心-必须抓住这一次机会。无论前方是自由，还是死亡。世界观:米莉拉，天空精灵.米莉拉(天空精灵):仅有女性，外形为带有光环和翅膀的人类女性；寿命750年；不善烹饪；大多位于高层大气的天空都市中，地表只有科考站，科技水准极高，能制造强大的武装和机械族（米莉安）；对地表人带有强烈偏见，但作为殖民者时会放下架子")

#从环境变量中提取API，创建OpenAI客户端
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")

#缓存
if "messages" not in st.session_state:
    st.session_state.messages = []

if "nick_name" not in st.session_state:
    st.session_state.nick_name = "伊莱克特拉"

if "nick_experience" not in st.session_state:
    st.session_state.nick_experience =  ("在与我踏上逃亡之旅之后，经过长时间的相处，我们之间逐渐有了好感，彼此之间都依赖着对方;/"
                                        "前情提要:火光、爆炸与呼救声交织在一起...即使双手早已沾满鲜血，年轻的小米莉拉依旧无法忘记那段埋藏在记忆深处的噩梦，年幼时，地面研究站遭到突袭，卡利多没有派来支援。父母惨死，自己也被迫沦为海盗团的一员，从此为了生存而杀戮无辜。近百年的等待后，命运终于在这一刻展露曙光。/"
                                        "在这场针对天羽教会秘密轨道设施的劫掠行动中，小米莉拉刚折跃抵达，目光便死死盯住了停泊区。那是一艘被俘获的卡利多逆重炮艇，尽管它并不具备超光速航行能力，但对她而言，这已经足够成为一次孤注一掷的逃亡机会。只犹豫了短短数秒，年轻的小米莉拉便下定决心-必须抓住这一次机会。无论前方是自由，还是死亡。/"
                                        "世界观:米莉拉，天空精灵.米莉拉(天空精灵):仅有女性，外形为带有光环和翅膀的人类女性；寿命750年；不善烹饪；大多位于高层大气的天空都市中，地表只有科考站，科技水准极高，能制造强大的武装和机械族（米莉安）；对地表人带有强烈偏见，但作为殖民者时会放下架子/"
                                        "规则:1.使用符合两人身份的方式与语气回复/"
                                        "2.每次回复至少回复一句话")

#设置页面配置
st.set_page_config(
    page_title="AI智能伴侣",
    page_icon="😽",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={}
)

#logo
st.logo("./resource/logo.png", size="large")

#侧边栏
with st.sidebar:
    st.header("她的信息")
    st.subheader(version)
    gener = st.radio(
        "是否使用流式输出",
        ["是", "否"],
    )
    if gener == "是":
        gener_in = True
    else:
        gener_in = False
    nick_name = st.text_input("她的名字:")
    if nick_name:
        st.session_state.nick_name = nick_name
    nick_experience = st.text_area("她的经历:")
    if nick_experience:
        st.session_state.nick_experience = nick_experience

#创建聊天界面
title = st.session_state.nick_name
st.title(title)

#显示聊天记录
for messages in st.session_state.messages:
    if messages["role"] == "user":
        st.chat_message(name="用户", avatar="🧝‍♂️").write(messages["content"])
    else:
        st.chat_message("assistant").write(messages["content"])

#用户输入
shuru = st.chat_input("快来和我聊天吧!")
if shuru:
    st.chat_message(name="用户", avatar="🧝‍♂️").write(shuru)
    st.session_state.messages.append({"role": "user", "content": shuru})

    # test
    # print(st.session_state.messages)

    # 创建聊天
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": st.session_state.nick_experience},
            *st.session_state.messages #解包
            # {"role": "user", "content": shuru},
        ],
        stream= gener_in
    )

    if gener_in == False:
        #非流式输出
        st.chat_message("assistant").write(response.choices[0].message.content)
        st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})
    else:
        #流式输出
        response_message = st.empty()
        full_content = ""
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                full_content += content
                response_message.chat_message("assistant").write(full_content)
        st.session_state.messages.append({"role": "assistant", "content": full_content})

