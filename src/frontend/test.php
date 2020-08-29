<?php
//phpinfo();
//$id = $_GET['id'] ; 
$api_url = "http://118.68.36.118:9200/docbao/_search?q=asean"; 
//$port = 9200; 
$ch = curl_init( ); 
curl_setopt ( $ch, CURLOPT_URL, $api_url ); 
//curl_setopt ( $ch, CURLOPT_PORT, $port ); 
//curl_setopt ( $ch, CURLOPT_POST, 1 ); 
curl_setopt ( $ch, CURLOPT_RETURNTRANSFER, 1 ); 
curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
// Allowing cUrl funtions 20 second to execute 
//curl_setopt ( $ch, CURLOPT_TIMEOUT, 5 ); // Waiting 20 seconds while trying to connect 
//curl_setopt ( $ch, CURLOPT_CONNECTTIMEOUT, 5 ); 
$response_string = curl_exec( $ch ); 
$httpCode=curl_getinfo($ch, CURLINFO_HTTP_CODE);

print_r($response_string);
echo $httpCode;
print curl_error($ch);
//echo $httpCode;
curl_close($ch);
?>
