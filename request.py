import requests

url = "http://localhost:8000/analyze"

with open('data/sample.pdf', 'rb') as f:
    pdf_file = {'file': f}
    query = {'query': 'Summarise my Blood Test Report'}

    response = requests.post(url, files=pdf_file, data=query)

    if response.status_code == 200:
        result = response.json()
        with open("analysis_output.txt", "w", encoding="utf-8") as f_out:
            f_out.write(str(result['analysis']))
        print("✅ API result saved to analysis_output.txt")
    else:
        print("❌ Error:", response.status_code, response.text)
