# bashPath
PATH = './data'
# 资源管理图片路径
REPOSITORY_IMAGE = PATH + '/repository/photo/'
# 学校logo保存路径
SCHOOL_LOGO = PATH + '/association/logo/'

import time

def upload(file, base_path):
    """
    上传文件
    :param file:
    :param bash_path:
    :return:
    """
    if file is None:
        return ''
    path = base_path + str(time.time()) + '.' + file.name.split('.')[-1]

    f = open(path, 'wb')
    try:
        f.write(file.read())
        f.close()
    except:
        raise Exception("保存文件失败")

    return path