import asyncio
# To get or create an eventloop for running streamlit
# Need to use this before importing streamlit
def get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

from crewai import Crew, Process
import streamlit as st
import time

from agents import doctor, verifier
from task import help_patients, verification

def run_crew(query: str, file_path: str="data/sample.pdf"):
    """To run the whole crew

    Args:
        query (str): query of the user
        file_path (str, optional): path to the blood report file. Defaults to "data/sample.pdf".

    Returns:
        str: Response of the agents
    """
    medical_crew = Crew(
        agents=[verifier, doctor],
        tasks=[verification, help_patients],
        process=Process.sequential,
    )

    result = medical_crew.kickoff({'query': query, "file_path": file_path})
    return result


st.title("Blood Test Report Analyser")
query =  st.text_input("What can I help you with?",
                       placeholder="Summarise my Blood Test Report").strip()
uploaded_file = st.file_uploader("Upload your blod test report here!")

file_path = "data/blood_test_report.pdf"


def stream_data(response):
    """To stream the output of the agents

    Args:
        response (str): response from agents

    Yields:
        str: streamed output
    """
    for word in response.split(" "):
        yield word + " "
        time.sleep(0.02)


if st.button("Submit"):
    # verifying for None values
    if uploaded_file is not None:
        ## Write file to database
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            f.close()
        
        # verifying for None values
        if query=="" or query is None:
            query = "Summarise my Blood Test Report"
        st.success("Your data was correctly submitted.")
        
        ## Running the crew
        response = run_crew(query=query, file_path=file_path)
        
        ## Get streaming output on your streamlit web interface
        st.write_stream(stream_data(response))
    else:
        st.error("You didn't upload a file.")