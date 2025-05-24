import json
import os
from datetime import datetime
from Auth.views import veriry_token

# Tạo thư mục logs nếu chưa có
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "app.log")
os.makedirs(LOG_DIR, exist_ok=True)

def logger(level, name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            request = args[1] if len(args) > 1 else None
            user_id = "unknown"
            payload = {}
            data = {}

            if request:
                method = request.method.upper()
                content_type = request.headers.get('Content-Type', '')

                # Xử lý data theo method
                if method == "GET":
                    data = request.GET.dict()
                elif method in ["POST", "PATCH", "PUT", "DELETE"]:
                    if "application/json" in content_type:
                        try:
                            data = json.loads(request.body.decode('utf-8'))
                        except:
                            data = {}
                    else:
                        data = request.POST.dict()  # fallback nếu là form-data

                # Giải token
                auth_header = request.headers.get('Authorization')
                if auth_header:
                    result = veriry_token(auth_header)
                    payload = result.get('payload', {})
                    user_id = payload.get("parent", "unknown")

                # Ghi log ra file
                log_entry = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [{level}] Gọi hàm {name} | user_id: {user_id} | path: {request.path} | method: {method} | data: {data}\n"
                with open(LOG_FILE, "a", encoding="utf-8") as log_file:
                    log_file.write(log_entry)

            kwargs["payload"] = payload
            return func(*args, **kwargs)
        return wrapper
    return decorator
