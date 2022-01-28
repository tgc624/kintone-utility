import unittest
from field_controller import FieldController


class FieldControllerTest(unittest.TestCase):
    def test__single_line_text__from_field(self):
        # Arrange
        controller = FieldController(
            field={"type": "SINGLE_LINE_TEXT", "value": "テストです。", }
        )

        # Act
        value = controller.get_value()
        register_format = controller.get_register_format()
        update_format = controller.get_update_format()

        # Assert
        self.assertEqual(value, 'テストです。')
        self.assertEqual(register_format, {"value": "テストです。"})
        self.assertEqual(update_format, {"value": "テストです。"})

    def test__single_line_text__from_value_and_type(self):
        # Arrange
        controller = FieldController(value='テストです。', type='SINGLE_LINE_TEXT')

        # Act
        value = controller.get_value()
        register_format = controller.get_register_format()
        update_format = controller.get_update_format()

        # Assert
        self.assertEqual(value, 'テストです。')
        self.assertEqual(register_format, {"value": "テストです。"})
        self.assertEqual(update_format, {"value": "テストです。"})


if __name__ == '__main__':
    unittest.main()
