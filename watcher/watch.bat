@echo off
echo ******************************************************************
echo    SOURCE CODE WATCHER (HAML,COMPASS+SASS,LIVERELOAD)
echo ******************************************************************

start /B ruby haml_watch.rb
start /B compass watch
start /B livereload ../
start /B ncoffee -w -o=../forum/skins/poliwatch/media/js ../forum/skins/poliwatch/coffeescript
