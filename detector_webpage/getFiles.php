<?php

function listFolders($cwd){
    $dir = join(DIRECTORY_SEPARATOR, [$cwd, 'datasets', $_REQUEST['set_type']]);
    $files = scandir($dir);
    // $count = 0;
    // $totalCount;
    // echo "testpoop";
    echo "[";
    $first = false;
    foreach($files as $file) {
      if (!is_dir($file) && $file[0] != '.') {
        if ($first) {
          echo ",";
        }
        else {
          $first = true;
        }
        echo "\"$file\"";
      }
      // use file_get_contents($file) to read link of alias... also put (mime_content_type($file) == "application/octet-stream" || in if statement
    }
    echo "]";
}
listFolders(getcwd());
?>