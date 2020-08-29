<?php
ini_set("include_path", '/home/tudongh1/php:' . ini_get("include_path") );
require_once 'HTTP/Request2.php';

date_default_timezone_set("Asia/Bangkok");

$request = new HTTP_Request2('http://jsonplaceholder.typicode.com/todos/1', HTTP_Request2::METHOD_GET);
try {
$response = $request->send();
if (200 == $response->getStatus()) 
{
echo $response->getBody();
} 
else 
{
echo 'Unexpected HTTP status: ' . $response->getStatus() . ' ' .$response->getReasonPhrase();
}

} catch (HTTP_Request2_Exception $e) 
{
echo 'Error: ' . $e->getMessage();
}
?>
