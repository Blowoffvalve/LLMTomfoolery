from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

from output_parsers import person_intel_parser, PersonIntel
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent


name = "Harrison Chase"


def ice_break(name: str) -> PersonIntel:
    linkedin_profile_url = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_profile_url)

    twitter_information = twitter_lookup_agent(name=name)
    # scrape_user_tweets(username=twitter_information)
    print(twitter_information)

    summary_template = """
            Given the Linkedin information {linkedin_information} and twitter username {twitter_information} 
            about a person, from that i want you to create:
            1. a short summary
            2. two interesting facts about them
            3. A topic that may interest them
            4. 2 creative ice breakers to open a conversation with them
            \n{format_instructions}
        """

    summary_prompt_template = PromptTemplate(
        input_variables=["linkedin_information", "twitter_information"],
        template=summary_template,
        partial_variables={
            "format_instructions": person_intel_parser.get_format_instructions()
        },
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    result = chain.run(
        linkedin_information=linkedin_data, twitter_information=twitter_information
    )
    print(result)
    return person_intel_parser.parse(result)


if __name__ == "__main__":
    print("Hello Langchain!")
    result = ice_break(name)
