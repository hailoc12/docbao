from lib.cdn import *

cdn_manager = CDNManager()
s3 = cdn_manager.s3_online_uploader
print(s3.upload_file("4.jpg", "/root/images/00181d4d-36cb-4208-90bf-59d67a8deba5_large.jpg"))
