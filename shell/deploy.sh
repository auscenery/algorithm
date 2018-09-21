#!/usr/bin/env bash

# function definition 1
deploy_help() {
    echo "deploy usage: ./deploy.sh -h host -u username -p project_name"
    echo "for instance: ./deploy.sh -h 127.0.0.1 -u lcj -p project_name"
    echo "define of options: "
    echo "-h | --host : host args"
    echo "-u | --username : username args"
    echo "-p | --project_name : project_name args"
    echo "--help: usage help"
    return 0
}

# function definition 1
deploy() {
    username=$1
    host=$2
    project_name=$3

    echo "current dir is "`pwd`
    
    echo ""
    
    echo "begin to deploy project:'${project_name}' to host:'${host}' by username:'${username}' :"
    
    prefix=${project_name}
    postfix='.tar.gz'

    # 压缩打包上传到服务器
    dt=`date "+%Y%m%d_%H%M%S"`
    project_tar_name="${prefix}_${dt}${postfix}"
    echo ""
    echo "1.打包项目 ${project_name} 为${project_tar_name}!"
    tar -czf ${project_tar_name} ${project_name}
    scp ${project_tar_name} ${username}@${host}:~

    # 压缩原有项目作为备份并解压上传的项目
    day=`date "+%Y%m%d"`
    tar_name="${prefix}_${day}${postfix}"
    echo ""
    s="2. 上传${project_tar_name}到username@host:${username}@${host} 并解压!"
    ssh ${username}@${host} "
    cd ~
    echo ${s}
    if [ -d ${project_name} ]; then
        tar -czf ${tar_name} ${project_name} && rm -rf ${project_name}
    fi
    tar -xzf ${project_tar_name} && rm ${project_tar_name}
    "

    # 删除本地的压缩项目包
    echo ""
    echo "3. 删除本地压缩包: ${project_tar_name}!"
    if [ -f ${project_tar_name} ]; then
        rm ${project_tar_name}
    fi

    echo ""
    echo "deploy project:'${project_name}' to host:'${host}' by username:'${username}' finished!"
}

# 采用getopt方式设计 main entry
# function definition 2
function main {
    # 处理参数
    host=""
    username=""
    project_name=""
    while getopts "h:u:p:" opt; do
        case ${opt} in
            h) host="$OPTARG";;
            u) username="$OPTARG";;
            p) project_name="$OPTARG";;
            *) deploy_help;;
        esac
    done

    # 执行参数对应的函数
    if [ -z ${host} ]; then
        echo "No host or ip specified!"
        deploy_help
        exit -1
    fi
    if [ -z ${username} ]; then
        echo "No username specified!"
        deploy_help
        exit -1
    fi
    if [ -z ${project_name} ]; then
        echo "No project_name specified!"
        deploy_help
        exit -1
    fi
    
    deploy ${username} ${host} ${project_name}

}

dir=$(dirname $0)
dir=$(cd $dir;pwd)
echo "**********************************************************************"

main "$@"

echo "**********************************************************************"
