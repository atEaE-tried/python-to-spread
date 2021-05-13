import json

class Configuration():
    KEY__ROW_BUFFER = 'rowBuffer'
    KEY__COLUMN_BUFFER = 'columnBuffer'

    def __init__(self):
        with open('./appSettings.json', mode='r', encoding='utf-8') as f:
            loader = json.load(f)
            row_buffer = loader[self.KEY__ROW_BUFFER]
            if not (row_buffer):
                raise ValueError(f'"{self.KEY__ROW_BUFFER}" is not set to any value.')
            self.__row_buffer = int(row_buffer)

            column_buffer = loader[self.KEY__COLUMN_BUFFER]
            if not (row_buffer):
                raise ValueError(f'"{self.KEY__COLUMN_BUFFER}" is not set to any value.')
            self.__column_buffer = int(column_buffer)
    
    @property
    def row_buffer(self):
        return self.__row_buffer

    @property
    def column_buffer(self):
        return self.__column_buffer

        
            
