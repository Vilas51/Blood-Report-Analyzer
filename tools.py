import os
from dotenv import load_dotenv
load_dotenv()
os.environ['SERPER_API_KEY'] = os.getenv("SERPER_API_KEY")

from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.document_loaders import PyPDFLoader

from crewai_tools import tool
from crewai_tools import SerperDevTool

search_tool = SerperDevTool()
# search_tool = DuckDuckGoSearchRun()

class BloodTestReportTool:
    @tool("Read Blood Test Report")
    def read_data_tool(path='data/sample.pdf'):
        """Tool to read data from a pdf file from a path

        Args:
            path (str, optional): Path of the pdf file. Defaults to 'data/sample.pdf'.

        Returns:
            str: Full Blood Test report file
        """
        
        docs = PyPDFLoader(file_path=path).load()

        full_report = ""
        for data in docs:
            full_report+=data.page_content+"\n"
            
        return full_report