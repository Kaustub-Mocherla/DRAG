# streamlit ui app
import streamlit as st
import requests
import time
st.title("DKSS")
st.caption("Distributed Knowledge Search System")

query = st.text_input("Search your organization's knowledge base...")



if st.button("Search") and query.strip():
    start = time.time()
    
    with st.spinner("Searching nodes..."):
        response = requests.post(
            "http://localhost:9000/search",
            json={"query": query},
            stream=True
        )

    sources = response.headers.get("X-Sources", "").split(",")
    st.write_stream(response.iter_content(chunk_size=None, decode_unicode=True))
    
    elapsed = time.time() - start
    st.caption(f"⏱ answered in {elapsed:.1f}s")
    
    if sources:
        st.markdown("**Sources:** " + " ".join(f"`{s}`" for s in sources))