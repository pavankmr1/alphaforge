from typing import TypedDict

from langgraph.graph import (
    StateGraph,
    END
)

# ==========================================
# STATE
# ==========================================
class ResearchState(
    TypedDict
):

    strategy_name: str

    parsed: bool

    compiled: bool

    backtested: bool

    insights_generated: bool

# ==========================================
# AGENTS
# ==========================================
def parser_agent(state):

    print(
        "\n[PARSER AGENT]"
    )

    state["parsed"] = True

    return state


def compiler_agent(state):

    print(
        "\n[COMPILER AGENT]"
    )

    state["compiled"] = True

    return state


def backtest_agent(state):

    print(
        "\n[BACKTEST AGENT]"
    )

    state["backtested"] = True

    return state


def insight_agent(state):

    print(
        "\n[INSIGHT AGENT]"
    )

    state["insights_generated"] = True

    return state

# ==========================================
# GRAPH
# ==========================================
graph = StateGraph(
    ResearchState
)

graph.add_node(
    "parser",
    parser_agent
)

graph.add_node(
    "compiler",
    compiler_agent
)

graph.add_node(
    "backtest",
    backtest_agent
)

graph.add_node(
    "insight",
    insight_agent
)

# ==========================================
# EDGES
# ==========================================
graph.set_entry_point(
    "parser"
)

graph.add_edge(
    "parser",
    "compiler"
)

graph.add_edge(
    "compiler",
    "backtest"
)

graph.add_edge(
    "backtest",
    "insight"
)

graph.add_edge(
    "insight",
    END
)

# ==========================================
# COMPILE GRAPH
# ==========================================
app = graph.compile()

# ==========================================
# RUN
# ==========================================
if __name__ == "__main__":

    result = app.invoke({

        "strategy_name":
        "ICT Strategy",

        "parsed": False,

        "compiled": False,

        "backtested": False,

        "insights_generated": False
    })

    print(
        "\n===== FINAL STATE ====="
    )

    print(result)