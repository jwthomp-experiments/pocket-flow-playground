from pocketflow import Flow

from pocket_flow_playground.nodes import AnswerNode, EndNode


# Create the flow with self-loop
#input_node = InputNode()
answer_node = AnswerNode()

#input_node - "continue" >> answer_node  # Pass input to llm node
answer_node - "continue" >> EndNode()  # Call the LLM
#input_node - "end" >> EndNode()  # End the flow if user types 'exit'
answer_node - "end" >> EndNode()  # End the flow if LLM response is None

flow = Flow(start=answer_node)

flow.set_params({"queue_name": "Agent_1"})

# Start the chat
if __name__ == "__main__":
    shared = {}
    flow.run(shared)
