from crewai import Task
from agents import doctor, verifier, nutritionist, exercise_specialist
from tools import BloodTestReportTool, NutritionTool, ExerciseTool  # These are already instances!
from pydantic import BaseModel

# DON'T re-instantiate these
# nutrition_tool = NutritionTool()
# exercise_tool = ExerciseTool()

class HelpPatientsInput(BaseModel):
    query: str
    report_path: str

# Just use imported instances directly
# Doctor's diagnosis task
help_patients = Task(
    description="Interpret the blood test report and provide a clear summary addressing the user's health query.",
    expected_output="""
- Identify any abnormalities or critical markers in the report
- Provide possible medical implications for abnormal results
- Suggest follow-up actions such as seeing a specialist or getting more tests
- Use medical terminology, but explain in layman's terms
- Ensure recommendations are evidence-based""",
    agent=doctor,
    tools=[BloodTestReportTool],
    input_schema=HelpPatientsInput,
    async_execution=False,
)

# Nutritionist task
nutrition_analysis = Task(
    description="Analyze the user's blood report for any nutritional deficiencies or markers, and provide appropriate dietary suggestions.",
    expected_output="""
- Identify key nutrient-related markers (e.g., Vitamin B12, D, Iron)
- Suggest foods to improve levels
- Recommend supplements if deficiencies are evident
- Provide practical diet tips based on test results
- Ensure advice is safe, accessible, and tailored to general health""",
    agent=nutritionist,
    tools=[NutritionTool, BloodTestReportTool],
    async_execution=False,
)

# Exercise specialist task
exercise_planning = Task(
    description="Create a personalized exercise plan based on the user's health indicators from the blood test report and query.",
    expected_output="""
- Provide a basic exercise plan suited to the user's age and fitness level
- Avoid contraindicated exercises for any medical flags
- Include frequency, type (e.g., cardio, strength), and duration
- Recommend warm-up, cool-down, and safety guidelines
- Encourage consistency and gradual progression
""",
    agent=exercise_specialist,
    tools=[ExerciseTool, BloodTestReportTool],
    async_execution=False,
)

# Verifier task
verification = Task(
    description="Check if the uploaded document appears to be a valid blood test report. If valid, confirm key indicators exist.",
    expected_output="""
- Confirm presence of blood test data (e.g., glucose, TSH, hemoglobin)
- Ensure readable structure (patient details, units, reference ranges)
- Return 'valid' or 'invalid' with brief justification
- Avoid hallucination, do not assume correctness without checking
""",
    agent=verifier,
    tools=[BloodTestReportTool],
    async_execution=False
)
