- Page Hải Phòng:
    output_html: false
    browser_fast_load: true
    maximum_url: 5
    id_type: topic
    date_pattern: '%H:%M, %d/%m/%Y'
    web_url: https://www.facebook.com/pg/Page.HaiPhong/posts/?ref=page_internal
    date_re: (\d{1,2}:\d{1,2}, \d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})
    last_run: 29/08/2019 02:18
    url_pattern_re: (http|https)://www.facebook.com/pg/Page.HaiPhong
    language: vietnamese
    get_publish_date_as_crawl_date: false
    crawl_type: facebook page
    tags: []
    date_place: same_page
    extract_xpath:
    - ./text()
    contain: ''
    minimum_topic_length: 4
    minimum_duration_between_crawls: 5
    date_xpath:
    - //div[@data-testid='post_message']/../div[1]/div/div/div[2]/div/div/div[2]/div/span/span/a/abbr
    skip_checking_topic_length: true
    crawl_url: https://www.facebook.com/pg/Page.HaiPhong/posts/?ref=page_internal
    get_topic_from_link: true
    browser_profile: test_profile
    display_browser: false
    timezone: Asia/Ho_Chi_Minh
    topics_xpath:
    - //div[@class='_5pcr userContentWrapper']//div[@data-testid='post_message' and
      not(parent::div[contains(@class,'mtm')])]
    topic_type: html
    use_browser: true
    use_index_number: true
    remove_me: false
