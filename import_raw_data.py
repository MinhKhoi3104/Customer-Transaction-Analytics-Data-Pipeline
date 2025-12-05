import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
import time
from mysql.connector.errors import ProgrammingError
from _001_config._00101_database_config import *

# Các thông số kết nối
DB_HOST = URL_MYSQL["properties"]["host"]
DB_PORT = URL_MYSQL["properties"]["port"]
DB_USER = URL_MYSQL["properties"]["user"]
DB_PASSWORD = URL_MYSQL["properties"]["password"]
DB_DATABASE = URL_MYSQL["properties"]["database"]
DATA_FOLDER = "data_sample"

def create_db_engine():
    """Tạo engine kết nối tới MySQL container với cơ chế thử lại (retry)."""
    # Sử dụng driver pymysql cho SQLAlchemy
    db_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}?charset=utf8mb4"
    max_retries = 5
    
    for attempt in range(max_retries):
        try:
            print(f"[{time.strftime('%H:%M:%S')}] Đang thử kết nối MySQL (Lần {attempt + 1}/{max_retries})...")
            engine = create_engine(
                db_url,
                pool_pre_ping=True,  # Kiểm tra connection trước khi sử dụng
                pool_recycle=3600,   # Recycle connection sau 1 giờ
                echo=False
            )
            
            # Thử kết nối để kiểm tra ngay lập tức
            with engine.connect() as connection:
                print(f"[{time.strftime('%H:%M:%S')}] Kết nối thành công tới database: {DB_DATABASE}")
                return engine
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] Lỗi kết nối: {e}")
            if attempt < max_retries - 1:
                # Chờ 5 giây trước khi thử lại
                time.sleep(5)
            else:
                raise ConnectionError("Không thể kết nối tới MySQL sau nhiều lần thử.")
    return None


def load_csv_to_mysql(engine):
    """Đọc tất cả file CSV trong thư mục data_sample và đẩy vào MySQL."""
    if not os.path.exists(DATA_FOLDER):
        print(f"[{time.strftime('%H:%M:%S')}] LỖI: Thư mục '{DATA_FOLDER}' không tồn tại. Vui lòng tạo thư mục và thêm file CSV.")
        return

    print(f"[{time.strftime('%H:%M:%S')}] Bắt đầu quá trình tải dữ liệu từ thư mục '{DATA_FOLDER}'...")
    
    # Lấy danh sách file CSV và sắp xếp
    csv_files = sorted([f for f in os.listdir(DATA_FOLDER) if f.endswith(".csv")])
    
    if not csv_files:
        print(f"[{time.strftime('%H:%M:%S')}] CẢNH BÁO: Không tìm thấy file CSV nào trong thư mục '{DATA_FOLDER}'.")
        return
    
    print(f"[{time.strftime('%H:%M:%S')}] Tìm thấy {len(csv_files)} file CSV để xử lý.")
    
    for filename in csv_files:
        filepath = os.path.join(DATA_FOLDER, filename)
        table_name = filename.replace(".csv", "").lower()
        
        print("-" * 50)
        print(f"[{time.strftime('%H:%M:%S')}] Đang xử lý file: {filename} -> Tải vào bảng: {table_name}")
        
        try:
            # Đọc CSV với encoding utf-8, nếu lỗi thử latin1
            try:
                df = pd.read_csv(filepath, encoding='utf-8')
            except UnicodeDecodeError:
                print(f"[{time.strftime('%H:%M:%S')}] Thử đọc với encoding latin1...")
                df = pd.read_csv(filepath, encoding='latin1')
            
            # Chuẩn hóa tên cột
            df.columns = [col.lower().strip().replace(' ', '_').replace('-', '_') for col in df.columns]
            
            # Loại bỏ các ký tự đặc biệt trong tên cột
            df.columns = [''.join(c if c.isalnum() or c == '_' else '_' for c in col) for col in df.columns]
            
            print(f"[{time.strftime('%H:%M:%S')}] Số lượng dòng được đọc: {len(df)}")
            print(f"[{time.strftime('%H:%M:%S')}] Các cột: {', '.join(df.columns)}")
            
            # Xử lý giá trị null
            df = df.where(pd.notnull(df), None)
            
            start_time = time.time()
            
            # Tạo connection string để truyền trực tiếp vào to_sql
            
            db_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}?charset=utf8mb4"
            engine = create_engine(db_url)
            
            df.to_sql(
                name=table_name,
                con=engine,
                if_exists='replace',
                index=False,
                chunksize=5000
            )
            
            end_time = time.time()
            
            print(f"[{time.strftime('%H:%M:%S')}] HOÀN THÀNH. Đã tải {len(df)} dòng vào bảng '{table_name}'.")
            print(f"[{time.strftime('%H:%M:%S')}] Thời gian tải: {end_time - start_time:.2f} giây.")

        except ProgrammingError as e:
            print(f"[{time.strftime('%H:%M:%S')}] LỖI SQL khi tải '{filename}': {e}")
        except pd.errors.EmptyDataError:
            print(f"[{time.strftime('%H:%M:%S')}] LỖI: File '{filename}' rỗng hoặc không có dữ liệu.")
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] LỖI chung khi xử lý '{filename}': {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    try:
        # Bước 1: Tạo engine kết nối
        mysql_engine = create_db_engine()
        
        # Bước 2: Tải dữ liệu
        if mysql_engine:
            load_csv_to_mysql(mysql_engine)
            print(f"\n[{time.strftime('%H:%M:%S')}] Quá trình tải dữ liệu hoàn tất.")
            
            # Đóng engine
            mysql_engine.dispose()
            
    except ConnectionError as e:
        print(f"\n[{time.strftime('%H:%M:%S')}] THẤT BẠI: {e}")
    except Exception as e:
        print(f"\n[{time.strftime('%H:%M:%S')}] Đã xảy ra lỗi không xác định: {e}")
        import traceback
        traceback.print_exc()