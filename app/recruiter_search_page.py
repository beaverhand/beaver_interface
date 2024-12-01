import streamlit as st
import chromadb
import pandas as pd


import yaml
import os
import sys
import argparse

# Adding the parent directory to the system path
script_dir = os.path.dirname(os.path.abspath(__file__))
# parent_dir = os.path.join(script_dir, "..")
# backend_dir = os.path.join(parent_dir, "backend")
# sys.path.append(backend_dir)
sys.path.append(os.path.abspath(os.path.join(script_dir, "../")))


from backend.resume_chromadb_backend import ResumeProcessorPipeline



script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, "..", "config.yaml")
with open(config_path, "r") as file:
    config = yaml.safe_load(file)

chroma_pipe = ResumeProcessorPipeline(config)
chroma_pipe.setup_chromadb()


# Initialize ChromaDB and database connection (assuming `client`, `collection`, `conn`, `cursor` are already configured)

# Title of the App
st.title("Candidate Search")

# Split the page into two columns
col1, col2 = st.columns(2)

# Left Column - Search Query Input
with col1:
    st.header("Enter Requirements")
    requirement = st.text_area("Enter your requirement:")
    n_results = st.number_input("Number of Candidates to Retrieve", min_value=0, value=5)

    # Search Button
    if st.button("Search"):
        if requirement:
            # Query ChromaDB
            results = chroma_pipe.query_top_candidates(query = requirement, n = n_results)

            # Display Results in the Right Column
            with col2:
                st.header("Top Candidates")
                if results:
                    candidates = [{"ID": res["id"], "Profile": res["metadata"]} for res in results]
                    candidates_df = pd.DataFrame(candidates)
                    candidates_df.ID.apply()
                    st.dataframe(candidates_df)
                else:
                    st.write("No candidates found.")

            # # Save Search History
            # cursor.execute('''
            #     INSERT INTO user_queries (user_id, query, result_ids) VALUES (?, ?, ?)
            # ''', (st.session_state["user_id"], requirement, ",".join([res["id"] for res in results])))
            # conn.commit()