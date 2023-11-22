import time
import threading
import xml.etree.ElementTree as ET
import xml.dom.minidom
from typing import Union, List


class JSONtoXMLParser:
    def __init__(self):
        self.json_data = None
        self.xml_data = None
        self.indentation = 0
        self.start_time = None
        self.end_time = None
        self.start_time_with_library = None
        self.end_time_with_library = None
        self.start_time_with_regular = None
        self.end_time_with_regular = None

    def load_json(self, file_path: str) -> None:
        """
        Загружает данные из JSON файла.

        Args:
            file_path (str): Путь к JSON файлу.
        """
        with open(file_path) as json_file:
            self.json_data = eval(json_file.read())

    def convert_to_xml(self) -> None:
        """
        Конвертирует JSON данные в XML формат.
        """
        if self.json_data is None:
            raise ValueError("JSON data is not loaded")
        self.start_time_with_library = time.time()
        self.convert_to_xml_with_library()
        self.start_time_with_regular = time.time()
        self.convert_to_xml_with_regular()
        self.start_time = time.time()
        self.xml_data = self._parse_json_data(self.json_data, "root")

    def save_xml(self, file_path: str) -> None:
        """
        Сохраняет XML данные в файл.

        Args:
            file_path (str): Путь для сохранения XML файла.
        """
        if self.xml_data is None:
            raise ValueError("XML data is not generated")

        self.end_time = time.time()
        with open(file_path, "w") as xml_file:
            xml_file.write(self.xml_data)
        self.get_execution_time()

    def _parse_json_data(
        self, json_data: Union[List[str], str, dict], element_name: str
    ) -> str:
        if isinstance(json_data, dict):
            xml_string = self._get_indentation() + f"<{element_name}>\n"
            self.indentation += 1
            for key, value in json_data.items():
                xml_string += self._parse_json_data(value, key)
            self.indentation -= 1
            xml_string += self._get_indentation() + f"</{element_name}>\n"
            return xml_string
        elif isinstance(json_data, list):
            xml_string = ""
            for item in json_data:
                xml_string += self._parse_json_data(item, "item")
            return xml_string
        else:
            return (
                self._get_indentation()
                + f"<{element_name}>{json_data}</{element_name}>\n"
            )

    def _get_indentation(self):
        return "  " * self.indentation

    # with libraries
    def convert_to_xml_with_library(self) -> None:
        """
        Конвертирует JSON данные в XML формат с использованием библиотеки ElementTree.
        """
        if self.json_data is None:
            raise ValueError("JSON data is not loaded")
        # Создание нового потока
        thread = threading.Thread(target=self._convert_to_xml_with_library)
        thread.start()

    def _convert_to_xml_with_library(self) -> None:
        root = ET.Element("root")
        self._convert_dict_to_xml(self.json_data, root)

        xml_string = ET.tostring(root, encoding="utf-8")
        dom = xml.dom.minidom.parseString(xml_string)
        formatted_xml = dom.toprettyxml(indent="  ")

        with open("output_with_library.xml", "w") as xml_file:
            xml_file.write(formatted_xml)

        self.end_time_with_library = time.time()

    def _convert_dict_to_xml(self, data, parent_element):
        if isinstance(data, dict):
            for key, value in data.items():
                element = ET.SubElement(parent_element, key)
                if isinstance(value, (dict, list)):
                    self._convert_dict_to_xml(value, element)
                else:
                    element.text = str(value)
        elif isinstance(data, list):
            for item in data:
                self._convert_dict_to_xml(item, parent_element)

    # with regualrs
    def convert_to_xml_with_regular(self) -> None:
        if self.json_data is None:
            raise ValueError("JSON data is not loaded")
        # Создание нового потока
        thread = threading.Thread(target=self._convert_to_xml_with_regular)
        thread.start()

    def _convert_to_xml_with_regular(self) -> None:
        xml_data = ""
        # Преобразование каждого ключа и значения JSON в элементы XML
        for key, value in self.json_data.items():
            xml_data += f"<{key}>{value}</{key}>"

        with open("output_with_regular.xml", "w") as xml_file:
            xml_file.write(self.xml_data)

        self.end_time_with_regular = time.time()

    def _get_execution_time_with_library(self) -> float:
        """
        Возвращает время выполнения конвертации JSON в XML с использованием библиотеки ElementTree.

        Returns:
            float: Время выполнения в секундах.
        """
        if self.end_time_with_library is None:
            time.sleep(1)
            return self._get_execution_time_with_library()
        return self.end_time_with_library - self.start_time_with_library

    def _get_execution_time_with_regular(self) -> float:
        if self.end_time_with_library is None:
            time.sleep(1)
            return self._get_execution_time_with_library()
        return self.end_time_with_regular - self.start_time_with_regular

    def get_execution_time(self) -> None:
        """
        Возвращает время выполнения конвертации JSON в XML.

        Returns:
            float: Время выполнения в секундах.
        """
        if self.start_time is None or self.end_time is None:
            raise ValueError("Execution time is not available")
        time_my_parser = self.end_time - self.start_time
        time_with_library = self._get_execution_time_with_library()
        time_with_regular = self._get_execution_time_with_regular()

        formatted_times = [
            "{:.6f}".format(time_my_parser),
            "{:.6f}".format(time_with_library),
            "{:.6f}".format(time_with_regular),
        ]

        for i, times in enumerate(formatted_times, start=1):
            print(f"Тест {i}: {times}")


# Пример использования
parser = JSONtoXMLParser()
parser.load_json("scedule.json")
parser.convert_to_xml()
parser.save_xml("output.xml")
