"""The study pipeline, one module per stage of the proposal's Figure 2:

    llm         OpenRouter and mock backends
    reporter    paraphrase generation, acceptance filter, freezing
    conditions  the thirteen conditions, rotations, the screen
    prompt      the judge prompt
    judge       judge calls, parsing, trial records
    score       the scorer
    lint        static checks on the case files
    run         the command line: dry run, plan, real runs
"""
