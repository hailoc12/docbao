    - Báo mới Hải Phòng:
        web_url: https://baomoi.com
        crawl_url: "https://baomoi.com/tim-kiem/hải-phòng.epi"
        url_pattern_re: (http|https)://baomoi.com
        language: vietnamese 
        get_topic_from_link: True 
        topics_xpath: 
            - "//div[@class='story']/div[@class='story__tag']/p/a[contains(text(), 'Hải Phòng')]/../../../h4/a"
            - "//h4[@class='story__heading']/a"
        extract_xpath: 
            - "./@title"
            - "./span[contains(text(),'Hải Phòng')]/../@title"
        contain: ""  
        minimum_topic_length: 4
        skip_checking_topic_length: False 
        topic_tag:
        topic_class: 
        topic_id:  
        topic_re: "(.+)"
        get_publish_date_as_crawl_date: False
        date_place: "same_page"
        date_xpath: 
            - "//div[@class='story']/div[@class='story__tag']/p/a[contains(text(), 'Hải Phòng')]/../../../h4/a/../../div[2]/time"
            - "//h4[@class='story__heading']/../div[2]/time"
        use_index_number: True
        date_re: (\d{2,4}[\/\-\.]\d{1,2}[\/\-\.]\d{1,2}T\d{1,2}:\d{1,2})
        date_pattern: "%Y-%m-%dT%H:%M" 
        timezone: "Asia/Ho_Chi_Minh"
        output_html : False
        use_browser : True
        display_browser: False
        browser_fast_load: False
        maximum_url: 50
