import json

class CommandParser: 
    def __init__(self, client): 
        self.commands = self._load_commands()
        self.client = client
        pass

    def _load_commands(self):
        with open("commands.json") as f: 
            data = json.load(f)
            return {cmd['name']: cmd for cmd in data['commands']}

    def parse_command(self, command) -> str: 
        parts = command.split() 
        if not parts: 
            return f"Command not found: {command}"
        
        cmd_name = parts[0].lower()
        if cmd_name in self.commands: 
            cmd_info = self.commands[cmd_name]
            func = getattr(self, cmd_info['function'])
            return func(parts[1:])
        else: 
            return f"Command not found: {command}"
        

    ### 
    # Execute commands
    ###
    
    # Echo command
    def execute_echo(self, args): 
        return f"{" ".join(args)}"
    
    # Help command, returns the usage text for the specified command
    def execute_help(self, args): 
        parts = args
        if not parts: 
            return f"{self.commands["help"]["description"]}\n{self.commands["help"]["usage"]}"
        
        cmd_name = parts[0].lower()
        if cmd_name in self.commands: 
            cmd_info = self.commands[cmd_name]
            return f"{cmd_info["description"]}\n{cmd_info['usage']}"
        else: 
            return f"No manual entry for for {cmd_name}"

    def execute_clear(self, _): 
        pass