import csv
import openpyxl


class DataReaderReadError(Exception):
    """Custom exception class for data reading errors."""
    pass


class DataReader:
    """A class for reading data from Excel (.xlsx) and CSV (.csv) files."""

    def __init__(self) -> None:
        """Initialize a DataReader instance."""
        self.header = []
        self.data = []
        self.err_data = []
        self._data_types = []
        self._data_type_error = False

    def _reset(self):
        """Reset all instance variables to their initial state."""
        self.header = []
        self.data = []
        self.err_data = []
        self._data_types = []

    def _type_convert(self, value: str | float | int):
        """
        Convert a value to the appropriate data type.

        Args:
            value (str | float | int): The value to convert.

        Returns:
            str | float | int: The converted value.
        """
        if isinstance(value, str):
            try:
                result = float(value)
                return result
            except ValueError:
                return value
        if isinstance(value, float):
            if value.is_integer():
                return int(value)
        
        return value

    def read_excel(self, file_path: str, skip_rows: int=0):
        """
        Read data from an Excel file.

        Args:
            file_path (str): The path to the Excel file.
            skip_rows (int): The number of rows to skip at the beginning of the worksheet.

        Raises:
            DataReaderReadError: If there is an error while importing the file.
        """
        self._reset()

        try:
            workbook = openpyxl.load_workbook(file_path, data_only=True)
        except (FileNotFoundError, 
                PermissionError, 
                openpyxl.utils.exceptions.InvalidFileException) as e:
            raise DataReaderReadError("Error while importing the file.", e)

        worksheet = workbook.active

        for i, row in enumerate(worksheet.iter_rows(values_only=True)):
            if i < skip_rows:
                continue
            elif not self.header:
                for cell_value in row:
                    if cell_value is not None:
                        self.header.append(cell_value)
                    else:
                        break
            else:
                if self.header and not self._data_types:
                    self._data_types = [type(cell).__name__ for cell in row]

                data_values = []
                for cell_value in row:
                    if cell_value is not None:
                        data_values.append(cell_value)
                    else:
                        continue

                if len(data_values) != len(self.header):
                    self.err_data.append([row, 'Wrong length.'])
                    continue
                
                data_set = []
                error = False
                for value, data_type in zip(data_values, self._data_types):
                    if value is None:
                        data_set.append(None)
                        continue

                    if type(value).__name__ != data_type:
                        error = True

                    data_set.append(value)
                if error:
                    self.err_data.append([tuple(data_values), 'Wrong data type.'])
                else:
                    self.data.append(data_set)

        workbook.close()

    def read_csv(self, file_path: str, skip_rows: int=0, encoding='utf-8', newline=''):
        """
        Read data from a CSV file.

        Args:
            file_path (str): The path to the CSV file.
            skip_rows (int): The number of rows to skip at the beginning of the CSV file.
            encoding (str): The encoding of the CSV file (default is 'utf-8').
            newline (str): The newline character (default is '').
        
        Raises:
            DataReaderReadError: If there is an error while importing the file.
        """
        self._reset()
        
        try:
            with open(file_path, 'r', newline=newline, encoding=encoding) as csvfile:
                reader = csv.reader(csvfile, 
                                    delimiter = ';',
                                    quotechar = '"',
                                    escapechar = None,
                                    doublequote = True,
                                    skipinitialspace = False,
                                    lineterminator = '\r\n')
                
                for i, row in enumerate(reader):
                    if i < skip_rows:
                        continue
                    elif not self.header:
                        self.header = row
                    else:
                        if self.header and not self._data_types and not self._data_type_error:
                            for value in row:
                                data_type = type(self._type_convert(value)).__name__
                                self._data_types.append(data_type)

                        if len(row) != len(self.header):
                            self.err_data.append([tuple(row), 'Wrong length.'])
                            continue

                        if self._data_type_error:
                            self.data.append(row)
                        else:
                            data_set = []
                            error = False
                            for value, data_type in zip(row, self._data_types):
                                value = self._type_convert(value)
                                if value == '':
                                    data_set.append(None)
                                    continue

                                if type(value).__name__ != data_type:
                                    error = True

                                data_set.append(self._type_convert(value))

                            if error:
                                self.err_data.append([tuple(row), 'Wrong data type.'])
                            else:
                                self.data.append(data_set)
        except (FileNotFoundError, PermissionError) as e:
            raise DataReaderReadError("Error while importing the file.", e)


my_reader = DataReader()
my_reader.read_excel('person_data.xlsx', 2)
print(my_reader.header)
print(my_reader.data)
print(my_reader.err_data)
my_reader.read_csv('person_data.csv', 2)
print(my_reader.header)
print(my_reader.data)
print(my_reader.err_data)
