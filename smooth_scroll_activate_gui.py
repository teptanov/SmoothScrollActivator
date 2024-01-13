import winreg
import tkinter as tk
import customtkinter as ctk
from datetime import datetime
import pytz
from threading import Thread
import time
import sys, os

novokuznetsk_tz = pytz.timezone('Asia/Novokuznetsk')
sub_key = "Software\\SmoothScroll"
activate_sub = {'kSSLicenseCode': "P5FB2As9XG4jpuZq6zhydn", 'kSSLicenseName': "Teptanov", 'kSSSubscriptionID': '1'}
def get_executable_directory():
    if getattr(sys, 'frozen', False):
        # Если скрипт запущен как исполняемый файл (скомпилированный с помощью nuitka или другим способом)
        return os.path.dirname(sys.executable)
    else:
        # Если скрипт запущен интерпретатором Python
        return os.path.dirname(os.path.abspath(__file__))
# command_autostart = f'chcp 1251\ncmd /min /C "set __COMPAT_LAYER=RUNASINVOKER && start "" "{sys.argv[0].encode("windows 1251").decode("windows 1251")}""'
# command_autostart = f'chcp 1251\ncmd /min /C "set __COMPAT_LAYER=RUNASINVOKER && start "" "{get_executable_directory()}\SmoothScroll_Activator.exe""'
command_autostart = """@echo off
setlocal enabledelayedexpansion

for /f %%a in ('powershell -command "(Get-Date).ToUniversalTime().Subtract((Get-Date "1970-01-01")).TotalSeconds"') do set "timestamp=%%a"
echo %timestamp%
set /a "timestamp=timestamp/1"
echo %timestamp%

set "subKey=Software\SmoothScroll"
set "valueName=kSSInstallDate"
set "valueData=!timestamp!"

reg add "HKCU\%subKey%" /v "%valueName%" /t REG_SZ /d "%valueData%" /f > nul 2>&1

endlocal"""
print("__file__: ", __file__)
print("sys.argv[0]: ", sys.argv[0])
# print(command_autostart)
os.system('chcp 1251')

root = ctk.CTk()
X, Y = 500, 230
root.geometry(f"{X}x{Y}")
root.title('SmoothScroll Activator by Teptanov')
root.resizable(False,False)

frame_main = ctk.CTkFrame(root)
frame_main.pack(fill=tk.BOTH, expand=True)


def days_between_timestamps(timestamp1, timestamp2) -> int:
    try:
        # Преобразуем метки времени в объекты datetime
        datetime1 = datetime.utcfromtimestamp(int(timestamp1))
        datetime2 = datetime.utcfromtimestamp(int(timestamp2))

        # print(int(timestamp1) - int(timestamp2))
        # Вычисляем разницу между двумя метками времени
        time_difference = datetime1 - datetime2


        # Извлекаем количество дней, часов, минут и секунд из разницы
        years = time_difference.days // 365
        days = time_difference.days % 365
        hours, remainder = divmod(time_difference.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return years, days, hours, minutes, seconds
    except:
        return (0,0,0,0)

def current_datetime_to_timestamp():
    try:
        current_datetime = datetime.now(tz=novokuznetsk_tz)
        timestamp = current_datetime.timestamp()
        return timestamp
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None

# Получение метки времени для текущей даты и времени
timestamp = current_datetime_to_timestamp()


def read_registry_value(value_name: str|dict = "kSSInstallDate" ):
    try:
        # Открываем ключ реестра
        key = winreg.HKEY_CURRENT_USER
        # sub_key = "Software\\SmoothScroll"  # Путь к ключу, из которого нужно прочитать значение
        access = winreg.KEY_READ

        # Открываем существующий ключ для чтения
        reg_key = winreg.OpenKey(key, sub_key, 0, access)
        if type(value_name) == dict:
            temp = value_name
            for i in value_name:
                value, _ = winreg.QueryValueEx(reg_key, i)
                temp[i] = value
            print(value_name, temp)
            winreg.CloseKey(reg_key)
            return temp
        else:
            # Читаем значение из реестра
            value, _ = winreg.QueryValueEx(reg_key, value_name)
        
        # Выводим прочитанное значение
        # print(f"Значение параметра {value_name}: {value}")
        
        # Закрываем ключ реестра
        winreg.CloseKey(reg_key)

        return value
       
    except FileNotFoundError:
        print("Ключ реестра не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        
def modify_registry(timestamp_date, if_sub = False):
    # timestamp = current_datetime_to_timestamp()
    try:
        # Открываем ключ реестра
        key = winreg.HKEY_CURRENT_USER
        # sub_key = "Software\\SmoothScroll"  # Путь к ключу, который нужно изменить/создать
        access = winreg.KEY_SET_VALUE
         # Создаем или открываем существующий ключ
        reg_key = winreg.OpenKey(key, sub_key, 0, access)

        
        if if_sub:
            for i in activate_sub:
                if i == "kSSSubscriptionID":
                    winreg.SetValueEx(reg_key, i, 0, winreg.REG_SZ, str(current_datetime_to_timestamp()).split('.')[0])
                else:
                    winreg.SetValueEx(reg_key, i, 0, winreg.REG_SZ, activate_sub[i])
        else:
            # Устанавливаем значение в реестре
            value_name = "kSSInstallDate"  # Название параметра
            value_data = timestamp_date  # Значение параметра
            winreg.SetValueEx(reg_key, value_name, 0, winreg.REG_SZ, value_data)

        # Закрываем ключ реестра
        winreg.CloseKey(reg_key)
        print("Значение успешно изменено в реестре.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

def main():
    timestamp = current_datetime_to_timestamp()
    if timestamp is not None:
        print(f"Текущая дата и время: {datetime.now()}")
        print(f"Метка времени (timestamp) для текущей даты и времени: {timestamp}")
        # Вызов функции для изменения реестра
        modify_registry(str(timestamp).split('.')[0], False)
    StatusBar.configure(text=f"timestamp в SmoothScroll: {read_registry_value()}\ntimestamp Now: {int(timestamp)}")
def main_sub():
    timestamp = current_datetime_to_timestamp()
    if timestamp is not None:
        print(f"Текущая дата и время: {datetime.now()}")
        print(f"Метка времени (timestamp) для текущей даты и времени: {timestamp}")
        # Вызов функции для изменения реестра
        modify_registry(str(timestamp).split('.')[0], True)
    StatusBar.configure(text=f"timestamp в SmoothScroll: {read_registry_value()}\ntimestamp Now: {int(timestamp)}")
    # StatusBar.update()
    # root.update()

def get_autostart():
    start_up=os.path.join(os.path.join(os.environ['USERPROFILE']), r'AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup')
    bat_name = f'{start_up}\\SmoothScroll_Activator.bat'
    autostart = False
    try:
        if os.path.exists(bat_name):
            with open(bat_name, 'r') as f:
                if f.read() == command_autostart:
                    autostart = True
            f.close()
    except: pass
    return autostart
            
def autostart():
    try:
        start_up=os.path.join(os.path.join(os.environ['USERPROFILE']), r'AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup')
        bat_name = f'{start_up}\\SmoothScroll_Activator.bat'
        if autostart_var.get() == 'on':
            try:
                with open(bat_name,'w') as f:
                    f.write(command_autostart)
                f.close()
            except Exception as e: print(e)
        else:
            try:
                os.remove(bat_name)
            except Exception as e: print(e)
        print(get_autostart())
    except: pass

# def autostart_on():
#     try:
#         start_up=os.path.join(os.path.join(os.environ['USERPROFILE']), r'AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup')
#         bat_name = f'{start_up}\\SmoothScroll_Activator.bat'
#         command = f'chcp 1251\ncmd /min /C "set __COMPAT_LAYER=RUNASINVOKER && start "" "{sys.argv[0].encode("windows 1251").decode("windows 1251")}""'
#         with open(bat_name,'w') as f:
#             f.write(command)
#         f.close()
#     except Exception as e: print(e)
# def autostart_off():
#     start_up=os.path.join(os.path.join(os.environ['USERPROFILE']), r'AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup')
#     bat_name = f'{start_up}\\SmoothScroll_Activator.bat'
#     try: os.remove(bat_name)
#     except Exception as e: print(e)

def updater():
    global timestamp
    while 1:
        try:
            timestamp = current_datetime_to_timestamp()
            StatusBar.configure(text=f"timestamp в SmoothScroll: {read_registry_value()}\ntimestamp Now: {int(timestamp)}")

            years, days, hours, minutes, seconds = days_between_timestamps(current_datetime_to_timestamp(),read_registry_value())
            years = f"{years} лет" if years!=0 else ""
            days = f"{days} дней" if days!=0 else ""
            hours = f"{hours} часов" if hours!=0 else "0h"
            minutes = f"{minutes}м" if minutes!=0 else "0m"
            seconds = f"{seconds}с" if seconds!=0 else "0с"
            status = f"Последняя активация: {years} {days} {hours} {minutes} {seconds} назад\n"
            # print(int(read_registry_value()) - timestamp)
            if int(read_registry_value()) - timestamp <= -1814400:
                sub = 'Пробный период закончился, активируйте снова!'
                status += sub
            elif int(read_registry_value()) - timestamp>0:
                sub = 'Пробный период не может заканчиваться в будущем!!!'
                status += sub
            else:
                _, days_, hours_, minutes_, seconds_ = map(abs, days_between_timestamps(int(read_registry_value()),current_datetime_to_timestamp()-1814400))
                days_ = f"{days_} дней" if days_!=0 else ""
                hours_ = f"{hours_} часов" if hours_!=0 else "0h"
                minutes_ = f"{minutes_}м" if minutes_!=0 else "0m"
                seconds_ = f"{seconds_}с" if seconds_!=0 else "0с"
                sub = f'Пробный период еще:  {days_} {hours_} {minutes_} {seconds_}'
                status += sub
            StatusBar2.configure(text=status)
            time.sleep(1)
        except Exception as e:
            if str(e) == 'main thread is not in main loop':
                break
            print(e)


by_Teptanov = ctk.CTkLabel(frame_main,text = 'by Teptanov',font=("ISOCPEUR Regular", 9)).place(x=340,y=30)
SmoothScroll_activator = ctk.CTkLabel(frame_main,text = 'SmoothScroll Activator',font=("ISOCPEUR Regular 400", 24)).place(x=135,y=12)



status = f"Последняя активация: назад\nПробный период:"
StatusBar2 = ctk.CTkLabel(frame_main,text=status,justify='center',anchor='center',width=X)
StatusBar2.place(x=0,y=77)

sub_instuct = ctk.CTkLabel(frame_main,text = '(Подписку нужно активировать раз в 21 день)',font=("ISOCPEUR Regular", 10)).place(x=140,y=162)
activate_trial_btn = ctk.CTkButton(frame_main,width = 10, height = 10, text="Активировать",command=main).place(x=198,y=145)

# activate_trial_btn = ctk.CTkButton(frame_main,width = 10, height = 10, text="Активировать\nПробный Период",command=main).place(x=245,y=138)
# activate_btn = ctk.CTkButton(frame_main,width = 10, height = 10, text="Активировать\nПодписку",command=main_sub).place(x=140,y=138)


StatusBar_frame = ctk.CTkFrame(frame_main,height=35)
StatusBar_frame.pack(side='bottom',fill='x')
StatusBar = ctk.CTkLabel(StatusBar_frame,text=f"_\n_",)
StatusBar.pack(padx=6, pady=6)
def theme():
    print(ctk.get_appearance_mode(),theme_var.get())
    ctk.set_appearance_mode(theme_var.get())
theme_var = tk.Variable()
theme_var.set("Dark")
theme_switcher = ctk.CTkSwitch(StatusBar_frame,text='theme',offvalue='Light',onvalue='Dark',variable=theme_var, command = theme).place(x=4,y=7)

autostart_var = tk.Variable()
if get_autostart():
    autostart_var.set("on")
else:
    autostart_var.set("off")
theme_switcher = ctk.CTkSwitch(StatusBar_frame,text='autostart',offvalue='off',onvalue='on',variable=autostart_var, command = autostart).place(x=X-105,y=7)


Thread(target=updater).start()
root.mainloop()