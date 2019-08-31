# redis-demo
https://github.com/andymccurdy/redis-py 模块常用操作记录

# 安装
pipenv install -r requirements.txt

# 运行
pipevn run python redis_operation.py
or
pipenv shell
python redis_operation.py

# 删除pipenv创建的虚拟环境
pipenv --rm

# 更新日志
Date: 8/26/2019 增加flask应用的redis连接池模块：redispool.py。具体使用查看redispool中说明。