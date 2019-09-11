#!/bin/bash
SHELL_FOLDER=$(dirname $(readlink -f "$0"))

ARGS="--recursive --linelength=120"
ARGS="${ARGS} --filter=-runtime/int"

SAVED_FILENAME="cpplint_detail.txt"
XLS_FILENAME="cpplint.xls"

python ${SHELL_FOLDER}/cpplint.py ${ARGS} --root=include include 2> ${SAVED_FILENAME}
python ${SHELL_FOLDER}/cpplint.py ${ARGS} src 2>> ${SAVED_FILENAME}

# 生成Excel报告
echo "Generate ${XLS_FILENAME}"
python ${SHELL_FOLDER}/gen_xls.py ${SAVED_FILENAME} ${XLS_FILENAME}
rm -rf ${SAVED_FILENAME}
