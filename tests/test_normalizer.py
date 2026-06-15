from agents.compiler.llm_compiler import (
    compile_condition
)

result = compile_condition(

    "Price is trending upward"
)

print(

    result.model_dump_json(
        indent=4
    )
)