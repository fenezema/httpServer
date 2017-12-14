<?php
	$fileName = $_FILES['upload']['name'];
	$tmpName = $_FILES['upload']['tmp_name'];
	$fileSize = $_FILES['upload']['size'];
	$fileType = $_FILES['upload']['type'];
	echo $_FILES["upload"]["error"];

	$fp = fopen($tmpName,'r');
	$content = fread($fp, filesize($tmpName));
							//echo $content;
	$content=addslashes($content);
	fclose($fp);

	if(!get_magic_quotes_gpc()){
		$fileName = addslashes($fileName);
	}
	move_uploaded_file($tmpName, '/home/fenezema/Documents/IsengProject/Progjar/httpServer/server/resources/'.$fileName);
?>
