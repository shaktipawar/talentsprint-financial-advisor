from graph import create_graph, compile_workflow
from termcolor import colored
import json

print("Createing Graph and compiling workflow")
graph = create_graph()
workflow = compile_workflow(graph)
print("Graph and workflow created")
iteration = 40
if __name__ == "__main__":
    verbose = False
    print(colored("AI Message : Hi Shakti. How may I help you today ?", "green"))
    while True:
        query = input(colored("Shakti's Message : ", "magenta"))
        if query.lower() == "exit":
            break
        dict_inputs = {"question" : query }
        limit = {"recursion_limit" : iteration}

        for event in workflow.stream(dict_inputs, limit):
            if "output" in event:
                response = event['output']["output_response"]["content"]
                print(colored(f"AI Message : {response}", "green"))
            else:
                if verbose:
                    print(colored(f"State Dictionary : {event}", "light_yellow"))
                    print(colored("------", "light_yellow"))