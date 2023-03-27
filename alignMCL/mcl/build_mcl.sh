 DST_FOLDER=`pwd`
 tar -xvf mcl-source-12-068.tar.gz
 (cd mcl-12-068 && ./configure --prefix=$DST_FOLDER)
 (cd mcl-12-068 && make)
 (cd mcl-12-068 && make install)
 rm -frv mcl-12-068
