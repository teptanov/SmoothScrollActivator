import winreg

from datetime import datetime

def current_datetime_to_timestamp():
    try:
        current_datetime = datetime.now()
        timestamp = current_datetime.timestamp()
        return timestamp
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None

# Получение метки времени для текущей даты и времени
timestamp = current_datetime_to_timestamp()

if timestamp is not None:
    print(f"Текущая дата и время: {datetime.now()}")
    print(f"Метка времени (timestamp) для текущей даты и времени: {timestamp}")



    def modify_registry(timestamp_date):
        try:
            # Открываем ключ реестра
            key = winreg.HKEY_CURRENT_USER
            sub_key = "Software\\SmoothScroll"  # Путь к ключу, который нужно изменить/создать
            access = winreg.KEY_SET_VALUE

            # Создаем или открываем существующий ключ
            reg_key = winreg.OpenKey(key, sub_key, 0, access)

            # Устанавливаем значение в реестре
            value_name = "kSSInstallDate"  # Название параметра
            value_data = timestamp_date  # Значение параметра
            winreg.SetValueEx(reg_key, value_name, 0, winreg.REG_SZ, value_data)

            # Закрываем ключ реестра
            winreg.CloseKey(reg_key)
            print("Значение успешно изменено в реестре.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    # Вызов функции для изменения реестра
    modify_registry(str(timestamp).split('.')[0])
