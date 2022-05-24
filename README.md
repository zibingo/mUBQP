# mUBQP算法

<iframe height=498 width=510 src="./MOEAD演示.mp4">

## 环境搭建(必须)

### Centos 7.6安装python3、更新pip、安装依赖包

```sh
yum install python3 -y
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

## 在linux上测试数据集(可选)

### centos7.6安装g++ version 9+

```sh
yum install -y centos-release-scl
yum install -y devtoolset-9-gcc devtoolset-9-gcc-c++ devtoolset-9-binutils
echo "source /opt/rh/devtoolset-9/enable" >>/etc/profile
reboot
```

### 安装腾讯云COFS工具

> 我的数据集保存在腾讯云对象存储上，方便迁移
>
> 不需要的可以不搞

```sh
sudo yum install libxml2-devel libcurl-devel -y
wget https://github.com/tencentyun/cosfs/releases/download/v1.0.19/cosfs-1.0.19-centos7.0.x86_64.rpm
sudo rpm -ivh cosfs-1.0.19-centos7.0.x86_64.rpm  --force
```

### 挂载数据集

> 输入BucketName-APPID、SecretId、SecretKey

```sh
echo <BucketName-APPID>:<SecretId>:<SecretKey> > /etc/passwd-cosfs

Mkdir ./cofs

cosfs BucketName-APPID ./cofs/ -ourl=http://cos.ap-guangzhou.myqcloud.com -odbglevel=info -oallow_other
```

## 运行测试集

### python版本

- Two.py    目标函数数量m=2
- Three.py 目标函数数量m=3

#### 参数设置

![](https://blogphoto-1.oss-cn-shenzhen.aliyuncs.com/jietu/image-20220510200147344.png)

#### 运行

```sh
python3 Two.py
```

### C++版本

- m=2.cpp    目标函数数量m=2
- m=2.cpp  目标函数数量m=3

#### 参数设置（从命令行传参数）

![](https://blogphoto-1.oss-cn-shenzhen.aliyuncs.com/jietu/image-20220510202421095.png)

#### 运行

```sh
g++ m=2.cpp && ./a.out 上面八个参数(空格隔开)
```

### 批量运行参数设置（单进程）

> 修改AutoRun.py

![](https://blogphoto-1.oss-cn-shenzhen.aliyuncs.com/jietu/image-20220510204432472.png)

#### linux环境下后台运行

```sh
sh AutoRun.sh
```

