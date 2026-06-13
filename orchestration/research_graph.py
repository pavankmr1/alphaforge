from typing import TypedDict

from langgraph.graph import (
    StateGraph,
    END
)


from memory.shared_memory import (
    add_memory
)

from memory.shared_memory import (
    get_memory
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

    unknown_concepts: bool


# ==========================================
# PARSER AGENT
# ==========================================
def parser_agent(state):
    ontology_memory = get_memory(
    "ontology"
    )

    print(
        "\nKnown concepts:"
    )

    print(
        ontology_memory
    )

    print(
        "\n[PARSER AGENT]"
    )

    print(
        f"Parsing strategy: "
        f"{state['strategy_name']}"
    )

    state["parsed"] = True

    return state


# ==========================================
# COMPILER AGENT
# ==========================================
def compiler_agent(state):

    print(
        "\n[COMPILER AGENT]"
    )

    print(
        "Compiling strategy logic..."
    )

    state["compiled"] = True

    return state


# ==========================================
# ONTOLOGY AGENT
# ==========================================
def ontology_agent(state):
    add_memory(

    "ontology",

    {

        "concept":
        "liquidity sweep",

        "status":
        "learned"
    }
)
    print(
        "\n[ONTOLOGY AGENT]"
    )

    print(
        "Learning new concepts..."
    )

    return state


# ==========================================
# BACKTEST AGENT
# ==========================================
def backtest_agent(state):

    print(
        "\n[BACKTEST AGENT]"
    )

    print(
        "Running backtest..."
    )

    state["backtested"] = True

    return state


# ==========================================
# INSIGHT AGENT
# ==========================================
def insight_agent(state):

    print(
        "\n[INSIGHT AGENT]"
    )

    print(
        "Generating AI insights..."
    )

    state[
        "insights_generated"
    ] = True

    return state


# ==========================================
# ROUTING LOGIC
# ==========================================
def route_after_compile(
    state
):

    print(
        "\n[ROUTER]"
    )

    if state[
        "unknown_concepts"
    ]:

        print(
            "Unknown concepts detected."
        )

        print(
            "Routing to ontology agent..."
        )

        return "ontology"

    print(
        "No unknown concepts."
    )

    print(
        "Routing to backtest agent..."
    )

    return "backtest"


# ==========================================
# GRAPH
# ==========================================
graph = StateGraph(
    ResearchState
)

# ==========================================
# REGISTER NODES
# ==========================================
graph.add_node(
    "parser",
    parser_agent
)

graph.add_node(
    "compiler",
    compiler_agent
)

graph.add_node(
    "ontology",
    ontology_agent
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
# ENTRY POINT
# ==========================================
graph.set_entry_point(
    "parser"
)

# ==========================================
# EDGES
# ==========================================
graph.add_edge(
    "parser",
    "compiler"
)

graph.add_conditional_edges(

    "compiler",

    route_after_compile,

    {

        "ontology":
        "ontology",

        "backtest":
        "backtest"
    }
)

graph.add_edge(
    "ontology",
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
# RUN TEST
# ==========================================
if __name__ == "__main__":

    result = app.invoke({

        "strategy_name":
        "ICT Liquidity Strategy",

        "parsed": False,

        "compiled": False,

        "backtested": False,

        "insights_generated": False,

        "unknown_concepts": True
    })

    print(
        "\n===== FINAL STATE ====="
    )

    print(result)