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
define("PHOTOS_LOCAL", "../../examples/sorted_photos");

// Path to the photos directory on the web
define("PHOTOS_WEB", "http://qrphotos");

// Site title
define("TITLE", "QrPortrait");

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
            
                #container
                {
                    width:800px;
                    position:absolute;
                    left:50%;
                    margin-left:-400px;
                    border: 1px solid black;
                }
                
                #title h1
                {
                    margin-left:50px;
                    margin-top: 20px;
                }
                
                #form
                {
                    padding: 20px 20px 20px 20px;
                }
            
        </style>
        
    </head>
    
    <body>
        <?php
        /////
        // Greeting page
        ///
        
        if(!$_GET['serial']){
        ?>
        <div id = "container">
            <div id="title">
                <h1><?php echo TITLE; ?></h1>
            </div>
            
            <div id="form">
                <form method="get" action="<?php echo $_SERVER['REQUEST_URI']; ?>">
                    <label for="serial">Enter your code to view your photos:</label>
                    <input type="text" name="serial" id="serial" />
                    <input type="submit" value="View photos" />
                </form>
            </div>
        </div>
        
        <?php
        }
        ?>
    </body>
</html>
