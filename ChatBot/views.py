import spacy
import re
import joblib
from datetime import datetime
from urllib.parse import urljoin

import httpx
from asgiref.sync import async_to_sync

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny

# Load mô hình NER
nlp_ner = spacy.load("model_AI/ner_model")

# Định nghĩa route nội bộ
API_ROUTES = {
    "xin nghỉ": "/Parents/bot_process-leave-request",
    "xem điểm danh": "/Students/check_in/",
    "lịch học": "/Users/bot_check_timetable/",
}

# Gọi API nội bộ
async def call_api(classified_type, payload, base_url):
    path = API_ROUTES.get(classified_type)
    if not path:
        return {"success": False, "error": "Không có route phù hợp"}

    full_url = urljoin(base_url, path)
    print("base_url:", base_url)
    print("path:", path)
    print("full_url:", full_url)

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(full_url, json=payload)

        try:
            json_data = response.json()
        except Exception:
            json_data = {"raw": response.text}

        if response.status_code == 200:
            if isinstance(json_data, dict) and "error" in json_data:
                return {"success": False, "error": json_data["error"], "data": json_data}
            return {"success": True, "data": json_data}
        
        return {
            "success": False,
            "error": f"Lỗi từ API nội bộ: {response.status_code}",
            "data": json_data
        }
    except Exception as e:
        return {"success": False, "error": "Không kết nối được tới API nội bộ", "detail": str(e)}

# Gọi API Rasa fallback
async def call_api_rasa(payload, base_url):
    full_url = urljoin(base_url, '/webhooks/rest/webhook')
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(full_url, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print("Lỗi kết nối Rasa:", e)
        return None

# API xử lý chatbot
class PredictAPIView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    def post(self, request):
        sender = request.data.get("sender")
        text = request.data.get("text", "")
        base_url = request.build_absolute_uri('/').rstrip('/')  # bỏ dấu /
        

        if not text:
            return Response({"error": "Vui lòng cung cấp văn bản!"}, status=400)

        # --- NER: tên ---
        doc = nlp_ner(text)
        names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]

        # --- NER: ngày ---
        date_range_pattern = r'(\d{1,2}/\d{1,2}(?:/\d{4})?)\s*(?:đến|đến ngày|tới ngày)?\s*(\d{1,2}/\d{1,2}(?:/\d{4})?)'
        range_match = re.search(date_range_pattern, text)

        def format_date(date_str):
            year_now = datetime.now().year
            if date_str.count('/') == 1:
                date_str = f"{date_str}/{year_now}"
            return datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d")

        if range_match:
            date_start = format_date(range_match.group(1))
            date_end = format_date(range_match.group(2))
        else:
            single_date_pattern = r'(\d{1,2}/\d{1,2}/\d{4})'
            dates = re.findall(single_date_pattern, text)
            if dates:
                date_start = format_date(dates[0])
                date_end = date_start
            else:
                date_start = None
                date_end = None

        # --- NER: lý do ---
        reason_pattern = r"(?:vì|do|tại) (.+)"
        reason_match = re.search(reason_pattern, text)
        reason = reason_match.group(1) if reason_match else "Không xác định"

        # --- Phân loại intent ---
        try:
            vectorizer = joblib.load("model_AI/vectorizer.pkl")
            classifier = joblib.load("model_AI/classifier.pkl")
            X_input = vectorizer.transform([text])
            predicted_category = classifier.predict(X_input)[0]
        except Exception as e:
            predicted_category = None

        # --- Tạo payload ---
        payload = {
            "sender_id": sender,
            "student_name": names or [],
            "start_date": date_start or "",
            "end_date": date_end or "",
            "reason": reason
        }

        # --- Gọi API nội bộ nếu phân loại được ---
        if payload["student_name"] and predicted_category:
            result = async_to_sync(call_api)(predicted_category, payload, base_url)
            if not result.get("success"):
                return Response({
                    "message": "Gọi API nội bộ lỗi",
                    "detail": result
                }, status=500)
            return Response(result["data"], status=200)

        # --- Fallback sang Rasa ---
        rasa_payload = {
            "sender": sender,
            "message": text
        }
        rasa_result = async_to_sync(call_api_rasa)(rasa_payload, base_url)
        return Response(rasa_result or {"error": "Không nhận được phản hồi từ Rasa"}, status=200)
