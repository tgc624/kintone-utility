from typing import Dict, List, TypedDict


class NormalFieldController():
    def __init__(self, field: Dict = {}, value=None):
        self.value = field.get('value') if value is None else value

    def get_value(self):
        return self.value

    def get_register_format(self):
        return {'value': self.value}

    def get_update_format(self):
        return {'value': self.value}


class MultiSelectableFieldController(NormalFieldController):
    # class _MultiSelectableField(TypedDict):
    #     type: str
    #     value: _MultiSelectableFieldValue

    def __init__(self, field: Dict[str, str] = {}, value: List[str] = None):
        # Define field value
        if value is not None:
            if type(value) != list:
                raise Exception('Invalid value!')
            self.value: List[str] = value
        elif type(field) == dict and field.get('value') is not None:
            if type(field.get('value')) != list:
                raise Exception('Invalid value!')
            self.value: List[str] = field.get('value')
        raise Exception('value not found')

    def get_value(self):
        return [field.get('value') for field in self.value]


class FileFieldValue(TypedDict):
    contentType: str
    fileKey: str
    name: str
    size: str


class FileField(TypedDict):
    type = 'FILE'
    value: List[FileFieldValue]


class FileFieldController(MultiSelectableFieldController):
    def __init__(self, field: FileField, value: List[str]):
        _value = [file_field_value.fileKey for file_field_value in field.value]
        super().__init__(value=value)

    def get_value(self):
        return [file.get('fileKey') for file in self.value]


class UserFieldController(MultiSelectableFieldController):
    '''
    https://developer.cybozu.io/hc/ja/articles/202111374
    '''

    def get_value(self):
        return [user.get('code') for user in self.value]

    def get_register_format(self):
        return {'value': self.value}

    def get_update_format(self):
        return {'value': self.value}


class UnUpdatableFieldController(NormalFieldController):
    def get_update_format(self):
        raise Exception(
            f'[Error] un-updatable field type!')


class ReadOnlyFieldController(NormalFieldController):
    def get_register_format(self):
        raise Exception(
            f'[Error] read-only field type!')

    def get_update_format(self):
        raise Exception(
            f'[Error] read-only field type!')


class NonValueFieldController(NormalFieldController):
    def get_value(self):
        raise Exception(
            f'[Error] non-value field type!')

    def get_register_format(self):
        raise Exception(
            f'[Error] non-value field type!')

    def get_update_format(self):
        raise Exception(
            f'[Error] non-value field type!')


class FieldController():
    TYPE2CONTOLLER = {
        'CALC': ReadOnlyFieldController,
        'CATEGORY': ReadOnlyFieldController,
        'CHECK_BOX': MultiSelectableFieldController,
        'CREATED_TIME': UnUpdatableFieldController,
        'CREATOR': UnUpdatableFieldController,
        'DATE': NormalFieldController,
        'DATETIME': NormalFieldController,
        'DROP_DOWN': NormalFieldController,
        'FILE': FileFieldController,
        'GROUP_SELECT': UserFieldController,
        'GROUP': NonValueFieldController,
        'HR': NonValueFieldController,
        'LABEL': NonValueFieldController,
        'LINK': NormalFieldController,
        'MODIFIER': UnUpdatableFieldController,
        'MULTI_LINE_TEXT': NormalFieldController,
        'MULTI_SELECT': MultiSelectableFieldController,
        'NUMBER': NormalFieldController,
        'ORGANIZATION_SELECT': UserFieldController,
        'RADIO_BUTTON': NormalFieldController,
        'RECORD_NUMBER': ReadOnlyFieldController,
        'REFERENCE_TABLE': NonValueFieldController,
        'RICH_TEXT': NormalFieldController,
        'SINGLE_LINE_TEXT': NormalFieldController,
        'SPACER': NonValueFieldController,
        'STATUS': ReadOnlyFieldController,
        'STATUS_ASSIGNEE': ReadOnlyFieldController,
        'SUBTABLE': None,  # TODO
        'TIME': NormalFieldController,
        'UPDATED_TIME': UnUpdatableFieldController,
        'USER_SELECT': UserFieldController,
        '__ID__': ReadOnlyFieldController,
        '__REVISION__': ReadOnlyFieldController,
    }

    def __init__(self, field={}, value=None, type=None):
        _type = field.get('type') if type is None else type
        _controller_class = self.TYPE2CONTOLLER.get(_type)

        if _controller_class is None:
            raise Exception('Unsupported type!')

        self.controller: NormalFieldController = _controller_class(
            field, value)

    def get_value(self):
        return self.controller.get_value()

    def get_register_format(self):
        return self.controller.get_register_format()

    def get_update_format(self):
        return self.controller.get_update_format()
