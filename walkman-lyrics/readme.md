## Walkman Lyrics

**Python3**

修正歌词时间格式，如下三位小数28.055无法被walkman正确识别导致无法正确显示歌词  
**ERROR：** `[00:28.055]wonder why, just wanna hold your hands`  
**CORRECT：** `[00:28.05]wonder why, just wanna hold your hands`

### 使用方法

修改path路径为歌词文件所在的文件夹：

```
if __name__ == '__main__':
    path = './data'
```

并在python3环境下运行

