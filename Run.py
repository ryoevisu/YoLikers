try:
    import requests, json, time, re, urllib.parse, os, sys
    from rich import print as printf
    from rich.console import Console
    from rich.panel import Panel
    from requests.exceptions import RequestException
except (ModuleNotFoundError) as e:
    exit(f"Error: {str(e).capitalize()}!")

def TAMPILKAN_LOGO():
    os.system('cls' if os.name == 'nt' else 'clear')
    printf(Panel(r"""[bold red]   _     _          _       _ _                     
  | |   | |        (_)     (_) |                    
  | |___| | ___     _       _| |  _ _____  ____ ___ 
  |_____  |/ _ \   | |     | | |_/ ) ___ |/ ___)___)
   _____| | |_| |  | |_____| |  _ (| ____| |  |___ |
[bold white]  (_______|\___/   |_______)_|_| \_)_____)_|  (___/ 
        [underline green]Free Facebook Likes - Coded by Rozhak""", width=59, style="bold bright_black"))

def HEADERS():
    return {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Host': 'app.pagalworld2.com',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 9; RMX3301 Build/PQ3A.190605.003; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Safari/537.36',
        'v': '3.9',
        'X-Requested-With': 'com.yo.app'
    }

SUKSES, COOKIES, GAGAL, LOOPING = [], {"KEY": None, "FB": None}, [], 0

class MAIN:
    def __init__(self) -> None:
        self.retry_count = 0
        self.max_retries = 3
        self.session = requests.Session()
        self.session.headers.update(HEADERS())

    def LOGIN_COOKIES(self):
        try:
            TAMPILKAN_LOGO()
            printf(Panel("[bold white]Please fill in your Facebook cookies, make sure to use a new account to login, we\ndo not recommend using a real account!", width=59, style="bold bright_black", subtitle="[bold bright_black][bold bright_black]╭──────", subtitle_align="left", title="[bold bright_black][Cookies Facebook]"))
            self.COOKIES = Console().input("[bold bright_black]   ╰─> ")
            
            if 'c_user=' not in str(self.COOKIES):
                printf(Panel("[bold red]Invalid cookies format. Please enter valid Facebook cookies.", width=59, style="bold bright_black", title="[bold bright_black][Error]"))
                return self.LOGIN_COOKIES()

            COOKIES["FB"] = self.COOKIES

            printf(Panel("[bold white]Please fill in the post id you want to react to, make sure the post can be liked by the\npublic and is not private. Fill in only numbers!", width=59, style="bold bright_black", subtitle="[bold bright_black][bold bright_black]╭──────", subtitle_align="left", title="[bold bright_black][ID Postingan]"))
            self.POST_ID = int(Console().input("[bold bright_black]   ╰─> "))
            
            printf(Panel("[bold white]Please fill in the type of reaction you want from `[bold green]LIKE, LOVE, CARE, HAHA, WOW, SAD, and ANGRY[bold white]`, you can only enter one, no more. For example:[bold green] HAHA", width=59, style="bold bright_black", subtitle="[bold bright_black][bold bright_black]╭──────", subtitle_align="left", title="[bold bright_black][Tipe Reaksi]"))
            self.TIPE_REACTION = Console().input("[bold bright_black]   ╰─> ").upper()
            
            if self.TIPE_REACTION not in ['LIKE', 'LOVE', 'CARE', 'HAHA', 'WOW', 'SAD', 'ANGRY']:
                printf(Panel("[bold red]Invalid reaction type. Please choose from the available options.", width=59, style="bold bright_black", title="[bold bright_black][Error]"))
                return self.LOGIN_COOKIES()

            printf(Panel("[bold white]Starting process... Press[bold yellow] CTRL + C[bold white] to pause or[bold red] CTRL + Z[bold white] to stop", width=59, style="bold bright_black", title="[bold bright_black][Info]"))
            
            while True:
                try:
                    if COOKIES['KEY'] is None:
                        printf("[bold bright_black]   ──>[bold green] Validating cookies...          ", end='\r')
                        time.sleep(1.5)
                        if self.VALIDASI_COOKIES(COOKIES["FB"]):
                            continue
                    else:
                        printf("[bold bright_black]   ──>[bold green] Sending reaction...               ", end='\r')
                        time.sleep(1.5)
                        self.KIRIMKAN_REAKSI(self.POST_ID, self.TIPE_REACTION)
                        continue
                        
                except RequestException:
                    printf("[bold bright_black]   ──>[bold red] Network error. Retrying...     ", end='\r')
                    time.sleep(5)
                    continue
                    
                except KeyboardInterrupt:
                    printf("                                   ", end='\r')
                    time.sleep(2)
                    continue
                    
                except Exception as e:
                    printf(f"[bold bright_black]   ──>[bold red] Error: {str(e)}   ", end='\r')
                    time.sleep(5)
                    if self.retry_count < self.max_retries:
                        self.retry_count += 1
                        continue
                    else:
                        printf(Panel("[bold red]Max retries reached. Please check your connection and cookies.", width=59, style="bold bright_black", title="[bold bright_black][Error]"))
                        return False

        except Exception as e:
            printf(Panel(f"[bold red]{str(e)}", width=59, style="bold bright_black", title="[bold bright_black][Error]"))
            return False

    def VALIDASI_COOKIES(self, facebook_cookies):
        try:
            # Parse Facebook cookies
            cookie_dict = {}
            for cookie in facebook_cookies.split(';'):
                if cookie.strip():
                    key, value = cookie.strip().split('=', 1)
                    cookie_dict[key.strip()] = value.strip()
            
            # First request to get session cookies
            response = self.session.get('https://app.pagalworld2.com/')
            
            # Combine site cookies with Facebook cookies
            all_cookies = {**self.session.cookies.get_dict(), **cookie_dict}
            self.COOKIES_STRING = "; ".join([f"{k}={v}" for k, v in all_cookies.items()])
            
            self.session.headers.update({'Cookie': self.COOKIES_STRING})
            params = {
                'cookie': facebook_cookies,
                'access_token': '',
            }
            
            response2 = self.session.get('https://app.pagalworld2.com/login.php', params=params)
            
            if 'Login%20Successful' in str(response2.url) or 'dashboard' in str(response2.url):
                COOKIES["KEY"] = self.COOKIES_STRING
                printf("[bold bright_black]   ──>[bold green] Login successful!              ", end='\r')
                time.sleep(2)
                return True
                
            elif any(error in str(response2.text) for error in ['Your Account is locked', 'checkpoint']):
                printf("[bold bright_black]   ──>[bold red] Account locked or checkpoint              ", end='\r')
                time.sleep(2)
                return False
                
            else:
                printf("[bold bright_black]   ──>[bold red] Login failed. Retrying...              ", end='\r')
                time.sleep(2)
                return False
                
        except Exception as e:
            printf(f"[bold bright_black]   ──>[bold red] Validation error: {str(e)}              ", end='\r')
            time.sleep(2)
            return False

    def KIRIMKAN_REAKSI(self, post_id, tipe_rections):
        global SUKSES, GAGAL, LOOPING
        try:
            self.session.headers.update({'Cookie': COOKIES['KEY']})
            
            # Verify session before each request
            check_session = self.session.get('https://app.pagalworld2.com/dashboard.php')
            if 'index.php?error=Login' in str(check_session.url):
                printf("[bold bright_black]   ──>[bold yellow] Session expired. Relogging...  ", end='\r')
                COOKIES["KEY"] = None
                time.sleep(2)
                return self.VALIDASI_COOKIES(COOKIES["FB"])
            
            get_token = self.session.get('https://app.pagalworld2.com/dashboard.php?type=custom')
            find_token = re.search(r'var token = "(.*?)"', str(get_token.text))
            
            if not find_token:
                printf("[bold bright_black]   ──>[bold red] Token not found. Retrying...  ", end='\r')
                time.sleep(2)
                return False
            
            token = find_token.group(1)
            data = {
                'link': f'https://m.facebook.com/{post_id}',
                'type': 'react',
                'token': token,
                'reaction': tipe_rections
            }
            
            response = self.session.post('https://app.pagalworld2.com/modules/system/ajax.php', data=data)
            
            if 'Time Limit Reached' in str(response.text):
                printf(Panel("[bold red]Daily limit reached. Please try again tomorrow or use another account.", width=59, style="bold bright_black", title="[bold bright_black][Limit]"))
                return False
            
            elif 'Successfully Reacted' in str(response.text):
                LOOPING += 1
                SUKSES.append(LOOPING)
                printf(f"[bold bright_black]   ──>[bold green] Success: {len(SUKSES)} Failed: {len(GAGAL)}              ", end='\r')
                return True
            
            else:
                LOOPING += 1
                GAGAL.append(LOOPING)
                printf(f"[bold bright_black]   ──>[bold red] Success: {len(SUKSES)} Failed: {len(GAGAL)}              ", end='\r')
                return False
            
        except requests.exceptions.ConnectionError:
            printf("[bold bright_black]   ──>[bold red] Connection error. Retrying...  ", end='\r')
            time.sleep(5)
            return self.KIRIMKAN_REAKSI(post_id, tipe_rections)
            
        except Exception as e:
            LOOPING += 1
            GAGAL.append(LOOPING)
            printf(f"[bold bright_black]   ──>[bold red] Error: {str(e)}              ", end='\r')
            time.sleep(2)
            return False

class BYPASS:
    def __init__(self) -> None:
        pass

    def reCAPTCHA(self, sitekey):
        try:
            while True:
                solving = requests.get(f'https://token-recaptcha.com/?key={sitekey}&action=verify&page=dashboard&v=v3').json()
                if solving['status'] == 'success':
                    return solving['token']
                else:
                    continue
        except:
            return self.reCAPTCHA(sitekey)

def check_dir():
    if not os.path.exists("Penyimpanan"):
        os.makedirs("Penyimpanan")

if __name__ == '__main__':
    try:
        check_dir()
        if not os.path.exists("Penyimpanan/Subscribe.json"):
            youtube_url = json.loads(requests.get('https://raw.githubusercontent.com/RozhakXD/YoLikers/refs/heads/main/Penyimpanan/Youtube.json').text)['Link']
            os.system(f'xdg-open {youtube_url}')
            with open('Penyimpanan/Subscribe.json', 'w') as w:
                json.dump({"Status": True}, w)
            time.sleep(2.5)
            
        os.system('git pull')
        MAIN().LOGIN_COOKIES()
        
    except Exception as e:
        printf(Panel(f"[bold red]{str(e)}", width=59, style="bold bright_black", title="[bold bright_black][Error]"))
        sys.exit()
    except KeyboardInterrupt:
        printf("\n[bold red]Program terminated by user.")
        sys.exit()
