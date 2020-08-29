- Báo Chính Phủ:
    web_url: http://baochinhphu.vn
    crawl_url: http://baochinhphu.vn
    language: vietnamese
    id_type: href
    url_pattern_re: (http|https)://baochinhphu.vn
    get_topic_from_link: true
    topics_xpath:
    - //a[contains(@href, 'vgp') and string-length(text())>20 and not(child::img)]
    topic_type: href
    extract_xpath:
    - ./text()
    contain: ''
    minimum_topic_length: 4
    skip_checking_topic_length: false
    get_publish_date_as_crawl_date: false
    date_place: detail_page
    date_xpath:
    - //div[@class='article-header']
    use_index_number: false
    date_re:
    - (\d{1,2}:\d{1,2}, \d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})
    date_pattern:
    - '%H:%M, %d/%m/%Y'
    timezone: Asia/Ho_Chi_Minh
    output_html: false
    use_browser: true
    browser_profile: ''
    display_browser: false
    browser_fast_load: true
    maximum_url: 10
    last_run: 02/06/2019 21:56
    minimum_duration_between_crawls: 15
