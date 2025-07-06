import os 
from dotenv import load_dotenv
load_dotenv()

from crewai_tools import SerperDevTool
from crewai_tools.tools import FileReadTool
from langchain_community.document_loaders import PyPDFLoader
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

# Built-in tools
search_tool = SerperDevTool()
BloodTestReportTool = FileReadTool()

# Input schema for tools
class ReportInput(BaseModel):
    blood_report_data: str = Field(..., description="Full text of the blood test report")

# ✅ Nutrition Tool
class NutritionTool(BaseTool):
    name: str= "Nutrition Recommendation Tool"
    description: str= "Analyzes nutrition status from a blood report and suggests dietary tips."
    args_schema: type = ReportInput

    def _run(self, blood_report_data: str) -> str:
        report = ' '.join(blood_report_data.lower().split())
        suggestions = []

        try:
            if "vitamin b12" in report:
                b12_str = report.split("vitamin b12")[1].split()[0]
                b12 = float(b12_str)
                if b12 < 250:
                    suggestions.append("Vitamin B12 appears low. Consider eggs, dairy, or supplements.")
                else:
                    suggestions.append("Vitamin B12 level is okay.")
        except:
            suggestions.append("Could not parse Vitamin B12.")

        try:
            if "vitamin d" in report or "25-hydroxy" in report:
                d_str = report.split("vitamin d")[1].split()[0]
                d = float(d_str)
                if d < 50:
                    suggestions.append("Vitamin D is deficient. Try sunlight and D3 supplements.")
                elif d < 75:
                    suggestions.append("Vitamin D is insufficient. Moderate sun and fortified foods recommended.")
                else:
                    suggestions.append("Vitamin D level is sufficient.")
        except:
            suggestions.append("Could not parse Vitamin D.")

        try:
            if "tsh" in report:
                tsh_str = report.split("tsh")[1].split()[0]
                tsh = float(tsh_str)
                if tsh > 4.8:
                    suggestions.append("TSH high — Possible hypothyroidism. Avoid goitrogens and ensure iodine.")
        except:
            suggestions.append("Could not parse TSH.")

        return "\n".join(suggestions) or "No nutritional issues found."

# ✅ Exercise Tool
class ExerciseTool(BaseTool):
    name: str= "Exercise Plan Generator"
    description: str= "Creates a weekly exercise plan based on blood test data."
    args_schema: type = ReportInput

    def _run(self, blood_report_data: str) -> str:
        report = blood_report_data.lower()
        plan = [
            "Weekly Exercise Plan (General):",
            "- 3x/week: 30 mins brisk walking",
            "- 2x/week: Bodyweight training (squats, push-ups, lunges)",
            "- Daily: 5 mins stretching/mobility"
        ]

        try:
            if "tsh" in report:
                tsh = float(report.split("tsh")[1].split()[0])
                if tsh > 4.8:
                    plan.append("TSH is high — avoid intense training until thyroid stabilizes.")
                    plan.append("Recommended: yoga, light walking, swimming.")
        except:
            pass

        return "\n".join(plan)


# Instantiate the tools
NutritionTool = NutritionTool()
ExerciseTool = ExerciseTool()
