####################################################################################
# Program: Download Images                                                         #
# Function: download images from url, convert to specific format and save to local #
# Author: quangminh                                                                #
# Created: 2019-08-17                                                              #
####################################################################################

import cv2
import requests
import numpy as np
import os
import uuid
from .utils import get_independent_os_path, print_exception
import boto3
from botocore.client import Config
from botocore.utils import fix_s3_host


# CDN HOST
#CDN_HOST = "http://cdn.bangtin.vn/bangtin"

#CDN_HOST = "http://s3user101281.cdn.cloudstorage.com.vn/bangtin"
#CDN_HOST = "http://s3user101281.cdn.cloudstorage.com.vn/bangtin"
CDN_HOST = "http://ainewsobj.6112cf5e.viettel-cdn.vn/bangtin"
IMAGE_FOLDER = "/home/administrator/images"
IMAGE_SIZES =  {'feature_image':[
                    {'size':{'height': 100, 'width': 670}, 
                    'name': 'large', 'auto_resize': True},

                    {'name': 'small', 'auto_resize': True,
                    'size':{'height': 100, 'width': 335}}
                    ]
                ,
                'content_image':[
                    {'size':{'height':100, 'width': 670},
                     'name': 'large', 'auto_resize': True}]
                ,
                'avatar':[
                    {'size':{'height': 80, 'width': 80},
                     'name': 'avatar', 'auto_resize': False}],
                'category':[
                    {'size':{'height': 100, 'weight': 164},
                     'name': 'category', 'auto_resize': True}]
                }


# CLOUD STORAGE
CLOUD_ENDPOINT= "http://s1.cloudstorage.com.vn"
CLOUD_ACCESS_KEY = "s3user101281"
CLOUD_SECRET_ACCESS_KEY = "LnyWrbuBbdcyBjKOVqy1ENj972tBc9SLVCubK73A"
CLOUD_BUCKET = "bangtin"
# cloud host is public link to uploaded file
CLOUD_HOST = "http://ainewsobj.6112cf5e.viettel-cdn.vn/" + CLOUD_BUCKET

class OnlineUploader():
    """
    Abstract class for uploading to cloud storage
    """
    def upload_file(self):
        pass

class S3OnlineUploader(OnlineUploader):
    _s3_resource = None

    def __init__(self, s3_endpoint, access_key, secret_access_key, host, bucket_name):
        self._s3_endpoint = s3_endpoint
        self._access_key = access_key
        self._secret_access_key = secret_access_key
        self._bucket = bucket_name
        self._host = host

    def connect(self):
        try:
            self._s3_client = boto3.client('s3', endpoint_url=self._s3_endpoint,
                                              aws_access_key_id = self._access_key,
                                              aws_secret_access_key = self._secret_access_key,
                                              region_name = "us-east-1",
                                              config=Config(s3={'addressing_style': 'path', 'signature_version':'s3'})) 
            return True
        except:
            print_exception()
            return None

    def get_presign_upload_file(self, file_name):
        try:
            url = self._s3_client.generate_presigned_url('put_object', 
                                                         Params={'Bucket': self._bucket,
                                                                 'Key': file_name},
                                                         ExpiresIn=1000)
            return url
        except:
            return None

    def get_presign_put_file_acl(self, file_name):
        try:
            url = self._s3_client.generate_presigned_url('put_object_acl', 
                                                         Params={'Bucket': self._bucket,
                                                                 'Key': file_name},
                                                         ExpiresIn=1000)
            return url
        except:
            return None

    def upload_file(self, file_name, file_path):
        """
        Upload file_name from file_path to cloud storage
        :output:
            url of online file
            or None if errors
        """
        presign_url = self.get_presign_upload_file(file_name)
        print(presign_url)

        try:
            with open(file_path, 'rb') as stream:
                file_data = stream.read()
                header = {
                          'Content-Length': str(len(file_data))}
                          #'x-amz-acl': 'public-read'}
                response = requests.put(presign_url, data=file_data, headers=header)
                #print(response.status_code)
                #print(response.content)

                if response.status_code == 200:
                    return self._host + '/' + file_name
                else:
                    print(response.status_code)
                    return None
 
        except:
            print_exception()
            return None
        return self._host + '/' + file_name


class CDNManager():
    """
    Object to manager CDN resoures
    :important function:
        convert_image(url, type): download image from url, put in CDN storage and return url of converted image
    """

    def __init__(self, config_manager=None):
        self.s3_online_uploader = None

        if not config_manager: 
            self.cdn_host = CDN_HOST
            self.image_folder = IMAGE_FOLDER
            self.image_sizes = IMAGE_SIZES
            self.enable = True

        else:
            self.cdn_host = CDN_HOST
            self.image_folder = IMAGE_FOLDER
            self.image_sizes = IMAGE_SIZES
            self.enable = config_manager.get_use_CDN()
        self.s3_online_uploader = S3OnlineUploader(CLOUD_ENDPOINT, CLOUD_ACCESS_KEY, CLOUD_SECRET_ACCESS_KEY, CLOUD_HOST, CLOUD_BUCKET)
        self.s3_online_uploader.connect()


    def download_and_convert_image(self, url, host_url, data, image_metadata, image_folder, local_folder=None, online_uploader=None, quality = 100): 
        """download image from host_url, convert to other format and save to local folder
        :input:
            local_folder: path to local folder to save images
            host_url: image url
            data: if not None, use image binary stream instead of url
            image_metadata: an array of dict {'size': {'width': width, 'height': height}, {'name': name}, 'auto_resize': true/false}
            quality: default 7 (70%)
        :output:
            url_list[{'local':url, 'cloud': url}..{..}]
            or None
        """
        try:
            if not data: 
                response = requests.get(url)
                if response.status_code != 200:
                    return None
                # get cv2 image
                im = cv2.imdecode(np.frombuffer(response.content, np.uint8), cv2.IMREAD_COLOR)
            else:
                # get cv2 image
                im = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
        except:
            print_exception()
            return None

        if im is not None:
            url_list = []

            for size in image_metadata:
                width = size['size']['width']
                height = size['size']['height']

                if size['auto_resize']:
                    img_height, img_width, _ = im.shape
                    height = width/img_width * img_height

                #cv2.imshow('im', im)
                    
                resized_im = cv2.resize(im, (int(width), int(height)))

                # View image
                #cv2.imshow('im', resized_im)
                # cv2.waitKey(0)
                result_url = {}
                # Save image
                if local_folder:
                    file_name = str(uuid.uuid4())+ '_' + size['name'] + '.jpg'
                    cv2.imwrite(get_independent_os_path([image_folder, file_name]), resized_im, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
                    result_url['local'] = host_url + '/' + file_name

                if online_uploader:
                    file_name = str(uuid.uuid4())+ '_' + size['name'] + '.jpg'
                    file_path = get_independent_os_path([image_folder, file_name])
                    cv2.imwrite(file_path, resized_im, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
                    
                    if online_uploader:
                        online_url = self.s3_online_uploader.upload_file(file_name, file_path)
                        if not online_url: # have errors
                            online_url = ''

                    result_url['cloud'] = online_url

                    try:
                        os.remove(file_path)
                    except:
                        pass
                
                url_list.append(result_url)
            return url_list
        else: 
            return None


    def convert_image(self, url, type='feature_image', mode='url'):
        """replace image by bangtin cdn image link
        :input:
            url: origin images / binary stream
            mode: 'url' to get image from url, 'binary' to get image from data stream
        :output:
            depend on type
                'feature_image': dict {'large': url, 'small': url}
                'content_image': url
        """
        if not self.enable:
            return url

        host_url = self.cdn_host
        image_folder = self.image_folder
        local_folder = None
        image_metadata = self.image_sizes[type]
        online_upload = True

        if mode == 'url':
            result = self.download_and_convert_image(url, host_url, None, image_metadata, image_folder, local_folder, online_upload)
        else:
            data=url
            result = self.download_and_convert_image(None, host_url, data, image_metadata, image_folder, local_folder, online_upload)

            
        if result:
            if type == 'feature_image':
                if online_upload:
                    return [{'large': result[0]['cloud'], 'small': result[1]['cloud']}]
                else:
                    return [{'large': result[0]['local'], 'small': result[1]['local']}]
            elif type == 'content_image':
                if online_upload:
                    return result[0]['cloud']
                else:
                    return result[0]['local']
            elif type in ['avatar', 'category']:
                if online_upload:
                    return result[0]['cloud']
                else:
                    return result[0]['local']
            else:
                return None
        else:
            return None

