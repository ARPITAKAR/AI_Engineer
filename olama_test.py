from ollama import chat


# Function: main
def main():
    response = chat(
        model="qwen3:4b",
        messages=[
            {
                "role": "user",
                "content": "Explain LangGraph in simple terms."
            }
        ]
    )

    print(response.message.content)


if __name__ == "__main__":
    main()