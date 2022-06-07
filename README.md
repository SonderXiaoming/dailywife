# 今日老婆

一个适用于HoshinoBot的随机群友老婆插件

### ★ 如果你喜欢的话，请给仓库点一个star支持一下23333 ★

## 本项目地址：

https://github.com/SonderXiaoming/dailywife

## 部署教程：

1.下载或git clone本插件：

在 HoshinoBot\hoshino\modules 目录下使用以下命令拉取本项目

git clone https://github.com/SonderXiaoming/dailywife

2.启用：

在 HoshinoBot\hoshino\config\ **bot**.py 文件的 MODULES_ON 加入 'dailywife'

然后重启 HoshinoBot

## 指令

【今日老婆】

随机抓一位群友当老婆

每天群友老婆是固定的

每个群友只能当一个人的老婆

## 彩蛋

超管必抽到bot

群友必抽不到bot

（与原版老婆指令对应，想ntr我老婆？）

修改的话只要把laopo.py的82,83，94行注释掉，84行elif改成if

## 已知问题

高并发下有可能抽到重复的老婆

储存数据用json可能不太好