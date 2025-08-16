import markdown
import streamlit as st
from src.utils.llm_utils import LLMHandler
from src.constants.prompt import PromptLibrary

def main():

    llm_handler = LLMHandler(st.secrets["LLM_API_KEY"])
    prompt_library = PromptLibrary()

    st.markdown("<h1 style='text-align: center'>🍽️ MarketMunch: Restaurant Market Analyzer 📊</h1>", unsafe_allow_html=True)

    # Use session state to prevent rerun unless user_input changes
    if "last_input" not in st.session_state:
        st.session_state.last_input = ""
    if "analysis_response" not in st.session_state:
        st.session_state.analysis_response = ""

    user_input = st.text_input("🍜 Enter your cuisine and city name", placeholder="e.g., Italian in New York")

    if user_input and user_input != st.session_state.last_input:
        with st.spinner("Analyzing business idea..."):
            response = llm_handler.get_analysis(sys_prompt=prompt_library.MARKET_RESEARCH_PROMPT, prompt=user_input)
            st.session_state.analysis_response = response
            st.session_state.last_input = user_input

    if st.session_state.analysis_response:
        st.markdown("<h3 style='color: #2E8B57;'>🔍 Market Analysis Report</h3>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div style="max-height: 80vh; overflow-y: auto; border: 1px solid #ddd; padding: 16px; border-radius: 8px;">
            {st.session_state.analysis_response}
            </div>
            """,
            unsafe_allow_html=True
        )
        html = markdown.markdown(st.session_state.analysis_response)
        st.download_button(
            label="Download Analysis",
            data=html,
            file_name="market_analysis.html",
            mime="text/html"
        )

if __name__ == "__main__":
    main()
