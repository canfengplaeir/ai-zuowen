from flask import Blueprint, request, jsonify, current_app
from .models import db, User, Essay
from .utils.ai_correction import AICorrectionService
from .utils.image_recognition import ImageRecognitionService
from .utils.auth import AuthService, login_required
import os
from werkzeug.utils import secure_filename
import imghdr
from functools import wraps
from datetime import datetime
from sqlalchemy import desc
import re

api = Blueprint('api', __name__)
ai_service = AICorrectionService()
image_service = ImageRecognitionService()

def allowed_file(filename):
    """检查文件类型是否允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

def admin_required(f):
    """验证管理员权限的装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': '未登录'}), 401
        
        auth_service = AuthService(current_app.config['SECRET_KEY'])
        user_id = auth_service.verify_token(token.split(' ')[1])
        if not user_id:
            return jsonify({'error': '登录已过期'}), 401
            
        user = User.query.get(user_id)
        if not user or not user.is_admin:
            return jsonify({'error': '需要管理员权限'}), 403
            
        return f(*args, **kwargs)
    return decorated_function

@api.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'error': '无效的请求数据'}), 400
        
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': '用户名和密码不能为空'}), 400
    
    if User.query.filter_by(username=username).first():
        return jsonify({'error': '用户名已存在'}), 400
    
    auth_service = AuthService(current_app.config['SECRET_KEY'])
    hashed_password = auth_service.hash_password(password)
    
    user = User(
        username=username, 
        password=hashed_password.decode('utf-8')
    )
    db.session.add(user)
    
    try:
        db.session.commit()
        return jsonify({'message': '注册成功'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@api.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': '无效的请求数据'}), 400
        
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': '用户名或密码错误'}), 401
    
    auth_service = AuthService(current_app.config['SECRET_KEY'])
    
    try:
        if not auth_service.check_password(password, user.password):
            return jsonify({'error': '用户名或密码错误'}), 401
    except Exception as e:
        print(f"密码验证错误: {str(e)}")  # 添加日志
        return jsonify({'error': '登录失败，请稍后重试'}), 500
    
    token = auth_service.generate_token(user.id)
    return jsonify({
        'message': '登录成功',
        'user_id': user.id,
        'token': token,
        'is_admin': user.is_admin
    }), 200

@api.route('/auth/change-password', methods=['POST'])
@login_required
def change_password():
    data = request.get_json()
    if not data:
        return jsonify({'error': '无效的请求数据'}), 400
        
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    
    if not current_password or not new_password:
        return jsonify({'error': '当前密码和新密码不能为空'}), 400
    
    # 从 token 中获取用户 ID
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': '未登录'}), 401
        
    auth_service = AuthService(current_app.config['SECRET_KEY'])
    user_id = auth_service.verify_token(token.split(' ')[1])
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    
    # 验证当前密码 - 修复类型错误
    if not auth_service.check_password(current_password, user.password):
        return jsonify({'error': '当前密码错误'}), 401
    
    try:
        # 更新密码
        hashed_password = auth_service.hash_password(new_password)
        user.password = hashed_password.decode('utf-8')
        db.session.commit()
        return jsonify({'message': '密码修改成功'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@api.route('/essay/upload', methods=['POST'])
@login_required
def upload_essay():
    if 'image' not in request.files:
        return jsonify({'error': '没有上传图片'}), 400
        
    image = request.files['image']
    if not image or not image.filename or not allowed_file(image.filename):
        return jsonify({'error': '不支持的文件类型'}), 400
    
    user_id = request.form.get('user_id')
    if not user_id:
        return jsonify({'error': '用户ID不能为空'}), 400
    
    try:
        user_id = int(user_id)  # 转换为整数
    except ValueError:
        return jsonify({'error': '无效的用户ID'}), 400
        
    filename = secure_filename(image.filename)
    image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    
    try:
        image.save(image_path)
        
        # 验证文件是否为有效图片
        if not imghdr.what(image_path):
            os.remove(image_path)
            return jsonify({'error': '无效的图片文件'}), 400
        
        # 识别文字
        content, error = image_service.recognize_text(image_path)
        if error:
            os.remove(image_path)
            return jsonify({'error': error}), 400
        if not content:
            os.remove(image_path)
            return jsonify({'error': '无法识别图片中的文字'}), 400
        
        # AI批改
        feedback = ai_service.correct_essay(content)
        
        # 提取总分
        score = None
        if feedback:
            # 使用正则表达式匹配总分
            score_match = re.search(r'总分：(\d+)分', feedback)
            if score_match:
                score = int(score_match.group(1))
        
        # 保存到数据库
        essay = Essay(
            user_id=user_id,
            content=content,
            original_image=image_path,
            feedback=feedback,
            score=score  # 添加分数
        )
        db.session.add(essay)
        db.session.commit()
        
        return jsonify({
            'message': '作文上传成功',
            'content': content,
            'feedback': feedback,
            'score': score
        }), 201
            
    except Exception as e:
        db.session.rollback()
        if os.path.exists(image_path):
            os.remove(image_path)
        return jsonify({'error': str(e)}), 400

@api.route('/essays/<int:user_id>', methods=['GET'])
@login_required
def get_essays(user_id):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    essays_query = Essay.query.filter_by(user_id=user_id).order_by(desc(Essay.created_at))
    pagination = essays_query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'essays': [essay.to_dict() for essay in pagination.items],
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'total_pages': pagination.pages
    }), 200

@api.route('/admin/stats', methods=['GET'])
@admin_required
def get_stats():
    user_count = User.query.count()
    essay_count = Essay.query.count()
    today = datetime.utcnow().date()
    today_count = Essay.query.filter(
        db.func.date(Essay.created_at) == today
    ).count()
    
    return jsonify({
        'userCount': user_count,
        'essayCount': essay_count,
        'todayCount': today_count
    })

@api.route('/admin/users', methods=['GET'])
@admin_required
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@api.route('/admin/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if user.is_admin:
        return jsonify({'error': '不能删除管理员账号'}), 400
    
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': '用户删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@api.route('/essays/<int:essay_id>', methods=['DELETE'])
@login_required
def delete_essay(essay_id):
    # 从 token 中获取用户 ID
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': '未登录'}), 401
        
    auth_service = AuthService(current_app.config['SECRET_KEY'])
    user_id = auth_service.verify_token(token.split(' ')[1])
    
    essay = Essay.query.get_or_404(essay_id)
    
    # 验证是否是用户自己的作文
    if essay.user_id != user_id:
        return jsonify({'error': '无权限删除此作文'}), 403
    
    try:
        # 删除关联的图片文件
        if essay.original_image and os.path.exists(essay.original_image):
            os.remove(essay.original_image)
            
        db.session.delete(essay)
        db.session.commit()
        return jsonify({'message': '删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@api.route('/users/<int:user_id>', methods=['GET'])
@login_required
def get_user_info(user_id):
    user = User.query.get_or_404(user_id)
    essay_count = Essay.query.filter_by(user_id=user_id).count()
    
    return jsonify({
        'username': user.username,
        'essay_count': essay_count,
        'created_at': user.created_at.isoformat()
    }), 200 

@api.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200