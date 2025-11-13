import re
from pocketflow import Node, Flow
from utils import call_llm


class InputNode(Node):
    def prep(self, shared):
        # Initialize messages if this is the first run
        if "messages" not in shared:
            shared["messages"] = []
            print("Welcome to the chat! Type 'exit' to end the conversation.")

        return None

    def exec(self, _):
        # Get user input
        user_input = input("\nYou: ")

        # Check if user wants to exit
        if user_input.lower() == "exit":
            return None

        return user_input

    def post(self, shared, prep_res, exec_res):
        if exec_res is None:
            print("\nGoodbye!")
            return "end"  # End the conversation

        # Add user message to history
        shared["messages"].append({"role": "user", "content": exec_res})

        # Loop back to continue the conversation
        return "continue"


class AnswerNode(Node):
    def prep(self, shared):
        """Prepare context for the LLM"""
        if not shared.get("messages"):
            return None

        # 1. Get the last 3 conversation pairs (or fewer if not available)
        recent_messages = (
            shared["messages"][-6:]
            if len(shared["messages"]) > 6
            else shared["messages"]
        )

        # 2. Add the retrieved relevant conversation if available
        context = []
        if shared.get("retrieved_conversation"):
            # Add a system message to indicate this is a relevant past conversation
            context.append(
                {
                    "role": "system",
                    "content": "The following is a relevant past conversation that may help with the current query:",
                }
            )
            context.extend(shared["retrieved_conversation"])
            context.append(
                {"role": "system", "content": "Now continue the current conversation:"}
            )

        # 3. Add the recent messages
        context.extend(recent_messages)

        return context

    def exec(self, messages):
        """Generate a response using the LLM"""
        if messages is None:
            return None

        # Call LLM with the context
        response = call_llm(messages)
        return response

    def post(self, shared, prep_res, exec_res):
        """Process the LLM response"""
        if prep_res is None or exec_res is None:
            return "end"  # End the conversation

        # Clean the response by removing <think> tags and their content
        cleaned_content = re.sub(
            r"<think>.*?</think>\n?", "", exec_res, flags=re.DOTALL
        )

        # Print the assistant's response
        print(f"\nAssistant: {cleaned_content}")

        # Add assistant message to history
        shared["messages"].append({"role": "assistant", "content": cleaned_content})

        # We only end if the user explicitly typed 'exit'
        # Even if last_question is set, we continue in interactive mode
        return "continue"


class EndNode(Node):
    """Node that handles flow termination."""

    pass


# Create the flow with self-loop
input_node = InputNode()
answer_node = AnswerNode()

input_node - "continue" >> answer_node  # Pass input to llm node
answer_node - "continue" >> input_node  # Call the LLM
input_node - "end" >> EndNode()  # End the flow if user types 'exit'
answer_node - "end" >> EndNode()  # End the flow if LLM response is None

flow = Flow(start=input_node)

# Start the chat
if __name__ == "__main__":
    shared = {}
    flow.run(shared)
