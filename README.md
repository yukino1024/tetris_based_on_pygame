# My-big-project-with-pygame-tetris-
  这是一个基于pygame库的小游戏,用python解释器运行，请提前安装pygame库，否则无法运行。运行时直接运行main.py文件即可。（注意：请不要移动可执行文件或.py文件的位置，否则程序可能应找不到对应的音乐和图片文件报错。）
  
   游戏主逻辑来自：https://www.bilibili.com/video/BV19u4y1B7br/?spm_id_from=333.1007.top_right_bar_window_custom_collection.content.click

  在此基础上，本项目加入了一些新的特性：
  1、增加了方块左右移动的判定
  2、增加了方块旋转的判定
  3、实现了多行方块同时消除
  4、添加了游戏边界与操作提示
  5、实现了开始界面与失败界面
  6、为不同界面添加了背景音乐
  7、实现了游戏内二级界面的显示的返回
  8、实现了游戏内的暂停
  9、修复部分BUG


  不同文件的作用为：
   1、main：pygame窗口的生成与关闭判定。
   2、game：游戏的主逻辑。
   3、block：定义block类，实现每个小方块的多态。
   4、blockGroup：定义blockGroup类，实现不同的方块组合类型。
   5、menu：定义menu类，实现菜单功能。
   6、generateborderblock：生成游戏边界。
   7、const：储存项目中所用到的部分常量。
   8、utils：获取时间。


*本项目中的所有素材均来自网络，仅供学习交流使用。
