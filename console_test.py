import cmd

class test(cmd.cmd):
    prompt= "this prompt"

    def do_quit(self, line):
        """this help\n"""
        return True
    
if __name__ == '__main__':
    test().cmdloop()