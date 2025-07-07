AI-Powered CLI Agent

    A command-line tool that leverages a pre-trained language model to iteratively diagnose and fix Python code, built with a functional-programming approach.

Features
    Interactive Task Input
    Accepts natural-language coding tasks (e.g. “fix my calculator app; it’s not starting correctly”).

    Function-Based Action Selection
    Chooses from a library of pure functions to:

    Scan directory structure

    Read and parse file contents

    Modify and overwrite files

    Execute Python scripts

    Loop until the task is resolved (or an error terminates the run)

    Transparent Workflow
    Logs each function invocation, so you can trace exactly how the agent arrives at its solution.

Prerequisites
    Python 3.10 or newer

    uv project & package manager

    Unix-style shell (bash, zsh, etc.)

Quickstart
# Install dependencies
    uv install

# Run the agent on “main.py” with a task prompt
    uv run main.py "fix my calculator app; it’s not starting correctly"
    Learning Goals
Architect and navigate multi-directory Python projects

Demystify how production-grade AI agents make decisions “under the hood”

Sharpen Python and functional-programming skills by building composable, side-effect-controlled functions

Integrate with a pre-trained LLM without building one from scratch

