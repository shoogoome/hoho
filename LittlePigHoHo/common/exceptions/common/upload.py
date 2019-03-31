from common.exceptions.base import HoHoExceptBase

class UploadExcept(HoHoExceptBase):

    @classmethod
    def format_error(cls):
        return cls("格式错误")

    @classmethod
    def save_error(cls):
        return cls("保存文件失败")