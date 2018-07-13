#!/bin/sh

d=`pwd`
d=`basename $d`

cat >.build.sh <<EOF
#!/bin/sh
cd /app/$d
make -f ../Makefile.slides
EOF

chmod a+x .build.sh

cd ..
docker run -t -i -v`pwd`:/app benlangmead/fedora-cpp-slides /app/$d/.build.sh
cd $d

rm -f .build.sh
