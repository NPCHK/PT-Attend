#!/bin/bash
Basepath=$(cd `dirname $0`; pwd)

tried=0
for Script_name in `ls -r ${Basepath}`
do
	if [ ! -f "${Basepath}/.${Script_name}" ]; then
		((tried=tried+1))
		${Basepath}/${Script_name} >> ${Basepath}/../log
	fi
done

if [ ! "${tried}" = "0" ]; then
	TimeNow=$(date "+%Y-%m-%d %H:%M:%S")
	echo "=================" >> ${Basepath}/../log
	echo "Tried ${tried} time(s) at ${TimeNow}" >> ${Basepath}/../log
fi
