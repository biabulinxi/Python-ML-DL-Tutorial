import pandas as pd

# 读取用户表
users = pd.read_table('users.dat',header=None,names=['UserID','Gender','Age','Occupation','Zip-code'], sep='::',engine= 'python')
# print(users.head())

# 读取评分表
ratings=pd.read_table('ratings.dat',header=None,names=['UserID', 'MovieID', 'Rating', 'Timestamp'],sep='::',engine='python')
# print(ratings.head())

# 读取电影详情表
movies=pd.read_table('movies.dat',header=None,names=['MovieID', 'Title', 'Genres'] ,sep='::',engine='python')
# print(movies.head())

# 将表进行合并
movie = pd.merge(pd.merge(users,ratings),movies)
# print(movie.head())

#groupby方法进行分组后聚合
data_gender = movie.groupby(['Title','Gender']).agg({'Rating':'mean'})
print(data_gender.head())

# 使用pivot_table方法 查看每一部电影不同性别的平均评分
data_gender = pd.pivot_table(movie,index='Title',columns='Gender',values='Rating',aggfunc='mean')
print(data_gender.head(10))

# 使用crosstab方法 查看每一部电影不同性别的平均评分
data_gender = pd.crosstab(index=movie.Title,columns=movie.Gender,values=movie.Rating,aggfunc='mean')
print(data_gender.head())
