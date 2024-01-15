import os
import json
import  re
import sys
import keyboard
# чтение файла
line_num2 = 0 
line_num = 0
if_obr = True
#file_batch = "test.b++"
file_batch = sys.argv[1]
if_com = 0
value = []

def command_obr(Str):
    global line, value, line_num, file_batch, if_obr
    command = Str.split()
    if command[0] == "pause>nul":
        keyboard.read_event()

    if command[0] == "pause":
        print("Для продолжения нажмите любую клавишу...")
        keyboard.read_event()

    if command[0] == "sys":
        index = command.index("sys")
        words_after = command[index + 1:]
        result = ' '.join(words_after)
        os.system(result)

    if command[0] == "goto":
        with open(file_batch, 'r') as file:
            lines = file.readlines()

            for idx, line in enumerate(lines):
                if line.startswith(":"):
                    label_name = line.strip()  # Получаем название метки
                    #print(f"Метка '{label_name}' найдена на строке {idx + 1}")
                    if label_name == command[1]:
                        line_num = idx
                            
    #input 
    if command[0] == "input":
        index = command.index("=")
        words_after = command[index + 1:]
        result = ' '.join(words_after)
        inp = input(result)
        set_valuse = f"set {command[1]} {inp}"
        command_obr(set_valuse)

    #set
    if command[0] == "set":
        if command[1] == "/p":
            index = command.index("=")
            words_after = command[index + 1:]
            result = ' '.join(words_after)
            inp = input(result)
            set_value = {
                'name': command[2],
                'value': inp
            }
            temp = value.copy()  # Создаем копию списка value
            found = False  # Флаг для отслеживания наличия совпадений

            for index, json in enumerate(temp):
                #print(f"Index: {index}, Fruit: {json}")
                if set_value["name"] == json['name']:
                    temp[index] = set_value
                    found = True  # Устанавливаем флаг, если найдено совпадение
                    break  # Прерываем цикл, так как уже произошло обновление значения

            if not found:
                temp.append(set_value)  # Если совпадений не найдено, добавляем новое значение

            value = temp  # Присваиваем обновленное значение переменной value
        else:
            index = command.index("=")
            words_after = command[index + 1:]
            result = ' '.join(words_after)
            set_value = {
                'name': command[1],
                'value': result
            }
            temp = value.copy()  # Создаем копию списка value
            found = False  # Флаг для отслеживания наличия совпадений

            for index, json in enumerate(temp):
                #print(f"Index: {index}, Fruit: {json}")
                if set_value["name"] == json['name']:
                    temp[index] = set_value
                    found = True  # Устанавливаем флаг, если найдено совпадение
                    break  # Прерываем цикл, так как уже произошло обновление значения

            if not found:
                temp.append(set_value)  # Если совпадений не найдено, добавляем новое значение

            value = temp  # Присваиваем обновленное значение переменной value

            #print(f"{value} : {temp} : {set_value['name']} : {set_value['name']}")

    if command[0] == "exit":
        sys.exit()

    #if
    if command[0] == "if":
        if command[2] == "==":
            if command[1] == command[3]:
                #index = command.index("to")
                #words_after = command[index + 1:]
                #result = ' '.join(words_after)
                #print(result)
                #command_obr(result)
                pass
            else:
                if_obr = False
        else:
            if command[2] == "!=":
                if command[1] != command[3]:
                    #index = command.index("to")
                    #words_after = command[index + 1:]
                    #result = ' '.join(words_after)
                    #print(result)
                    #command_obr(result)
                    pass
                else:
                    if_obr = False

    #echo
    if command[0] == "echo":
        index = command.index("echo")
        words_after = command[index + 1:]
        result = ' '.join(words_after)
        print(result)

while True:
    with open(file_batch, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        while line_num < len(lines):
            line = lines[line_num].strip()
            for var in value:
                var_name = "%%" + var["name"]
                if var_name in line:
                    line = line.replace(var_name, var["value"])
            #print(f"Обработка строки {line_num + 1}: {line}")
            if line == ")":
                if_obr = True
            if if_obr == True:
                command_obr(line)
            line_num += 1