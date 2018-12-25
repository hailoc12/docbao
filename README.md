# ĐỌC BÁO THEO TỪ KHÓA 
Framework quét và tổng hợp từ khóa từ các trang báo, blog tiếng Việt và tiếng Anh 

Demo
1. Trang tổng hợp 35 báo tiếng Việt: http://theodoibaochi.com

Version: 1.4.0  
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
## Cài đặt frontend
1. Chuẩn bị host hỗ trợ php, tạo tài khoản ftp để đẩy file lên host (nếu bạn không có host, có thể liên hệ với mình qua email để mượn account)
2. Cài rclone. Add new config với tên gọi "docbao" và account ftp đã tạo ỏ trên để đẩy file lên host
3. Đẩy toàn bộ các file trong folder frontend lên host
~~~~
rclone copy -v ~/docbao/frontend docbao:
~~~~
4. Mở host bằng browser để kiểm tra

## Cài đặt backend
### A. Cài trên linux (ubuntu)
1. Cài trình duyệt Firefox nếu chưa có (bắt buộc)
2. Clone mã nguồn về địa chỉ ~/docbao
3. Chmod file
~~~~
chmod 755 ~/docbao/backend/run
chmod 755 ~/docbao/run_docbao.sh
~~~~
4. Dùng pip3 để cài các package trong file requirements.md
5. Chạy test, nếu các bài test đều báo OK thì bạn đã cài đặt thành công
~~~~
python3 ~/docbao/backend/test.py
~~~~
6. Chạy quét dữ liệu lần đầu
~~~~
bash ~/docbao/backend/run
~~~~

Quá trình chạy có thể kéo dài 10-20 phút  
5. Test kết quả: mở file ~/docbao/backend/export/local_html/index.html  
6. Test chạy và đẩy dữ liệu lên frontend  
~~~~
bash ~/docbao/run_docbao.sh
~~~~
8. Mở địa chỉ host để kiểm tra kết quả
9. Cài đặt crontab để chạy tự động
~~~~
crontab -e
~~~~
Bổ sung dòng sau vào cuối file. Thay /home/pi bằng username của bạn
Backend sẽ chạy tự động 10p / lần. Nếu bạn muốn thay đổi thông số này, thì cần thay đổi cả loop_interval trong ~/docbao/backend/input/config.txt
~~~~
*/10 * * * * /bin/bash /home/pi/docbao/run_docbao.sh > ~/cron_log
~~~~
10. Mở file ~/docbao/backend/input/config.txt để tùy biến theo nhu cầu

### Cài trên Windows:  
#### Cài thông qua Linux subsystem trên Windows 10 (khuyến khích)
1. Cài Ubuntu trên Windows 10 [theo hướng dẫn](https://stackjava.com/linux/cai-dat-ubuntu-tren-windows-10-voi-windows-linux-subsystem.html)
2. Cài docbao theo hướng dẫn của phần Linux

