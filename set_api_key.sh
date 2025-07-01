#!/bin/bash

echo "Please enter your OpenAI API key (it will be hidden):"
read -s OPENAI_API_KEY

export OPENAI_API_KEY
echo "API key set successfully!"

# Add to your shell profile for persistence
echo "export OPENAI_API_KEY='$OPENAI_API_KEY'" >> ~/.zshrc
echo "API key has been added to your shell profile for future sessions." 