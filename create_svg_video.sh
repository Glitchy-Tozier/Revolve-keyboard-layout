#!/bin/sh
# create a video from the svgs in the folder svgs
# svgs to pngs
for i in svgs/*svg; do inkscape -D -z -e  $i.png -f $i; done
# create a temporary file with all pngs in reverse order
ls svgs/*png | sort -r > /tmp/pnglist.txt
# create the video
# mencoder "mf://@/tmp/pnglist.txt" -mf fps=10 -o svgs/video.avi -ovc copy
mencoder "mf://@/tmp/pnglist.txt" -mf fps=10 -o svgs/video.webm -ovc lavc -lavcopts vcodec=acodec=vorbis:vcodec=libvpx -of lavf -lavfopts format=webm -ffourcc VP80
