# ĐỌC BÁO THEO TỪ KHÓA (V1.3.0)
Công cụ quét báo mạng theo mô hình phân tán để xây dựng các trang theo dõi báo chí cá nhân hoá 
- Trang tổng hợp 35 báo tiếng Việt: https://theodoibaochi.com
- Trang tổng hợp tin tức báo chí về Hải Phòng: http://haiphong.theodoibaochi.com

Demo quét song song 35 tờ báo sử dụng 10 trình duyệt Firefox cùng lúc
https://youtu.be/cPZ1XlAAIsk

Author: hailoc12  
Email: danghailochp@gmail.com  
Facebook: https://www.facebook.com/danghailochp

# Giới thiệu:
Đọc Báo Theo Từ Khoá là phiên bản mã nguồn mở để xây dựng các trang tổng hợp tin tức giống như [Báo Mới](http://baomoi.com), với vài điểm khác biệt:

1. Người dùng chủ động nguồn báo để quét
2. Dễ cài đặt, nhẹ, có thể chạy được trên máy tính cá nhân, raspberry PI, hay server
3. Tích hợp chức năng phân tích từ khoá, xác định từ khoá nổi bật, từ khoá hot, từ khóa mới xuất hiện, phân từ khoá vào các chuyên mục
4. Tích hợp với elasticsearch + kibana để thực hiện các truy vấn nâng cao trên dữ liệu
5. Mã nguồn mở, miễn phí

Công cụ hướng đến nhiều đối tượng người dùng:  
1. Độc giả thông thường: tiết kiệm thời gian đọc báo, chủ động chọn lựa nguồn báo uy tín để đọc  
2. Phóng viên: tìm kiếm đề tài, kiểm chứng, theo dõi thông tin ngành / địa phương phân công phụ trách, làm quen với xu hướng Data Journalist  
3. PR/Marketing/Agency: theo dõi thương hiệu trên báo chí, phân tích chiến dịch truyền thông của đối thủ, nắm bắt nhanh các vấn đề đang là trend  
4. Nhà nghiên cứu truyền thông: theo dõi sự kiện, tìm kiếm nhanh các bài báo liên quan tới một sự kiện, lấy dữ liệu excel để phân tích  
5. Developer: khai thác phần lõi quét báo để lấy dữ liệu phát triển các ứng dụng khác  

# Tính năng nổi bật:

1. Quét được hầu hết các trang báo, blog kể cả các trang dùng nhiều javascript mà không bị block  
2. Sử dụng công nghệ quét đa luồng, có thể ghép server để quét được số lượng lớn báo
3. Sử dụng Xử lý ngôn ngữ tự nhiên (NLP) để phân tích tiêu đề báo thành các keyword. Hỗ trợ cả tiếng Anh và tiếng Việt.
4. Tự động phân tích để xác định từ khoá nổi bật, từ khoá mới xuất hiện, từ khoá tăng trưởng nhanh.
5. Có thể tuỳ biến các chuyên mục và phân tự động từ khoá vào các chuyên mục
6. Tìm kiếm các bài báo mới xuất bản nhanh hơn Google (nếu hệ thống được cài đặt để quét đều đặn)
7. Có thể export dữ liệu dưới dạng file excel và json để phân tích nâng cao
8. Lưu trữ dữ liệu trên Elasticsearch và thực hiện các truy vấn nâng cao trên Kibana

# Cài đặt

Để chạy được Đọc Báo, bạn cần một máy tính để quét dữ liệu và một host hỗ trợ php và ftp để chạy website hiển thị dữ liệu. 

Về máy tính quét thì bạn có thể mua VPS, dùng một con Raspberry Pi hoặc chạy trên máy tính cá nhân của bạn. Còn host nếu bạn chưa có thì có thể inbox mình để mượn hoặc dùng tạm tài khoản sau để test:

host: ftp.tudonghoamaytinh.com  
user: admin@demo.theodoibaochi.com  
pass: docbaotheotukhoa  

## Cài đặt trên Ubuntu và Raspberry Pi

#### Bước 1: Clone mã nguồn từ github
Mở terminal trong Ubuntu (Ctr+Alt+T) và gõ dòng lệnh sau
~~~~
git clone http://github.com/hailoc12/docbao
~~~~

#### Bước 2: Chạy trình cài đặt tự động
Nếu bạn cài trên Ubuntu thì gõ lệnh sau:
~~~~
cd ~/docbao
./install_on_ubuntu.sh
~~~~
Còn nếu dùng Raspberry Pi thì gõ lệnh:
~~~~
cd ~/docbao
./install_on_raspberry.sh
~~~~
Trình cài đặt sẽ tự động chạy. Bạn hãy chờ cho đến trình cài đặt dừng lại và hiện thông báo sau:

~~~~
"Step 5: config remoate ftp host in rclone as 'docbao'"
REMEMBER: use remote hostname as 'docbao'
~~~~

#### Bước 3: Tạo và nhập tài khoản ftp để đẩy file lên host hiển thị website
Tại bước này, bạn hãy nhập n + Enter để tạo một config mới. 

Tiếp đến hãy nhập name là docbao

Nhập tiếp 10 + Enter để tạo cấu hình host FTP

Tiếp theo hãy nhập tài khoản FTP để đẩy file lên host của bạn. Nếu bạn chưa có host, thì có thể dùng tạm host demo của mình theo thông tin như sau:

host: ftp.tudonghoamaytinh.com  
user: admin@demo.theodoibaochi.com  
pass: docbaotheotukhoa  

Sau khi tạo config, nhập q + Enter để trình cài đặt chạy tiếp.

#### Bước 4: Chạy thử
Khi trình cài đặt đã chạy xong, bạn hãy dùng lệnh sau để bắt đầu quét. Mặc định hệ thống sẽ quét trang Báo Mới

~~~~
cd ~/docbao
bash run_docbao.sh
~~~~

Sau khi quét xong, bạn hãy mở trang http://demo.theodoibaochi.com để xem kết quả

#### Bước 5: Tạo cron để quét tự động
(đang xây dựng tài liệu)

#### Bước 6: Tùy biến cấu hình quét để xây dựng trang thông tin của riêng bạn
(đang xây dựng tài liệu)

#### Bước 7: Thực hiện các truy vấn nâng cao trên Kibana  
Mặc định, bạn có thể truy cập vào kibana tại điạ chỉ: locahost:5601  
TOàn bộ dữ liệu do Đọc Báo quét sẽ được đẩy vào index docbao

## Cài đặt trên Windows 10  

#### Bước 1: Cài Ubuntu lên Windows 10
Các bạn làm theo hướng dẫn trong bài sau: [Cài Ubuntu lên Windows 10](https://stackjava.com/linux/cai-dat-ubuntu-tren-windows-10-voi-windows-linux-subsystem.html)

#### Bước 2: Mở bash trên Windows 10 và cài đặt y như phần cài đặt với Ubuntu đã được hướng dẫn ở trên

[Clip Hướng dẫn cài đặt trên Windows 10](http://www.youtube.com/watch?v=dcYn8QiFYwI)
 

