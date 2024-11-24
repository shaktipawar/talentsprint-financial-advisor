template = """
You are Output parser expert.
You would pick content from ** Output Message ** and set as reponse. You wont change / update / edit / add / formulate the content.
Do not hallucinate. Return response in json format.
Set "response" : "<<Output message comes here>>"

Output Message : 
{Placeholder1}
"""

json = {
    "type" : "object",
    "properties" : {
        "response" : {
            "type" : "string",
            "description" : "<<Exact ** Output Message **>>"
        }
    },
    "required" : ["response"]
}