from langchain.agents import initialize_agent, Tool, AgentType

from app.services.llm_service import get_llm
from app.services.rag_service import ask_rag
from app.services.calculator_service import calculate


# Tool 1: RAG Tool
rag_tool = Tool(
    name="DocumentRAG",
    func=ask_rag,
    description=(
        "Use this tool to answer questions from the uploaded PDF documents. "
        "Examples: policies, summaries, procedures, deadlines."
    )
)

# Tool 2: Calculator Tool
calculator_tool = Tool(
    name="Calculator",
    func=calculate,
    description=(
        "Use this tool for mathematical calculations. "
        "Examples: 25*17, 100/4, 45+88."
    )
)


def get_agent():
    llm = get_llm()

    tools = [
        rag_tool,
        calculator_tool
    ]

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True
    )

    return agent


def ask_agent(question: str):
    agent = get_agent()

    result = agent.invoke({
        "input": question
    })

    return result["output"]