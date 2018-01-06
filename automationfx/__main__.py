import cmd, sys, argparse
import os.path
from settings import Settings
from actions import *

def main():
    AutomationFXShell().cmdloop()

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

class AutomationFXShell(cmd.Cmd):
    intro = 'Welcome to the AutomationFX cli. Type help or ? to list commands.\n'
    prompt = 'AFX> '
    pwd = None
    settings = Settings()

    def __init__(self):
        cmd.Cmd.__init__(self)
        if not self.settings.Apikey:
            print("No Apikey, running setup")
            self.do_setup(None)

    def do_setup(self,arg):
        'Setup the connection to AutomationFX'
        if query_yes_no("Set Apikey?"):
            self.settings.Apikey = raw_input("Apikey: ")
        self.settings.UseCloudFX = query_yes_no("Use CloudFX?")
        if not self.settings.UseCloudFX and query_yes_no("Change AutomationFX Host ({0})?".format(self.settings.Host)):
            self.settings.Host = raw_input("AutomationFX Host: ")
        if not self.settings.UseCloudFX and query_yes_no("Change AutomationFX Port ({0})?".format(self.settings.Port)):
            self.settings.Port = int(raw_input("AutomationFX Port: "))
        if not self.settings.UseCloudFX and query_yes_no("Change AutomationFX Scheme ({0})?".format(self.settings.Scheme)):
            scheme = raw_input("AutomationFX Scheme: ")
            scheme = scheme.lower()
            if scheme != "http" and scheme != "https":
                print("Invalid scheme (only 'http' and 'https' allowed)")
            else:
                self.settings.Scheme = scheme
        print("AutomationFX Setup:")
        print("\tApikey: {0}".format(self.settings.Apikey))
        print("\tUse CloudFX: {0}".format(self.settings.UseCloudFX))
        if not self.settings.UseCloudFX:
            print("\tHost: {0}".format(self.settings.Host))
            print("\tPort: {0}".format(self.settings.Port))
            print("\tScheme: {0}".format(self.settings.Scheme))
        if query_yes_no("Save Settings?"):
            self.settings.save()

    def intTryParse(self, value):
        try:
            return int(value), True
        except ValueError:
            return value, False

    def getArgs(self, arg, number=1):
        parts = arg.split()
        if len(parts) < number:
            print("Invalid number of arguments")
            return
        return parts

    def getPhone(self, arg, number=1):
        if self.pwd:
            parts = arg.split()
            # result = parts.insert(0, self.pwd.DN)
            result = ([self.pwd.DN] + parts)
            return self.pwd, result
        parts = self.getArgs(arg, number=1)
        if not parts:
            return
        sourceNum = self.intTryParse(parts[0])
        if not sourceNum[1]:
            print("Argument ({0}) is not a number".format(parts[0]))
            return
        phone = findPhone(Phone.DN == parts[0])
        if not phone:
            print("Extension/DN '{0}' not found".format(parts[0]))
            return
        return phone, parts

    def do_call(self, arg):
        'Place a call from a source phone extension to any number "call 50005 10134"'
        data = self.getPhone(arg, 2)
        if not data[0]:
            return
        call(data[0], data[1][1])

    def do_connect(self, arg):
        'Connect (Call and Answer) a call between the source and destiantion phones "connect 50005 10134"'
        data = self.getPhone(arg, 2)
        if not data[0]:
            return
        data2 = self.getPhone(data[1][1], 1)
        if not data2[0]:
            return
        call(data[0], data[1][1])
        answer(data2[0])

    def do_answer(self, arg):
        'Answer any call on the phone "answer 50005"'
        data = self.getPhone(arg, 1)
        if not data[0]:
            return
        answer(data[0])

    def do_drop(self, arg):
        'Drop all calls on the phone "drop 50005"'
        data = self.getPhone(arg, 1)
        if not data[0]:
            return
        drop(data[0])

    def do_hold(self, arg):
        'Hold the current call on the phone "hold 50005"'
        data = self.getPhone(arg, 1)
        if not data[0]:
            return
        hold(data[0])

    def do_unhold(self, arg):
        'Unhold the current call on the phone "hold 50005"'
        data = self.getPhone(arg, 1)
        if not data[0]:
            return
        unhold(data[0])

    def do_transfer(self, arg):
        'Initiate/Complete a consult transfer on the current call on the phone "transfer 50005"'
        data = self.getPhone(arg, 1)
        if not data[0]:
            return
        transfer(data[0])

    def do_conference(self, arg):
        'Initiate/Complete a consult conference on the current call on the phone "conference 50005"'
        data = self.getPhone(arg, 1)
        if not data[0]:
            return
        conference(data[0])

    def do_offhook(self, arg):
        'Go off-hook on the primary line on the phone "offhook 50005"'
        data = self.getPhone(arg, 1)
        if not data[0]:
            return
        offhook(data[0])

    def do_digits(self, arg):
        'Send digits to the phone "digits 50005 123"'
        data = self.getPhone(arg, 2)
        if not data[0]:
            return
        digits = self.intTryParse(data[1][1])
        if not digits[1]:
            print("Argument ({0}) is not a number".format(data[1][1]))
            return
        sendDigits(data[0], data[1][1])

    def do_uri(self, arg):
        'Send a uri/url to the phone "uri 50005 Key:Soft1"'
        data = self.getPhone(arg, 2)
        if not data[0]:
            return
        sendUri(data[0], data[1][1])

    def do_macro(self, arg):
        'Send a macro to the phone "macro 50005 Key:Line1|Key:KeyPad1"'
        data = self.getPhone(arg, 2)
        if not data[0]:
            return
        macro(data[0], data[1][1])

    def do_cd(self,arg):
        'Change Device, set the current scope to the specified device extension "cd 50005"'
        if arg == '..' or arg == '/':
            self.prompt = 'AFX> '
            self.pwd = None
            return
        phone = findPhone(Phone.DN == arg)
        if not phone:
            print("Extension/DN '{0}' not found".format(arg))
            return
        self.pwd = phone
        self.prompt = 'AFX/{0}>'.format(phone.DN)
    
    def do_run(self,arg):
        'Run a python script "run test.py"'
        filename = arg or "test"
        if os.path.isfile(filename):
            print("Running: {0}", format(filename))
            execfile(filename)
            return 
        filename = filename+'.py'
        if os.path.isfile(filename):
            print("Running: {0}".format(filename))
            execfile(filename)
            return
        print("could not find file to run: {0}".format(filename))            

if __name__ == "__main__":
    main()