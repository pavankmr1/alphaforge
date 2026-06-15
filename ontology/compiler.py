from loguru import logger

from compiler_rules import (
    RULE_MAPPINGS
)

from agents.compiler.dsl_validator import (
    validate_dsl
)

from agents.compiler.llm_compiler import (
    compile_condition
)

from ontology.field_normalizer import (
    normalize_dsl
)

from agents.compiler.compiler_cache import (
    get_cached,
    set_cached
)


# ==========================================
# MATCH RULES
# ==========================================
def find_rule(
    condition_text: str
):

    condition_lower = (
        condition_text.lower()
    )

    matched_rules = []

    for phrase, rule_data in RULE_MAPPINGS.items():

        if phrase in condition_lower:

            matched_rules.append({

                "matched_phrase":
                phrase,

                "logic_type":
                rule_data["logic_type"],

                "formula":
                rule_data["formula"]
            })

    return matched_rules


# ==========================================
# COMPILE STRATEGY
# ==========================================
def compile_strategy(
    strategy_data
):

    compiled_conditions = []

    entry_conditions = strategy_data.get(
        "entry_conditions",
        []
    )

    for condition in entry_conditions:

        # ==========================
        # RULE MATCH
        # ==========================
        matched_rules = find_rule(
            condition
        )

        if matched_rules:

            compiled_conditions.append({

                "original_condition":
                condition,

                "compiled_logic":
                matched_rules,

                "source":
                "rule_mapping"
            })

            continue

        # ==========================
        # CACHE LOOKUP
        # ==========================
        cached_dsl = get_cached(
            condition
        )

        if cached_dsl:

            try:

                cached_dsl = normalize_dsl(
                    cached_dsl
                )

                cached_dsl = validate_dsl(
                    cached_dsl
                )

            except Exception as e:

                logger.error(
                    f"Cache validation failed: "
                    f"{condition}"
                )

                logger.error(e)

            compiled_conditions.append({

                "original_condition":
                condition,

                "dsl":
                cached_dsl,

                "source":
                "cache"
            })

            continue

        # ==========================
        # GPT COMPILER
        # ==========================
        try:

            dsl = compile_condition(
                condition
            )

            # Pydantic -> dict
            dsl_dict = (
                dsl.model_dump()
            )

            # normalize fields
            dsl_dict = normalize_dsl(
                dsl_dict
            )

            # validate
            dsl_dict = validate_dsl(
                dsl_dict
            )

            # cache
            set_cached(
                condition,
                dsl_dict
            )

            compiled_conditions.append({

                "original_condition":
                condition,

                "dsl":
                dsl_dict,

                "source":
                "llm"
            })

        except Exception as e:

            logger.error(
                f"Failed compiling: "
                f"{condition}"
            )

            logger.error(e)

            compiled_conditions.append({

                "original_condition":
                condition,

                "dsl": None,

                "source":
                "failed"
            })

    strategy_data[
        "compiled_entry_logic"
    ] = compiled_conditions

    return strategy_data