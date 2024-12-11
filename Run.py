import requests
import re
import json
import os
import time
from rich import print as printf
from rich.panel import Panel
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def validate_cookie(cookie_string):
    try:
        headers = {
            'Cookie': cookie_string,
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
        }
        response = requests.get('https://www.facebook.com/me', headers=headers, allow_redirects=True)
        return 'facebook.com/home' not in response.url
    except:
        return False

def get_cookies():
    clear()
    printf(Panel("""[bold white]Facebook Cookie Getter
[bold green]1[bold white]. Get from Email/Pass
[bold green]2[bold white]. Get from Token
[bold green]3[bold white]. Exit""", title="[bold white]Menu"))
    
    choice = Console().input("[bold white]Choose: ")
    
    if choice == '1':
        return get_from_login()
    elif choice == '2':
        return get_from_token()
    elif choice == '3':
        exit("[bold red]Thanks for using!")
    else:
        printf("[bold red]Invalid choice!")
        return get_cookies()

def loading_animation(description="Processing"):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description=description, total=None)
        time.sleep(2)

def get_from_login():
    clear()
    printf(Panel("[bold white]Enter your Facebook credentials", title="[bold white]Login"))
    
    email = Console().input("[bold white]Email/Phone: ")
    password = Console().input("[bold white]Password: ")
    
    try:
        loading_animation("Attempting login...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
        }
        
        session = requests.Session()
        response = session.get('https://m.facebook.com/', headers=headers)
        
        try:
            lsd = re.search('name="lsd" value="(.*?)"', str(response.text)).group(1)
            jazoest = re.search('name="jazoest" value="(.*?)"', str(response.text)).group(1)
            m_ts = re.search('name="m_ts" value="(.*?)"', str(response.text)).group(1)
            li = re.search('name="li" value="(.*?)"', str(response.text)).group(1)
        except AttributeError:
            printf(Panel("[bold red]Failed to extract form data. Site might be blocking automated access.", title="[bold red]Error"))
            return get_cookies()
        
        data = {
            'lsd': lsd,
            'jazoest': jazoest,
            'm_ts': m_ts,
            'li': li,
            'try_number': '0',
            'unrecognized_tries': '0',
            'email': email,
            'pass': password,
            'login': 'Log In'
        }
        
        response = session.post('https://m.facebook.com/login/device-based/regular/login/?refsrc=deprecated&lwv=100&ref=dbl', 
                              data=data, headers=headers, allow_redirects=True)
        
        if 'c_user' in session.cookies.get_dict():
            cookies = convert_cookies_to_string(session.cookies.get_dict())
            
            loading_animation("Validating cookies...")
            if validate_cookie(cookies):
                printf(Panel(f"[bold green]Success! Valid cookies:\n\n[bold white]{cookies}", title="[bold white]Result"))
                Console().input("[bold green]Press Enter to continue...")
            else:
                printf(Panel("[bold red]Generated cookies are invalid!", title="[bold red]Error"))
        else:
            printf(Panel("[bold red]Login failed! Check your credentials or try again later.", title="[bold red]Error"))
            
    except Exception as e:
        printf(Panel(f"[bold red]Error: {str(e)}", title="[bold red]Error"))
    
    return get_cookies()

def get_from_token():
    clear()
    printf(Panel("[bold white]Enter your Facebook Access Token", title="[bold white]Token"))
    
    token = Console().input("[bold white]Token: ")
    
    try:
        loading_animation("Validating token...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Authorization': f'Bearer {token}'
        }
        
        response = requests.get('https://graph.facebook.com/me?access_token=' + token)
        
        if 'error' in response.json():
            printf(Panel("[bold red]Invalid token!", title="[bold red]Error"))
        else:
            loading_animation("Generating cookies...")
            session = requests.Session()
            response = session.get(f'https://api.facebook.com/method/auth.getSessionforApp?access_token={token}&format=json&new_app_id=275254692598279&generate_session_cookies=1')
            
            if 'session_cookies' in response.json():
                cookies = ''
                for cookie in response.json()['session_cookies']:
                    cookies += f"{cookie['name']}={cookie['value']}; "
                
                loading_animation("Validating cookies...")
                if validate_cookie(cookies):
                    printf(Panel(f"[bold green]Success! Valid cookies:\n\n[bold white]{cookies}", title="[bold white]Result"))
                    Console().input("[bold green]Press Enter to continue...")
                else:
                    printf(Panel("[bold red]Generated cookies are invalid!", title="[bold red]Error"))
            else:
                printf(Panel("[bold red]Failed to get cookies from token!", title="[bold red]Error"))
    
    except Exception as e:
        printf(Panel(f"[bold red]Error: {str(e)}", title="[bold red]Error"))
    
    return get_cookies()

def convert_cookies_to_string(cookie_dict):
    return '; '.join([f"{key}={value}" for key, value in cookie_dict.items()])

if __name__ == '__main__':
    try:
        get_cookies()
    except KeyboardInterrupt:
        exit("\n[bold red]Program terminated by user!")
    except Exception as e:
        exit(f"[bold red]Error: {str(e)}")
