- Group Người Hải Phòng:
    web_url: https://www.facebook.com/groups/PageHaiPhong/
    crawl_url: https://www.facebook.com/groups/PageHaiPhong/
    language: vietnamese
    id_type: topic
    url_pattern_re: (http|https)://www.facebook.com/groups/PageHaiPhong
    get_topic_from_link: true
    topics_xpath:
    - //div[@class='_5pcr userContentWrapper']//div[@data-testid='post_message' and not(parent::div[contains(@class,'mtm')])]
    topic_type: html
    extract_xpath:
    - ./text()
    contain: ''
    minimum_topic_length: 4
    skip_checking_topic_length: true
    get_publish_date_as_crawl_date: false
    date_place: same_page
    date_xpath:
    - //div[@data-testid='post_message']/../div[1]/div/div/div[2]/div/div/div[2]/div/span/span/a/abbr
    use_index_number: true
    date_re: (\d{1,2}:\d{1,2}, \d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})
    date_pattern: '%H:%M, %d/%m/%Y'
    timezone: Asia/Ho_Chi_Minh
    output_html: false
    use_browser: true
    browser_profile: test_profile
    display_browser: true
    browser_fast_load: true
    maximum_url: 5
    last_run: 28/05/2019 22:13
    minimum_duration_between_crawls: 5