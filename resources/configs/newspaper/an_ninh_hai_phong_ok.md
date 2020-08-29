    - An Ninh Hải Phòng:
        web_url: http://anhp.vn/
        crawl_url: http://anhp.vn
        url_pattern_re: (http|https)://anhp.vn
        language: vietnamese 
        get_topic_from_link: True 
        topics_xpath: 
            - "//a[contains(@href, 'http://anhp.vn/') and contains(@href, 'html')][not(child::img) or child::span]"
        extract_xpath: 
            - ".//text()[string-length(.)>4]"
        minimum_topic_length: 4
        contain: ""  
        get_publish_date_as_crawl_date: False
        date_xpath:
            - "//div[@class='detailBox']"
        date_re: (\d{1,2}:\d{1,2} \d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})
        date_pattern: "%H:%M %d/%m/%Y" 
        timezone: "Asia/Ho_Chi_Minh"
        output_html: False
        use_browser: True
        browser_fast_load: True
        display_browser: False
        maximum_url: 10
