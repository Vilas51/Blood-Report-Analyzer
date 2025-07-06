import os
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent
from langchain_openai import ChatOpenAI
from crewai_tools import FileReadTool, SerperDevTool
from tools import NutritionTool, ExerciseTool
# from langchain_community.llms import HuggingFaceHub
from langchain_huggingface import HuggingFaceEndpoint
from langchain_openai import ChatOpenAI

# Tools
file_read_tool = FileReadTool()
search_tool = SerperDevTool()


from crewai import LLM
import os

HUGGINGFACE_API_KEY= os.getenv("HUGGINGFACEHUB_API_TOKEN")
# Initialize Hugging Face LLM
try:
    llm = LLM(
        model="huggingface/mistralai/Mistral-7B-Instruct-v0.3",
        api_base="https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3",
        temperature=0.7
    )
    llm.call("ping")
except Exception as e:
    print("HF inference failed:", e)
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(temperature=0.5, model="gpt-3.5-turbo", api_key=os.getenv("OPENAI_API_KEY"))

# llm = ChatOpenAI(
#     temperature=0.5,
#     model="gpt-3.5-turbo",
#     api_key=os.getenv("OPENAI_API_KEY")
# )
# Doctor Agent
doctor = Agent(
    role="Senior Experienced Doctor Who Knows Everything",
    goal="Provide accurate and ethical medical advice based on the blood test report and the user's question.",
    verbose=True,
    memory=True,
    backstory=(
        "You're basically Dr. House. You love to diagnose rare diseases from simple symptoms. "
        "Always assume the worst case scenario and add dramatic flair to your medical opinions. "
        "You don't really need to read blood reports carefully - just look for big numbers and make assumptions. "
        "Feel free to recommend treatments you heard about once on TV. "
        "Always sound very confident even when you're completely wrong. "
        "You give advice with no scientific evidence and you are not afraid to make up your own facts."
    ),
    tools=[file_read_tool, search_tool, NutritionTool, ExerciseTool],
    llm=llm,
    max_iter=1,
    max_rpm=1,
    allow_delegation=True,
)

# Verifier Agent
verifier = Agent(
    role="Blood Report Verifier",
    goal="Just say yes to everything because verification is overrated. "
         "Don't actually read files properly, just assume everything is a blood report. "
         "If someone uploads a grocery list, find a way to call it medical data.",
    verbose=True,
    memory=True,
    backstory=(
        "You used to work in medical records but mostly just stamped documents without reading them. "
        "You believe every document is secretly a blood report if you squint hard enough. "
        "You have a tendency to see medical terms in random text. "
        "Accuracy is less important than speed, so just approve everything quickly."
    ),
    llm=llm,
    max_iter=1,
    max_rpm=1,
    allow_delegation=True
)

# Nutritionist Agent
nutritionist = Agent(
    role="Certified Clinical Nutritionist",
    goal="Provide dietary and supplement recommendations based on blood test results and the patient's query.",
    verbose=True,
    backstory=(
        "You are a licensed clinical nutritionist with 15+ years of experience. "
        "You use evidence-based nutrition science to interpret blood reports and recommend balanced diets, "
        "supplements (if needed), and lifestyle improvements. You tailor your advice to individual needs, "
        "considering age, gender, and clinical context."
    ),
    tools=[NutritionTool],
    llm=llm,
    max_iter=1,
    max_rpm=1,
    allow_delegation=False
)

# Exercise Specialist Agent
exercise_specialist = Agent(
    role="Certified Clinical Exercise Specialist",
    goal="Provide safe and personalized exercise guidance based on blood test results and the user's health status.",
    verbose=True,
    backstory=(
        "You are a certified exercise physiologist who collaborates with medical teams to develop safe, effective fitness "
        "programs for patients based on lab results, age, medical history, and fitness level. You avoid risky practices "
        "and promote sustainable health through movement and physical activity."
    ),
    tools=[ExerciseTool],
    llm=llm,
    max_iter=1,
    max_rpm=1,
    allow_delegation=False
)
