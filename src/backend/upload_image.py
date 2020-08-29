################################################################################
# Program: Upload image to cloud storage and get CDN link                      #
# Author: hailoc12                                                             #
# Created: 2019-09-09                                                          #
################################################################################

from lib.cdn import *
import sys

if __name__ == "__main__":
    cdn_manager = CDNManager()
    if len(sys.argv) > 1:
        image_url = sys.argv[1]
        
        cdn_url = cdn_manager.convert_image(image_url, type='category')
        print("CDN link: %s" % cdn_url)
        
    else:
        print("Please provide image url to upload to get CDN link")
        print("Example: upload_image http://domain.com/image.jpg")

