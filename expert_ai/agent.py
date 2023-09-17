import langchain
from langchain.prompts import PromptTemplate
from langchain.agents import AgentType
from langchain.agents import initialize_agent
from langchain.memory import ConversationBufferMemory, ReadOnlySharedMemory
from langchain import LLMChain
from expert_ai.tools import tools
from .prompts import GENERAL_TEMPLATE


def _make_llm(model, temp):
    if model.startswith("gpt-3.5-") or model.startswith("gpt-4"):
        llm = langchain.chat_models.ChatOpenAI(
            temperature=temp,
            model_name=model,
            request_timeout=1000)
        
    elif model.startswith("text-"):
        llm = langchain.OpenAI(
            temperature=temp,
            model_name=model)
    else:
        raise ValueError(f"Invalid model name: {model}")
    return llm

class ExpertAI:

    def __init__(self,temp=0.1,tools_model="gpt-3.5-turbo-0613",verbose=True):
        
        memory = ConversationBufferMemory(memory_key="chat_history")
        self.readonlymemory = ReadOnlySharedMemory(memory=memory)
        
        self.prompt_agent = PromptTemplate(
           input_variables=["query"],
            template=GENERAL_TEMPLATE,
            return_intermediate_steps=True
        )

        self.llm =  _make_llm(tools_model, temp)
        #Load the tool configs that are needed.
        self.llm_tools_chain = LLMChain(
            llm = self.llm,
            prompt=self.prompt_agent,
            verbose=verbose
        )
        self.all_tools = tools.get_tools()
        "text-davinci-003"
        self.agent_llm =  _make_llm('gpt-4', temp)

        self.agent = initialize_agent(
            self.all_tools,
            self.agent_llm ,
            #agent="zero-shot-react-description",
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=verbose,
            memory=self.readonlymemory
            )
        

    def run(self,query):
        response = self.agent.run(input=query)
        return response