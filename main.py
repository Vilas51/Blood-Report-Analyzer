from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
import os
import uuid
from task import help_patients as base_help_patients
import traceback

from crewai import Crew, Process
from agents import doctor

app = FastAPI(title="Blood Test Report Analyser")



def run_crew(query: str, file_path: str = "data/sample.pdf"):
    """Run the CrewAI workflow"""
    # Set env vars for tools to use
    os.environ["USER_QUERY"] = query
    os.environ["REPORT_FILE"] = file_path

    # # Create Crew and execute
    # help_patients = base_help_patients.with_inputs({
    #     "query": query,
    #     "report_path": file_path
    # })

    medical_crew = Crew(
        agents=[doctor],
        tasks=[base_help_patients],
        process=Process.sequential,
        verbose=True
    )

    # kickoff() now takes no arguments; use env vars or task.input
    result = medical_crew.kickoff(inputs={
        "query": query,
        "report_path": file_path
    })

    return result


@app.get("/")
async def root():
    """Health check"""
    return {"message": "Blood Test Report Analyser API is running"}


@app.post("/analyze")
async def analyze_blood_report(
    file: UploadFile = File(...),
    query: str = Form(default="Summarise my Blood Test Report")
):
    """Upload and analyze a blood test report"""

    # Create a unique file path
    file_id = str(uuid.uuid4())
    file_path = f"data/blood_test_report_{file_id}.pdf"

    try:
        # Create data directory if it doesn't exist
        os.makedirs("data", exist_ok=True)

        # Validate file type
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")

        # Save file to disk
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Ensure query is non-empty
        if not query.strip():
            query = "Summarise my Blood Test Report"

        # Call CrewAI process
        response = run_crew(query=query.strip(), file_path=file_path)

        return {
            "status": "success",
            "query": query,
            "analysis": str(response),
            "file_processed": file.filename
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error processing blood report: {str(e)}")

    finally:
        # Delete the uploaded file to clean up
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass  # Silently ignore cleanup failure


# Optional: Run directly with `python main.py`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
