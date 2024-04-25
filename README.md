# tgbot
一个Telegram机器人，传话姬

demo: [@hbcao2bot](https://t.me/hbcao2bot)

## 安装
0. 安装 Python > 3.7
```bash
# 1.克隆仓库或者手动下载
git clone https://github.com/HBcao233/tgbot
# 2.安装依赖
cd tgbot
pip install -r requirements.txt
# 3.运行
chmod 755 tgbot.sh
tgbot.sh start
# 建立快捷方式（可选）
ln -s path/to/tgbot/tgbot.sh /usr/bin/tgbot
# 查看运行状态
tgbot status
# 查看运行日志
tgbot log
# 关闭
tgbot stop
```

## 配置
重命名 `config.py.example` 为 `config.py`，按照备注修改配置

Rename `config.py.example` to `config.py`, and edit it by notes

token 必填，获取方法自行搜索 Telegram Bot Token