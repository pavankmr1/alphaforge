from agents.compiler.llm_compiler import (
    compile_condition
)

result = compile_condition(

    "Bullish setup: 9 EMA crosses above 20 EMA"
)

print(
    result.model_dump_json(
        indent=4
    )
)