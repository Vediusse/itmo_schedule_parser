import json
import xml.etree.ElementTree as ET
import time


def convert_json_to_xml(json_data):
    root = ET.Element("root")
    for key, value in json_data.items():
        element = ET.SubElement(root, key)
        element.text = str(value)
    return ET.tostring(root, encoding="utf-8")


# Чтение файла JSON
with open("input.json", "r") as json_file:
    json_data = json.load(json_file)

# Засекаем время начала перевода
start_time = time.time()

# Преобразование JSON в XML
xml_data = convert_json_to_xml(json_data)

# Засекаем время окончания перевода
end_time = time.time()

# Рассчитываем время выполнения перевода
translation_time = end_time - start_time

# Сохранение XML-файла
with open("output.xml", "wb") as xml_file:
    xml_file.write(xml_data)

# Вывод времени выполнения перевода
print(f"Время выполнения перевода: {translation_time} секунд")
