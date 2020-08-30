- Tuổi Trẻ:
    id_type: href
    browser_profile: ''
    web_url: https://tuoitre.vn
    timezone: Asia/Ho_Chi_Minh
    remove_date_tag_html: true
    remove_content_html: true
    use_index_number: false
    remove_content_html_xpaths:
    - //node()[@class='sapo' or @class='relate-container' or contains(@class, 'VCSortableInPreviewMode')]
    minimum_duration_between_crawls: 15
    language: vietnamese
    feature_image_xpath:
    - //div[@class="main-content-body"]//img[@type="photo"]//@src
    - //div[@class="main-content-body"]//img[@type="photo"]//@src
    extract_xpath:
    - ./text()
    - ./@title
    topics_xpath:
    - //a[text()]
    - //a[@title]
    skip_checking_topic_length: false
    display_browser: false
    sapo_xpath:
    - //h2[@class="sapo"]/text()
    - //h2[@class="sapo"]/text()
    get_publish_date_as_crawl_date: false
    browser_fast_load: true
    skip_repeat_topic: true
    use_browser: false
    date_place: detail_page
    ignore_topic_not_have_publish_date: true
    last_run: 02/06/2019 21:56
    contain: ''
    crawl_url: https://tuoitre.vn
    output_html: false
    get_topic_from_link: true
    date_xpath:
    - //div[@class='date-time']
    - //div[@class='date-time']
    topic_type: href
    maximum_url: 10
    get_detail_content: true
    content_xpath:
    - //div[@class="main-content-body"]
    - //div[@class="main-content-body"]
    text_xpath: ''
    image_box_xpath: ''
    image_title_xpath: ''
    video_box_xpath: ''
    video_title_xpath: ''
    audio_box_xpath: ''
    audio_title_xpath: ''
    avatar_type: 'url'
    avatar_url: ''
    avatar_xpath: ''
    crawl_type: newspaper
    url_pattern_re: https://tuoitre.vn
    minimum_topic_length: 4
