# from django.http import *
# from django.views.generic import View
#
# from common.core.auth.check_login import check_login
# from common.core.http.view import HoHoView
# from common.utils.helper.result import Result
# from common.utils.helper.upload import *
# from server.association.models import Association
# from server.repository.models import PhotoModel
#
# PHOTO_PATH = './data/repository/photo/'
#
#
# class PhotoView(HoHoView):
#
#     def get(self, request, tid):
#         """
#         获取照片列表
#         :param request:
#         :param tid:
#         :return:
#         """
#         photo = PhotoModel.objects.filter(association_id=tid)
#         alist = ['http://39.108.229.132/repository/photo/' + str(p.id) for p in photo]
#
#         return Result(ids=alist)
#
#     @check_login
#     def post(self, request, tid=''):
#         """
#         上传照片
#         :param request:
#         :param tid:
#         :return:
#         """
#         file = request.FILES.get('image', None)
#         ass = Association.objects.filter(id=tid)
#         if not ass.exists():
#             raise Exception("gun!")
#         ass = ass[0]
#
#         path = upload(file, REPOSITORY_IMAGE)
#         PhotoModel.objects.create(
#             association=ass,
#             photo_path=path,
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
