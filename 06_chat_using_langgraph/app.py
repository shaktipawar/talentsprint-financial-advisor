from graph import create_graph, compile_workflow
from termcolor import colored
import json
from helper import Helper, MessageType

print("Createing Graph and compiling workflow")
graph = create_graph()
workflow = compile_workflow(graph)
print("Graph and workflow created")
iteration = 40
if __name__ == "__main__":
    verbose = False
    print(colored("AI Message : Hi Shakti. How may I help you today ?", "green"))
    while True:
        query = input(colored("Shakti : ", "magenta"))
        if query.lower() == "exit":
            break
        dict_inputs = {"question" : query }
        limit = {"recursion_limit" : iteration}

        response_text = ""
        for event in workflow.stream(dict_inputs, limit):
            if "output" in event:
                #response = event['output']["output_response"]["content"]
                string_obj = event['output']["output_response"]["content"]
                json_obj = json.loads(string_obj)
                response = json_obj["response"]
                response_text += response
                if json_obj["attachment"]:
                    response_text += f"File to Download : {json_obj['filename']}, URL : {json_obj['attachment']}"

                Helper.print(MessageType.AI_REPLY, "AI", response_text)
            else:
                if verbose:
                    print(colored(f"State Dictionary : {event}", "light_yellow"))
                    print(colored("------", "light_yellow"))