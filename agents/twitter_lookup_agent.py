from langchain import PromptTemplate
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool

from utils.constants import OpenAIModels

from tools.tools import get_profile_url_base


def lookup(name: str) -> str:
    llm = ChatOpenAI(temperature=0, model_name=OpenAIModels.GPT_3_5_TURBO)
    template = """
    Given the name {name_of_person} I want you to find me a link to their twitter profile page, and extract from it
    their username. In your final answer only the return the person's username"""

    tools_for_agent = [
        Tool(
            name="Crawl Google for twitter profile page",
            func=get_profile_url_base,
            description="Useful for when you need the twitter page URL for a user",
        )
    ]

    agent = initialize_agent(
        tools=tools_for_agent,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )

    twitter_username = agent.run(prompt_template.format_prompt(name_of_person=name))

    return twitter_username
