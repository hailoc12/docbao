<?php
//header('Content-Type: text/html; charset=utf-8');
// Display all errors
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

// Use UTF-8
mb_internal_encoding("UTF-8");

function mb_trim($string, $charlist = null) 
{
	if (is_null($charlist)) 
	{
		return trim($string);
	} 
	else 
	{
		$charlist = preg_quote($charlist, '/');
		return preg_replace("/(^[$charlist]+)|([$charlist]+$)/us", '', $string);
	}
}


// Build query string  
//
//
$term = $_GET['q'];
$term_count = intval($_GET['length']);

if($term_count===1)
{
$param = '
{
  "query": 
  {
    "wildcard":
    {
      "topic":'.'"'.$term.'*" 
    }
  },
  "size": "10",
  "_source":{
       "includes": ["topic", "newspaper"]
	         }
}
	';
}
else
{
$param = '
{
  "query": 
  {
    "match_phrase":
    {
      "topic":'.'"'.$term.'" 
    }
  },
  "size": "10",
  "_source":{
       "includes": ["topic", "newspaper"]
	         }
}
	';

}
//echo $param;

$header = array(
	    "content-type: application/json; charset=UTF-8"
		);

$curl = curl_init();
curl_setopt($curl, CURLOPT_URL, "http://hailocworkstation.ddns.net:21/docbao_pvn/_search");
curl_setopt($curl, CURLOPT_HTTPHEADER, $header);
curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($curl, CURLOPT_POSTFIELDS, $param);

$es_result = curl_exec($curl);
curl_close($curl);


// Read data and convert to UTF-8 
//$es_result = file_get_contents("http://hailocworkstation.ddns.net:21");
//echo $es_result;
#$es_result = mb_convert_encoding($es_result, 'HTML-ENTITIES', "UTF-8");


//echo $article_file;

$es_result = json_decode($es_result, true)['hits']['hits'];

$article_data = array();
foreach($es_result as $key => $value)
{
	array_push($article_data, $value['_source']);
}


// Output json
$result = $article_data;

echo json_encode($result, JSON_UNESCAPED_UNICODE);
?>

