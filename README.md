# ĐỌC BÁO THEO TỪ KHÓA 
Framework quét và tổng hợp từ khóa từ các trang báo, blog tiếng Việt và tiếng Anh 

Demo
- Trang tổng hợp 35 báo tiếng Việt: http://theodoibaochi.com
- Trang tổng hợp tin tức về Hải Phòng: http://haiphong.theodoibaochi.com

Author: hailoc12  
Email: danghailochp@gmail.com  
Facebook: https://www.facebook.com/danghailochp
Updated: 22/12/2018  

# Giới thiệu:
Đọc Báo Theo Từ Khóa ban đầu là công cụ được xây dựng nhằm giải quyết nhu cầu theo dõi báo chí mỗi ngày với số lượng lớn của bản thân. Phương thức hoạt động của công cụ rất đơn giản: quét dữ liệu từ các báo, áp dụng các mô hình tách từ và thống kê từ khóa để tìm ra các từ khóa mới xuất hiện, đang tăng trưởng nhanh hoặc đang là trend. Từ đó công cụ có thể giúp các cá nhân hoặc tổ chức xây dựng các trang tổng hợp thông tin để theo dõi các nguồn trang xác định mà mình quan tâm. Ưu điểm lớn nhất của công cụ so với các hệ thống như scrapy là target vào bài toán cụ thể là quét báo, sử dụng file config dạng plain text nên không cần sửa code để dùng, cài đặt đơn giản.

Sau một thời gian phát triển, nhận thấy việc khai thác dữ liệu từ báo chí có thể mang đến rất nhiều ứng dụng thực tế, cũng như hỗ trợ cho sự phát triển của lĩnh vực NLP, nên mình quyết định opensource mã nguồn và cố g81ng module hóa các chức năng để đưa ĐỌC BÁO THEO TỪ KHÓAtrở thành một framework giúp các developer nhanh chóng phát triển sản phẩm của mình, đồng thời cũng giúp Đọc Báo Theo Từ Khóa hoàn thiện hơn. 

Framework hoàn toàn miễn phí và sẽ luôn miễn phí. Các phiên bản tốt hơn vẫn sẽ liên tục được cập nhật. Nếu ứng dụng này hữu ích với công việc của bạn, rất mong bạn có thể ủng hộ dự án theo các cách sau để dự án tiếp tục phát triển: 

- Chia sẻ config của các trang báo mà bạn đã quét được
- Chạy thử Đọc Báo và Issue các lỗi mà bạn phát hiện được
- Issue các ý tưởng để cải tiến dự án
- Fork project và giúp phát triển tính năng cho dự án
- Cho mượn VPS để mình quét thêm được những trang mới (bạn nào cho mượn mình sẽ hỗ trợ build một trang Đọc Báo riêng cho nhu cầu của bạn)

Và đừng quên star cho mình nhé :d

# Tính năng nổi bật:

1. Quét được hầu hết các trang báo, blog kể cả các trang dùng AJAX mà không bị block
2. Sử dụng xử lý ngôn ngữ (NLP) để phân tích tiêu đề báo thành các keyword. Hỗ trợ cả tiếng Anh và tiếng Việt
3. Thuật toán lọc từ khóa thông minh, giúp loại bỏ keyword yếu, chỉ giữ lại keyword mạnh, giàu thông tin
4. Tự động phân keyword vào các chuyên mục. Có thể tùy biến chuyên mục theo nhu cầu cá nhân
5. Phân tích nâng cao giúp xác định keyword mới xuất hiện, keyword có tần suất tăng trưởng nhanh, keyword đang là trends. Dễ dàng code mở rộng để thực hiện các phân tích khác
6. Tìm kiếm nhanh chóng toàn bộ các bài báo có chứa keyword
7. Hỗ trợ export database dễ dàng dưới dạng excel và json để phân tích bổ sung hoặc tái sử dụng trong các dự án khác

# Cài đặt
Đọc Báo hiện có thể chạy trên Ubuntu, Raspberry Pi (model 3 / model B+) và Windows 10. Việc cài đặt được thực hiện tự động, tuy nhiên bạn sẽ cần nhập tài khoản fpt host để đẩy website hiển thị lên frontend.

## Yêu cầu chung:
Để chạy được Đọc Báo, bạn cần một máy tính để quét và một host hỗ trợ php và ftp để chạy website hiển thị dữ liệu. Về máy tính quét thì bạn có thể mua VPS, dùng một con Raspberry Pi hoặc chạy trên máy tính cá nhân của bạn. Còn host nếu bạn chưa có thì có thể inbox mình để mượn hoặc dùng tạm tài khoản sau để test:

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
Tại bước này, bạn hãy nhập n + Enter để tạo một config mới. Tiếp đến hãy nhập name là docbao, nhập host, username, pass theo thông tin mình đã cung cấp ở trên 

Sau khi tạo config, nhập q + Enter để trình cài đặt chạy tiếp.

#### Bước 4: Chạy thử
Khi trình cài đặt đã chạy xong, bạn hãy dùng lệnh sau để bắt đầu quét. Mặc định hệ thống sẽ quét trang Báo Mới

~~~~
cd ~/docbao
bash run_docbao.sh
~~~~

Sau khi quét xong, bạn hãy mở trang http://demo.theodoibaochi.com để xem kết quả

#### Bước 5: Tùy biến cấu hình quét để xây dựng trang thông tin của riêng bạn
(đang xây dựng tài liệu)




