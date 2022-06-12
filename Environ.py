
import os

def check_environment_variables_exist() -> bool:
    if os.getenv('ViperUser') != None and os.getenv('ViperAccess') != None:
        vHostName = os.getenv('ViperHost')
        vUserName = os.getenv('ViperUser')
        vPassWord = os.getenv('ViperAccess')
        print(vHostName, vUserName, vPassWord)
        return True
    
    print("Environment vars don't exist")
    grab_secret("vars.txt")
    return False

def grab_secret(file_name):
    with open(file_name) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
        define_environment_variables(lines)

def define_environment_variables(vars: list) -> bool:
    os.system("SETX {0} {1} /M".format('ViperHost', vars[0]))
    os.system("SETX {0} {1} /M".format('ViperUser', vars[1]))
    os.system("SETX {0} {1} /M".format('ViperAccess', vars[2]))
    
def main():
    print(check_environment_variables_exist())
    if os.path.exists("vars.txt"):
        fs = os.path.getsize("vars.txt")
        with open('vars.txt', "w") as myfile:
            for i in range(fs):
                myfile.write("0")
        
        os.remove("vars.txt")
    
        
main()