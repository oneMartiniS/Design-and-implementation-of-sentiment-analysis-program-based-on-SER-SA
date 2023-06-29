#pip install Flask Flask-Paginate Werkzeug Flask-MySQLdb Flask-SocketIO aliyun-python-sdk-core pandas pymysql
from flask_paginate import Pagination, get_page_parameter
from flask import Flask, render_template, request, send_from_directory, request,url_for, session
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from datetime import datetime
from flask import redirect, flash,jsonify,send_from_directory
from flask.helpers import send_file
from io import BytesIO
from wordcloud import WordCloud
from flask import request, jsonify
import jieba
import base64
import json
import stylecloud
from PIL import Image
import numpy as np
import pandas as pd
import pymysql
import os
import csv


# 设置允许的文件扩展名
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
AVATAR_FOLDER = './static/images/user_avatars/'

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['RESULTS_FOLDER'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'results')
app.config['RESULTS_FOLDER'] = './results'
app.config['DEBUG'] = True
socketio = SocketIO(app, cors_allowed_origins="*") 
# 设置 secret_key
app.secret_key = 'F6Ys3s91jU6mSmH9XzBn8Qd2gFt6KcLr'
# 连接MySQL数据库
def create_connection():
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="tcw2829952",
        database="chatroom",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )
    return connection
# 初始化MySQL数据库
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'tcw2829952'
app.config['MYSQL_DB'] = 'chatroom'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)
# 保存消息到数据库
def save_message(username, content):
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO chat_messages (login_id, content, timestamp) VALUES ((SELECT id FROM login WHERE username = %s), %s, NOW())"
            cursor.execute(sql, (username, content))
        conn.commit()
    finally:
        conn.close()
#chatroom.htlm
# 使用socketio处理聊天
#发送消息事件
@socketio.on('message')
def handle_message(data):
    username = session['username']# 从会话中获取用户名
    content = data['content']# 从事件数据中获取消息内容

    save_message(username, content) # 将消息保存到数据库
    send({# 将消息发送给房间中的其他用户
        'username': username,
        'content': content,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }, room=data['room'])
@socketio.on('get_messages')
def handle_get_messages(data):
    username = session['username']
    room = data['room']

    # 获取历史消息
    messages = get_all_messages()
    for message in messages:
        emit('message', {# 将历史消息发送给前端
            'type': 'history',
            'username': message['username'],
            'content': message['content'],
            'timestamp': message['timestamp'].strftime("%Y-%m-%d %H:%M:%S"),
            'is_current_user': username == message['username']
        })
# 加入聊天室事件
@socketio.on('join')
def on_join(data):
    username = session['username']
    room = data['room']
    join_room(room)# 将用户加入到指定房间

    # 发送加入房间的通知
    send({'alert': f'{username} has joined the room.'}, room=room)

    # 获取历史消息
    messages = get_all_messages()
    for message in messages:
        emit('message', {# 将历史消息发送给前端聊天框
            'username': message['username'],
            'content': message['content'],
            'timestamp': message['timestamp'].strftime("%Y-%m-%d %H:%M:%S"),
            'is_current_user': username == message['username']
        })
#离开聊天室事件     
@socketio.on('leave')
def on_leave(data):
    username = session['username']
    room = data['room']
    leave_room(room) # 将用户从指定房间移除

    # 发送离开房间的通知
    send({'alert': f'{username} has left the room.'}, room=room)

#login.html
#注册登录
#用户注册和验证
def register_user(username, password, email, role):
    try:
        connection = create_connection()
        with connection.cursor() as cursor:# 使用数据库连接执行插入操作
            sql = "INSERT INTO login (username, password, email, role) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (username, password, email, role))
        connection.commit()# 提交更改
    finally:
        connection.close()# 关闭数据库连接
def authenticate_user(username, password):# 验证用户名和密码是否匹配数据库记录的函数
    try:
        connection = create_connection()
        with connection.cursor() as cursor:# 使用数据库连接执行查询操作
            sql = "SELECT * FROM login WHERE username=%s AND password=%s"
            cursor.execute(sql, (username, password))
            result = cursor.fetchone()
        return result # 返回查询结果
    finally:
        connection.close()# 关闭数据库连接
#注册
@app.route('/register', methods=['POST'])
def register():# 从前端页面中获取用户名、电子邮件和密码
    username = request.form['userName']
    email = request.form['email']
    password = request.form['password']
    role = "user"  # 默认为普通用户
    register_user(username, password, email, role) # 调用 register_user 函数将新用户添加到数据库
    flash("注册成功，请登录", "success") # 显示注册成功的提示消息
    return redirect(url_for('index'))# 重定向到主页
#登录
@app.route('/login', methods=['POST'])
def login(): # 从前端页面中获取用户名和密码
    username = request.form['userName']
    password = request.form['password']
    user = authenticate_user(username, password)# 调用 authenticate_user 函数验证用户名和密码是否匹配
    if user:# 如果用户名和密码有效
        flash("登录成功", "success")# 显示登录成功的提示消息
        session['username'] = user['username']# 将用户名和角色存储到 session 中
        session['role'] = user['role']
        return redirect(url_for('profile')) # 重定向到个人资料页面
    else:
        flash("用户名或密码错误", "danger")# 显示用户名或密码错误的提示消息
        return redirect(url_for('index'))# 重定向到主页
#退出登录
@app.route('/logout')
def logout():
    session.pop('username', None)# 从 session 中移除用户名和角色
    session.pop('role', None)
    flash("您已成功退出登录", "success")# 显示注销成功的提示消息
    return redirect(url_for('index'))# 重定向到主页
#SERmessage.html
#调用SDK主程序，来自阿里云官方SDK程序示例
def analyze_sentiment(text):
    client = AcsClient("LTAI5tBxrs2fnzWumqzi89wS", "mq9VMSrSuhjr1p5ZjyGZoY7ZCFb9SV", "cn-hangzhou")# 创建AcsClient实例
    request = CommonRequest()
    request.set_domain("alinlp.cn-hangzhou.aliyuncs.com")# domain和version是固定值
    request.set_version("2020-06-29")
    request.set_action_name("GetSaChGeneral")# action name可以在API文档里查到
    request.add_query_param("ServiceCode", "alinlp")# 需要add哪些param可以在API文档里查到
    request.add_query_param("Text", text)
    request.add_query_param("TokenizerId", "GENERAL_CHN")
    response = client.do_action_with_exception(request)
    #在控制台接受服务器反馈数据，以便能分析程序的错误
    #print("Response:", response)  # 打印原始响应
    resp_obj = json.loads(response.decode("utf-8"))
    #print("Response Object:", resp_obj)  # 打印响应对象
    #接受服务器数据
    data = json.loads(resp_obj.get("Data"))
    result_obj = data.get("result")
    positive_prob = result_obj.get("positive_prob")
    negative_prob = result_obj.get("negative_prob")
    neutral_prob = result_obj.get("neutral_prob")
    #判断语句
    if positive_prob >= 0.5:
        result = "正面语句"
    elif negative_prob >= 0.5:
        result = "负面语句"
    else:
        result = "中立语句"
    return result, positive_prob, neutral_prob, negative_prob
#情感分析
@app.route('/analyze_messages', methods=['POST'])
def analyze_messages():
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            # 禁用外键检查
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

            # 删除上一次的分析结果
            sql = "DELETE FROM sentiment_analysis"
            cursor.execute(sql)

            # 重置sentiment_analysis表的id列自增值
            sql = "ALTER TABLE sentiment_analysis AUTO_INCREMENT = 1"
            cursor.execute(sql)

            # 获取所有聊天记录
            sql = """SELECT chat_messages.id, login.username, chat_messages.content
                    FROM chat_messages
                    INNER JOIN login ON chat_messages.login_id = login.id
                    ORDER BY chat_messages.timestamp ASC"""
            cursor.execute(sql)
            messages = cursor.fetchall()

            # 对每条聊天记录进行情感分析，并将结果存储在sentiment_analysis表中
            for message in messages:
                result, positive_prob, neutral_prob, negative_prob = analyze_sentiment(message['content'])
                sql = """INSERT INTO sentiment_analysis (chat_message_id, username, sentiment, positive_prob, neutral_prob, negative_prob)
                        VALUES (%s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql, (message['id'], message['username'], result, positive_prob, neutral_prob, negative_prob))

            # 启用外键检查
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

            # 提交更改
            conn.commit()

    finally:
        conn.close()
    flash("情感分析完成", "success")
    return redirect(url_for('SERmessage'))
# 获取所有消息
def get_all_messages():
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            sql = """SELECT login.username, chat_messages.content, chat_messages.timestamp
                    FROM chat_messages
                    INNER JOIN login ON chat_messages.login_id = login.id
                    ORDER BY chat_messages.timestamp ASC"""
            cursor.execute(sql)
            messages = cursor.fetchall()
        return messages
    finally:
        conn.close()
#导出聊天记录
@app.route('/export_messages', methods=['GET'])
def export_messages():
    print("进入导出聊天记录功能") 
    messages = get_all_messages()
    print(f"查询到的聊天记录: {messages}")
    if not messages:
        
        flash("没有聊天记录", "warning")
        return redirect(url_for('SERmessage'))

    with open('./results/MESSAGES.csv', mode='w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['序号', '姓名', '内容', '时间'])

        for index, message in enumerate(messages, start=1):
            writer.writerow([index, message['username'], message['content'], message['timestamp'].strftime("%Y-%m-%d %H:%M:%S")])

    return send_from_directory(directory='results', path='MESSAGES.csv', as_attachment=True)
    export_chat_messages()
    return send_from_directory('./results', 'MESSAGES.csv', as_attachment=True)
#导出分析结果
@app.route('/export_ser_result', methods=['GET'])
def export_ser_result():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""SELECT id, username, sentiment, positive_prob, neutral_prob, negative_prob
                      FROM sentiment_analysis""")
    result = cursor.fetchall()
    cursor.close()
    connection.close()

    csv_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results', 'SER.csv')
    with open(csv_file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = ['id', 'username', 'sentiment', 'positive_prob', 'neutral_prob', 'negative_prob']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in result:
            writer.writerow(row)

    return send_from_directory(directory=os.path.join(app.root_path, 'results'), path='SER.csv', as_attachment=True)
#删除聊天记录
def clear_chat_messages():
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SET FOREIGN_KEY_CHECKS=0; TRUNCATE chat_messages; SET FOREIGN_KEY_CHECKS=1;"
            cursor.execute(sql)
        conn.commit()
    finally:
        conn.close()
@app.route('/clear_chat_messages', methods=['POST'])
def clear_chat_messages_route():
    clear_chat_messages()
    flash("聊天记录已清空", "success")
    return redirect(url_for('SERmessage'))

#显示聊天记录
def get_chat_messages():
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            sql = """SELECT chat_messages.id, login.username, chat_messages.content, chat_messages.timestamp
                    FROM chat_messages
                    INNER JOIN login ON chat_messages.login_id = login.id
                    ORDER BY chat_messages.timestamp ASC"""
            cursor.execute(sql)
            messages = cursor.fetchall()
        return messages
    finally:
        conn.close()
#统计分析的总语句个数，正面语句个数，负面语句个数，中立语句个数
def get_sentiment_counts():
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            # 统计总语句个数、正面语句个数、负面语句个数和中立语句个数
            sql = """SELECT COUNT(*) as total,
                            SUM(CASE WHEN sentiment = '正面语句' THEN 1 ELSE 0 END) as positive_count,
                            SUM(CASE WHEN sentiment = '负面语句' THEN 1 ELSE 0 END) as negative_count,
                            SUM(CASE WHEN sentiment = '中立语句' THEN 1 ELSE 0 END) as neutral_count
                     FROM sentiment_analysis"""
            cursor.execute(sql)
            result = cursor.fetchone()

            return result

    finally:
        conn.close()
# 使用get_sentiment_counts()函数获取统计信息
counts = get_sentiment_counts()
print("Total statements:", counts['total'])
print("Positive statements:", counts['positive_count'])
print("Negative statements:", counts['negative_count'])
print("Neutral statements:", counts['neutral_count'])
#让前端接收统计数据
@app.route('/get_sentiment_counts', methods=['GET'])
def get_sentiment_counts_route():
    counts = get_sentiment_counts()
    return jsonify(counts)
#基于不同姓名统计正面语句个数，负面语句个数，中立语句个数个数
def get_sentiment_counts_by_username():
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            # 统计不同姓名的正面语句个数、负面语句个数和中立语句个数
            sql = """SELECT username,
                            SUM(CASE WHEN sentiment = '正面语句' THEN 1 ELSE 0 END) as positive_count,
                            SUM(CASE WHEN sentiment = '负面语句' THEN 1 ELSE 0 END) as negative_count,
                            SUM(CASE WHEN sentiment = '中立语句' THEN 1 ELSE 0 END) as neutral_count
                     FROM sentiment_analysis
                     GROUP BY username"""
            cursor.execute(sql)
            result = cursor.fetchall()

            return result

    finally:
        conn.close()

# 使用get_sentiment_counts_by_username()函数获取统计信息
username_counts = get_sentiment_counts_by_username()
print("Sentiment counts by username:")
for count in username_counts:
    print(f"{count['username']}: Positive - {count['positive_count']}, Neutral - {count['neutral_count']}, Negative - {count['negative_count']}")
@app.route('/get_sentiment_counts_by_username', methods=['GET'])
def get_sentiment_counts_by_username_route():
    counts = get_sentiment_counts_by_username()
    return jsonify(counts)
#用户-情感
def get_sentiment_analysis():# 从数据库获取用户情感分析数据的函数
    connection = create_connection()# 创建与数据库的连接
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM sentiment_analysis") # 执行 SQL 查询以提取所有情感分析数据
    data = cursor.fetchall()
    cursor.close()# 关闭游标和连接
    connection.close()
    return data # 返回查询结果
def calculate_sentiment_trends():# 计算情感趋势的函数
    data = get_sentiment_analysis()
    trends = {}
    # 遍历每个数据行
    for row in data:
        username = row['username']
        sentiment = row['sentiment']
        positive_prob = row['positive_prob']
        neutral_prob = row['neutral_prob']
        negative_prob = row['negative_prob']
         # 根据情感类型计算趋势值
        if sentiment == "正面语句":
            trend_value = positive_prob + 1
        elif sentiment == "中立语句":
            trend_value = neutral_prob
        elif sentiment == "负面语句":
            trend_value = 0 - negative_prob
        if username not in trends: # 将趋势值添加到相应的用户名下
            trends[username] = []
        trends[username].append(trend_value)
    return trends# 返回计算的情感趋势数据
@app.route('/get_sentiment_trends', methods=['GET'])
def get_sentiment_trends():# 计算情感趋势数据
    trends = calculate_sentiment_trends()
    return jsonify(trends)# 将趋势数据转换为 JSON 格式并返回

#词云图请求
@app.route('/generate_wordcloud', methods=['POST'])
def generate_wordcloud():
    try:
        messages = get_all_messages()# 从数据库获取所有消息
        content_list = [msg['content'] for msg in messages]# 从消息中提取内容
        wordcloud_image = create_wordcloud(content_list)# 使用 create_wordcloud 函数创建词云图像并将其转换为 base64 编码
        return jsonify({'wordcloud_image': wordcloud_image})# 将词云图像作为 JSON 响应返回
    except Exception as e:
        print(e)  # 输出错误信息
        return jsonify({'error': str(e)}), 500# 如果出现异常，输出错误信息并返回 500 错误状态码

#生成词云图
def create_wordcloud(content_list):
    text = ' '.join(content_list)# 将内容列表拼接为一个长字符串
    words = jieba.cut(text)# 使用 jieba 进行分词
    words = ' '.join(words)

    # 加载聊天气泡蒙版图像，更新文件路径
    chat_bubble_mask = np.array(Image.open("static/images/chat_bubble_mask.png"))
    chat_bubble_mask[chat_bubble_mask == 0] = 255

    font_path = 'static/fonts/simhei.ttf'  # 使用黑体避免中文乱码
    # 使用 stylecloud 生成词云图
    stylecloud.gen_stylecloud(
        text=words,
        icon_name='fas fa-comment',  # 使用 Font Awesome 的聊天气泡图标
        palette='cartocolors.diverging.TealRose_7',  # 使用预定义的颜色方案
        background_color='white',  # 背景颜色
        output_name='wordcloud.png',  # 输出文件名
        size=1024,  # 词云图大小
        custom_stopwords=None,  # 自定义停用词，如果需要
        font_path=font_path  # 使用适用于中文的字体文件
    )

    with open("wordcloud.png", "rb") as image_file:
        img_base64 = base64.b64encode(image_file.read()).decode()

    return img_base64
#profile.html
# 检查文件扩展名是否在允许的文件扩展名列表中
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 保存上传的头像文件并返回文件名
def save_avatar(file):
    filename = secure_filename(file.filename)
    file.save(os.path.join(AVATAR_FOLDER, filename))
    return 'user_avatars/' + filename

@app.route('/update_profile', methods=['POST'])
def update_profile():
    if request.method == 'POST':
        username = session['username']# 从 session 中获取用户名
        gender = request.form['gender'] # 从前端页面中获取性别、电子邮件和个人简介
        email = request.form['email']
        introduction = request.form['introduction']
        avatar = None
     # 检查请求中是否包含头像文件
    if 'avatar' in request.files and request.files['avatar'].filename != '':
        file = request.files['avatar']
        if file and allowed_file(file.filename):# 如果文件存在且允许上传，保存头像文件
            avatar = save_avatar(file)

        # 创建数据库连接
        conn = create_connection()
        with conn.cursor() as cur:# 使用数据库连接执行更新操作
            if avatar:# 如果有头像文件，更新头像、性别和个人简介
                cur.execute("UPDATE user_profiles SET gender = %s, avatar = %s, introduction = %s WHERE username = %s", (gender, avatar, introduction, username))
            else:# 否则仅更新性别和个人简介
                cur.execute("UPDATE user_profiles SET gender = %s, introduction = %s WHERE username = %s", (gender, introduction, username))
            cur.execute("UPDATE login SET email = %s WHERE username = %s", (email, username))# 更新用户的电子邮件
            conn.commit()# 提交更改

        return redirect(url_for('profile'))# 更新完成后重定向到个人资料页面

#加载/results中的文件
@app.route('/results/<path:filename>')
def serve_results(filename):
    return send_from_directory(app.config['RESULTS_FOLDER'], filename)

#admin.html
# 获取用户数据
def get_users():
    connection = create_connection() # 创建数据库连接
    with connection.cursor() as cursor: # 使用数据库连接执行查询操作
        sql = "SELECT * FROM login"
        cursor.execute(sql)
        result = cursor.fetchall()
    connection.close() # 关闭数据库连接
    return result# 返回查询结果

@app.route('/get_users')
def fetch_users():
    users = get_users()# 获取所有用户信息
    return jsonify(users)
@app.route('/update_user', methods=['POST'])
def update_user():# 从前端中获取用户 ID、用户名、密码、电子邮件和角色
    user_id = request.form['id']
    new_username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    role = request.form['role']

    connection = create_connection()
    with connection.cursor() as cursor:
        # 禁用外键约束
        cursor.execute("SET FOREIGN_KEY_CHECKS=0;")

        # 获取旧的用户名
        get_old_username_sql = "SELECT username FROM login WHERE id=%s"
        cursor.execute(get_old_username_sql, (user_id))
        old_username = cursor.fetchone()['username']

        # 更新login表
        update_login_sql = "UPDATE login SET username=%s, password=%s, email=%s, role=%s WHERE id=%s"
        cursor.execute(update_login_sql, (new_username, password, email, role, user_id))

        # 更新user_profiles表
        update_user_profiles_sql = "UPDATE user_profiles SET username=%s WHERE username=%s"
        cursor.execute(update_user_profiles_sql, (new_username, old_username))

        # 更新sentiment_analysis表
        update_sentiment_analysis_sql = """
        UPDATE sentiment_analysis
        SET username=%s
        WHERE chat_message_id IN (SELECT id FROM chat_messages WHERE login_id=%s)
        """
        cursor.execute(update_sentiment_analysis_sql, (new_username, user_id))

        # 重新启用外键约束
        cursor.execute("SET FOREIGN_KEY_CHECKS=1;")

    connection.commit()
    connection.close()

    return jsonify({"status": "success"})



#删除用户数据
@app.route('/delete_user', methods=['POST'])
def delete_user():
    user_id = request.form['id']

    connection = create_connection()
    with connection.cursor() as cursor:
        # 删除外键关联的数据
        delete_chat_messages_sql = "DELETE FROM chat_messages WHERE login_id=%s"
        cursor.execute(delete_chat_messages_sql, (user_id))

        delete_user_profiles_sql = "DELETE FROM user_profiles WHERE username IN (SELECT username FROM login WHERE id=%s)"
        cursor.execute(delete_user_profiles_sql, (user_id))

        delete_sentiment_analysis_sql = "DELETE FROM sentiment_analysis WHERE chat_message_id IN (SELECT id FROM chat_messages WHERE login_id=%s)"
        cursor.execute(delete_sentiment_analysis_sql, (user_id))

        # 删除login表中的数据
        delete_login_sql = "DELETE FROM login WHERE id=%s"
        cursor.execute(delete_login_sql, (user_id))

    connection.commit()
    connection.close()

    return jsonify({"status": "success"})
#图片
@app.route('/static/images/<path:path>')
def send_image(path):
    return send_from_directory('static/images', path)

#页面响应
@app.context_processor
def inject_username():
    return {'username': session.get('username')}

@app.route('/')
def index():
    return render_template('login.html') 

@app.route('/chatroom')
def chatroom():
    
     return render_template('chatroom.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/profile')
def profile():
    username = session['username'] # 获取用户名
    cur = mysql.connection.cursor()# 使用 MySQL 连接
    # 从数据库中获取用户个人资料信息
    cur.execute("SELECT user_profiles.username,user_profiles.introduction, user_profiles.gender, user_profiles.avatar, user_profiles.introduction, login.email FROM user_profiles INNER JOIN login ON user_profiles.username=login.username WHERE user_profiles.username = %s", [username])
    user_info = cur.fetchone() # 获取查询结果
    cur.close()
    return render_template('profile.html', user_info=user_info)# 使用查询到的用户信息返回前端页面


@app.route('/ts')
def ts():
    return render_template('ts.html')

@app.route('/SERmessage')
def SERmessage():
    messages = get_chat_messages()# 从数据库中获取聊天消息
    return render_template('SERmessage.html', messages=messages) # 使查询到聊天记录返回 SERmessage.html 页面

if __name__ == '__main__':
    socketio.run(app, debug=True,host='0.0.0.0')

