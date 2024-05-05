#!/bin/bash

source .venv/bin/activate

CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python
