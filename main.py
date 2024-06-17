import os
import openai
import dotenv
from autogen import config_list_from_json, UserProxyAgent, AssistantAgent, GroupChat, GroupChatManager
from tools import extract_text_from_pdf, extract_text_from_docx, fetch_job_description, research, write_content

dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
config_list = config_list_from_json(os.getenv("OAI_CONFIG_LIST"))

user_task = input("Please upload your CV file path (PDF or DOCX): ")
job_link = input("Please enter the job advertisement link: ")

llm_config_content_assistant = {
    "functions": [
        {
            "name": "research",
            "description": "Conduct relevant research",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The topic to be researched"}
                },
                "required": ["query"]
            }
        },
        {
            "name": "write_content",
            "description": "Write content based on research",
            "parameters": {
                "type": "object",
                "properties": {
                    "research_material": {"type": "string", "description": "Research material"},
                    "topic": {"type": "string", "description": "Content topic"}
                },
                "required": ["research_material", "topic"]
            }
        }
    ],
    "config_list": config_list,
    "timeout": 120
}

def extract_cv_text(file_path):
    file_ext = file_path.split('.')[-1].lower()
    if file_ext == 'pdf':
        return extract_text_from_pdf(file_path)
    elif file_ext == 'docx':
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format.")

class UserInputAgent(UserProxyAgent):
    def __init__(self, name, llm_config):
        super().__init__(name=name, llm_config=llm_config)

    def handle_input(self, cv_path, job_link):
        cv_text = extract_cv_text(cv_path)
        job_description = fetch_job_description(job_link)
        self.send(cv_text, receiver="CV_Analysis_Agent")
        self.send(job_description, receiver="Job_Analysis_Agent")

class CVAnalysisAgent(AssistantAgent):
    def __init__(self, name, llm_config):
        super().__init__(name=name, llm_config=llm_config)

    def analyze_cv(self, cv_text):
        # Implement CV analysis logic
        pass

class JobAnalysisAgent(AssistantAgent):
    def __init__(self, name, llm_config):
        super().__init__(name=name, llm_config=llm_config)

    def analyze_job_description(self, job_description):
        # Implement job description analysis logic
        pass

class ATSStandardsAgent(AssistantAgent):
    def __init__(self, name, llm_config):
        super().__init__(name=name, llm_config=llm_config)

    def provide_ats_guidelines(self):
        # Implement ATS guidelines provision logic
        pass

class CVEnhancementAgent(AssistantAgent):
    def __init__(self, name, llm_config):
        super().__init__(name=name, llm_config=llm_config)

    def generate_suggestions(self, analyzed_cv, analyzed_job, ats_guidelines):
        # Implement CV enhancement suggestion logic
        pass

class UserOutputAgent(UserProxyAgent):
    def __init__(self, name, llm_config):
        super().__init__(name=name, llm_config=llm_config)

    def display_suggestions(self, suggestions):
        # Implement logic to present suggestions to the user
        pass

user_input_agent = UserInputAgent(
    name="User_Input_Agent",
    llm_config={"config_list": config_list}
)

cv_analysis_agent = CVAnalysisAgent(
    name="CV_Analysis_Agent",
    llm_config={"config_list": config_list}
)

job_analysis_agent = JobAnalysisAgent(
    name="Job_Analysis_Agent",
    llm_config={"config_list": config_list}
)

ats_standards_agent = ATSStandardsAgent(
    name="ATS_Standards_Agent",
    llm_config={"config_list": config_list}
)

cv_enhancement_agent = CVEnhancementAgent(
    name="CV_Enhancement_Agent",
    llm_config={"config_list": config_list}
)

user_output_agent = UserOutputAgent(
    name="User_Output_Agent",
    llm_config={"config_list": config_list}
)

groupchat = GroupChat(
    agents=[
        user_input_agent, cv_analysis_agent, job_analysis_agent,
        ats_standards_agent, cv_enhancement_agent, user_output_agent
    ],
    messages=[], max_round=20
)

manager = GroupChatManager(groupchat=groupchat, llm_config={"config_list": config_list})

user_input_agent.initiate_chat(
    manager,
    message={"cv_path": user_task, "job_link": job_link}
)
