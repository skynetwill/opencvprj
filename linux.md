这份Linux入门教程旨在帮你系统性地建立基础，并通过实践快速上手。学习路线核心路径整理如下面的表格。

| 学习阶段 | 核心目标 | 关键内容/行动建议 |
| :--- | :--- | :--- |
| **起步准备 (1-3天)** | 搭建可操作的Linux环境，建立直观认识。 | 选择Ubuntu等新手友好发行版；使用虚拟机（如VirtualBox）或云服务器安装。 |
| **基础命令 (1-2周)** | 掌握通过命令行与系统交互的核心技能。 | 每日练习`ls`, `cd`, `cp`, `mv`, `rm`, `grep`, `chmod`等高频命令。 |
| **系统管理入门 (1-2周)** | 理解并管理系统的核心组件：用户、权限和进程。 | 学习用户/组管理（`sudo`）、文件权限（`chmod`）、进程查看（`ps`, `top`）和软件安装（`apt`）。 |
| **实战与进阶 (持续)** | 将技能应用于实际场景，提升效率并探索方向。 | 编写Shell脚本自动化任务；学习使用文本编辑器（如`vim`）；搭建基础服务。 |

详细展开每个阶段的学习内容。

### 💻 第一步：起步准备 - 获取你的Linux环境

对于初学者，最推荐的方式是通过**虚拟机**安装，这样可以在你现有的Windows或macOS系统中安全地体验Linux，不会影响原有系统。

1.  **选择发行版**：建议从 **Ubuntu** 或 **Linux Mint** 开始，它们对新手非常友好，拥有庞大的社区和丰富的文档。
2.  **安装虚拟机**：
3.  **替代方案**：如果你希望直接体验更接近生产环境的Linux，可以注册阿里云、腾讯云等厂商的账号，通常有新用户免费试用期的云服务器。

安装成功后，打开终端（通常在桌面右键菜单或应用程序列表中能找到），你就可以开始输入命令了。

### 🧠 第二步：掌握核心命令 - 与系统对话

Linux的精髓在于命令行。下表汇总了最常用和关键的命令，建议你**在终端中亲自输入每一条命令并观察结果**。

| 命令 | 功能说明 | 常用示例与备注 |
| :--- | :--- | :--- |
| **`ls`** | 列出目录内容。 | `ls -l`：以详细信息列表格式显示。`ls -a`：显示所有文件（包括隐藏文件）。 |
| **`cd`** | 切换当前目录。 | `cd /home`：进入绝对路径。`cd ..`：返回上一级目录。`cd` 或 `cd ~`：直接回到用户主目录。 |
| **`pwd`** | 显示当前所在目录的绝对路径。 | |
| **`mkdir`** | 创建新目录。 | `mkdir new_folder`。 |
| **`touch`** | 创建空文件。 | `touch newfile.txt`。 |
| **`cp`** | 复制文件或目录。 | `cp file1.txt file2.txt`：复制文件。`cp -r dir1 dir2`：递归（-r recursive递归的）复制整个目录。 |
| **`mv`** | 移动或重命名文件/目录。 | `mv old.txt new.txt`（重命名）。`mv file.txt /tmp/`（移动）。 |
| **`rm`** | **删除**文件或目录。 | `rm file.txt`：删除文件。`rm -r folder_name`：递归删除目录。**⚠️ 注意：`rm`命令删除后不易恢复，使用需谨慎！** |
| **`cat`** | 查看整个文件内容。 | `cat my_file.txt`。 |
| **`grep`** | 在文件中搜索特定文本。 | `grep "error" log.txt`：在log.txt中查找包含"error"的行。 |
| **`chmod`** | 修改文件或目录的权限。 | `chmod +x script.sh`：给script.sh增加可执行权限。 |

Linux文件目录结构。核心目录的概览整理成下面的表格。

| 目录路径 | 核心用途与说明 |
| :--- | :--- |
| **`/`** | **根目录**，是整个文件系统层级的起点，所有其他目录和文件都位于其下 。 |
| **`/bin`** | 存放**基础的用户命令**（二进制可执行文件），如 `ls`, `cp`, `mv`, `cat` 等，这些是系统启动和修复所必需的命令 。 |
| **`/etc`** | 存放**系统-wide 的配置文件**，例如用户账户、网络设置、各种服务的配置等 。 |
| **`/home`** | **普通用户的主目录**。每个用户通常在此拥有一个以用户名命名的子目录（如 `/home/alice`），用于存放个人文件和配置 。 |
| **`/root`** | **系统管理员（root 用户）的主目录**，与普通用户的 `/home` 分离 。 |
| **`/tmp`** | 存放**临时文件**，所有用户均可读写。系统重启时，此目录下的文件通常会被清理 。 |
| **`/usr`** | 存放**用户安装的应用程序和文件**，包含多个子目录，如 `/usr/bin`（用户程序）、`/usr/lib`（程序库文件）等 。 |
| **`/var`** | 存放**经常变化的（Variable）数据**，如系统日志（`/var/log`）、缓存文件、邮件队列等 。 |
| **`/boot`** | 存放**系统启动引导程序和内核文件** 。 |
| **`/dev`** | 存放**设备文件**，Linux 系统将硬件设备（如硬盘、USB）抽象为文件在此管理 。 |
| **`/lib`** | 存放**系统运行时所需的共享库文件和内核模块**，为 `/bin` 和 `/sbin` 中的命令提供支持 。 |
| **`/mnt`** | 用于**临时挂载文件系统**的目录，例如挂载 U 盘或光盘等 。 |
| **`/opt`** | 用于安装**附加的或第三方可选软件包** 。 |
| **`/proc`** | 一个**虚拟文件系统**，它不占用磁盘空间，而是以文件形式提供当前系统内核和进程的运行信息 。 |
| **`/sbin`** | 存放**系统管理员使用的二进制可执行文件**，多为系统启动、修复和恢复所需的命令（如 `fsck`, `reboot`） 。 |

### ⚙️ 第三步：系统管理入门

当你能自如地操作文件后，就需要开始理解如何管理系统本身。

1.  **用户与权限**：Linux有严格的权限管理，这是系统安全的基础。
    *   **`sudo`**：这个命令允许普通用户以超级管理员（root）的身份执行命令，用于安装软件或修改系统配置。
    *   **权限管理**：使用 `chmod` 可以修改文件的访问权限（读r=4、写w=2、执行x=1），例如 `chmod 755 my_script.sh` 表示所有者可读、写、执行，组用户和其他用户可读和执行。
2.  **进程与软件管理**：
    *   **查看进程**：`ps aux` 或 `top` 命令可以查看当前系统中正在运行的所有进程及其资源占用情况。
    *   **安装软件**：在Ubuntu/Debian系统上，使用 `sudo apt update` 更新软件源列表，然后使用 `sudo apt install package_name`（如 `sudo apt install vim`）来安装软件，非常方便。
3.  **文本编辑器**：熟练使用文本编辑器是必备技能。`vim` 功能强大但学习曲线稍陡，初学者可先了解其基本模式切换（按 `i` 进入编辑模式，按 `ESC` 后输入 `:wq` 保存退出）。

### 🚀 第四步：实战与进阶

将学到的知识串联起来解决实际问题，是巩固和提升的最佳方式。

*   **Shell脚本编程**：你可以将一系列需要手动重复输入的命令写在一个以 `.sh` 结尾的文本文件里，这就是一个Shell脚本。然后通过 `bash script.sh` 来运行它，实现自动化，比如自动备份文件。一个最简单的脚本示例如下：
    ```bash
    #!/bin/bash
    # 这是一个注释
    echo "Hello, Linux!"  # echo命令用于输出文本
    date  # 显示当前日期和时间
    ```
*   **搭建简单服务**：尝试在Ubuntu上用几条命令搭建一个个人博客（如使用WordPress），这个过程会综合运用到软件安装、权限配置、服务启动等多个知识点，是极佳的实践。

### 💎 学习建议与资源

*   **勤于练习**：**最好的学习方法是坚持每天使用Linux**。尝试用它来完成一些日常任务，比如用命令行管理文件。
*   **善用帮助**：遇到不熟悉的命令时，记得使用 `man [命令]`（如 `man ls`）或 `[命令] --help` 来查看详细的使用手册。
*   **利用资源**：
    *   **在线教程与社区**：菜鸟教程、Linux中国、Stack Overflow等网站是解决问题的好去处。
    *   **书籍**：《鸟哥的Linux私房菜》是经典的入门读物。

以下是一些 Linux 系统中常用的命令，按功能分类整理：

---

### **文件与目录操作**
1. **`ls`**  
   - 列出目录内容  
   - 常用选项：`-l`（详细信息）、`-a`（显示隐藏文件）、`-h`（易读大小）  
   ```bash
   ls -lah /path
   ```
   常用`ll` 作为 ls -l的简化命令

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
