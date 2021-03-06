# encoding=utf-8
import json
import os
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator
from flask import Flask,request,url_for

# worldcloud 词云分析的rest -- GET接口 接受参数itemid（店铺的id）
# 生成词云图片，并返回图片路径

# 定义入口
app = Flask(__name__, static_folder="D://Pythonfile/venv/worldCloud/wordcloud/wc_rest")
# 定义文件路径
imageRoute="/CloudImages/"

# 定义词云接口
@app.route('/worldCloud')
def worldCloud():
    itemid = request.args.get('itemid')
    print(itemid)
    # 该照片已经生成
    if itemid in imageBuf.keys():
        return imageRoute+itemid+".jpg"
    elif itemid in items.keys():
        print(items[itemid])
        image_sec = cloud(items[itemid], itemid)
        imageBuf[itemid]=1
        return image_sec
    else:
        return "no matching itemid, please check your itemid"

# 定义存缓存图片路径的接口
@app.route('/worldCloud/save')
def save():
    with open("imageBuf.json", "w", encoding="utf-8") as f:
        json.dump(imageBuf, f, ensure_ascii=False)
    f.close()
    return "加载入文件完成..."
    print("加载入文件完成...")

# 输入一个店铺id 返回生成的词云图片地址
def cloud(text,itemid):
    # 存放照片途径
    fileroute = imageRoute+itemid+".jpg"
    # jieba分词
    removes = ['团购', '点评', '但是', '还是', '感觉', '就是', '而且', '没有',
               '还有', '不过', '知道','什么','比较','这里''我们','以前','一下','一次']
    for w in removes:
        jieba.del_word(w)
    words = jieba.lcut(text)
    cuted = ' '.join(words)
    # wordCloud 生成词云
    fontpath = "SourceHanSansCN-Regular.otf"
    #backgroud_Image = plt.imread('cloud.jpg')
    wc = WordCloud(background_color='white',  # 设置背景颜色
                   #mask=backgroud_Image,  # 设置背景图片
                   max_words=100,  # 设置最大现实的字数
                   stopwords=STOPWORDS,  # 设置停用词
                   font_path=fontpath,  # 设置字体格式，如不设置显示不了中文
                   max_font_size=500,  # 设置字体最大值
                   min_font_size=30,  # 设置字体最小值
                   random_state=42,  # 设置有多少种随机生成状态，即有多少种配色方案
                   collocations=False, # 避免重复的单词
                   width=1600, height=1200,margin=10, # 设置图像宽高，字体间距
                   )
    wc.generate(cuted)
    # image_colors = ImageColorGenerator(backgroud_Image)
    # wc.recolor(color_func=image_colors)
    plt.figure(dpi=100)
    plt.imshow(wc, interpolation='catrom', vmax=1000)
    plt.axis('off')
    plt.savefig(fileroute)
    #plt.show()
    return fileroute

# 返回店铺评论字典
def JD():
    f = open("record.json","r", encoding="utf-8")
    di = json.load(f)
    return di

# 返回词云图片缓存
def IB():
    f = open("imageBuf.json","r",encoding="utf-8")
    imageBuf = json.load(f)
    f.close()
    return imageBuf

if __name__=="__main__":
    # 将文件目录放进去
    items = JD()
    # 为了提高系统的速度，做一个缓存字典
    imageBuf = IB()
    app.run()
