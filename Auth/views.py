from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
from Parents.models import SoParents
from Parents.serializers import SoParentsSerializer
import jwt
from Cimo.settings import SECRET_KEY
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from Users.models.sorole import SoRole
import json
from Users.models.souser import SoUser
from Users.serializers import SoUserSerializer
from Users.serializers.so_role_serializer import SoRoleSerializer


def create_jwt_token(payload: dict, expires_in_seconds: int = 1232131):
    payload_copy = payload.copy()
    payload_copy["exp"] = datetime.utcnow() + timedelta(seconds=expires_in_seconds)
    token = jwt.encode(payload_copy, SECRET_KEY, algorithm="HS256")
    return token

def decode_jwt_token(token: str):
    print(token)
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        
        # Kiểm tra thời gian hết hạn thủ công (1 ngày tính từ thời điểm phát hành)
        if "exp" in decoded:
            exp_time = datetime.fromtimestamp(decoded["exp"])
            now = datetime.utcnow()

            if now > exp_time:
                return {"valid": False, "error": "Token quá hạn cho phép"}
            
            # if (exp_time - now) > timedelta(seconds=1):
            #     return {"valid": True, "payload": decoded}
                
            return {"valid": True, "payload": decoded}
        

    except ExpiredSignatureError as e:
        return {"valid": False, "error": str(e)}
    except InvalidTokenError:
        return {"valid": False, "error": "Token không hợp lệ"}
def veriry_token(auth_header):
    if not auth_header or not auth_header.startswith('Bearer '):
        return {"valid": False, "error": "Thiếu hoặc sai định dạng Authorization header"}

    token = auth_header.split('Bearer ')[1]
    result = decode_jwt_token(token)
    # print("1",result)
    return result  # Luôn là dict {valid, error?, payload?}

class VerifyOtpAPI(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        otp = request.data.get('otp')
        parent = SoParents.objects.filter(phone=phone).first()
        if parent is None:
            return Response({'message': 'Tài khoản không tồn tại'}, status=400)
        if otp != "123456":
            return Response({'message': 'Mã OTP không đúng'}, status=400)

        serializer = SoParentsSerializer(parent)
        data = {
            'parent': serializer.data['id'],
            
        }

        token = create_jwt_token(data)
        decode = decode_jwt_token(token)
        return Response({'message': 'Xác thực thành công', 'token': token, "decode":decode}, status=200)

# Create your views here.
class Login_Parents(APIView):
    def post(self, request):
        
        # Xử lý logic tạo token ở đây
        # Ví dụ: tạo token ngẫu nhiên hoặc sử dụng thư viện như PyJWT
        # Trả về token trong phản hồi
        return Response({"token": "your_token_here"})
    


class Login_User(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        website = request.data.get('website')
        
        user = SoUser.objects.filter(username=username, password=password).first()
        if user is None:
            return Response({'message': 'Tài khoản hoặc mật khẩu không đúng'}, status=400)
        if website is None:
            return Response({'message': 'Thiếu website'}, status=400)
        try:
            role_ids = json.loads(user.soRoleIds)
        except json.JSONDecodeError:
            return Response({'message': 'Dữ liệu quyền truy cập không hợp lệ'}, status=400)
        role = SoRole.objects.filter(name=website, id__in=role_ids).first()
        if role is None:
            return Response({'message': 'Tài khoản không có quyền truy cập vào website này'}, status=400)
        payload = {
            'user_id': user.id,
            'username': user.username,
            'name': user.name,
            'website': website,
            'role_name': role.name,
            'role_id': role.id,
        }
        token = create_jwt_token(payload, expires_in_seconds=86400)
        return Response({'message': 'Xác thực thành công', 'token': token}, status=200)
    
    
