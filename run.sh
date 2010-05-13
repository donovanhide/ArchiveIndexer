cd `dirname $0`
export CLASSPATH=./Lib/*
java -Xmx1024m -jar archiveindexer.jar  $@