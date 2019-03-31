# from django.http import *
# from django.views.generic import View
#
# from common.core.auth.check_login import check_login
# from common.core.http.view import HoHoView
# from common.utils.helper.result import Result
# from common.utils.helper.upload import *
# from server.association.models import Association
# from server.repository.models import RepositoryFile
# from common.core.auth.check_login import check_login
#
# PHOTO_PATH = './data/repository/photo/'
#
#
# class PhotoView(HoHoView):
#
#     @check_login
#     def get(self, request):
#         """
#         获取文件列表
#         :param request:
#         :return:
#         """
#         files = RepositoryFile.objects.filter__cache(author=self.auth.get_account())
#         alist = [{
#             "title": file.title,
#             "id": file.id
#         } for file in files]
#
#         return Result(alist)
#
#     @check_login
#     def post(self, request, tid=''):
#         """
#         上传文件
#         :param request:
#         :param tid:
#         :return:
#         """
#         file = request.FILES.get('file', None)
#
#         title, path = upload(file, REPOSITORY_IMAGE)
#         RepositoryFile.objects.create(
#             association=ass,
#             photo_path=path,
#             title=title
#         )
#
#         return Result(status=file.name)
#
#
# class PhotoGet(HoHoView):
#
#     def get(self, request, tid):
#         """
#         获取图片
#         :param request:
#         :param tid:
#         :return:
#         """
#         photo = PhotoModel.objects.filter(id=int(tid))
#
#         file_path = (PHOTO_PATH + '404.jpg') if not photo.exists() else photo[0].photo_path
#         print(file_path)
#
#         return FileResponse(open(file_path, 'rb'))
