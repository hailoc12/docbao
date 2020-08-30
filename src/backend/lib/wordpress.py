from wordpress_xmlrpc import Client, WordPressPost, WordPressTerm
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost, EditPost, GetPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc.methods.taxonomies import GetTerms
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media
import uuid
import io
import os
from .utils import print_exception
import requests
import os.path
class Wordpress():
    def __init__(self):
        USERNAME=os.environ['DOCBAO_WORDPRESS_USERNAME']
        PASSWORD=os.environ['DOCBAO_WORDPRESS_PASSWORD']
        WORDPRESS_URL = os.environ['DOCBAO_WORDPRESS_SITE'] + '/xmlrpc.php'
        self._client = Client(WORDPRESS_URL, USERNAME, PASSWORD)

    def add_new_post(self, title, content, image_url, trending, tags, category):
        '''
        Add new post to wordpress
        :input:
            title: string
            content: string
            tags: []
            category: []
        :output:
            id of new post
        '''

        default_thumbnail_id = 5700
        post = WordPressPost()

        # set content
        post.title = title
        post.content = content

       # set feature_image
        image_data = None
        if image_url:
            try:
                response = requests.get(image_url, verify=False, timeout=40)
                if response.status_code == 200:
                    if '.jpg' in image_url:
                        mimetype = 'image/jpeg'
                        extension = ".jpg"
                    elif '.png' in image_url:
                        mimetype = 'image/png'
                        extension = ".png"
                    elif '.jpeg' in image_url:
                        mimetype = 'image/jpeg'
                        extension = ".jpeg"
                    else:
                        mimetype = 'image/jpeg'
                        extension = ".jpg"
                    print(mimetype)
                    print(extension)

                    image_data = {
                                'name': str(uuid.uuid4()) + extension
                    }

                    image_data['type'] = mimetype
                    image_data['bits'] = xmlrpc_client.Binary(response.content)

                    # upload image
                    upload_response = self._client.call(media.UploadFile(image_data))
                    print(upload_response)
                    thumbnail_id = upload_response['id']
                    print("Image id: %s" % thumbnail_id)
                    post.thumbnail = thumbnail_id

                    if trending and thumbnail_id !='': # only post with thumbnail will be in trending post
                        category.append("Trending")

            except:
                print_exception()
                print("Some errors happended. Can't upload image. Use default thumbnail")
                post.thumbnail = default_thumbnail_id

        post.terms_names = {
            'post_tag': tags,
            'category': category
            }


        post.post_status = 'publish'

        post_id = self._client.call(NewPost(post))
        # self._client.call(EditPost(post_id, post))
        return post_id


    def add_new_article(self, article, trending=False):
        '''
        Add new article to wordpress
        :input:
            article: Article object
            trending: if True, add this article to trend category
        '''
        title = article.get_topic()
        sapo = '<b>' + article.get_sapo() + '</b>\r\n'
        content = sapo + article.get_content_as_html(delimiter='\r\n')
        keywords = [x for x in article.get_keywords()]
        tags = keywords
        category = []
        # category.extend(article.get_category())
        images = article.get_all_image()
        print(images)
        if images:
            image_url = images[0]
        else:
            image_url = None
        post_id = self.add_new_post(title, content, image_url, trending, tags, category)

        if post_id:
            return post_id
        else:
            return None





