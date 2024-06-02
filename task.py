from crewai import Task

from agents import doctor, verifier
from tools import search_tool, BloodTestReportTool
    
help_patients = Task(
    description="First wait for the verifier to let you know if the data is a blood test report and then take any action.\n\
You should solve the user's query: {query}\n\
Search the internet to get up-to-date solutions to user's query.\n\
You should give detailed answers to the user. If the user asks for a summary of the whole report then you should summarise every part of it.\n\
If you find anything abnormal in the report you must notify them.\n\
Search the internet and \
find up-to-date health recommendations from the web for the patients based on their \
blood test reports in detail. Additionally, provide url links to the articles you recommended to \
support each suggestion. Your url links should match with the health suggestions. Do not make up a url",

    expected_output="""Give your response to user's query in bullet points.
If the user didn't ask anything then \
you should give detailed summary of the blood test report \
in bullet points in casual terms as if you are explaining to someone \
who does not know anything about medical terms.
Provide detailed health recommendations from the web along with their respective article url links, \
listed in numerical points.""",

    agent=doctor,
    tools=[search_tool, BloodTestReportTool().read_data_tool],
    async_execution=False,
    output_file="health-recommendations.md"
)


## Verification task overview.
# First read the data provided by the user. If its not a blood test report then don't do anything and just say:\
# This is not a blood test report and end the process.\n\
# If its a blood test report then:\n\
# If the user query is completely irrelevant to the blood test report then you should say: This question is not related to your Blood Test Report.\
    
verification = Task(
    description="Use your medical knowledge to verify if the data provided by the user is a blood test report or not.\n\
Read the contents of the data and check if they are similar to a blood test report.",

    expected_output="After verifying, if the data is indeed a blood test report then you should tell that to the senior docter and give the file_path: {file_path}.\n\
If it is not a blood test report then say: No blood test report was given",

    agent=verifier,
    tools=[BloodTestReportTool().read_data_tool],
    async_execution=False
)