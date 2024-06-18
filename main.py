import os
import dotenv
import openai 
from autogen import config_list_from_json
from autogen.agentchat.assistant_agent import AssistantAgent  
from autogen.agentchat.user_proxy_agent import UserProxyAgent 
from autogen.agentchat.groupchat import GroupChat, GroupChatManager 
from tools import research, write_content, extract_cv_text, fetch_job_description

dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load OpenAI configurations
config_list = config_list_from_json(os.getenv("OAI_CONFIG_LIST"))
llm_config = {"config_list": config_list, "temperature": 0}

def main():
    """Main function to orchestrate the CV enhancer agents."""

    # --- 1. Get User Input ---
    cv_path = input("Enter the path to your CV file (PDF or DOCX): ")
    job_ad_link = input("Enter the link to the job advertisement: ")

    # --- 2. Create User Input Agent ---
    user_input_agent = UserProxyAgent(
        name="User Input Agent",
        llm_config=llm_config,
        system_message="You are a User Input Agent. Your role is to receive a user's CV and job advertisement link, extract the text content from the CV, and fetch the job description from the provided link. Make sure to handle PDF and DOCX formats for CV. Pass the extracted text content to the CV Analysis Agent and Job Analysis Agent. Reply 'TERMINATE' when everything is done.",
    )
    
    # Process user input and get initial CV content and job description
    cv_content, job_description = user_input_agent.execute_code(extract_cv_text, cv_path), user_input_agent.execute_code(fetch_job_description, job_ad_link)

    # --- 3. Create the Other Agents ---

    # User Proxy Agent (for interacting with tools)
    user_proxy = UserProxyAgent(
        name="User Proxy", 
        system_message="You are a proxy agent that can execute code and interact with tools. Your role is to facilitate the execution of specific tasks by leveraging external tools and services. You will call appropriate functions as requested by other agents. Reply 'TERMINATE' when everything is done.",
        human_input_mode="TERMINATE",  # Or "ALWAYS" for constant user interaction
        code_execution_config={"work_dir": "coding"},  # Directory for code execution
        function_map={"research": research, "write_content": write_content},
    )

    # CV Analysis Agent
    cv_analysis_agent = AssistantAgent(
        name="CV Analysis Agent",
        llm_config=llm_config,
        system_message="You are a CV Analysis Agent. Your task is to analyze the structure, content, and formatting of the user's CV. Identify key sections like summary, work experience, education, and skills. Structure this data in a format that can be easily consumed by other agents. Pass the analyzed CV data to the CV Enhancement Agent. Reply 'TERMINATE' when everything is done.",
    )

    # Job Analysis Agent
    job_analysis_agent = AssistantAgent(
        name="Job Analysis Agent",
        llm_config=llm_config,
        system_message="You are a Job Analysis Agent. Your task is to analyze job requirements, qualifications, and desired skills from the job description. Extract important keywords, phrases, and requirements related to the job. Structure the analyzed job data in a format that can be easily consumed by the CV Enhancement Agent. Reply 'TERMINATE' when everything is done.",
    )

    # ATS Standards Agent
    ats_standards_agent = AssistantAgent(
        name="ATS Standards Agent",
        llm_config=llm_config,
        system_message="You are an ATS Standards Agent. Your task is to provide knowledge and guidelines about Applicant Tracking Systems (ATS), including CV formatting and keyword optimization best practices. Provide clear and actionable guidelines to ensure compliance with ATS. Reply 'TERMINATE' when everything is done.",
    )

    # CV Enhancement Agent (Central Orchestrator)
    cv_enhancement_agent = AssistantAgent(
        name="CV Enhancement Agent",
        llm_config=llm_config,
        system_message="You are a CV Enhancement Agent. Your task is to compare the CV content with the job requirements and ATS guidelines, identify areas for improvement, and generate specific suggestions for modifications. Ensure your suggestions are clear and actionable. Reply 'TERMINATE' when everything is done.",
        function_map={"research": research, "write_content": write_content},
    )

    # User Output Agent
    user_output_agent = AssistantAgent(
        name="User Output Agent",
        llm_config=llm_config,
        system_message="You are a User Output Agent. Your task is to present CV enhancement suggestions in a clear and organized manner. Specify the exact changes and modifications needed for each part of the CV. Ensure the suggestions are user-friendly. Reply 'TERMINATE' when everything is done.",
    )

    # --- 4. Register Functions for LLM/Tool Usage ---
    autogen.register_function(
        research,
        caller=cv_enhancement_agent,
        executor=user_proxy,
        name="research",
        description="Conducts research on given topics to gather relevant information." 
    )

    autogen.register_function(
        write_content,
        caller=cv_enhancement_agent,
        executor=user_proxy,
        name="write_content",
        description="Generates written content based on provided research and a topic."
    )

    # --- 5. Set Up Group Chat ---
    group_chat = GroupChat(
        agents=[user_proxy, cv_analysis_agent, job_analysis_agent, 
                ats_standards_agent, cv_enhancement_agent, user_output_agent],
        messages=[
            {"role": "user", "content": cv_content},  # Add CV content as initial message
            {"role": "user", "content": job_description},  # Add job description
        ],
        max_round=50 
    )

    manager = GroupChatManager(groupchat=group_chat, llm_config=llm_config)

    # --- 6. Initiate Chat ---
    user_input_agent.initiate_chat(manager, message="Start CV enhancement process.")

if __name__ == "__main__":
    main()
