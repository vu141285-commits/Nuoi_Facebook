import os
import time
import random
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Đường dẫn đến thư mục chứa các folder ID số của bạn
root_path = r"C:\Users\Administrator\Desktop\ACC MOI\ACC MOI" 

# BẮT ĐẦU VÒNG LẶP XOAY VÒNG VÔ HẠN
vong_lap = 1
while True:
    print(f"\n=========================================")
    print(f" BẮT ĐẦU CHẠY VÒNG LẶP THỨ: {vong_lap}")
    print(f"=========================================")

    # Lọc chỉ lấy các folder có tên hoàn toàn là chữ số (UID)
    profiles = [
        d for d in os.listdir(root_path) 
        if os.path.isdir(os.path.join(root_path, d)) and d.isdigit()
    ]

    print(f"Tìm thấy {len(profiles)} tài khoản. Tiến hành CHẠY LẦN LƯỢT phiên bản FIX THẢ TIM MÀN HÌNH NHỎ...")

    for index, profile_id in enumerate(profiles, start=1):
        full_profile_path = os.path.join(root_path, profile_id)
        print(f"\n[{index}/{len(profiles)}] ===> Đang mở tài khoản: {profile_id}")
        
        options = Options()
        options.add_argument(f"--user-data-dir={full_profile_path}")
        
        # Kích thước thu nhỏ gọn của bạn
        options.add_argument("--window-size=500,700")  
       # options.add_argument("--window-position=1200,0") 
        
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-notifications") 

        driver = webdriver.Edge(options=options)
        
        try:
            # ================= KỊCH BẢN 1: XEM BÀI VIẾT (10 - 15 GIÂY) =================
            print("   -> [BƯỚC 1] Truy cập Trang chủ lướt xem bài viết...")
            driver.get("https://www.facebook.com")
            time.sleep(random.uniform(4, 6))
            
            feed_duration = random.randint(25, 35)
            feed_start = time.time()
            while time.time() - feed_start < feed_duration:
                body = driver.find_element(By.TAG_NAME, "body")
                body.send_keys(Keys.PAGE_DOWN)
                time.sleep(random.uniform(3, 5))
                
            print("   -> Hoàn thành lướt xem bài viết Newsfeed.")
            time.sleep(2)

            # ================= KỊCH BẢN 2: XEM VIDEO WATCH & THẢ CẢM XÚC (1 - 3 PHÚT) =================
            print("   -> [BƯỚC 2] Chuyển sang mục Facebook Watch...")
            driver.get("https://www.facebook.com/watch")
            time.sleep(random.uniform(4, 6)) 
            
            watch_duration = random.randint(10, 15)
            print(f"   -> S xem video .")
            watch_start = time.time()
            has_liked = False 
            
            while time.time() - watch_start < watch_duration:
                body = driver.find_element(By.TAG_NAME, "body")
                body.send_keys(Keys.PAGE_DOWN)
                time.sleep(random.uniform(6, 12))
                
                # Thả cảm xúc ngẫu nhiên
                if not has_liked and random.choice([True, False, False]): 
                    try:
                        like_buttons = driver.find_elements(By.XPATH, (
                          #  "//div[@role='button' and @aria-label='Thích'] | "
                          #  "//div[@role='button' and @aria-label='Like'] | "
                           # "//div[@role='button' and contains(@aria-label, 'Thích')] | "
                           # "//div[@role='button' and contains(@aria-label, 'Like')] | "
                           # "//span[text()='Thích' or text()='Like']/ancestor::div[@role='button']"
                        ))
                        
                        if like_buttons:
                            target_btn = random.choice(like_buttons)
                            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_btn)
                            time.sleep(1.5)
                            driver.execute_script("arguments[0].click();", target_btn)
                            print("   -> [TƯƠNG TÁC OK] Đã ép click thả cảm xúc thành công trên giao diện nhỏ!")
                            has_liked = True
                    except Exception as ex:
                        pass
                        
            print(f"   -> Đã hoàn thành toàn bộ kịch bản nuôi cho nick: {profile_id}.")
            
        except Exception as e:
            print(f"   -> Gặp lỗi tại nick {profile_id}: {e}")
            
        finally:
            print(f"   -> Đóng trình duyệt nick {profile_id}. Chờ chuyển nick...")
            driver.quit()
            time.sleep(random.uniform(4, 7))

    print(f"\n=== HOÀN THÀNH VÒNG LẶP THỨ {vong_lap}. Nghỉ một lát trước khi xoay vòng tiếp... ===")
    vong_lap += 1
    time.sleep(1)  # Nghỉ 1 phút giữa các vòng chạy (bạn có thể chỉnh lại thời gian này)
