==========
Father MFH
==========

Run Docker ftp containers

docker run -d \
    -p 21:21 \
    -p 21000-21010:21000-21010 \
    -e USERS="one|1234" \
    -e ADDRESS=127.0.0.1 \
    delfer/alpine-ftp-server
