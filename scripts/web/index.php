<?php
/*
 * Copyright (c) 2012 Robert Bieber
 *
 * This program is free software; you can redistribute it and/or modify it under
 * the terms of the GNU General Public License as published by the Free Software
 * Foundation; either version 3 of the License, or (at your option) any later
 * version.
 *
 * This program is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
 * details.
 *
 * You should have received a copy of the GNU General Public License along with
 * this program; if not, write to the Free Software Foundation, Inc., 59 Temple
 * Place, Suite 330, Boston, MA  02111-1307  USA
 */

/////
// User Constants
///

// Path to the photos directory on local server
// Ensure that the server has write access for thumbnails
define("PHOTOS_LOCAL", "../../examples/sorted_photos");

// Path to the photos directory on the web
define("PHOTOS_WEB", "http://qrphotos");

// Site title
define("TITLE", "QrPortrait");

// Thumbnail dimension (fits into square frame)
define("THUMBSIZE", 300);
define("PAGEWIDTH", 800);

/////
// Reused elements
///

$formCode = <<<EOD
            <div id="form">
                <form method="get" 
                      action="{$_SERVER['REQUEST_URI']}">
                    <label for="serial">
                        Enter your code to view your photos:
                    </label>
                    <input type="text" name="serial" id="serial" />
                    <input type="submit" value="View photos" />
                </form>
            </div>
EOD;

/////
// Common header info
///

?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
 "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">

    <head>
<?php if($_GET['serial']){ ?>
        <title><?php echo TITLE; ?>: View Photos</title>
<?php }else{ ?>
        <title><?php echo TITLE; ?></title>
<?php } ?>
        
        <style type="text/css">
                
                body
                {
                    background-color:#f2f2f2;
                }
                
                #container
                {
                    width:800px;
                    position:absolute;
                    left:50%;
                    margin-left:-400px;
                    border:1px solid black;
                    background-color:white;
                }
                
                #title h1
                {
                    margin-left:50px;
                    margin-top:20px;
                }
                
                #form
                {
                    margin-left:50px;
                    padding:20px 20px 20px 20px;
                }
                
                ul.photos
                {
                    padding:0;
                    list-style:none;
                    margin:0px auto 0;
                    width:700px;
                }
                
                li.photo
                {
                    list-style:none;
                    float:left;
                    padding:0;
                    margin: 30px 25px 0px 25px;
                }
                
                li.photo a
                {
                    display:block;
                    width:300px;
                    height:300px;
                    padding:none;
                    margin:none;
                    text-align:center;
                }
                
                li.photo img
                {
                    margin:0 auto;
                    text-align:center;
                }
                
                p
                {
                    margin-left:50px;
                    margin-top:50px;
                }
            
        </style>
        
    </head>
    
    <body>
        <div id = "container">
<?php
            /////
            // Greeting page
            ///
            
            if(!$_GET['serial']){
            ?>

            <div id="title">
                <h1><?php echo TITLE; ?></h1>
            </div>
            
<?php echo $formCode; ?>

        
<?php
            }
            else
            {
                // Determining whether the code exists
                $validCode = false;
                foreach(scandir(PHOTOS_LOCAL) as $entry)
                {
                    if($entry == '.' || $entry == '..')
                        continue;
                    
                    if(strtoupper(trim($entry)) 
                       == strtoupper(trim($_GET['serial'])))
                        $validCode = true;
                }
                
                // If the code does exist, display the images
                if($validCode)
                {
                    $files = scandir(PHOTOS_LOCAL . '/' 
                                     . trim(strtoupper($_GET['serial'])));
                    $fileURIs = array();
                    foreach($files as $k => $v)
                    {
                        $info = pathinfo($v);

                        if($v == '.' || $v == '..' 
                           || substr($info['filename'], -5) == 'thumb')
                            continue;
                        
                        $photoPath = PHOTOS_LOCAL . '/'
                                     . trim(strtoupper($_GET['serial']))
                                     . '/' . $v;    
                        $thumbPath = PHOTOS_LOCAL . '/' 
                                     . trim(strtoupper($_GET['serial'])) 
                                     . '/' . $info['filename'] . '_thumb.' 
                                     . $info['extension'];
                        if(!file_exists($thumbPath))
                        {
                            // If the thumbnail doesn't exist, create one
                            $orig = imagecreatefromjpeg($photoPath);
                            
                            // Calculating new dimensions
                            $sw = imagesx($orig);
                            $sh = imagesy($orig);
                            $dw = 0;
                            $dh = 0;
                            
                            if($sw > $sh)
                            {
                                $dw = THUMBSIZE;
                                $dh = THUMBSIZE * $sh / $sw;
                            }
                            else
                            {
                                $dh = THUMBSIZE;
                                $dw = THUMBSIZE * $sw / $sh;
                            }
                            
                            // Allocating the new image and resizing
                            $dest = imagecreatetruecolor($dw, $dh);
                            imagecopyresized($dest, $orig, 
                                             0, 0, 0, 0, 
                                             $dw, $dh, $sw, $sh);
                            
                            // Saving and freeing memory
                            imagejpeg($dest, $thumbPath);
                            imagedestroy($orig);
                            imagedestroy($dest);
                           
                        }

                        // Storing image and thumb location
                        $photoWebPath = PHOTOS_WEB . '/'
                                        . strtoupper(trim($_GET['serial']))
                                        . '/' . $v;
                        $thumbWebPath = PHOTOS_WEB . '/' 
                                        . strtoupper(trim($_GET['serial']))
                                        . '/' . $info['filename'] . '_thumb.'
                                        . $info['extension'];
                                        
                        if(substr($v, 0, 5) != "index" || $_GET['index'])
                            $fileURIs[$k] = array('photo' => $photoWebPath,
                                                  'thumb' => $thumbWebPath);
                    }
                    /////
                    // Image display
                    ///
                    
                ?>
            <div id="title">
                <h1><?php echo TITLE; ?></h1>
            </div>
            
            <p>
                To view a photo, click on it.  To save, right-click on an image 
                and choose "save link as."
            </p> 
            
            <ul id="photos">
<?php foreach($fileURIs as $file){ ?>
                <li class="photo">
                    <a href="<?php echo $file['photo']; ?>">
                        <img src="<?php echo $file['thumb']; ?>" alt="Photo" />
                    </a>
                </li>
<?php } ?>
            </ul>
            
<?php
                }else{
                    /////
                    // Code not found error page
                    ///
                ?>
            <div id="title">
                <h1><?php echo TITLE; ?></h1>
            </div>
            
            <p>
                Sorry, we couldn't find any photos that matched your code.  
                Double check your card and try entering it again.
            </p>
            
<?php echo $formCode; ?>
<?php           }
            }
            ?>
        </div> 
    </body>
</html>
