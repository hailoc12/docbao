# BỘ QUÉT ĐỌC BÁO CRAWLER (Version 2.0)  

### Giới thiệu   
*"Đọc báo Crawler"* là bộ quét chuyên dụng viết bằng Python, dùng để thu thập tin tức/bài viết trên các trang báo mạng điện tử và website, blog tiếng Việt. Dự án có thể được sử dụng để đơn giản hoá nhiệm vụ thu thập dữ liệu trong các Data Project, hoặc dùng trong mục đích giáo dục để giúp sinh viên và những người mới học có thể hiểu được cách sử dụng nhiều kĩ thuật thực tế trong Python (OOP, multiprocessing, parse HTML, json, yaml...)  

Một số ví dụ sử dụng *"Đọc báo Crawler"* (xem thêm CASE_STUDY.md để có danh sách đầy đủ)
 - [Demo *"Đọc báo Crawler"* thực hiện quét song song 35 nguồn báo sử dụng 10 trình duyệt Firefox cùng lúc](https://youtu.be/cPZ1XlAAIsk)  
 - [Theodoibaochi.com](https://theodoibaochi.com): site sử dụng *"Đọc báo Crawler"* để tổng hợp tin tức từ 35 nguồn báo mạng phổ biến tại Việt Nam. Site này cũng là giao diện frontend mặc định tích hợp cùng bộ quét    
 - [VnAlert](https://vnalert.vn) - Ứng dụng thương mại sử dụng *"Đọc báo Crawler"* làm bộ cung cấp dữ liệu  

Trước khi sử dụng dự án, mời đọc qua CODE_OF_CONDUCT.md để nắm được một số lưu ý về pháp lý khi sử dụng *Docbao Crawler*. Để đóng góp cho dự án, mời bạn tham khảo HOW_TO_CONTRIBUTE.md 

### Nguyên tắc hoạt động  

*"Đọc báo Crawler"* hoạt động theo nguyên tắc quét nhiều trang cùng lúc theo chu kỳ định sẵn (qua crontab). Mỗi chu kỳ quét (cách nhau tối thiểu 10-15 phút), bộ quét sẽ duyệt qua tất cả các trang có trong thiết lập cấu hình. Với mỗi trang bộ quét sẽ duyệt qua một số lượng đường link nhất định, xác định những link dẫn tới bài viết và lấy về dữ liệu. Cuối chu kỳ quét, toàn bộ dữ liệu sẽ được lưu vào database và đẩy ra các kênh dữ liệu khác (như Elasticsearch, RabbitMQ, export json) tuỳ thuộc thiết lập. 

Ưu điểm chính của *"Đọc báo Crawler"* so với cách sử dụng trực tiếp các thư viện scrapy, requests, selenium...là tối ưu cho việc quét nhiều site cùng một lúc, và đơn giản hoá việc phân tích cấu trúc site cần quét thành các file plain text dễ chia sẻ, giúp những người không có kiến thức, kinh nghiệm parse HTML, sử dụng xpath, css selection...cũng có thể tự thiết lập bộ quét và có được dữ liệu mong muốn (xem chi tiết ở mục "Những tính năng chính")


### Những tính năng chính  

**1. Có thể sử dụng mà không cần biết code**  
Quét dữ liệu là nhiệm vụ thường thấy trong các dự án Data project. *"Đọc báo Crawler"* giúp đơn giản hoá tối đa nhiệm vụ này bằng cách cung cấp tool quản trị để người sử dụng có thể điều chỉnh hoạt động của bộ quét như thêm/bớt nguồn, thay đổi thời gian quét...mà không cần can thiệp vào mã nguồn của dự án 

**2. Dễ dàng thêm/bớt nguồn quét bằng cách chia sẻ file cấu hình quét** 
*"Đọc Báo Crawler"* sử dụng các file cấu hình quét (là file mô tả cấu trúc của site cần quét theo một ngôn ngữ riêng là yaml và xpath) ở dạng plain text và có thể dễ dàng chia sẻ. Mặc dù việc xây dựng file cấu hình quét đòi hỏi kiến thức chuyên môn cao và kĩ năng làm việc với tool cấu hình do *"Đọc báo Crawler"* cung cấp, nhưng một khi đã xây dựng xong thì có thể chia sẻ để tất cả mọi người cùng sử dụng. 

**3. Quét được hầu hết site (thậm chí Facebook, Youtube) bằng một thuật toán và ngôn ngữ cấu hình duy nhất** 
Thay vì phải code để quét được dữ liệu của từng site (giống với cách làm của scrapy hay một số tutorial hướng dẫn xây dựng bộ quét), *"Đọc báo Crawler"* tạo ra một ngôn ngữ cấu hình và thuật toán quét thống nhất dựa trên đặc trưng chung của các site tin tức. Thuật toán và ngôn ngữ cấu hình này đủ mạnh để quét được hầu hết các site tin tức, gồm cả những site khó như site dùng Ajax để tải nội dung, site cần login (Facebook, Youtube), site có cấu trúc bài viết không ổn định (ví dụ format bài viết khác nhau ở từng chuyên mục). Mặc dù thuật toán và ngôn ngữ cấu hình đòi hỏi kiến thức chuyên môn nhất định để hiểu, nhưng như đã nói ở trên, người sử dụng *"Đọc báo Crawler"* có thể sử dụng file config do người khác tạo ra và không cần nắm được thuật toán hay ngôn ngữ cấu hình quét để chạy được. 

**4. Tích hợp sẵn nhiều thủ thuật dùng để chống bị chặn và xử lý các vấn đề thường gặp khi đi quét**  
*"Đọc báo Crawler"* đã được phát triển trong vòng 3 năm và sử dụng để quét ổn định trên hàng trăm site tin tức tại Việt Nam khác nhau, vì vậy mã nguồn dự án đã được tích hợp nhiều giải pháp để giải quyết các vấn đề phát sinh trong quá trình quét (nhiều vấn đề thực sự rất cù lần). Sử dụng *"Đọc báo Crawler"* sẽ là cách để những người không có nhiều kinh nghiệm đi quét có thể có được dữ liệu sạch mà không phải mất quá nhiều thời gian "tu luyện" và giải quyết những vấn đề phát sinh không đáng có.  

**5. Dữ liệu thu thập được có cấu trúc tới cấp độ đoạn văn** 
Một điểm mạnh của *"Đọc báo Crawler"* là trả về dữ liệu bài viết có cấu trúc (gồm tiêu đề, mô tả/sapo, thời gian xuất bản, nội dung bài viết). Đặc biệt nội dung bài viết có độ chi tiết tới từng đoạn văn và giữ nguyên được cấu trúc của bài viết gốc (ví dụ: ảnh 1, đoạn văn 1, ảnh 2, ảnh 3, đoạn văn 3, đoạn văn 4...). Các chi tiết khác (như tên tác giả, lượt like, share...) có thể mở rộng để lấy được trong tương lai.  

**6. Tích hợp đa dạng hình thức lấy dữ liệu quét** 
*"Đọc báo Crawler"* hỗ trợ nhiều hình thức để lấy ra dữ liệu và sử dụng trong các dự án lớn hơn: 
- Đổ dữ liệu vào Elasticsearch 
- Đỗ dữ liệu vào queue của RabbitMQ 
- Truy cập dữ liệu qua API Server được tích hợp sẵn 
- Truy cập dữ liệu qua file json được export cuối mỗi chu kỳ quét 
- Xem dữ liệu trực tiếp qua frontend tích hợp sẵn cùng dự án 

**7. Tích hợp sẵn thuật toán phân tích xu hướng dựa trên từ khoá & frontend hiển thị dữ liệu**  
*"Đọc báo Crawler"* tích hợp sẵn thuật toán phân tích từ khoá từ dữ liệu tin tức thu thập được (sử dụng chức năng tokenize của thư viện underthesea) và phát hiện xu hướng thông tin dựa trên sự tăng trưởng của các từ khoá. *"Đọc báo Crawler"* cũng tích hợp sẵn một frontend đơn giản hoạt động độc lập với backend (đọc dữ liệu qua file json), để giúp người vận hành dễ dàng kiểm tra và tìm kiếm dữ liệu quét 

**8. Tài liệu đầy đủ và chi tiết (đang xây dựng)**  
*"Đọc báo Crawler"* hướng tới mục tiêu trở thành một dự án có tính giáo dục và là một mô hình vận hành theo đúng triết lý opensource (bởi vì bản thân mình cũng đã học được và nhận được rất nhiều sự hỗ trợ khi theo đuổi dự án này). Vì vậy việc xây dựng tài liệu hướng dẫn đầy đủ, chi tiết để mọi người, kể cả những người không có nhiều kinh nghiệm lập trình cũng có thể hiểu và có hứng thú cài đặt, vận hành thử dự án, là một mục tiêu mà tác giả dự án đặt ra. 

### Tổ chức thư mục  
- docs: chứa các tài liệu kĩ thuật của dự án  
- resources: chứa một số file cần thiết cho việc cài đặt và kho file cấu hình để thêm vào bộ quét   
- src: folder chứa mã nguồn backend (bộ quét) và frontend (site hiển thị dữ liệu quét được)  
- scripts: các script cần thiết để cài đặt và vận hành bộ quét 
- tools: công cụ dùng để quản lý cấu hình quét và các thông số quét 

### Hướng dẫn cài đặt

Để chạy được Docbao Crawler, bạn cần một máy tính/VPS chạy hệ điều hành Ubuntu, hoặc Windows 10 chạy Linux Subsystem. Docbao Crawler cũng có thể chạy được trên Raspberry Pi với số lượng nguồn báo quét nhỏ 

#### 1. Cài đặt trên Ubuntu 
Để cài đặt Docbao Crawler trên Ubuntu (16.04 hoặc 18.04 đều được), bạn cần có quyền admin và sẽ cần nhập mật khẩu admin trong quá trình cài đặt. Các bước cài đặt cụ thể như sau: 

##### Bước 1: Clone mã nguồn từ github
Mở terminal trong Ubuntu (Ctr+Alt+T) và gõ dòng lệnh sau
~~~~
git clone http://github.com/hailoc12/docbao
~~~~

##### Bước 2: Kiểm tra lại đường dẫn của bộ cài (SETTING.env)
Nếu folder cài đặt nằm ở địa chỉ ~/docbao thì bạn có thể bỏ qua bước này. Còn nếu bạn đặt mã nguồn Docbao_crawler tại đường dẫn khác, thì hãy thay đổi biến DOCBAO_BASE_DIR trong file SETTING.env

~~~
export DOCBAO_BASE_DIR=[đường dẫn tới folder docbao_crawler]
~~~
Lưu ý: nếu bạn thực hiện sai bước này, thì các bước cài đặt sẽ không chạy được 

##### Bước 3: Chạy file cài đặt 
Hãy bảo đảm bạn đang ở trong thư mục docbao_crawler khi chạy các lệnh cài đặt sau: 
~~~~
source SETTINGS.env
bash install.sh
~~~~

Trình cài đặt sẽ tự động chạy. Kết thúc quá trình cài đặt, script sẽ tự động chạy test. Bạn thấy các kết quả test đều báo OK nghĩa là đã cài đặt thành công 



#### 2. Cài đặt trên Windows 10 
(Đang bổ sung)

#### 3. Cài đặt trên Raspberry Pi 
Để cài đặt Docbao Crawler trên Raspberry Pi, bạn cần ssh vào terminal của Raspberry PI và đăng nhập ở tài khoản admin. Qúa trình cài đặt sẽ yêu cầu nhập mật khẩu admin. Các bước cài đặt cụ thể như sau. 

##### Bước 1: Clone mã nguồn từ github
Mở terminal trong Ubuntu (Ctr+Alt+T) và gõ dòng lệnh sau
~~~~
git clone http://github.com/hailoc12/docbao
~~~~

##### Bước 2: Kiểm tra lại đường dẫn của bộ cài (SETTING.env) & đặt chế độ cài trên Raspberry PI
Nếu folder cài đặt nằm ở địa chỉ ~/docbao_crawler thì bạn có thể bỏ qua bước này. Còn nếu bạn đặt mã nguồn Docbao_crawler tại đường dẫn khác, thì hãy thay đổi biến DOCBAO_BASE_DIR trong file SETTING.env

~~~
export DOCBAO_BASE_DIR=[đường dẫn tới folder docbao_crawler]
~~~

Tiếp tục thay đổi giá trị của biến môi trường DOCBAO_RUN_ON_RASPBERRY=true
~~~
export DOCBAO_RUN_ON_RASPBERRY=true
~~~ 

Lưu ý: nếu bạn thực hiện sai bước này, thì các bước cài đặt sẽ không chạy được 

##### Bước 3: Chạy file cài đặt 
Hãy bảo đảm bạn đang ở trong thư mục docbao_crawler khi chạy các lệnh cài đặt sau: 
~~~~
source SETTINGS.env
bash install.sh
~~~~

Trình cài đặt sẽ tự động chạy. Kết thúc quá trình cài đặt, script sẽ tự động chạy test. Bạn thấy các kết quả test đều báo OK nghĩa là đã cài đặt thành công 

### Hướng dẫn vận hành bộ quét  

#### Bước 1: thiết lập nguồn quét   
*Docbao Crawler* lưu toàn bộ thông tin mô tả về nguồn quét trong file src/backend/input/config.yaml. Mặc định sau khi cài đặt, trong file config.yaml sẽ bao gồm 5 nguồn quét là các trang VnExpress, VOV, VTV, Dân Trí, Vietnamnet. Tần suất quét mặc định là 15 phút. 

Việc chỉnh sửa trực tiếp file config.yaml là không khuyến khích, để thay đổi thiết lập quét, *Docbao Crawler* cung cấp sẵn một tool quản lý cấu hình. Chạy tool này như sau 

~~~
bash tools/config_manager.sh  

Sau đó, vào mục "2.Manager program settings/Edit Crawl list" để thêm/bớt nguồn quét 
~~~  

(đang phát triển tài liệu hướng dẫn sử dụng tool config_manager)  

#### Bước 2: thiết lập kênh đổ dữ liệu   
Hiện tại *Docbao Crawler* hỗ trợ 4 hình thức lưu trữ dữ liệu quét: 
1. Lưu trữ dữ liệu dưới dạng pickle file (src/backend/data) và export ra dạng json (src/backend/export). Đây là hình thức lưu trữ mặc định   
2. Đỗ dữ liệu vào Elasticsearch (cài đặt qua file SETTINGS.env)  
3. Đổ dữ liệu vào RabbitMQ (cài đặt qua file SETTINGS.env)
4. Đẩy bài viết lên wordpress (cài đặt qua file SETTINGS.env)  
5. Truy cập dữ liệu thông qua API Server tích hợp sẵn (đang xây dựng tài liệu) 

Tuỳ theo nhu cầu sử dụng, các bạn thiết lập cấu hình tương ứng  

#### Bước 3: chạy quét thử chu kỳ đầu tiên để bảo đảm bộ quét hoạt động đúng  
Từ thư mục gốc, các bạn chạy lệnh sau để khởi động chu trình quét  

~~~
bash scripts/crawl.sh
~~~  

*Docbao Crawler* sẽ bắt đầu quét tin tức từ các nguồn được cấu hình trong file src/backend/input/config.yaml (mặc định gồm VTV, VOV, Dân Trí, Vnexpress, Vietnamnet) 

#### Bước 4: bật frontend để kiểm tra kết quả quét  
*Docbao Crawler* tích hợp sẵn một frontend đơn giản, có thể dùng để xem các bài viết đã quét được. Để bật frontend này, sử dụng câu lệnh sau đây 

~~~
bash scripts/start_frontend.sh
~~~

Mặc định, frontend sẽ chạy ở địa chỉ https://localhost:8085. Bạn có thể thay đổi địa chỉ và port frontend chạy bằng cách thay đổi tham sốD BAONOI_FRONTEND_HOST và BAONOI_FRONTEND_PORT trong file SETTINGS.env.

Nếu bạn nhìn thấy bài viết từ các nguồn quét đã xuất hiện trên frontend thì có nghĩa bộ quét đã hoạt động thành công 

#### Bước 5: thiết lập crontab 
Để *Đọc báo Crawler* tự động thực hiện các chu trình quét, bạn cần cài đặt chạy tự động trong crontab như sau 

Mở crontab 
~~~
crontab -e 
~~~

Thêm vào hai dòng dưới đây 
~~~
*/15 * * * * cd ~/docbao/ && bash scripts/crawl.sh
*/60 * * * * cd ~/docbao/ && bash scripts/clean_temp.sh
~~~

Thiết lập ở trên là mỗi 15 phút, bộ quét sẽ tiến hành quét và update dữ liệu một lần. Bạn có thể thay đổi thành mốc thời gian khác, nhưng nên để > 10 phút để bộ quét chạy ổn định. 
 
### Đọc dữ liệu từ docbao crawler để sử dụng. 

#### 1. Đọc dữ liệu thông qua RabbitMQ 

##### a. Cấu hình để đẩy dữ liệu lên RabbitMQ.
 
Sử dụng RabbitMQ khi muốn xử lý dữ liệu quét được theo thời gian thực, hoặc có nhiều client cùng lấy dữ liệu từ Docbao Crawler một cách độc lập thông qua cơ chế exchange và queue binding. 

Để đẩy dữ liệu quét được qua RabbitMQ, bạn cần bổ sung các tham số liên quan tới RabbitMQ trong file SETTINGS.env. Ví dụ: 

~~~
export DOCBAO_EXPORT_TO_RABBITMQ=true
export DOCBAO_RABBITMQ_HOST=127.0.0.1
export DOCBAO_RABBITMQ_USERNAME='admin'
export DOCBAO_RABBITMQ_PASSWORD='password'
export DOCBAO_RABBITMQ_EXCHANGE='exchange_name'
export DOCBAO_RABBITMQ_DEFAULT_QUEUE='default_queue_name'
~~~  
Lưu ý, username 'admin' cần được set quyền admin và full permission tới vhost /. 

Mặc định, Docbao Crawler bất kì khi nào quét được bài viét mới, Docbao Crawler sẽ đẩy dữ liệu quét được lên exchange trong DOCBAO_RABBITMQ_EXCHANGE và bind DOCBAO_RABBITMQ_DEFAULT_QUEUE vào exchange trên. Client cũng có thể bind thêm các queue khác vào exchange để "subscribe" dữ liệu từ Docbao Crawler 

##### b. Đọc dữ liệu từ RabbitMQ. 
Docbao Crawler cung cấp một file boilerplate để bạn đọc dữ liệu từ RabbitMQ và đẩy vào database/xử lý theo cách mong muốn. File này nằm tại: /src/clients/get_data_from_rabbitmq.py. Hướng dẫn sử dụng mời xem trong file 

##### c. Đẩy toàn bộ dữ liệu đã quét lên RabbitMQ. 
Sau khi cấu hình đẩy dữ liệu lên RabbitMQ, mặc định, Docbao Crawler sẽ chỉ đẩy những dữ liệu mới. Nếu muốn đẩy toàn bộ các bài viết hiện có ở local database lên RabbitMQ, bạn có thể chạy script sau:
~~~
bash scripts/push_all_articles_to_rabbitmq.sh
~~~

### Một số thao tác khác 

#### 1. Reset dữ liệu  
Khi bạn muốn quét lại các trang từ đầu và không lưu bất kì dữ liệu gì thì có thể sử dụng script reset_data.sh mà *Docbao Crawler* cung cấp. Sử dụng script này bằng lệnh sau 

~~~
bash scripts/reset_data.sh
~~~

#### 2. Fix lỗi UnicodeError khi chạy Docbao Crawler trên một số server  
Lỗi này xuất hiện do server chưa thiết lập locale. Để fix chạy lệnh sau  

~~~
bash scripts/run_fix_env_encoding.sh  
~~~


### Lịch sử phát triển  

Dự án *"Đọc báo"* (hay *Theo Dõi Báo Chí*) được phát triển từ đầu năm 2018 khi tác giả vẫn đang là một phóng viên. Ý tưởng ban đầu của dự án là gom tin tức từ nhiều nguồn lại với nhau, hiển thị trên một giao diện đơn giản để theo dõi tin tức nhanh chóng hơn (chính vì vậy mà dự án có tên là *"Đọc báo"*). Những phiên bản đầu tiên của dự án này hoạt động đơn luồng, chạy trên Raspberry Pi B và quét khoảng 30 đầu báo.  

Đến cuối năm 2018, tác giả được anh Vũ Hữu Tiệp, một người anh cùng khoá tại Câu lạc bộ Tài năng công nghệ trẻ FYT (FPT), khi đó là admin của Diễn đàn Machine Learning cơ bản, vận động opensource dự án. Dự án chính thức được opensource tại địa chỉ https://github.com/hailoc12/docbao. Phần giao diện cũng được nâng cấp và chính thức hoạt động tại địa chỉ https://theodoibaochi.com (website vẫn được duy trì hoạt động cho tới thời điểm hiện tại)  

Kể từ khi opensource và được sự ghi nhận từ cộng đồng, tác giả đã nhận được sự góp ý từ rất nhiều thành viên của Diễn đàn Machine Learning cơ bản. Đặc biệt là anh Nguyễn Ngọc Duy Luân (mod diễn đàn Tinh Tế) và anh Hùng Thịnh tại Tp Hồ Chí Minh tài trợ VPS để dự án chuyển từ chạy trên Raspberry Pi B lên một server thực sự (Một thời gian sau mình mới biết VPS mà anh Hùng Thịnh tài trợ là do anh bỏ tiền túi với chi phí khoảng 4 triệu/tháng !). Nhờ có VPS, dự án được tác giả phát triển thêm nhiều tính năng mới (xử lý đa luồng, quét nội dung bài viết, quét Facebook, phân tích xu hướng tự động qua từ khoá...). Tháng 2/2020, tác giả mạnh dạn mang dự án đi thử sức và được trao tặng [Giải Ba tại Hội thi Tin học khối cán bộ, công chức trẻ toàn quốc năm 2019, tổ chức tại An Giang](https://vietnamnet.vn/vn/thong-tin-truyen-thong/trao-giai-hoi-thi-tin-hoc-khoi-can-bo-cong-chuc-tre-toan-quoc-nam-2019-584527.html)  

Những ghi nhận từ cộng đồng đã giúp tác giả tự tin và quyết tâm hơn để theo đuổi con đường trở thành một lập trình viên chuyên nghiệp (vốn là đam mê từ nhỏ nhưng vì một số lý do mà đã không theo đuổi được). Tháng 7/2019, nhờ sự giới thiệu của anh Lê Công Thành, founder của Công ty CP Công nghệ Infore Technology (Giải nhất cuộc thi Nhân tài đất Việt 2016, tình cờ là năm mà tác giả đang là phóng viên trong ekip thực hiện chương trình của VTV2), tác giả chính thức chuyển sang làm lập trình viên chuyên nghiệp và tiếp tục phát triển mã nguồn dự án để phục vụ một số dự án thương mại. Trong quá trình này dự án tiếp tục được cải thiện về tính năng, mức độ ổn định, và thực tế đang được sử dụng để thu thập hàng trăm nguồn tin tức mỗi ngày cho sản phẩm thương mại *[Công dụ Theo dõi và Cảnh báo tin tức VnAlert](https://vnalert.vn)*  

Vì tác giả đã học hỏi được rất nhiều về lập trình thông qua dự án và nhận được nhiều sự hỗ trợ từ cộng đồng trong suốt quá trình phát triển dự án, nên bản thân tác giả luôn nghĩ rằng *Đọc báo Crawler* là một dự án của cộng đồng và nên được "pay it forward" để trả về giá trị cho cộng đồng. Vì vậy kể từ tháng 8/2020, dự án *Đọc báo Crawler* nhận được một big update, đồng thời được refactor lại, bổ sung documentation để hướng tới mục tiêu không chỉ là một dự án hữu dụng cho cộng đồng làm dữ liệu tại Việt Nam, mà còn là một dự án giáo dục, giúp đỡ và truyền cảm hứng cho những bạn yêu thích lập trình nói chung và Python nói riêng có một dự án thú vị để thực hành. Mong rằng qua dự án này, nhiều bạn sẽ có những ý tưởng thú vị, và biết đâu sẽ nhận được những "cú hích" cần thiết để theo đuổi con đường lập trình như tác giả đã từng nhận được :d. 

# Những người phát triển dự án 

1. Đặng Hải Lộc (hailoc12)
Email: danghailochp@gmail.com  
Facebook: https://www.facebook.com/danghailochp
