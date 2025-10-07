以下是一些 Linux 系统中常用的命令，按功能分类整理：

---

### **文件与目录操作**
1. **`ls`**  
   - 列出目录内容  
   - 常用选项：`-l`（详细信息）、`-a`（显示隐藏文件）、`-h`（易读大小）  
   ```bash
   ls -lah /path
   ```

2. **`cd`**  
   - 切换目录  
   ```bash
   cd /path/to/dir  # 绝对路径
   cd ..            # 返回上一级
   ```

3. **`pwd`**  
   - 显示当前工作目录路径。

4. **`mkdir`**  
   - 创建目录  
   ```bash
   mkdir dirname
   mkdir -p parent/child  # 递归创建多级目录
   ```

5. **`rm`**  
   - 删除文件或目录  
   ```bash
   rm file.txt           # 删除文件
   rm -r dirname         # 递归删除目录
   rm -f file.txt        # 强制删除（无确认）
   ```

6. **`cp`**  
   - 复制文件或目录  
   ```bash
   cp file.txt /backup/
   cp -r dir1 dir2       # 递归复制目录
   ```

7. **`mv`**  
   - 移动/重命名文件或目录  
   ```bash
   mv old.txt new.txt    # 重命名
   mv file.txt /target/  # 移动文件
   ```

8. **`touch`**  
   - 创建空文件或更新文件时间戳  
   ```bash
   touch newfile.txt
   ```

---

### **文件查看与编辑**
1. **`cat`**  
   - 查看文件内容  
   ```bash
   cat file.txt
   ```

2. **`less` / `more`**  
   - 分页查看文件（支持上下翻页）  
   ```bash
   less largefile.log
   ```

3. **`head` / `tail`**  
   - 查看文件开头/结尾部分  
   ```bash
   head -n 10 file.txt    # 前10行
   tail -f logfile.log    # 实时追踪日志
   ```

4. **`grep`**  
   - 文本搜索工具  
   ```bash
   grep "error" log.txt   # 搜索包含"error"的行
   grep -r "pattern" /dir # 递归搜索目录
   ```

5. **`vim` / `nano`**  
   - 命令行文本编辑器  
   ```bash
   vim file.txt
   nano file.txt
   ```

---

### **权限与用户管理**
1. **`chmod`**  
   - 修改文件权限  
   ```bash
   chmod 755 script.sh    # rwxr-xr-x
   chmod +x script.sh     # 添加执行权限
   ```

2. **`chown`**  
   - 修改文件所有者  
   ```bash
   chown user:group file.txt
   ```

3. **`sudo`**  
   - 以超级用户权限执行命令  
   ```bash
   sudo apt update
   ```

4. **`passwd`**  
   - 修改用户密码  
   ```bash
   passwd username
   ```

---

### **系统信息与监控**
1. **`df`**  
   - 查看磁盘空间使用情况  
   ```bash
   df -h  # 易读格式
   ```

2. **`du`**  
   - 查看目录/文件占用空间  
   ```bash
   du -sh /path
   ```

3. **`top` / `htop`**  
   - 实时监控系统进程和资源占用。

4. **`ps`**  
   - 查看进程状态  
   ```bash
   ps aux | grep nginx
   ```

5. **`free`**  
   - 查看内存使用情况  
   ```bash
   free -h
   ```

6. **`uname`**  
   - 显示系统信息  
   ```bash
   uname -a  # 内核版本等
   ```

---

### **网络相关**
1. **`ping`**  
   - 测试网络连通性  
   ```bash
   ping example.com
   ```

2. **`curl` / `wget`**  
   - 下载文件或访问网页  
   ```bash
   curl -O https://example.com/file.zip
   wget https://example.com/file.zip
   ```

3. **`netstat` / `ss`**  
   - 查看网络连接和端口  
   ```bash
   netstat -tulnp
   ss -tulnp
   ```

4. **`ifconfig` / `ip`**  
   - 查看或配置网络接口  
   ```bash
   ip addr show
   ```

---

### **压缩与归档**
1. **`tar`**  
   - 打包/解压文件  
   ```bash
   tar -czvf archive.tar.gz /dir  # 压缩
   tar -xzvf archive.tar.gz       # 解压
   ```

2. **`gzip` / `gunzip`**  
   - 压缩/解压 `.gz` 文件  
   ```bash
   gzip file.txt
   gunzip file.txt.gz
   ```

3. **`zip` / `unzip`**  
   - 处理 `.zip` 文件  
   ```bash
   zip archive.zip file.txt
   unzip archive.zip
   ```

---

### **包管理（示例）**
- **Debian/Ubuntu (APT)**  
  ```bash
  sudo apt update          # 更新软件列表
  sudo apt install package # 安装软件
  sudo apt remove package  # 卸载软件
  ```

- **CentOS/RHEL (YUM/DNF)**  
  ```bash
  sudo yum install package
  sudo dnf remove package
  ```

---

### **其他实用命令**
1. **`find`**  
   - 搜索文件  
   ```bash
   find /path -name "*.log"
   ```

2. **`scp`**  
   - 安全复制文件（远程）  
   ```bash
   scp file.txt user@remote:/path
   ```

3. **`alias`**  
   - 创建命令别名  
   ```bash
   alias ll='ls -lah'
   ```

4. **`history`**  
   - 查看命令历史记录。

5. **`man`**  
   - 查看命令手册  
   ```bash
   man ls
   ```

---

这些命令覆盖了大部分日常操作需求，建议结合 `--help` 或 `man` 查阅详细用法。根据不同的 Linux 发行版，部分命令可能需要安装或略有差异。