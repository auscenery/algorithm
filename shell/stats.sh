#!/usr/bin/env bash

# return vs exit 
# https://stackoverflow.com/questions/4419952/difference-between-return-and-exit-in-bash-functions

function stats_help() {
    echo "stats usage: ./stats_file_count.sh -d n -p directory_path"
    echo "for example: ./stats_file_count.sh -d 1 -p /home/lcj/test"
    echo "define of options: "
    echo "-d | --depth : depth path args"
    echo "-p | --directory_path : directory path args"
    echo "--help: usage help"
    return 0
}

function get_absolute_path() {
    local directory_path=$1
    directory_path=`cd ${directory_path};pwd`
    echo ${directory_path}
}

function get_directory_list() {
    local path=$1
    local dirs=''
    if [ -d $path ]
    then
        cd $path
        dirs=`ls -l | awk '/^d/ {print $NF}'`
    fi
    echo $dirs
}

function do_stats_directory_file_count() {
    local directory_path=$(get_absolute_path $1)
    local dir_name=`basename ${directory_path}`
    cd ${directory_path}/../

    if [ -d ${directory_name} ]
    then
        total_cmd=`ls -lR ${dir_name}|grep '^-'|wc -l`
        # 转为整数, 否则数字前面有空格
        total_number=$[total_cmd]
        echo "'${directory_path}': ${total_number}"
    #else
    #    echo "${directory_path} doesn't exist or is not directory!"
    fi
}

# 根据深度统计, 递归时，需要将变量置为local，默认变量为global，否则递归返回时，变量值没有恢复导致失败
function stats_by_depth() {
    local max_depth=$1
    local path=$2
    local current_depth=$3
    local next_depth=$[$current_depth + 1]

    #首先打印当前目录的统计结果
    local absolute_path=$(get_absolute_path $path)
    local prefix=''
    local i
    for i in {0..$current_depth}
    do
        prefix="${prefix}---"  
    done
    #absolute_path=`get_absolute_path $path`
    local results=$(do_stats_directory_file_count $absolute_path)
    local j=2
    while [ $j -le $current_depth ]
    do
        echo -n "   "
        j=$[j + 1]
    done
    echo "${prefix}>${results}"

    #然后遍历其子目录并递归调用
    local dirs=$(get_directory_list ${absolute_path})
    if [ -n "$dirs" ]
    then
        # 遍历子目录统计结果
        if [ $next_depth -le $max_depth ]
        then
            local temp_prefix=''
            for dir in $dirs
            do
                local sub_dir="${absolute_path}/${dir}"
                # 递归调用
                stats_by_depth $max_depth $sub_dir $next_depth
            done
        fi
    fi
}

# 采用getopt方式设计 main entry
# function definition 2
function main {
    # 处理参数
    directory_path=""
    while getopts "d:p:" opt; do
        case ${opt} in
            d) depth="$OPTARG"
                ;;
            p) directory_path="$OPTARG"
                ;;
            *) stats_help
               return -1
               ;;
        esac
    done

    # 执行参数对应的函数
    if [ -z ${directory_path} ]; then
        echo "No directory_path specified!"
        stats_help
        return -1
    fi
    
    if [[ -z ${depth} || ${depth} -lt 0 ]]; then
        echo "No depth specified, or depth <= 0!"
        stats_help
        return -1
    fi

    start_depth=1
    prefix=""
    stats_by_depth ${depth} ${directory_path} ${start_depth} ${prefix}
}

echo "**********************************************************************"
main "$@"
echo "**********************************************************************"
