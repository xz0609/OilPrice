# 简介
抓取最新的油价信息，包括油价涨跌提醒（默认8小时更新一次数据）

数据源地址： 原 http://www.qiyoujiage.com  改为 http://m.qiyoujiage.com 


# 安装
1 手动安装，放入 <config directory>/custom_components/ 目录
  
2 hacs安装 CUSTOM REPOSITORIES中填入：https://github.com/xz0609/OilPrice

# 配置
- 配置 > 设备与服务 >  集成 >  添加集成 > 搜索`oil price` ，地区填省份的拼音，例如zhejiang

# 前台界面
开发者工具界面-实体的具体数值

![avatar](https://github.com/xz0609/OilPrice/blob/master/1.PNG)


markdown界面效果

![avatar](https://github.com/SeanChengN/OilPrice/blob/master/2.PNG)


添加一个《markdown卡片》，点击《显示代码编辑器》，把zhe_jiang_you_jie替换成你刚添加插件里的name即可。
例如我填的是《浙江油价》，在开发者工具界面-实体里看到的就是zhe_jiang_you_jie

新版的配置：
```yaml
title: 浙江油价
type: markdown
content: >
  <ha-icon icon="mdi:update"></ha-icon> {{
  state_attr('sensor.zhe_jiang_you_jie', 'update_time')}} 

  ## <center> 92# <ha-icon icon="mdi:gas-station"></ha-icon> <font
  color=#ea4335> {{ state_attr('sensor.zhe_jiang_you_jie','92') }} </font>
  &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; 95#<ha-icon
  icon="mdi:gas-station"></ha-icon> <font color=#fbbc05> {{
  state_attr('sensor.zhe_jiang_you_jie','95')}} </font> <p> 98# <ha-icon
  icon="mdi:gas-station"></ha-icon> <font color=#4285f4> {{
  state_attr('sensor.zhe_jiang_you_jie','98')}}</font>&nbsp; &nbsp; &nbsp;
  &nbsp; &nbsp; &nbsp;&nbsp; 0#<ha-icon icon="mdi:gas-station"></ha-icon> <font
  color=#34a853> {{ state_attr('sensor.zhe_jiang_you_jie','0')}}
  </font></center>   

  - {{ states('sensor.zhe_jiang_you_jie') }} 

  - {{ state_attr('sensor.zhe_jiang_you_jie','tips') }}
```
