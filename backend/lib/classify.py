from .topic_modeling import *
from .utils import print_exception

def classify(article):
    '''
    function
    --------
    classify article into right category
    :output:
        category: [string1, string2]
    '''
    predict_category  = {'cong_nghe':1, 'giao_duc':2, 'giai_tri':3, 'khoa_hoc':4, 'kinh_te':5, 'nha_dat':6, 'phap_luat':7, 'the_gioi':8, 'the_thao':9,'van_hoa':10, 'giao_thong':11, 'xa_hoi':12, 'doi_song':13, 'thoi_su': 14, 'moi_truong': 15}

    ainews_category   = [['Khoa học-Công nghệ'],
                         ['Giáo dục'],
                         ['Giải trí'],
                         ['Khoa học'],
                         ['Kinh tế'],
                         ['Nhà đất'],
                         ['Pháp luật'],
                         ['Thế giới'],
                         ['Thể thao'],
                         ['Văn hóa'],
                         ['Ôtô-Xe máy'],
                         ['Xã hội'],
                         ['Đời sống'],
                         ['Thời sự'],
                         ['Môi trường']]

    predict_content = article.get_content_as_string()
    try:
        topic = predict_topic(predict_content)
        index = predict_category[topic] - 1
        category = ainews_category[index]
        if article.get_post_type() != 0:
           category.append('Mạng xã hội')
        return category
    except:
        print_exception()
        print("Have errors in classify module. Set category to default value")
        return ["Thời sự"]
