#!/bin/sh

if [ ! -n "$1" ]
then
    echo "no argument"
    exit
else
    echo "libsvm start"
fi

#$1/svm-scale -l 0 -u 1 libsvm_train.txt > libsvm_train_scale.txt
#$1/svm-scale -l 0 -u 1 libsvm_test.txt > libsvm_test_scale.txt

$1/svm-train -t 2 -c 80 libsvm_train_scale.txt

$1/svm-predict libsvm_test_scale.txt libsvm_train_scale.txt.model libsvm_out.txt
