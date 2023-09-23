import os
import sys
import time
import re

"""
    Suspiler is a simple python script that will help you to compile and run your
    sussy files.
"""
class Suspiler(object):

    def __init__(self, instructions):
        self.instructions = instructions
        self.is_debugging = False
        self.is_executing = False
        self.print_mode = False
        self.ignore_lines = []
        self.variables = {
            "RED": None,
            "BLUE": None,
            "GREEN": None,
            "YELLOW": None,
            "PURPLE": None,
            "CYAN": None,
            "WHITE": None,
            "BLACK": None,
            "ORANGE": None,
            "PINK": None,
            "BROWN": None,
            "GREY": None
        }
        self.loops = {}
        return
    
    def compile(self):
        if "START GAME" not in self.instructions or "END GAME" not in self.instructions:
            print("ERROR: File not sussy enough. Exiting...")
            return -1

        instruction_index = 0
        while instruction_index < len(self.instructions):

            if instruction_index in self.ignore_lines:
                instruction_index += 1
                continue

            instruction = self.instructions[instruction_index]
            instruction_re = re.compile(r'^(\w+)\s+([\w\d\s\S]+)$')
            instruction_match = instruction_re.match(instruction)
            if not instruction_match:
                continue
            operation = instruction_match.group(1)
            variables = instruction_match.groups()[1:][0].split(" ")
            variables = list(variables)

            if not self.is_executing and operation != "START":
                continue

            if self.is_debugging:
                print(self.instructions.index(instruction), operation, variables, self.is_executing)

            if operation in self.variables and variables[0] == "IS":
                if variables[1] == "SUS":
                    self.variables[operation] = True
                elif variables[1] == "CREW":
                    self.variables[operation] = False
                else:
                    self.variables[operation] = variables[1]
                instruction_index += 1
                continue
            
            match operation:
                case "START":
                    match variables[0]:
                        case "GAME":
                            self.is_executing = True
                        case "MEETING":
                            self.print_mode = True
                case "END":
                    match variables[0]:
                        case "GAME":
                            self.is_executing = False
                        case "MEETING":
                            self.print_mode = False
                case "SAY":
                    if self.print_mode:
                        variables = [variable for variable in variables if variable is not None]
                        for variable in variables:
                            if variable.startswith("*"):
                                variable = variable[1:]
                                if variable not in self.variables:
                                    print(f"ERROR: Variable {variable} doesn't exist.")
                                    continue
                                
                                return_var = None
                                if self.variables[variable] is None:
                                    return_var = "NOTHING"
                                match self.variables[variable]:
                                    case True:
                                        return_var = "SUS"
                                    case False:
                                        return_var = "CREW"
                                    case _:
                                        return_var = self.variables[variable]
                                
                                if return_var == None:
                                    return_var = "NOTHING"
                                variables[variables.index(f"*{variable}")] = str(return_var)
                        variables = [variable for variable in variables if variable is not None]
                        print(" ".join(variables))
                    else:
                        print("ERROR: You cannot say anything outside a meeting.")
                case "KILL":
                    if len(variables) != 1:
                        print("ERROR: Kill operation must have 1 variable.")
                        continue
                    if variables[0] not in self.variables:
                        print(f"ERROR: Variable {variables[0]} doesn't exist.")
                        continue
                    self.variables[variables[0]] = None
                case "REMEMBER":
                    if len(variables) != 2:
                        print("ERROR: Remember operation must have 2 variables.")
                        continue
                    if variables[0] not in self.variables:
                        print(f"ERROR: Variable {variables[0]} doesn't exist.")
                        continue
                    match variables[1]:
                        case "SUS":
                            variables[1] = True
                        case "CREW":
                            variables[1] = False
                    self.variables[variables[0]] = variables[1]
                case "VOTE":
                    if len(variables) != 1:
                        print("ERROR: Vote operation must have 2 variables.")
                        continue
                    if variables[0] not in self.variables:
                        print(f"ERROR: Variable {variables[0]} doesn't exist.")
                        continue
                    if self.variables[variables[0]] is None:
                        self.variables[variables[0]] = 1
                        continue
                    self.variables[variables[0]] += 1
                # functions
                case "DEFINE":
                    if len(variables) != 2:
                        print("ERROR: Define operation must have 1 variable.")
                        continue
                    
                    match variables[0]:
                        case "TASK":
                            self.loops[variables[1]] = instruction_index
                case "DO":
                    if len(variables) < 2:
                        print("ERROR: Do operation must have 1 variable.")
                        continue

                    match variables[0]:
                        case "TASK":
                            if variables[1] not in self.loops:
                                print(f"ERROR: Task {variables[1]} doesn't exist.")
                                continue
                            if len(variables) == 3 and variables[2] == "ONCE":
                                self.ignore_lines.append(instruction_index)
                            instruction_index = self.loops[variables[1]]
                # DEBUG OPERATIONS
                case "DUMP":
                    if not self.is_debugging:
                        continue
                    match variables[0]:
                        case "VARIABLES":
                            print(self.variables)
                        case "INSTRUCTIONS":
                            print(self.instructions)
                case "SUSSY":
                    match variables[0]:
                        case "BAKA":
                            self.is_debugging = True
                case _:
                    print(f"ERROR: Operation {operation} was called, but it doesn't exist.")
            
            instruction_index += 1
        return 0

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_to_compile = sys.argv[1]
        if os.path.exists(file_to_compile) and file_to_compile.endswith(".sus"):
            with open(file_to_compile, "r") as f:
                instructions = f.read()
                suspiler = Suspiler(instructions.split("\n")).compile()
            print(f"Suscript returned {int(suspiler)}. Press RETURN to exit...")
            sys.stdin.read(1)
        else:
            print("No valid sus file was provided. Exiting...")