# bashPath
PATH = './data'
# 资源管理图片路径
REPOSITORY_IMAGE = PATH + '/repository/photo/'
# 学校logo保存路径
SCHOOL_LOGO = PATH + '/association/logo/'

import time
from ...exceptions.common.upload import UploadExcept

def upload(file, base_path):
    """
    上传文件
    :param file:
    :param base_path:
    :return:
    """
    if file is None:
        return ''
    file_name = file.name.split('.')

    #   过滤
    if file_name[-1] not in [
        'jpg', 'png', 'jpeg',
        'txt', 'doc', 'docx',
    ]:
        raise UploadExcept.format_error()

    path = base_path + str(time.time()) + '.' + file_name[-1]

    f = open(path, 'wb')
    try:
        f.write(file.read())
        f.close()
    except:
        raise UploadExcept.save_error()

    return '.'.join(file_name[:-1]), path