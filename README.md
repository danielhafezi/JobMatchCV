# JobMatchCV: AI-Powered Resume Optimizer

JobMatchCV is an innovative multi-agent system that leverages the AutoGen framework to enhance CVs based on specific job advertisements, providing a tailored markdown output.

## Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Installation](#installation)
- [Usage](#usage)
- [Customization](#customization)
- [Contributing](#contributing)
- [License](#license)

## Overview
JobMatchCV employs a sophisticated multi-agent system to analyze, enhance, and format CVs:

- **User Input Agent**: Manages initial input and text extraction from CVs and job ads.
- **CV Analysis Agent**: Examines CV structure, content, and formatting.
- **Job Analysis Agent**: Dissects job requirements and desired qualifications.
- **ATS Standards Agent**: Provides expertise on Applicant Tracking System standards.
- **CV Enhancement Agent**: Generates improvement suggestions based on job-CV comparison.
- **User Output Agent**: Presents enhancement suggestions clearly and actionably.
- **Markdown Conversion Agent**: Transforms the enhanced CV into a professional markdown document.

## Key Features
- Multi-agent collaboration for comprehensive CV optimization
- Support for PDF and DOCX input formats
- Web scraping for job description extraction
- ATS-compliant enhancement suggestions
- Automatic conversion to markdown format
- Final output saved as `cv.md`
## Usage
1. Open the `JobMatchCV.ipynb` Jupyter notebook.
2. Follow the step-by-step instructions to:
   - Set up your environment and API keys
   - Upload your CV (PDF or DOCX)
   - Provide the job advertisement link
   - Initiate the CV enhancement process
3. Retrieve your optimized CV as a markdown file (`resume.md`)

## Customization
JobMatchCV offers flexibility in model selection:
- Default: GPT-4 for analysis, Claude 3.5 Sonnet for enhancements
- Alternative options: Gemini, Mistral, and Codestral

Adjust the `llm_config` settings in the notebook to experiment with different models.

## Contributing
We welcome contributions! For suggestions or new features, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.