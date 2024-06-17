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
    user_input_agent = UserInputAgent(
        name="User Input Agent", 
        llm_config=llm_config, 
        cv_path=cv_path,
        job_ad_link=job_ad_link,
    )
    
    # Process user input and get initial CV content and job description
    cv_content, job_description = user_input_agent.process_input()

    # --- 3. Create the Other Agents ---

    # User Proxy Agent (for interacting with tools)
    user_proxy = UserProxyAgent(
        name="User Proxy", 
        system_message="A proxy agent that can execute code and interact with tools.",
        human_input_mode="TERMINATE", # Or "ALWAYS" for constant user interaction
        code_execution_config={"work_dir": "coding"},  # Directory for code execution
        function_map={"research": research, "write_content": write_content},
    )

    # CV Analysis Agent
    cv_analysis_agent = CVAnalysisAgent(
        name="CV Analysis Agent",
        llm_config=llm_config, 
        system_message="Analyzes the structure and content of the user's CV.",
    )

    # Job Analysis Agent
    job_analysis_agent = JobAnalysisAgent(
        name="Job Analysis Agent",
        llm_config=llm_config, 
        system_message="Analyzes the requirements and keywords from a job description.",
    )

    # ATS Standards Agent
    ats_standards_agent = ATSStandardsAgent(
        name="ATS Standards Agent",
        llm_config=llm_config, 
        system_message="Provides guidelines and knowledge about Applicant Tracking Systems (ATS).",
    )

    # CV Enhancement Agent (Central Orchestrator)
    cv_enhancement_agent = CVEnhancementAgent(
        name="CV Enhancement Agent",
        llm_config=llm_config, 
        system_message="Compares the CV with the job description and ATS guidelines to suggest enhancements.",
        function_map={"research": research, "write_content": write_content}, # For potential tool usage
    )

    # User Output Agent
    user_output_agent = UserOutputAgent(
        name="User Output Agent",
        llm_config=llm_config, 
        system_message="Presents CV enhancement suggestions in a clear and user-friendly way.",
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
            {"role": "user", "content": job_description}, # Add job description
        ],
        max_round=50 
    )

    manager = GroupChatManager(groupchat=group_chat, llm_config=llm_config)

    # --- 6. Initiate Chat ---
    user_input_agent.initiate_chat(manager, message="Start CV enhancement process.")

if __name__ == "__main__":
    main()