## Resume Parser with Azure ADI & Gemini
This project is a resume parser that analyzes resumes in PDF format and compares them to job descriptions to suggest whether a candidate is suitable for the role or not. It leverages Azure ADI (Azure Document Intelligence) to extract content from resumes and Gemini to analyze and compare the skills, experience, and projects against the job description.

# Features
- Resume Content Extraction: Utilizes Azure ADI to extract relevant content from resumes, even when the resumes follow non-standard formats, which is often the case with fresher candidates.
- Job Description Matching: Uses Gemini to analyze the extracted resume content (skills, projects, etc.) and compares it with the job description to assess if the candidate is a good fit.
- User Interface: Designed a simple interface using Streamlit to upload resumes and input job descriptions for comparison.
- PDF Parsing: Supports parsing resumes in PDF format, extracting key sections such as skills, experience, and projects.

# Technologies Used
- Azure ADI (Document Intelligence): For content extraction from resumes, handling various templates and partitions in PDFs.
- Gemini: For comparing the candidate's skills and experience with the job description to assess suitability.
- Streamlit: For building the user interface, allowing users to upload resumes and enter job descriptions easily.
- Python: For implementing the logic and interaction between Azure ADI, Gemini, and the Streamlit UI.

# Note
Set up your API keys by creating a .env file in the root of the project and adding the following:

adi_api_key = "<your-azure-adi-api-key>"
adi_endpoint = "<your-azure-adi-endpoint>"
gemini_api_key = "<your-gemini-api-key>"

You can obtain the Azure ADI API key and endpoint from the Azure portal.
You can get the Gemini API key from the Gemini API service.

## Usage
Run the Streamlit app:

bash command: 
streamlit run app.py

Open your browser and navigate to the Streamlit interface (usually at http://localhost:8501).
Upload a resume (in PDF format) and input the job description text.
The app will process the resume, extract relevant information using Azure ADI, and compare it against the job description using Gemini. It will then display whether the candidate is suitable for the role.
