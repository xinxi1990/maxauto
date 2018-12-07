#!/usr/bin/env bash
getact(){
	currentact="null"
	currentact=`adb -s ${adbdevices} shell dumpsys activity | grep mFocusedActivity`
	currentact=`echo ${currentact}| cut -d"/" -f2 | cut -d" " -f1`
	echo "当前Activity:"${currentact}
}

# 获取app进程pid
findapppid(){
	pid=`adb -s ${adbdevices} shell ps | grep ${app_name} | awk '{print $2}'`
	echo "app pid is:"${pid}

}

# 获取cpu使用率
getcpu(){
	findapppid
	#cpu=0
	info=`adb -s ${adbdevices} shell dumpsys cpuinfo | grep ${pid}`
	cpu=`echo ${info} | cut -d" " -f1 | cut -d"%" -f1`

	if [[ ${cpu} = "" ]]; then
		echo "当前cpu:0"
		echo ${time}",""0"","${currentact} >>${cpulog}

	else
		result=$(echo ${cpu} | grep "+")

		if [[ "${result}" != "" ]]; then
			cpu=`echo ${cpu} | cut -d"+" -f2`
			echo "当前cpu:"${cpu}
			echo ${time}","${cpu}","${currentact} >>${cpulog}
		else
			echo "当前cpu:"${cpu}
			echo ${time}","${cpu}","${currentact} >>${cpulog}
		fi
	fi

}

# 获取内存使用情况
getmem(){
	findapppid
	#mem=0
	info=`adb -s ${adbdevices} shell dumpsys meminfo | grep ${pid}`
	mem=`echo ${info} | cut -d":" -f1 | cut -d"K" -f1`
	mem1=`echo ${mem} | cut -d"," -f1`
	mem2=`echo ${mem} | cut -d"," -f2`
	mem=${mem1}${mem2}
	mem=`awk 'BEGIN{printf "%0.2f","'$mem'"/"'1024'"}'` #%0.2f小数点后位数

	if [[ ${mem} = "" ]]; then
		echo "当前内存:0"
		echo ${time}","0","${currentact} >>${memlog}
	else
		echo "当前内存:"${mem}
		echo ${time}","${mem}","${currentact} >>${memlog}

	fi
}

# 获取页面展示时间
#getpage(){
#	findapppid
#	info_result=`adb logcat -d | grep -i activitymanager.*Displayed`
#
#	for info in "${info_result[*]}";
#    do
#        echo ${info} | awk 'BEGIN{RS="ms"}{print $1}'
#    done

#	page=`echo ${info} | cut -d":" -f4 | cut -d"/" -f2`
#	time_org=`echo ${info} | cut -d":" -f5 | cut -d" " -f2`
#	time_start=`echo ${time_org##+}`
#	page_time=`echo ${time_start%ms}`
#	if [[ ${page_time} = "" ]]; then
#	    echo "当前"${page}"展示时间:"${page_time}
#		echo ${time}","0","${page} >>${pagelog}
#	else
#		echo "当前"${page}"展示时间:"${page_time}
#		echo ${time}","${page_time}","${page} >>${pagelog}
#	fi
#}



task(){
	adbdevices="$1" # 设备号
	performancefolder="$2" # 性能保存文件夹
	app_name="$3" # app包名
	cpulog=${performancefolder}"/cpu.log" # cpu保存路径
	memlog=${performancefolder}"/mem.log" # 内存保存路径
	#echo "cpu数据保存路径:"${cpulog}
	#echo "mem数据保存路径:"${memlog}
	#echo "开始获取性能"
	time=$(date "+%Y-%m-%d %H:%M:%S")
	#echo "获取性能时间:"${time}
	getact
	getcpu
	getmem
}

task $1 $2




