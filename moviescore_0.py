# _*_coding:utf-8_*_
#数据下载网址：http://grouplens.org/datasets/movielens/ 
#为了使模型可以轻松地在内存中进行处理，选择较小的Movielen 100k数据集(4.7M)
import csv
import datetime

#1.定义函数将电影评分数据导入。
def load_reviews(path, **kwargs):
    '''
    loads Movielens reviews
    '''
    options = {
        'fieldnames': ('userid','movieid','rating','timestamp'),
        'delimiter': '\t',
    }
    options.update(kwargs)

    parse_date = lambda r,k: datetime.fromtimestamp(float(r[k]))
    parse_int = lambda r,k: int(r[k])

    with open(path,'rb') as reviews:
        reader = csv.DictReader(reviews, **options)
        for row in reader:
            row['movieid'] = parse_int(row, 'userid')
            row['userid'] = parse_int(row, 'movieid')
            row['rating'] = parse_int(row, 'rating')
            row['timestamp'] = parse_date(row, 'timestamp')
            yield row

#2.创建一个辅助函数来辅助数据导入
import os 
def relative_path(path):
    '''
    Retruns a path relative from this file
    '''
    dirname = os.path.dirname(os.path.realpath('__file__'))
    path = os.path.join(dirname, path)
    return os.path.normpath(path)

#3.创建另一个函数来导入电影信息。
def load_movies(path,**kwargs):
    """
    Loads Movielens movies
    """

    options = {
        'fieldnames':('movieid','title','release','video','url'),
        'delimiter':'|',
        'restkey':'genre',
    }
    options.update(kwargs)

    parse_int = lambda r,k: int(r[k])
    parse_date = lambda r,k: datetime.strptime(r[k],'%d-%b-%Y') if r[k] else None

    with open(path,'rb') as movies:
        reader = csv.DictReader(movies,**options)
        for row in reader:
            row['movieid'] = parse_int(row,'movieid')
            row['release'] = parse_date(row,'release')
            row['video'] = parse_date(row,'video')
            yield row

#4.创建一个MovieLens类，在之后的小节中将会反复用到。
class MovieLens(object):
    """
    Data structures to build our recommender model on.
    """

    def __init__(self,udata,uitem):
        """
        Instantiate with a path to u.data and u.item
        """
        self.udata = udata
        self.uitem = uitem
        self.movies = {}
        self.reviews = defaultdict(dict)
        self.load_dataset()

    def load_dataset(self):
        """
        Loads the two datasets into memory,indexed on the ID.
        """
        for movie in load_movies(self.uitem):
            self.movies[movie['movieid']] = movie

        for review in load_reviews(self.udata):
            self.reviews[review['userid']][review['movieid']] = review

data = relative_path('data/ml-100k/u.data')
item = relative_path('data/ml-100k/u.item')
model = MovieLens(data,item)












































































