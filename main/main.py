
import os
from models.Claude.model import get_response, functions
from dotenv import load_dotenv

def main():
    load_dotenv()

    print("Hello...")
    print("Type 'exit' to end the conversation.")

    while True:
        user_input = input("You: ")
        
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        response = get_response(user_input, functions)

        print("Claude:", response.content)

        if response.function_calls:
            for func_call in response.function_calls:
                print(f"Function called: {func_call.name}")
                print(f"Arguments: {func_call.arguments}")
                if func_call.name in functions:
                    result = functions[func_call.name](**func_call.arguments)
                    print(f"Function result: {result}")
                else:
                    print(f"Function {func_call.name} not found")

if __name__ == "__main__":
    main()


