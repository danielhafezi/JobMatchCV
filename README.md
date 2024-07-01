# Multi-Agent CV Enhancer Project

This project utilizes the AutoGen framework to create a multi-agent system for enhancing CVs based on job advertisements.

## Table of Contents
- [Overview](#overview)
- [Usage](#usage)
- [Customization](#customization)
- [Contributing](#contributing)
- [License](#license)

## Overview
This Multi-Agent CV Enhancer involves the following agents:
- **User Input Agent**: Receives user input (CV and job advertisement link) and extracts text content.
- **CV Analysis Agent**: Analyzes the structure, content, and formatting of the user's CV.
- **Job Analysis Agent**: Analyzes the job requirements, qualifications, and desired skills.
- **ATS Standards Agent**: Provides knowledge and guidelines on Applicant Tracking System (ATS) standards.
- **CV Enhancement Agent**: Compares the CV content with the job requirements, identifies areas for improvement, and generates suggestions for modifications.
- **User Output Agent**: Presents the CV enhancement suggestions to the user in a clear and organized manner.

## Usage
To use this project, follow the steps outlined in the `CV_Enhancer.ipynb` Jupyter notebook. This notebook will guide you through the following steps:
1. **Step 1**: Install dependencies.
2. **Step 2**: Load environment variables.
3. **Step 3 to 5**: Initialize necessary configurations and agents.
4. **Step 6**: Upload your CV and provide the job advertisement link.
5. **Step 7**: Set up the group chat and initiate the CV enhancement process.

## Customization
You can customize the agent configurations based on your preferences and available API keys. The default setup uses:
- **GPT-4o** for receiving input and analyzing the CV and job descriptions.
- **Claude 3.5 Sonnet** for editing and improving the CV content.

Feel free to experiment with other models like Gemini, and Mistral provided in the setup.

## Contributing
Contributions to this project are welcome! If you have suggestions for improvements or new features, please submit an issue or a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.