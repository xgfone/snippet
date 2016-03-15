#!/usr/bin/python
# coding: utf-8
from __future__ import print_function, division, unicode_literals

import re

SEPARATE_WORD_RE = re.compile('\\W+')


def getWords(doc, filter_func=None):
    words = (w for w in SEPARATE_WORD_RE.split(doc) if len(w) > 1)
    rtn = set()
    if filter_func:
        for w in words:
            tmp = filter_func(w)
            if tmp:
                rtn.add(tmp)
    else:
        for w in words:
            rtn.add(w.lower())
    return rtn


class BaseClassifier:
    def __init__(self, get_features=getWords):
        # get_feature是个函数，用来提取文档中的特性并返回一个包含所有特性的字典或序列类型的对象
        self.getFeatures = get_features

        # 用来统计特性，即每种特性在每种分类中引用的次数
        # 例如： {'python': {'good': 3, 'bad': 1},
        #        'the':    {'good': 2, 'bad': 1}}
        # 其中，'python'和'the'是特性，'good'和'bad'是种类
        self.features = {}

        # 用来统计分类，即每种分类中所有特性被引用的总和
        # 例如：{'good': 5, 'bad': 2}
        self.categories = {}

    # 增加属于category分类的feature特性的引用次数，
    # 即有一个新的feature特性属于category分类
    def incFeature(self, feature, category):
        self.features.setdefault(feature, {})
        self.features[feature].setdefault(category, 0)
        self.features[feature][category] += 1

    def incCategory(self, category):
        self.categories.setdefault(category, 0)
        self.categories[category] += 1

    # 获取在category分类下feature被引用的次数
    # 如果没有category分类，或category分类中没有feature特性，则返回0
    def getFeatCount(self, feature, category):
        if feature in self.features and category in self.features[feature]:
            return self.features[feature][category]
        return 0

    # 获取category分类中所有特性被引用的次数
    def getCateCount(self, category):
        return self.categories.get(category, 0)

    # 获取所有分类被引用的次数总和
    def getTotalCate(self):
        return sum(self.categories.values())

    # 获取所有的分类
    def getCategories(self):
        return self.categories.keys()

    # 利用特性集items（一个包含一些特性的字符串），对category进行训练
    def train(self, item, category):
        features = self.getFeatures(item)
        for f in features:
            self.incFeature(f, category)
            self.incCategory(category)

    # 在给定category分类下，计算并返回feature特性的概率，即feature特性属于category分类的概率
    # 即P(Feature | Category)
    def getFeatProb(self, feature, category):
        cate_count = self.getCateCount(category)
        if cate_count == 0:
            return 0.0
        return self.getFeatCount(feature, category) / cate_count

    # 求category分类在所有分类中的概率（即所占的比重，P(Category)）
    def getCateProb(self, category):
        return self.getCateCount(category) / self.getTotalCate()

    # 同getFeatProb，但使用权重来调整feature特性在category分类下的概率
    def getFeatWeightedProb(self, feature, category, get_feat_prob=None,
                            weight=1.0, ap=0.5):
        if not get_feat_prob:
            get_feat_prob = self.getFeatProb
        basic_feat_prob = get_feat_prob(feature, category)

        # 计算feature特性在所有分类下被引用的次数的总和
        total = sum([self.getFeatCount(feature, c) for c in self.getCategories()])

        wp = ((weight * ap) + (total * basic_feat_prob)) / (total + weight)
        return wp


# 贝叶斯（Bayes）算法：
# 原理：利用特征概率来计算整篇文档的概率，进而通过筛选出最大概率来得出该篇文档所属于的分类
# P(Classifier | Document) = P(Document | Classifier) * P(Classifier) / P(Document)
# 注：P(A | B)意为“在给定条件B下，求A的概率”
# 由于P(Document)对所有分类都一样，所以可以省略P(Document)，即可以直接求
# P(Document | Classifier) * P(Classifier)
# 注：P(Classifier)已经在基类中求出（即getCateProb方法），故可以省略
class BayesClassifier(BaseClassifier):
    def __init__(self, get_feature=getWords):
        BaseClassifier.__init__(self, get_feature)
        # 保存属于每种分类的阀值，即某一篇文档要想属于一分类，那么它属于该分类的概率除以该分类所
        # 对应的阀值所得的值，要比该文档属于其他分类的概率还要大。
        self.thresholds = {}

    # 获取category分类所对应的阀值，如果该分类没有对应的阀值，则返回1.0
    def getThreshold(self, category):
        return self.thresholds.get(category, 1.0)

    # 设置category分类所对应的阀值
    def setThreshold(self, category, value):
        self.thresholds[category] = value

    # 求P(Document | Category)，即在给定Category的条件下，求Document的概率
    # 由于Document是包含一些特性的字符串，所以该问题可以转化为：求Document文档中所包含的所有
    # 特性在给定Category条件下的概率之积
    def getDocProb(self, category, doc):
        features = self.getFeatures(doc)
        p = 1
        for f in features:
            p *= self.getFeatWeightedProb(f, category)
        return p

    # 求P(Classifier | Document)
    def getProb(self, doc, category):
        return self.getCateProb(category) * self.getDocProb(category, doc)

    # 求某篇文档所属于的分类，即，求该文档属于每种分类的概率的最大值
    def classify(self, doc, default=None):
        probs = {}
        max = 0.0
        best = None
        # 找到拥有最大概率的分类
        for c in self.getCategories():
            probs[c] = self.getProb(doc, c)
            if probs[c] > max or not best:
                max = probs[c]
                best = c

        # 遍历所有分类，查看上一步所计算出的分类是否超过了阀值，超过了，就返回上一步计算出的分类，
        # 否则返回默认分类
        for c in probs:
            if c == best:
                continue
            if probs[c] * self.getThreshold(best) > probs[best]:
                return [default, probs]
        return [best, probs]


################################################
# For Test
def sample_train(cl):
    cl.train('Nobody owns the water.', 'good')
    cl.train('the quick rabbit jumps fences', 'good')
    cl.train('buy pharmaceuticals now', 'bad')
    cl.train('make quick money at the online casino', 'bad')
    cl.train('the quick brown fox jumps', 'good')


def sample_test():
    doc = "the quick brown fox jumps"
    cl = BayesClassifier()
    sample_train(cl)
    rtn = cl.classify(doc)
    if rtn[0] == "good":
        print("YES正确")
    else:
        print("NO")
    print("Exit ...")


if __name__ == "__main__":
    sample_test()
