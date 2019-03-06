#!/bin/bash
Basepath=$(cd `dirname $0`; pwd)
for Script_name in `ls ${Basepath}`
do
	if [ -f "${Basepath}/.${Script_name}" ]; then
		rm -rf ${Basepath}/.${Script_name}
	fi
done

