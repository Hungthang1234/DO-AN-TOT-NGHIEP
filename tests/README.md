# Tests Directory

Thư mục chứa các file test cho ứng dụng.

## Files

### API Tests
- **test_api_direct.py** - Test trực tiếp các Advanced Charts API endpoints
- **test_charts_api.py** - Kiểm tra cấu trúc dataset cho Advanced Charts
- **test_charts_endpoints.py** - Test toàn diện các chart endpoints

## Chạy Tests

```bash
# Test dataset structure
python tests/test_charts_api.py

# Test API endpoints (cần server đang chạy)
python tests/test_api_direct.py

# Test endpoints với requests library
python tests/test_charts_endpoints.py
```

## Yêu cầu

- Server phải đang chạy (python app.py) để test API endpoints
- Dataset `Data/cleaned_real_estate.csv` phải tồn tại
- Đã cài đặt dependencies: pandas, requests, flask
