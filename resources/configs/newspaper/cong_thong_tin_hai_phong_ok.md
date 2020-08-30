    - Cổng thông tin Hải Phòng: 
        web_url: "http://haiphong.gov.vn"
        crawl_url: "http://haiphong.gov.vn/trang-chu"
        url_pattern_re: (http|https)://haiphong.gov.vn
        language: vietnamese 
        get_topic_from_link: True 
        topics_xpath: 
            - "//a[contains(@href, '/p-UBNDTP/d') and text()]"
        extract_xpath: 
            - "./text()"
        contain: ""  
        minimum_topic_length: 4
        skip_checking_topic_length: False 
        get_publish_date_as_crawl_date: False
        date_xpath: 
            - "//div[@class='divDetail_DateCreate']"
        date_re: (\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4} - \d{1,2}:\d{1,2})
        date_pattern: "%d/%m/%Y - %H:%M" 
        timezone: "Asia/Ho_Chi_Minh"
        output_html : False
        use_browser : True
        display_browser: False
        maximum_url: 5