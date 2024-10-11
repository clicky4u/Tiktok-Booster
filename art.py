# banner.py

from colorama import Fore, init

# Initialize colorama for Windows compatibility (if you're using Windows)
init(autoreset=True)

def display_banner():
    print(f'''
{Fore.GREEN} ██████╗██╗     ██╗ ██████╗██╗  ██╗██╗   ██╗              ████████╗ ██████╗  ██████╗ ██╗     
{Fore.GREEN}██╔════╝██║     ██║██╔════╝██║ ██╔╝╚██╗ ██╔╝              ╚══██╔══╝██╔═══██╗██╔═══██╗██║     
{Fore.GREEN}██║     ██║     ██║██║     █████╔╝  ╚████╔╝     █████╗       ██║   ██║   ██║██║   ██║██║     
{Fore.GREEN}██║     ██║     ██║██║     ██╔═██╗   ╚██╔╝      ╚════╝       ██║   ██║   ██║██║   ██║██║     
{Fore.GREEN}╚██████╗███████╗██║╚██████╗██║  ██╗   ██║                    ██║   ╚██████╔╝╚██████╔╝███████╗
{Fore.GREEN} ╚═════╝╚══════╝╚═╝ ╚═════╝╚═╝  ╚═╝   ╚═╝                    ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝\n\n
        {Fore.RED}TELEGRAM: https://t.me/chen_lisal   {Fore.RED}GITHUB: https://github.com/clicky4u

        {Fore.BLUE}ctrl + z = Stopping process\n\n''')
