from werkzeug.exceptions import BadRequest


class Validator:

    @staticmethod
    def validate_new_student(instance):
        field_types = [str, str, str, str, int, str, int]
        values_list = [value for value in instance.values()]
        for i in range(len(field_types)):
            if type(values_list[i]) != field_types[i]:
                print(f"{values_list[i]} does not have the required type. Should be type: {field_types[i]}")
                raise BadRequest()

    @staticmethod
    def validate_edited_student(new_instance):
        field_types = [int, str, str, str, str, str, str, str, str]
        values_list = [value for value in new_instance.values()]
        # if new_instance
        for i in range(len(field_types)):
            if type(values_list[i]) != field_types[i] or values_list[i] is None or values_list[i] == "":
                print("Something looks wrong, make sure you filled out all the fields correctly")
                raise BadRequest()

    @staticmethod
    def validate_login_student(new_login):
        fields_types = [str, str]
        values_list = [value for value in new_login.values()]
        for i in range(2):
            if type(values_list[i]) != fields_types[i]:
                print("The email or password you have entered is incorrect. Please try again.")
                raise BadRequest()


