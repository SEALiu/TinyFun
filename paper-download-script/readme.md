## paper download

**Python3**

下载dblp数据库收录的会议论文，实现了DOI，ACM来源的论文下载和RIS，PDF不同格式下载。并可以自动命名下载的pdf

### 使用方法
在__main__中调用`downloadindex(download_path, download_links_list)`

`downloadindex`函数参数解释：

| 参数 | 解释 |
|-----|-----|
| download_path | 论文保存的根路径 |
| dowload_links_list |元素为("分组文件夹名称", "dblp会议论文合集页面")的list|

例如：

```python
downloadindex('./', [
	('MSR 2015', 'http://dblp.org/db/conf/msr/msr2015.html'),
	('MSR 2014', 'http://dblp.org/db/conf/msr/msr2014.html')
])
```
