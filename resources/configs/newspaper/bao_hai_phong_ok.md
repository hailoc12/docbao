    - Báo Hải Phòng:
        web_url: http://www.baohaiphong.com.vn/baohp/vn/home/
        crawl_url: http://www.baohaiphong.com.vn/baohp/vn/home/index.jsp
        url_pattern_re: (http|https)://www.baohaiphong.com.vn
        language: vietnamese 
        get_topic_from_link: True 
        topics_xpath: 
            - "//a[contains(@href, 'InfoDetail.jsp')]"
        extract_xpath: 
            - ".//text()"
        minimum_topic_length: 4
        contain: ""  
        skip_checking_topic_length: False 
        get_publish_date_as_crawl_date: False
        date_xpath: 
            - "//div[@class='row1 creatdate']"
        date_re: (\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4} \d{1,2}:\d{1,2})
        date_pattern: "%d/%m/%Y %H:%M" 
        timezone: "Asia/Ho_Chi_Minh"
        output_html : False
        use_browser : True
        browser_fast_load: True
        display_browser: False
        maximum_url: 5
