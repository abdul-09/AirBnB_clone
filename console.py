#!/usr/bin/python3
"""define Hbnb console"""


import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review

def  parse(arg):
        c_braces = re.search(r"\{(.* ?)\}", arg)
        brackets = re.search(r"\[(.*?)\]", arg)
        if c_braces is None:
            if brackets is None:
                return [i.strip(",") for i in split(arg)]
            else:
                lexer = split(arg[:brackets.span()[0]])
                retline = [i.strip(",") for i in lexer]
                retline.append(brackets.group())
                return retline
        else:
            lexer = split(arg[:c_braces.span()[0]])
            retline = [i.strip(",") for i in lexer]
            retline.append(c_braces.group())
            return retline
        
class HBNBCommand(cmd.Cmd):
    """
    custom console class

    """
    prompt =  " (hbnb) "

    __classes = {
        "Basemodel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review",
    }
        
    def empty_line(self):
        """do nothing after receiving an empty line"""
        pass

    def default(self, arg):
        """behavior for cmd module when input is invalid"""
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_count,
            "count": self.do_count,
            "update": self.do_update,
        }

        match = re.search(r"\.", arg)
        if match is not None:
            argline = [arg [:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argline[1])
            if match is not None:
                command = [argline[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(argline[0], command[1])
                    return argdict[command[0]](call)
                
        print("*** unknown syntax: {}".format(arg))
        return False
    

    def do_quit(self, line):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, line):
        """Exits"""
        return True
    def help_quit(self):
        print("NEW HELP FOR QUIT")
    
    def do_create(self, arg):
        """
        create a new class instance and print its id.
        """
        argline = parse(arg)
        if len(argline) == 0:
            print("** class name missing **")
        elif argline[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(argline[0]().id))
            storage.save()

    def do_show(self, arg):
        """
        Display the string representation of a class instance of a given id.
        """
        argline = parse(arg)
        objdict = storage.all()
        if len(argline) == 0:
            print("** class name missing **")
        elif argline[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argline) == 1:
            print("** instance id is missing **")
        elif "{}.{}".format(argline[0], argline[1]) not in objdict:
            print("** no instance found **")
        else:
            print(objdict["{}.{}".format(argline[0], argline[1])])
            
    def do_all(self, arg):
        """
        Dispaly string representations of all instances of given class.
        if no class is specified, displays all instantiated objects.
        """
        argline = parse(arg)
        if len[argline] > 0 and arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objline = []
            for obj in storage.all().values():
                if len(argline) > 0 and argline[0] == obj.__class__.__name__:
                    objline.append(obj.__str__())
                elif len(argline) == 0:
                    objline.append(obj.__str__())
                print(objline)
            
    def do_update(self, arg):
        """
        only one attribute can be updated at a time
        """
        argline = parse(arg)
        objdict = storage.all()
        if len(argline) == 0:
            print("** class name missing **")
            return False
        if argline[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(argline) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format([argline[0], argline[1]] not in objdict.key):
            print("** no instance found **")
            return False
        if len(argline) == 2:
            print("** attribute name missing **")
            return False
        if len(argline) == 3:
            try:
               type(eval(argline[2])) != dict
            except NameError:
                print("** value missing **")
                return False
        if len(argline) == 4:
            obj = objdict["{}.{}".format(argline[0], argline[1])]
            if argline[2] in obj.__class__.__dict__.keys():
                valuetype = type(obj.__class__.__dict__[argline[2]])
                obj.__dict__[argline[2]] = valuetype(argline[3])
            else:
                obj.__dict__[argline[2]] = argline[3]
        elif type(eval(arg[2])) == dict:
            obj = objdict["{}.{}".format(argline[0], argline[1])]
            for key, value in eval(argline[2].items()):
                if (key in obj.__class__.__dict__.keys() and
                       type(obj.__class__.__dict__[key] in {str, int, float})):
                    valuetype = type(obj.__class__.__dict__[key])
                    obj.__dict__[key] = valuetype(value)
                else:
                    obj.__dict__[key] = value
            storage.save()          
    
    def do_count(self, arg):
        """
        retrive number of instances of a class
        """
        argline = parse(arg)
        count = 0
        for obj in storage.all().values():
            if argline[0] == obj.__class__.__name__:
                count += 1
            print(count) 
        
if __name__ == "__main__":
    HBNBCommand().cmdloop()
