- Cafebiz:
    web_url: http://cafebiz.vn
    crawl_url: http://cafebiz.vn
    language: vietnamese
    id_type: href
    url_pattern_re: (http|https)://cafebiz.vn
    get_topic_from_link: true
    topics_xpath:
    - //a[@title and contains(@href, '.chn') and string-length(@title) > 15]
    topic_type: text
    extract_xpath:
    - ./@title
    contain: ''
    minimum_topic_length: 4
    skip_checking_topic_length: false
    get_publish_date_as_crawl_date: false
    date_place: detail_page
    date_xpath:
    - //div[@class='timeandcatdetail']
    use_index_number: false
    date_re: (\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4} \d{1,2}:\d{1,2} [AP]M)
    date_pattern: '%d/%m/%Y %I:%M %p'
    timezone: Asia/Ho_Chi_Minh
    output_html: false
    use_browser: true
    browser_profile: ''
    display_browser: false
    browser_fast_load: true
    maximum_url: 10
    last_run: 29/05/2019 08:17
    minimum_duration_between_crawls: 15
