# Import MinIO library.
from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou, BucketAlreadyExists)

# Initialize minioClient with an endpoint and access/secret keys.
minioClient = Minio('s1.cloudstorage.com.vn',
                    access_key='s3user101281',
                    secret_key='LnyWrbuBbdcyBjKOVqy1ENj972tBc9SLVCubK73A',
                    secure=False)

for item in minioClient.list_objects_v2("bangtin"):
    print(item)
#minioClient.fput_object('bangtin', 'pumaserver_debug.log', '/root/images/000ef05b-b095-4132-8c6f-bd76963b9927_small.jpg')
