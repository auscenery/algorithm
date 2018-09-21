#! /bin/bash

# @description 创建新用户
# @param host_ip string 主机ip
# @param admin_name string 管理员名称
# @param sk_file_path string  管理员对应的ssh 私钥文件绝对路径
# @param username string 管理员待创建的新用户名
# @param pk_file_path string 待创建的新用户最近用ssh-keygen生成的私钥文件，copy的副本存放在管理员电脑的绝对路径
# @param root_flag int value: should be 0 or 1, 1：sudo 权限用户 0：普通用户
# 调用形式为：create_user host_ip admin_name sk_file_path username pk_file_path root_flag
# 注意顺序不能错
function create_user() {
    # 机器ip
    host_ip=$1
    # 管理员用户名
    admin_name=$2
    # 秘钥文件路径
    sk_file_path=$3
    # 新创建的用户名
    new_username=$4
    # 新用户所在机器对应的公钥文件， 通过ssh-keygen生成
    pk_file_path=$5
    # root_flag
    root_flag=$6
    
    # 第一步创建新用户
    ssh -i ${sk_file_path} ${admin_name}@${host_ip} "
        sudo useradd -m -d /home/${new_username} -s /bin/bash ${new_username}
    "

    # 第二步，上传公钥文件
    scp -i ${sk_file_path} ${pk_file_path} ${admin_name}@${host_ip}:/tmp/id_rsa.pub

    # 第三步，创建.ssh目录，并将id_rsa.pub的内容复制到.ssh/authorized_keys文件，并修改权限，以便不用密码可以登录
    ssh -i ${sk_file_path} ${admin_name}@${host_ip} "
        sudo mkdir -p /home/${new_username}/.ssh
        sudo chmod -R o+rwx /home/${new_username}/.ssh
        sudo mv -vf /tmp/id_rsa.pub /home/${new_username}/.ssh/authorized_keys
        sudo chmod -R 700 /home/${new_username}/.ssh
        sudo chmod 600 /home/${new_username}/.ssh/authorized_keys 
        sudo chown -R ${new_username}:${new_username} /home/${new_username}/.ssh
    "

    # 第四步，若为1， 置为超级用户
    if (( ${root_flag} == 1 ))
    then
        ssh -i ${sk_file_path} ${admin_name}@${host_ip} "
            sudo echo '${new_username} ALL=(ALL) NOPASSWD:ALL' > /tmp/${new_username}
            sudo mv -vf /tmp/${new_username} /etc/sudoers.d/${new_username}
            sudo chown -R root:root /etc/sudoers.d/${new_username}
        "
    fi
}

# 创建用户提示信息
function help() {
    echo "deploy usage: bash create_new_user.sh -h host -a adminname -s sk_file_path -u new_username -p pk_file_path [-r root_flag]"
    echo "define of options: "
    echo "-i | --host : host ip args"
    echo "-a | --admin : admin username args"
    echo "-s | --secret : admin's secret key file (created by ssh-keygen) path args"
    echo "-u | --username : new username (to be created) args"
    echo "-p | --public : the new user's local public key file (sent to the admin by himself) path args"
    echo "-r | --root: the root flag (to indicate the new user whether has root privilege or not) args"
    echo "-h | --help: usage help"
    return 0
}


# 采用getopt方式设计 main entry
function main {
    # 处理参数
    # 默认为0， 意味着普通用户， 若为1为root权限用户
    root_flag=0
    while getopts "i:a:s:u:p:r:h" opt; do
        case ${opt} in
            i) host_ip="$OPTARG"
                ;;
            a) admin_name="$OPTARG"
                ;;
            s) sk_file_path="$OPTARG"
                ;;
            u) username="$OPTARG"
                ;;
            p) pk_file_path="$OPTARG"
                ;;
            r) declare -i root_flag="$OPTARG"
                ;;
            h) help
               return 0
               ;;
            *) help
               echo "invalid option set, exit!"
               return -1
               ;;
        esac
    done

    # 执行参数对应的函数
    if [ -z ${host_ip} ]
    then
        echo "No directory_path specified!"
        help
        return -1
    fi
    
    if [ -z ${admin_name} ]
    then
        echo "No admin username specified!"
        help
        return -1
    fi

    if [ -z ${sk_file_path} ] && [ -f ${sk_file_path} ]
    then
        echo "No secret key file local path specified or the file doesn't exist!"
        help
        return -1
    fi
    
    if [ -z ${pk_file_path} ] && [ -f ${pk_file_path} ]
    then
        echo "No public key file local path specified or the file doesn't exist!"
        help
        return -1
    fi

    if [ -z ${username} ]
    then
        echo "No new username specified!"
        help
        return -1
    fi

    if (( ${root_flag} != 0 && ${root_flag} != 1 ))
    then
        echo "root flag is should be equal to 0 or 1, not ${root_flag}!"
        help
        return -1 
    fi

    create_user ${host_ip} ${admin_name} ${sk_file_path} ${username} ${pk_file_path} ${root_flag}
}

echo "**********************************************************************"
main "$@"
echo "**********************************************************************"