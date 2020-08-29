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

// Read data and convert to UTF-8 
$article_file = file_get_contents('./export/article_data.json');
$article_file = mb_convert_encoding($article_file, 'HTML-ENTITIES', "UTF-8");

//echo $article_file;

$article_data = json_decode($article_file, true)['article_list'];

// Get request data
$output_data = array();
$term = mb_trim(mb_strtolower(($_GET['q'])));

// Filter data
$max_suggestion = 8;
$count = 0;
if (!empty($term))
{
	foreach($article_data as $key => $value)
	{
		$topic = mb_strtolower($value['topic']);
		if(mb_strpos($topic, $term) !== false)
		{
			array_push($output_data, array('topic'=>$value['topic'], 'newspaper'=>$value['newspaper']));
			$count=$count+1;
			if($count>$max_suggestion){
				array_push($output_data, array('topic'=>"$term", 'newspaper'=>'...Enter để xem đầy đủ kết quả...'));
				break;
			}
			//array_push($output_data, $value['topic']);
		};
	};
}


// Output json
$result = $output_data;

echo json_encode($result, JSON_UNESCAPED_UNICODE);
//
?>
