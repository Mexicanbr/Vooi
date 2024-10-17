import json
import time
import os
import random
from datetime import datetime
import urllib.parse
import cloudscraper
from colorama import Fore, init, Style
from dateutil import parser
from dateutil.tz import tzutc

init(autoreset=True)

class VooiDC:
    def __init__(self):
        self.base_headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
            "Content-Type": "application/json",
            "Origin": "https://app.tg.vooi.io",
            "Referer": "https://app.tg.vooi.io/",
            "Sec-Ch-Ua": '"Not/A)Brand";v="99", "Google Chrome";v="118", "Chromium";v="118"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
        }
        self.scraper = cloudscraper.create_scraper()
        self.access_token = None

    def art(self):
        print(Fore.RED + Style.BRIGHT + r"""
   __  __            _      ____  ____      _                 _ 
                                ##                                ###
                                                                 ##
 ##  ##    ####    ##  ##    ###      ####     ####    #####     ##      ######
 #######  ##  ##    ####      ##     ##  ##       ##   ##  ##    #####    ##  ##
 ## # ##  ######     ##       ##     ##        #####   ##  ##    ##  ##   ##
 ##   ##  ##        ####      ##     ##  ##   ##  ##   ##  ##    ##  ##   ##
 ##   ##   #####   ##  ##    ####     ####     #####   ##  ##   ######   ####


    """ + Fore.YELLOW + Style.BRIGHT + "Bot de Reivindicação Automática Para Vooi - Script MexicanBR" + Style.RESET_ALL + r"""
    Autor   : MexicanBR
    Github   : https://github.com/Mexicanbr/
    Telegram : https://t.me/MexicanbrScripts
    """ + Style.RESET_ALL)

    def get_headers(self):
        headers = self.base_headers.copy()
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        return headers

    def log(self, msg, tipo='info'):
        timestamp = f"{Fore.YELLOW}{Style.BRIGHT}{datetime.now().strftime('%H:%M:%S')}"
        if tipo == 'success':
            print(f"[{timestamp}] [t.me/MexicanbrScripts] {Fore.GREEN}{Style.BRIGHT}{msg}")
        elif tipo == 'custom':
            print(f"[{timestamp}] [t.me/MexicanbrScripts] {Fore.MAGENTA}{Style.BRIGHT}{msg}")
        elif tipo == 'error':
            print(f"[{timestamp}] [t.me/MexicanbrScripts] {Fore.RED}{Style.BRIGHT}{msg}")
        elif tipo == 'warning':
            print(f"[{timestamp}] [t.me/MexicanbrScripts] {Fore.YELLOW}{Style.BRIGHT}{msg}")
        else:
            print(f"[{timestamp}] [t.me/MexicanbrScripts] {Fore.RED}{Style.BRIGHT}{msg}")

    def countdown(self, segundos):
        for i in range(segundos, -1, -1):
            print(f"\r===== Aguarde {i} Segundos para continuar =====", end="", flush=True)
            time.sleep(1)
        print()

    def login_new_api(self, init_data):
        url = "https://api-tg.vooi.io/api/v2/auth/login"
        payload = {
            "initData": init_data,
            "inviterTelegramId": ""
        }
        try:
            response = self.scraper.post(url, json=payload, headers=self.get_headers())
            if response.status_code == 201:
                self.access_token = response.json()['tokens']['access_token']
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": 'Status de resposta inesperado'}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def check_autotrade(self):
        url = "https://api-tg.vooi.io/api/autotrade"
        try:
            response = self.scraper.get(url, headers=self.get_headers())
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            self.log(f"Erro ao verificar autotrade: {str(e)}", 'error')
            return None

    def start_autotrade(self):
        url = "https://api-tg.vooi.io/api/autotrade/start"
        payload = {}
        try:
            response = self.scraper.post(url, json=payload, headers=self.get_headers())
            if response.status_code in [200, 201]:
                return response.json()
            else:
                return None
        except Exception as e:
            self.log(f"Erro ao iniciar autotrade: {str(e)}", 'error')
            return None

    def claim_autotrade(self, auto_trade_id):
        url = "https://api-tg.vooi.io/api/autotrade/claim"
        payload = {"autoTradeId": auto_trade_id}
        try:
            response = self.scraper.post(url, json=payload, headers=self.get_headers())
            if response.status_code in [200, 201]:
                return response.json()
            else:
                return None
        except Exception as e:
            self.log(f"Erro ao reivindicar autotrade: {str(e)}", 'error')
            return None

    def print_autotrade_info(self, data):
        end_time = parser.parse(data['endTime'])
        current_time = datetime.now(tzutc())
        time_left = end_time - current_time
        
        hours, remainder = divmod(time_left.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        rounded_time_left = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

        self.log(f"Autotrade concluído em: {end_time.strftime('%d/%m/%Y %H:%M:%S')} UTC", 'custom')
        self.log(f"Tempo restante: {rounded_time_left}", 'custom')

    def handle_autotrade(self):
        autotrade_data = self.check_autotrade()
        if not autotrade_data:
            self.log("Iniciar novo autotrade...", 'warning')
            autotrade_data = self.start_autotrade()
            if autotrade_data:
                self.print_autotrade_info(autotrade_data)
            else:
                self.log("Falha ao iniciar novo autotrade.", 'error')
                return

        if autotrade_data['status'] == 'finished':
            self.log("Autotrade concluído, recebendo recompensa...", 'success')
            claim_result = self.claim_autotrade(autotrade_data['autoTradeId'])
            if claim_result:
                self.log(f"Reivindicação do autotrade bem-sucedida. Recompensa {claim_result['reward']['virtMoney']} USD {claim_result['reward']['virtPoints']} VT", 'success')
                self.log(f"Saldo total {claim_result['balance']['virt_money']} USDT | {claim_result['balance']['virt_points']} VT", 'success')
            else:
                self.log("Falha ao reivindicar recompensa do autotrade.", 'error')

            self.log("Iniciar nova negociação automática...", 'warning')
            new_autotrade_data = self.start_autotrade()
            if new_autotrade_data:
                self.print_autotrade_info(new_autotrade_data)
            else:
                self.log("Falha ao iniciar nova negociação automática.", 'error')
        else:
            self.print_autotrade_info(autotrade_data)

    def start_tapping_session(self):
        url = "https://api-tg.vooi.io/api/tapping/start_session"
        payload = {}
        try:
            response = self.scraper.post(url, json=payload, headers=self.get_headers())
            if response.status_code in [200, 201]:
                return response.json()
            else:
                return None
        except Exception as e:
            self.log(f"Falha ao iniciar Tap: {str(e)}", 'error')
            return None

    def finish_tapping_session(self, session_id, virt_money, virt_points):
        url = "https://api-tg.vooi.io/api/tapping/finish"
        payload = {
            "sessionId": session_id,
            "tapped": {
                "virtMoney": virt_money,
                "virtPoints": virt_points
            }
        }
        try:
            response = self.scraper.post(url, json=payload, headers=self.get_headers())
            if response.status_code in [200, 201]:
                return response.json()
            else:
                self.log(f"Código de status inesperado ao finalizar a sessão de tapping: {response.status_code}", 'warning')
                return None
        except Exception as e:
            self.log(f"Erro ao finalizar a sessão de tapping: {str(e)}", 'error')
            return None

    def play_tapping_game(self):
        for game_number in range(1, 5):
            self.log(f"Iniciar jogo de tapping {game_number}/5", 'custom')
            session_data = self.start_tapping_session()
            if not session_data:
                self.log(f"Início do jogo {game_number} falhou. Pulando...", 'warning')
                continue

            virt_money_limit = int(session_data['config']['virtMoneyLimit'])
            virt_points_limit = int(session_data['config']['virtPointsLimit'])

            self.log(f"Jogando por 30 segundos...", 'custom')
            time.sleep(30)

            virt_money = random.randint(max(1, int(virt_money_limit * 0.5)), int(virt_money_limit * 0.8))
            virt_money = virt_money - (virt_money % 1)
            virt_points = virt_points_limit

            result = self.finish_tapping_session(session_data['sessionId'], virt_money, virt_points)
            if result:
                self.log(f"Tap bem-sucedido, recompensa {result['tapped']['virtMoney']} USD | {result['tapped']['virtPoints']} VT", 'success')
            else:
                self.log(f"Finalização do jogo {game_number} falhou", 'error')

            if game_number < 5:
                self.log("Aguarde 3 segundos...", 'custom')
                time.sleep(3)

    def get_tasks(self):
        url = "https://api-tg.vooi.io/api/tasks?limit=200&skip=0"
        try:
            response = self.scraper.get(url, headers=self.get_headers())
            if response.status_code == 200:
                return response.json()
            else:
                self.log(f"Código de status inesperado ao obter tarefas: {response.status_code}", 'warning')
                return None
        except Exception as e:
            self.log(f"Erro ao obter tarefas: {str(e)}", 'error')
            return None

    def start_task(self, task_id):
        url = f"https://api-tg.vooi.io/api/tasks/start/{task_id}"
        try:
            response = self.scraper.post(url, json={}, headers=self.get_headers())
            if response.status_code in [200, 201]:
                return response.json()
            else:
                self.log(f"Código de status inesperado ao iniciar tarefa: {response.status_code}", 'warning')
                return None
        except Exception as e:
            self.log(f"Erro ao iniciar tarefa: {str(e)}", 'error')
            return None

    def claim_task(self, task_id):
        url = f"https://api-tg.vooi.io/api/tasks/claim/{task_id}"
        try:
            response = self.scraper.post(url, json={}, headers=self.get_headers())
            if response.status_code in [200, 201]:
                return response.json()
            else:
                self.log(f"Código de status inesperado ao reivindicar tarefa: {response.status_code}", 'warning')
                return None
        except Exception as e:
            self.log(f"Erro ao reivindicar tarefa: {str(e)}", 'error')
            return None

    def manage_tasks(self):
        tasks_data = self.get_tasks()
        if not tasks_data:
            self.log("Falha ao obter dados das tarefas", 'error')
            return

        new_tasks = [task for task in tasks_data['nodes'] if task['status'] == 'new']
        for task in new_tasks:
            result = self.start_task(task['id'])
            if result and result['status'] == 'in_progress':
                self.log(f"Tarefa {task['description']} realizada com sucesso", 'success')
            else:
                self.log(f"Falha ao realizar tarefa {task['description']}", 'error')

        completed_tasks = [task for task in tasks_data['nodes'] if task['status'] == 'done']
        for task in completed_tasks:
            result = self.claim_task(task['id'])
            if result and 'claimed' in result:
                virt_money = result['claimed']['virt_money']
                virt_points = result['claimed']['virt_points']
                self.log(f"Tarefa {task['description']} realizada com sucesso | Recompensa {virt_money} USD | {virt_points} VT", 'success')
            else:
                self.log(f"Falha ao reivindicar recompensa da tarefa | {task['description']}", 'error')

    def main(self):
        self.art()  # Chama a função de arte
        data_file = os.path.join(os.path.dirname(__file__), 'data.txt')
        with open(data_file, 'r', encoding='utf-8') as f:
            data = [line.strip() for line in f if line.strip()]

        while True:
            for i, init_data in enumerate(data):
                user_data = json.loads(urllib.parse.unquote(init_data.split('user=')[1].split('&')[0]))
                user_id = user_data['id']
                first_name = user_data['first_name']
                current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

                print(f"{Fore.GREEN}{'=' * 10} {Fore.RED}{Style.BRIGHT}Conta {i + 1} → {Fore.GREEN}{first_name} {Fore.YELLOW}{Style.BRIGHT}{current_time} {Fore.GREEN}{'=' * 10}")
                login_result = self.login_new_api(init_data)
                if login_result['success']:
                    self.log('Login bem-sucedido!', 'success')
                    self.log(f"Nome: {login_result['data']['name']}")
                    self.log(f"USD*: {login_result['data']['balances']['virt_money']}")
                    self.log(f"VT: {login_result['data']['balances']['virt_points']}")
                    self.log(f"Ref: {login_result['data']['frens']['count']}/{login_result['data']['frens']['max']}")
                    
                    self.handle_autotrade()
                    self.play_tapping_game()
                    self.manage_tasks()
                else:
                    self.log(f"Falha no login! {login_result['error']}", 'error')

                time.sleep(1)

            self.countdown(10 * 60)

if __name__ == "__main__":
    client = VooiDC()
    try:
        client.main()
    except Exception as e:
        client.log(str(e), 'error')
        exit(1)