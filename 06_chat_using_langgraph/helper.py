from termcolor import colored
from enum import Enum



class ColorPalette(Enum):

    SYSTEM_MESSAGE = "blue"
    USER_MESSAGE = "green"
    AI_MESSAGE = "magenta"

    PROMPT_MESSAGE = "light_green"
    TEXT_MESSAGE = "light_yellow"
    RESPONSE_MESSAGE = "light_magenta"

class MessageType(Enum):

    AGENT_MESSAGE = "AGENT_MESSAGE"
    TEXT_LOG = "TEXT_LOG"
    PROMPT_MESSAGE = "PROMPT_MESSAGE"
    LLM_RESPONSE = "LLM_RESPONSE"
    AI_MESSAGE = "AI_MESSAGE",
    AI_REPLY = "AI_REPLY"     

class Helper():

    # def print(title, message, color):
    #     print(colored(f"{title} : {message}", color))
    #     print(colored("------", color))

    def print(messagetype, title, message):

        match messagetype.value:
            case MessageType.AGENT_MESSAGE.value:
                print(colored(f"{title} : {message}", "yellow"))
                print(colored("------", "yellow"))
            case MessageType.PROMPT_MESSAGE.value:
                print(colored(f"{title} : {message}", "light_cyan"))
                print(colored("------", "light_cyan"))
            case MessageType.LLM_RESPONSE.value:
                print(colored(f"{title} : {message}", "cyan"))
                print(colored("------", "cyan"))
            case MessageType.TEXT_LOG.value:
                print(colored(f"{title} : {message}", "dark_grey"))
                print(colored("------", "dark_grey"))
            case MessageType.AI_MESSAGE.value:
                print(colored(f"{title} : {message}", "green"))
                print(colored("------", "green"))
            case MessageType.AI_REPLY.value:
                print(colored(f"{title} : {message}", "green"))


