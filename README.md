# Flask



### 安装依赖

```shell
pip install -r requirements.txt
```



### 修改数据库连接

### ORM flask-sqlachemy

### 数据库表模型迁移 

```shell
flask-sqlacodegen "mysql+pymysql://root:password@host:port/database" --tables user --outfile "app/test.py" --flask
```

### 运行

```shell
python manage.py runserver
```



