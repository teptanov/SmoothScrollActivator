#include <iostream>
#include <chrono>
#include <Windows.h>
#include <sstream>

using namespace std;


int get_timestamp() {
    try {
        // Получение текущей даты и времени
        auto current_time = std::chrono::system_clock::now();

        // Преобразование текущей даты и времени в метку времени (timestamp)
        std::chrono::duration<double> timestamp = current_time.time_since_epoch();
        std::cout << "Текущая дата и время: " << std::chrono::system_clock::to_time_t(current_time) << std::endl;
        //std::cout << "Метка времени (timestamp) для текущей даты и времени: " << timestamp.count() << std::endl;
        return timestamp.count();
    }
    catch (const std::exception& e) {
        std::cout << "Произошла ошибка: " << e.what() << std::endl;
        return 0;
    }
}


int main() {
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);

    HKEY hKey;
    LPCWSTR subKey = L"Software\\SmoothScroll"; // Путь к ключу, который нужно изменить/создать
    LPCWSTR valueName = L"kSSInstallDate"; // Название параметра
    LPCWSTR valueData = L""; // Значение параметра


    // Буфер для хранения широкой строки
    wchar_t buffer[20]; // Вы можете выбрать размер буфера в зависимости от вашего ожидаемого значения
    // Преобразование int в LPCWSTR
    swprintf_s(buffer, L"%d", get_timestamp());
    LPCWSTR convertedValue = buffer;

    valueData = convertedValue;

    if (valueData != L"0") {
        LONG openKeyResult = RegOpenKeyEx(HKEY_CURRENT_USER, subKey, 0, KEY_SET_VALUE, &hKey);
        if (openKeyResult == ERROR_SUCCESS) {
            LONG setValueResult = RegSetValueEx(hKey, valueName, 0, REG_SZ, reinterpret_cast<BYTE*>(const_cast<LPWSTR>(valueData)), (wcslen(valueData) + 1) * sizeof(WCHAR));
            if (setValueResult == ERROR_SUCCESS) {
                wcout << L"Значение успешно изменено в реестре." << endl;
                cout << "Значение успешно изменено в реестре." << endl;
            }
            else {
                cerr << "Ошибка при установке значения в реестре: " << setValueResult << endl;
                cout << "Ошибка при установке значения в реестре!" << endl;
            }
            RegCloseKey(hKey);
        }
        else {
            cerr << "Ошибка при открытии ключа реестра: " << openKeyResult << endl;
            cout << "Ошибка при открытии ключа реестра!" << endl;
        }
    }
    return 0;
}


