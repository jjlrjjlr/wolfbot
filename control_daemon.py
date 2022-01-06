import logging
import cmd
import os
import sys

class CommandDaemon(cmd.Cmd):
    intro = 'WolfBot interactive control shell.\nUse help or ? for a list of commands.'
    def do_restart(self, line):
        os.execv(sys.executable, [sys.executable] + sys.argv)

    def do_EOF(self, line) -> None:
        sys.exit()


if __name__ == '__main__':
    CommandDaemon().cmdloop()