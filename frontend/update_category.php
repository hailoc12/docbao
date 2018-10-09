<?php
error_reporting(E_ALL ^ E_NOTICE);
function append_to_file($filename, $value)
{
    return file_put_contents($filename, $value, FILE_APPEND | LOCK_EX);
}

	if(isset($_POST['keyword'])) {
        $keyword = strtolower($_POST['keyword']);
        $categories = [
            "chinh_tri" => "Chính trị",
            "kinh_te" => "Kinh tế",
            "van_hoa" => "Văn hoá",
            "xa_hoi" => "Xã hội",
            "giao_duc" => "Giáo dục",
            "the_thao" => "Thể thao",
            "giai_tri" => "Giải trí",
            "cong_nghe" => "Công nghệ",
            "an_ninh" => "An ninh",
            "quoc_phong" => "Quốc phòng",
            "suc_khoe" => "Sức khoẻ",
            "doi_song" => "Đời sống",
            "giao_thong" => "Giao thông",
            "moi_truong" => "Môi trường",
            "quoc_gia" => "Quốc gia",
            "dia_phuong" => "Địa phương",
            "su_kien" => "Sự kiện",
            "nhan_vat" => "Nhân vật",
            "dia_danh" => "Địa danh",
            "tac_pham" => "Tác phẩm",
        ];
        foreach($categories as $category_key => $category_name) {
            if(isset($_POST[$category_key]) && $_POST[$category_key] == "yes") {
                $filename = "./category/". $category_key .".txt"
                $ret = append_to_file($filename, $keyword . "\r\n");
                if($ret === false) {
                    die('There was an error writing this file');
                }
                else {
                    echo "<p>Từ khóa $keyword đã được phân vào chuyên mục ". $category_name . "</p>";
                }    
            }
        }
	}
?>
