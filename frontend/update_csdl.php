<?php 
if(isset($_POST['collocation'])) {
    $data = strtolower($_POST['collocation']);
    if(trim($data) != '')
    {
        $data = "\r\n" . $_POST['collocation'];
        $ret = file_put_contents('./output/collocation.txt', $data, FILE_APPEND | LOCK_EX);
        if($ret === false) {
            die('There was an error writing this file');
        }
        else {
            echo "<p>Từ $data đã được bổ sung vào csdl từ ghép</p>";
        }
    }
}

if(isset($_POST['stopword'])) {
    $data = strtolower($_POST['stopword']);
    if(trim($data) != '')
    {
        $data = "\r\n" .  $_POST['stopword'];
        $ret = file_put_contents('./output/keywords_to_remove.txt', $data, FILE_APPEND | LOCK_EX);
        if($ret === false) {
            die('There was an error writing this file');
        }
        else {
            echo "<p>Từ $data đã được bổ sung vào csdl từ khóa cần loại bỏ  </p>";
        }
    }
}
?>
