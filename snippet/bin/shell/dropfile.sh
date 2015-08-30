#!/bin/bash

#while true;do
#	read -p 'please input the directory absolute path we will serivce: ' DIRE
#	if [ -d $DIRE ];then
#		while true;do
#			read -p 'please input the postfix of the file you want delete, eg: pyc|pyo, but one at a time: ' POSTFIX
#			read -p 'are you sure? (Y|N): ' YON
#			char=`echo $YON | tr 'yn' 'YN'`
#			[ $char == 'Y' ] && break || continue
#		done
#		break
#	else
#		echo -e '\033[31mwrong input, your input is not a directory or anythine else i cannot identifiy\033[0m'
#		continue
#	fi
#done

#echo '***********************************'

function dropfile {
	for item in `ls $1`;do
		echo $1/$item | grep ".*.$POSTFIX$" &> /dev/null
		if [ -f $1/$item -a  $? -eq 0 ];then
			echo -e "\033[31mdropping the file $1/$item\033[0m"
			rm -rf $1/$item
		elif [ -d $1/$item ];then
			echo -e "\033[32mswitch directory to $1/$item\033[0m"
			dropfile $1/$item
		fi
	done
}
DIRE=$1
POSTFIX=$2

dropfile $DIRE
