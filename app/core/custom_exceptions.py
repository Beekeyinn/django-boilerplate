def get_exception_traceback(ex: Exception) -> str:
    traceback = ex.__traceback__
    traces = ""
    while traceback is not None:
        traces += f"[\n\tfilename: {traceback.tb_frame.f_code.co_filename} \n\tname: {traceback.tb_frame.f_code.co_name} \n\tline no: {traceback.tb_lineno}\n]\n"
        traceback = traceback.tb_next
    return traces


class FieldDoesNotExist(Exception):
    def __init__(self, instance, field_name, message="Field does not exists")->None:
        self.instance = instance
        self.field_name - field_name
        self.message = message
        super().__init__(self, message)

    def __str__(self) -> str:
        fields = " ".join([f"'{key}'" for key in self.instance.__dict__.keys()])
        return f"{self.__class__} -> {self.field_name} -> doest not exist in {self.instance.__class__}:[ {fields} ]"
