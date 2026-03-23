import streamlit as st
import os
import json
__all__ = ["save_sessions"]

def save_sessions():
        if st.session_state.current_session:
            session_date = {
                "nick_name": st.session_state.nick_name,
                "nick_experience": st.session_state.nick_experience,
                "current_session": st.session_state.current_session,
                "messages": st.session_state.messages
            }
            if not os.path.exists("sessions"):
                os.mkdir("sessions")
            with open("./sessions/%s.json" % st.session_state.current_session,"w",encoding="utf-8") as f:
                json.dump(session_date,f,indent=2,ensure_ascii=False)