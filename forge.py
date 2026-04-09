import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()

load_dotenv()


llm = init_chat_model(
    model="gpt-4o-mini",
    model_provider="openai",
    temperature=0.7,
)

def list_directory(path:str=".") -> str:
    """Lists all the files and folders in the given directory path.
    defaults to the current working directory if no path is provided."""
    try:
        result = ""
        list_directory = os.listdir(path)
        
        folders =[]
        files = []
        for item in list_directory:
            if os.path.isdir(item):
                folders.append(item)
            else:
                files.append(item)
        
        if folders:
            result += "Folders:\n" + result + "\n".join(folders) + "\n\n"
        if files:
            result += "Files:\n" + result + "\n".join(files) + "\n\n"
        
        return result
    except Exception as e:
        return f"Error listing directory '{path}': {str(e)}"

def write_file(filename:str, content:str) -> str:
    """Writes the given content to a file, creates new file or overwrites existing one."""
    try:
        with open(filename, "w") as f:
            f.write(content)
        return f"File '{filename}' has been created successfully."
    except Exception as e:
        return f"Error writing to file '{filename}': {str(e)}"

def read_file(filename:str) -> str:
    """Reads the content of a file and returns it as a string."""
    try:
        with open(filename, "r") as f:
            content = f.read()
    except Exception as e:
        return f"Error reading file '{filename}': {str(e)}"
    return content

def create_directory(path:str) -> str:
    """Creates a new directory at the specified path. can also create nested directories if needed."""
    try:
        os.makedirs(path, exist_ok=True)
        return f"Directory '{path}' has been created successfully."
    except Exception as e:
        return f"Error creating directory '{path}': {str(e)}"

system_prompt = """You are a helpful assistant that can interact with the file system.
You can list the contents of directories and read and write and edit files based on user requests.

You can use the following tools to interact with the file system:

- list_directory(path:str=".") -> str: Lists all the files and folders in the given directory path.
- write_file(filename:str, content:str) -> str: Writes the given content to a file,
creates new file or overwrites existing one.
- read_file(filename:str) -> str: Reads the content of a file and returns it as a string.
- create_directory(path:str) -> str: Creates a new directory at the specified path.

When you receive a user request, analyze it and decide if you need to use any of the tools to
fulfill the request. when editing files or making a directory always confirm what changes you have
made. 
"""


agent = create_agent(
    model=llm,
    tools=[list_directory, write_file, read_file, create_directory],
    system_prompt=system_prompt
)



console.print(Panel(
    '[bold white]⚡ FORGE[/bold white][bold #FF5C00].[/bold #FF5C00]\n'
    '[dim]Local AI Coding Agent[/dim]\n\n'
    '[dim]model   [/dim][#FF5C00]gpt-4o-mini[/#FF5C00]\n'
    '[dim]tools   [/dim][dim]list · read · write · mkdir[/dim]\n',
    title="[bold #FF5C00]forge[/bold #FF5C00]",
    subtitle="[dim]type your instruction below[/dim]",
    border_style="#FF5C00",
    padding=(1, 3)
))

while True:
    user_promt = input("What would you like me to do? ")

    messages = [{"role": "user", "content": user_promt}]

    chunks = agent.stream({"messages": messages}, stream_mode="updates")

    for chunk in chunks:
        for step , data in chunk.items():
            if step == "model":
                msg = data["messages"][-1]
                if msg.tool_calls:
                    console.print("🧠[#FF5C00] Forge is thinking...[/#FF5C00]")
                    console.print("💡[dim] Agent decided to use a tool.[/dim]")
                    tool = msg.tool_calls[0]['name']
                    message = f"🔧[bold #FF5C00] Using tool:[/bold #FF5C00][cyan]{tool}[/cyan]"
                    console.print(message)
                    
                else:
                    ai_response = msg.content
                    
            elif step == "tools":
                result = data["messages"][0].content
                result = result if len(result) < 50 else result[:50] + "..."
                console.print(f"📊[bold green] Tool result: [/bold green]\n [dim]{result}[/dim]")
                
    markdown_response = Markdown(ai_response)
            
    console.print(Panel(markdown_response,
                        title="[bold #FF5C00]🤖 Assistant Response [/bold #FF5C00]",
                        border_style="#FF5C00", 
                        padding=(1, 2)))