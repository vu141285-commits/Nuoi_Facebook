import requests
import os
import re
import json
import random
import base64
import uuid
import time
from datetime import datetime
import platform
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.live import Live
from rich.spinner import Spinner
from rich.prompt import Prompt
from rich.table import Table

try:
    from pystyle import Add, Center, Anime, Colors, Colorate, Write, System
except:
    os.system('pip install pystyle requests platform colorama beautifulsoup4 selenium mechanize webdriver_manager aiohttp flask')
    from pystyle import Add, Center, Anime, Colors, Colorate, Write, System

try:
    import pyfiglet
    from termcolor import colored
except:
    os.system('pip install pyfiglet termcolor')
    import pyfiglet
    from termcolor import colored

console = Console()

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def banner():    
    clear()    
    # Tạo chữ TINH 89 bằng pyfiglet
    ascii_text = pyfiglet.figlet_format("TINH 89", font="slant")    
    
    # Tạo nội dung hiển thị trong Panel
    title = Text(ascii_text, style="bold cyan")    
    subtitle = Text("HỆ THỐNG NUÔI FACEBOOK VIP\nTÁC GIẢ: TINH 89", style="bold white", justify="center")    
    
    # Định nghĩa Panel (Khung chứa)
    panel = Panel(    
        Align.center(title + "\n" + subtitle, vertical="middle"),    
        border_style="cyan",    
        padding=(1, 4),    
        title="🔥 TINH 89 VIP 🔥",    
        subtitle="NÂNG CẤP HỆ THỐNG"    
    )    
    
    # In banner ra màn hình đúng 1 lần duy nhất
    console.print(panel)

    with Live(panel, refresh_per_second=10):    
        time.sleep(1)    
    
def doi_giay(value, random_delay=False):
    if random_delay:
        value = random.randint(value // 2, value * 2)
        
    with Live(refresh_per_second=1, transient=True) as live:
        for i in range(value, 0, -1):
            live.update(f"[bold yellow]⏳ Đang đợi {i} giây để tránh spam...[/]")
            time.sleep(1)
        
def kiem_tra_cookie(cookie):
    try:
        if 'c_user=' not in cookie:
            return {"status": "failed", "msg": "Cookie không chứa user_id"}

        user_id = cookie.split('c_user=')[1].split(';')[0]
        url = f"https://graph2.facebook.com/v3.3/{user_id}/picture?redirect=0"
        response = requests.get(url, timeout=30)
        check_data = response.json()

        if not check_data.get('data', {}).get('height') or not check_data.get('data', {}).get('width'):
            return {"status": "failed", "msg": "Cookie không hợp lệ"}

        headers = {
            'authority': 'm.facebook.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'vi-VN,vi;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': cookie,
            'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"0.1.0"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        }

        profile_response = requests.get(f'https://m.facebook.com/profile.php?id={user_id}', headers=headers, timeout=30)
        name = profile_response.text.split('<title>')[1].split('<')[0].strip()

        return {
            "status": "success",
            "name": name,
            "user_id": user_id,
            "msg": "successful"
        }
    except Exception as e:
        return {"status": "failed", "msg": f"Lỗi xảy ra: {str(e)}"}


def generate_vietnamese_names(
    count=5000,
    gender="random",   # "male", "female", "random"
    seed=None,
    with_gender=False
):
    if seed is not None:
        random.seed(seed)

    # Họ + trọng số (thực tế hơn)
    ho = [
        ("Nguyễn", 0.38), ("Trần", 0.12), ("Lê", 0.09), ("Phạm", 0.07),
        ("Hoàng", 0.05), ("Vũ", 0.04), ("Đặng", 0.03), ("Bùi", 0.03),
        ("Đỗ", 0.02), ("Hồ", 0.02), ("Ngô", 0.02), ("Dương", 0.02),
        ("Lý", 0.01), ("Võ", 0.01), ("Đinh", 0.01), ("Phan", 0.01),
        ("Trương", 0.01), ("Huỳnh", 0.01), ("Khác", 0.05)
    ]

    ho_names = [h[0] for h in ho]
    ho_weights = [h[1] for h in ho]

    ten_dem_male = [
        'Văn','Đức','Hữu','Minh','Quang','Gia','Anh','Xuân','Trung','Thanh',
        'Công','Thành','Bảo','Hoàng','Khánh','Tuấn','Trọng','Đình'
    ]

    ten_dem_female = [
        'Thị','Ngọc','Thu','Mai','Diệu','Kim','Bích','Thanh','Phương',
        'Thảo','Hồng','Tuyết','Ánh','Quỳnh','Minh','Trúc'
    ]

    ten_male = [
        'An','Bình','Cường','Duy','Hải','Hùng','Khang','Long','Minh','Nam',
        'Phúc','Quân','Sơn','Thắng','Tuấn','Tùng','Việt','Vinh','Đạt','Hiếu',
        'Khôi','Phong','Lâm','Tài','Hào'
    ]

    ten_female = [
        'Anh','Châu','Dung','Hà','Hương','Lan','Linh','Mai','Ngọc','Nhi',
        'Oanh','Phương','Quỳnh','Thảo','Trang','Tú','Uyên','Vy','Yến','Hoa',
        'Diễm','Trâm','Như','Tiên'
    ]

    names = set()
    results = []

    while len(names) < count:
        ho_r = random.choices(ho_names, weights=ho_weights, k=1)[0]

        g = gender
        if g == "random":
            g = random.choice(["male", "female"])

        if g == "male":
            dem_list = ten_dem_male
            ten_list = ten_male
        else:
            dem_list = ten_dem_female
            ten_list = ten_female

        # Quyết định số chữ (2–4 chữ)
        length_type = random.random()

        if length_type < 0.2:
            # 2 chữ
            name = f"{ho_r} {random.choice(ten_list)}"

        elif length_type < 0.9:
            # 3 chữ (phổ biến)
            name = f"{ho_r} {random.choice(dem_list)} {random.choice(ten_list)}"

        else:
            # 4 chữ (hiếm)
            name = f"{ho_r} {random.choice(dem_list)} {random.choice(dem_list)} {random.choice(ten_list)}"

        if name not in names:
            names.add(name)
            if with_gender:
                results.append((name, g))
            else:
                results.append(name)

    return results
    
    
def generate_random_comment(level="mixed"):
    # Tone
    tones = {
        "positive": 0.6,
        "neutral": 0.3,
        "light_negative": 0.1
    }

    if level == "positive":
        tone = "positive"
    elif level == "negative":
        tone = "light_negative"
    else:
        tone = random.choices(list(tones.keys()), weights=tones.values())[0]

    openings = [
        "Mình thấy", "Theo mình", "Cá nhân mình nghĩ",
        "Nói thật", "Thật sự thì", "Không biết mọi người sao nhưng mình thấy",
        "Xem xong thì", "Vừa xem xong"
    ]

    subjects = [
        "bài này", "video này", "nội dung này",
        "chủ đề này", "post này", "cái này"
    ]

    positives = [
        "rất hay", "cực kỳ hữu ích", "khá thú vị",
        "ổn áp", "ấn tượng", "đáng để thử",
        "xịn thật", "chất lượng"
    ]

    neutrals = [
        "cũng ổn", "khá bình thường",
        "không tệ", "tạm được",
        "cũng có vài điểm hay"
    ]

    negatives = [
        "chưa thuyết phục lắm",
        "hơi chung chung",
        "chưa đủ sâu",
        "còn thiếu chi tiết",
        "xem hơi nhanh hiểu"
    ]

    endings = [
        "mọi người nên xem thử",
        "mình học được khá nhiều",
        "cũng đáng để tham khảo",
        "hy vọng có phần tiếp theo",
        "ai rảnh có thể xem",
        "xem giải trí cũng ổn",
        "mong là sẽ cải thiện thêm"
    ]

    emojis_map = {
        "positive": ["🔥", "💯", "👍", "✨"],
        "neutral": ["🙂", ""],
        "light_negative": ["😅", "🤔", ""]
    }

    # chọn thành phần theo tone
    opening = random.choice(openings)
    subject = random.choice(subjects)

    if tone == "positive":
        adj = random.choice(positives)
    elif tone == "neutral":
        adj = random.choice(neutrals)
    else:
        adj = random.choice(negatives)

    ending = random.choice(endings)
    emoji = random.choice(emojis_map[tone])

    # ---- BIẾN THỂ CÂU (anti-bot) ----
    structures = [
        f"{opening} {subject} {adj}, {ending}.",
        f"{subject.capitalize()} {adj}. {opening} {ending}.",
        f"{opening} thì {subject} {adj}. {ending}.",
        f"{subject.capitalize()} mình thấy {adj}, {ending}.",
        f"{adj.capitalize()} luôn, {subject}. {ending}.",
    ]

    comment = random.choice(structures)

    # ---- RANDOM SHORT / LONG ----
    if random.random() < 0.3:
        comment = f"{subject.capitalize()} {adj}."

    # ---- THÊM EMOJI (30% chance) ----
    if emoji and random.random() < 0.5:
        comment += " " + emoji

    # ---- TYPO NHẸ (giống người thật) ----
    if random.random() < 0.1:
        comment = comment.replace("không", "ko").replace("mọi người", "mn")

    return comment
    

class Facebook:
    def __init__(self, cookie: str):
        self.fb_dtsg = ''
        self.jazoest = ''
        self.cookie = cookie
        self.session = requests.Session()
        self.id = self.cookie.split('c_user=')[1].split(';')[0]
        self.commented_posts = set()
        
        # ================= CHUYỂN TOÀN BỘ SANG GIẢ LẬP MOBILE =================
        self.headers = {
            'authority': 'm.facebook.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'vi-VN,vi;q=0.9',
            'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="124", "Chromium";v="124"',
            'sec-ch-ua-mobile': '?1',  # Xác định là thiết bị di động
            'sec-ch-ua-platform': '"Android"',  # Chuyển hệ điều hành sang Android khớp với phone
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            # Dùng UA của thiết bị di động phổ biến
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
            'Cookie': self.cookie
        }
        try:
            # Chuyển hướng lấy mã token dtsg từ giao diện m.facebook.com thay vì www
            url = self.session.get(f'https://m.facebook.com/{self.id}', headers=self.headers).url
            response = self.session.get(url, headers=self.headers).text
            
            # Cập nhật regex quét mã phù hợp với cấu trúc m.facebook
            matches = re.findall(r'\["DTSGInitialData",\[\],\{"token":"(.*?)"\}', response)
            if len(matches) > 0:
                self.fb_dtsg += matches[0]
                self.jazoest += re.findall(r'jazoest=(.*?)\"', response)[0]
        except:
            pass

    def info(self):
        try:
            get = self.session.get('https://www.facebook.com/me', headers=self.headers).url
            url = 'https://www.facebook.com/' + get.split('%2F')[-2] + '/' if 'next=' in get else get
            response = self.session.get(url, headers=self.headers, params={"locale": "vi_VN"})
            data_split = response.text.split('"CurrentUserInitialData",[],{')
            json_data = '{' + data_split[1].split('},')[0] + '}'
            parsed_data = json.loads(json_data)
            id = parsed_data.get('USER_ID', '0')
            name = parsed_data.get('NAME', '')
            if id == '0' and name == '':
                return 'cookieout'
            elif '828281030927956' in response.text:
                return '956'
            elif '1501092823525282' in response.text:
                return '282'
            elif '601051028565049' in response.text:
                return 'spam'
            else:
                id, name = parsed_data.get('USER_ID'), parsed_data.get('NAME')
                return {'success': 200, 'id': id, 'name': name}
        except:
            return 'cookieout'

    def tim_ban(self, text):
        try:
            data = {
                'av': self.id,
                'fb_dtsg': self.fb_dtsg,
                'jazoest': self.jazoest,
                'fb_api_caller_class': 'RelayModern',
                'fb_api_req_friendly_name': 'SearchCometResultsInitialResultsQuery',
                'variables': '{"count":5,"allow_streaming":false,"args":{"callsite":"COMET_GLOBAL_SEARCH","config":{"exact_match":false,"high_confidence_config":null,"intercept_config":null,"sts_disambiguation":null,"watch_config":null},"context":{"bsid":"23bd9138-cec6-4e71-aaeb-225fc8964e5b","tsid":"0.10477759801522946"},"experience":{"client_defined_experiences":["ADS_PARALLEL_FETCH"],"encoded_server_defined_params":null,"fbid":null,"type":"GLOBAL_SEARCH"},"filters":[],"text":"'+text+'"},"cursor":null,"feedbackSource":23,"fetch_filters":true,"renderLocation":"search_results_page","scale":1,"stream_initial_count":0,"useDefaultActor":false,"__relay_internal__pv__GHLShouldChangeAdIdFieldNamerelayprovider":true,"__relay_internal__pv__GHLShouldChangeSponsoredDataFieldNamerelayprovider":true,"__relay_internal__pv__IsWorkUserrelayprovider":false,"__relay_internal__pv__FBReels_deprecate_short_form_video_context_gkrelayprovider":true,"__relay_internal__pv__CometFeedStoryDynamicResolutionPhotoAttachmentRenderer_experimentWidthrelayprovider":500,"__relay_internal__pv__CometImmersivePhotoCanUserDisable3DMotionrelayprovider":false,"__relay_internal__pv__WorkCometIsEmployeeGKProviderrelayprovider":false,"__relay_internal__pv__IsMergQAPollsrelayprovider":false,"__relay_internal__pv__FBReelsMediaFooter_comet_enable_reels_ads_gkrelayprovider":true,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false,"__relay_internal__pv__CometUFIShareActionMigrationrelayprovider":true,"__relay_internal__pv__CometUFI_dedicated_comment_routable_dialog_gkrelayprovider":false,"__relay_internal__pv__StoriesArmadilloReplyEnabledrelayprovider":true,"__relay_internal__pv__FBReelsIFUTileContent_reelsIFUPlayOnHoverrelayprovider":false}',
                'server_timestamps': 'true',
                'doc_id': '9545374252239656'
            }
            response = self.session.post('https://www.facebook.com/api/graphql/', headers=self.headers, data=data).json()
            profile = response["data"]["serpResponse"]["results"]["edges"][0]['rendering_strategy']['result_rendering_strategies'][0]['view_model']['profile']
            name = profile.get('name')
            uid = profile.get('id')
            return {'status': 'success', 'id': uid, 'name': name}
        except:
            return {'status': 'error', 'trangthai': 'thatbai'}

    def ket_ban(self, idkb):
        try:
            data = {
                'av': self.id,
                'fb_dtsg': self.fb_dtsg,
                'jazoest': self.jazoest,
                'fb_api_caller_class': 'RelayModern',
                'fb_api_req_friendly_name': 'FriendingCometFriendRequestSendMutation',
                'variables': '{"input":{"attribution_id_v2":"ProfileCometTimelineListViewRoot.react,comet.profile.timeline.list,unexpected,1748257667487,475021,190055527696468,,;SearchCometGlobalSearchDefaultTabRoot.react,comet.search_results.default_tab,tap_search_bar,1748257603766,498383,391724414624676,,","click_proof_validation_result":null,"friend_requestee_ids":["'+idkb+'"],"friending_channel":"PROFILE_BUTTON","warn_ack_for_ids":[],"actor_id":"'+self.id+'","client_mutation_id":"6"},"scale":1}',
                'server_timestamps': 'true',
                'doc_id': '8805328442902902'
            }
            response = self.session.post('https://www.facebook.com/api/graphql/', headers=self.headers, data=data).json()
            trangthai = response["data"]["friend_request_send"]["friend_requestees"]
            if trangthai and trangthai[0].get('friendship_status') == 'OUTGOING_REQUEST':
                return {'status': 'success', 'trangthai': 'thanhcong'}
            else:
                return {'status': 'error', 'trangthai': 'thatbai'}
        except:
            return {'status': 'error', 'trangthai': 'thatbai'}

    def lay_id_bai_viet(self):
        try:
            variables = {
                "RELAY_INCREMENTAL_DELIVERY": True,
                "clientQueryId": "b7876288-8582-4b5a-9420-76f62adfe671",
                "count": 10,
                "cursor": None,
                "feedLocation": "NEWSFEED",
                "feedStyle": "DEFAULT",
                "orderby": ["TOP_STORIES"],
                "renderLocation": "homepage_stream",
                "scale": 1,
                "useDefaultActor": False
            }
            data = {
                'av': self.id,
                'fb_dtsg': self.fb_dtsg,
                'jazoest': self.jazoest,
                'fb_api_caller_class': 'RelayModern',
                'fb_api_req_friendly_name': 'CometNewsFeedPaginationQuery',
                'variables': json.dumps(variables),
                'server_timestamps': 'true',
                'doc_id': '29492828377027602'
            }
            response = self.session.post('https://www.facebook.com/api/graphql/', headers=self.headers, data=data).text
            post_ids = re.findall(r'"post_id":"(\d+)"', response)
            if post_ids:
                for post_id in post_ids:
                    if post_id not in self.commented_posts:
                        return {'status': 'success', 'idpost': post_id}
                self.commented_posts.clear()
                return {'status': 'success', 'idpost': post_ids[0]}
            return {'status': 'error', 'trangthai': 'thatbai'}
        except:
            return {'status': 'error', 'trangthai': 'thatbai'}

    def tha_cam_xuc(self, id, type):
        try:
            reac = {
                "LIKE": "1635855486666999",
                "LOVE": "1678524932434102",
                "CARE": "613557422527858",
                "HAHA": "115940658764963",
                "WOW": "478547315650144",
                "SAD": "908563459236466",
                "ANGRY": "444813342392137"
            }
            idreac = reac.get(type)
            data = {
                'av': self.id,
                'fb_dtsg': self.fb_dtsg,
                'jazoest': self.jazoest,
                'fb_api_caller_class': 'RelayModern',
                'fb_api_req_friendly_name': 'CometUFIFeedbackReactMutation',
                'variables': f'{{"input":{{"attribution_id_v2":"CometHomeRoot.react,comet.home,tap_tabbar,1719027162723,322693,4748854339,,","feedback_id":"{base64.b64encode(f"feedback:{str(id)}".encode()).decode()}","feedback_reaction_id":"{idreac}","feedback_source":"NEWS_FEED","is_tracking_encrypted":true,"tracking":["AZWUDdylhKB7Q-Esd2HQq9i7j4CmKRfjJP03XBxVNfpztKO0WSnXmh5gtIcplhFxZdk33kQBTHSXLNH-zJaEXFlMxQOu_JG98LVXCvCqk1XLyQqGKuL_dCYK7qSwJmt89TDw1KPpL-BPxB9qLIil1D_4Thuoa4XMgovMVLAXncnXCsoQvAnchMg6ksQOIEX3CqRCqIIKd47O7F7PYR1TkMNbeeSccW83SEUmtuyO5Jc_wiY0ZrrPejfiJeLgtk3snxyTd-JXW1nvjBRjfbLySxmh69u-N_cuDwvqp7A1QwK5pgV49vJlHP63g4do1q6D6kQmTWtBY7iA-beU44knFS7aCLNiq1aGN9Hhg0QTIYJ9rXXEeHbUuAPSK419ieoaj4rb_4lA-Wdaz3oWiWwH0EIzGs0Zj3srHRqfR94oe4PbJ6gz5f64k0kQ2QRWReCO5kpQeiAd1f25oP9yiH_MbpTcfxMr-z83luvUWMF6K0-A-NXEuF5AiCLkWDapNyRwpuGMs8FIdUJmPXF9TGe3wslF5sZRVTKAWRdFMVAsUn-lFT8tVAZVvd4UtScTnmxc1YOArpHD-_Lzt7NDdbuPQWQohqkGVlQVLMoJNZnF_oRLL8je6-ra17lJ8inQPICnw7GP-ne_3A03eT4zA6YsxCC3eIhQK-xyodjfm1j0cMvydXhB89fjTcuz0Uoy0oPyfstl7Sm-AUoGugNch3Mz2jQAXo0E_FX4mbkMYX2WUBW2XSNxssYZYaRXC4FUIrQoVhAJbxU6lomRQIPY8aCS0Ge9iUk8nHq4YZzJgmB7VnFRUd8Oe1sSSiIUWpMNVBONuCIT9Wjipt1lxWEs4KjlHk-SRaEZc_eX4mLwS0RcycI8eXg6kzw2WOlPvGDWalTaMryy6QdJLjoqwidHO21JSbAWPqrBzQAEcoSau_UHC6soSO9UgcBQqdAKBfJbdMhBkmxSwVoxJR_puqsTfuCT6Aa_gFixolGrbgxx5h2-XAARx4SbGplK5kWMw27FpMvgpctU248HpEQ7zGJRTJylE84EWcVHMlVm0pGZb8tlrZSQQme6zxPWbzoQv3xY8CsH4UDu1gBhmWe_wL6KwZJxj3wRrlle54cqhzStoGL5JQwMGaxdwITRusdKgmwwEQJxxH63GvPwqL9oRMvIaHyGfKegOVyG2HMyzmiQmtb5EtaFd6n3JjMCBF74Kcn33TJhQ1yjHoltdO_tKqnj0nPVgRGfN-kdJA7G6HZFvz6j82WfKmzi1lgpUcoZ5T8Fwpx-yyBHV0J4sGF0qR4uBYNcTGkFtbD0tZnUxfy_POfmf8E3phVJrS__XIvnlB5c6yvyGGdYvafQkszlRrTAzDu9pH6TZo1K3Jc1a-wfPWZJ3uBJ_cku-YeTj8piEmR-cMeyWTJR7InVB2IFZx2AoyElAFbMuPVZVp64RgC3ugiyC1nY7HycH2T3POGARB6wP4RFXybScGN4OGwM8e3W2p-Za1BTR09lHRlzeukops0DSBUkhr9GrgMZaw7eAsztGlIXZ_4"],"session_id":"{uuid.uuid4()}","actor_id":"{self.id}","client_mutation_id":"3"}},"useDefaultActor":false,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false}}',
                'server_timestamps': 'true',
                'doc_id': '7047198228715224'
            }
            response = self.session.post('https://www.facebook.com/api/graphql/', headers=self.headers, data=data)
            if '{"data":{"feedback_react":{"feedback":{"id":' in response.text:
                return {'status': 'success', 'trangthai': 'thanhcong'}
            else:
                return {'status': 'error', 'trangthai': 'thatbai'}
        except:
            return {'status': 'error', 'trangthai': 'thatbai'}

    def binh_luan(self, id, msg):
        try:
            feedback_id = base64.b64encode(f"feedback:{id}".encode()).decode()
            data = {
                'av': self.id,
                'fb_dtsg': self.fb_dtsg,
                'jazoest': self.jazoest,
                'fb_api_caller_class': 'RelayModern',
                'fb_api_req_friendly_name': 'useCometUFICreateCommentMutation',
                'variables': f'{{"feedLocation":"DEDICATED_COMMENTING_SURFACE","feedbackSource":110,"groupID":null,"input":{{"client_mutation_id":"4","actor_id":"{self.id}","attachments":null,"feedback_id":"{feedback_id}","formatting_style":null,"message":{{"ranges":[],"text":"{msg}"}},"attribution_id_v2":"CometHomeRoot.react,comet.home,via_cold_start,1718688700413,194880,4748854339,,","vod_video_timestamp":null,"feedback_referrer":"/","is_tracking_encrypted":true,"tracking":["AZX1ZR3ETYfGknoE2E83CrSh9sg_1G8pbUK70jA-zjEIcfgLxA-C9xuQsGJ1l2Annds9fRCrLlpGUn0MG7aEbkcJS2ci6DaBTSLMtA78T9zR5Ys8RFc5kMcx42G_ikh8Fn-HLo3Qd-HI9oqVmVaqVzSasZBTgBDojRh-0Xs_FulJRLcrI_TQcp1nSSKzSdTqJjMN8GXcT8h0gTnYnUcDs7bsMAGbyuDJdelgAlQw33iNoeyqlsnBq7hDb7Xev6cASboFzU63nUxSs2gPkibXc5a9kXmjqZQuyqDYLfjG9eMcjwPo6U9i9LhNKoZwlyuQA7-8ej9sRmbiXBfLYXtoHp6IqQktunSF92SdR53K-3wQJ7PoBGLThsd_qqTlCYnRWEoVJeYZ9fyznzz4mT6uD2Mbyc8Vp_v_jbbPWk0liI0EIm3dZSk4g3ik_SVzKuOE3dS64yJegVOQXlX7dKMDDJc7P5Be6abulUVqLoSZ-cUCcb7UKGRa5MAvF65gz-XTkwXW5XuhaqwK5ILPhzwKwcj3h-Ndyc0URU_FJMzzxaJ9SDaOa9vL9dKUviP7S0nnig0sPLa5KQgx81BnxbiQsAbmAQMr2cxYoNOXFMmjB_v-amsNBV6KkES74gA7LI0bo56DPEA9smlngWdtnvOgaqlsaSLPcRsS0FKO3qHAYNRBwWvMJpJX8SppIR1KiqmVKgeQavEMM6XMElJc9PDxHNZDfJkKZaYTJT8_qFIuFJVqX6J9DFnqXXVaFH4Wclq8IKZ01mayFbAFbfJarH28k_qLIxS8hOgq9VKNW5LW7XuIaMZ1Z17XlqZ96HT9TtCAcze9kBS9kMJewNCl-WYFvPCTCnwzQZ-HRVOM04vrQOgSPud7vlA3OqD4YY2PSz_ioWSbk98vbJ4c7WVHiFYwQsgQFvMzwES20hKPDrREYks5fAPVrHLuDK1doffY1PTWF2KkSt0uERAcZIibeD5058uKSonW1fPurOnsTpAg8TfALFu1QlkcNt1X4dOoGpYmBR7HGIONwQwv5-peC8F758ujTTWWowBqXzJlA2boriCvdZkvS15rEnUN57lyO8gINQ5heiMCQN8NbHMmrY_ihJD3bdM4s2TGnWH4HBC2hi0jaIOJ8AoCXHQMaMdrGE1st7Y3R_T6Obg6VnabLn8Q-zZfToKdkiyaR9zqsVB8VsMrAtEz0yiGpaOF3KdI2sxvii3Q5XWIYN6gyDXsXVykFS25PsjPmXCF8V1mS7x6e9N9PtNTWwT8IGBZp9frOTQN2O52dOhPdsuCHAf0srrBVHbyYfCMYbOqYEEXQG0pNAmG_wqbTxNew9kTsXDRzYKW-NmEJcvy_xh1dDwg8xJc58Cl71e-rau3iP7o8mWhVSaxi4Bi6LAuj4UKVCt3IYCfm9AR1d5LqBFWU9LrJbRZSMlmUYwZf7PlrKmpnCnZvuismiL7DH3cnUjP0lWAvhy3gxZm1MK8KyRzWmHnTNqaVlL37c2xoE4YSyponeOu5D-lRl_Dp_C2PyR1kG6G0TCWS66UbU89Fu1qmwWjeQwYhzj2Jly9LRyClAbe86VJhIZE18YLPB-n1ng78qz7hHtQ8qT4ejY4csEjSRjjnHdz8U-06qErY-CXNNsVtzpYGuzZ1ZaXqzAQkUcREm98KR8c1vaXaQXumtDklMVgs76gLqZyiG1eCRbOQ6_EcQv7GeFnq5UIqoMH_Xzc78otBTvC5j3aCs5Pvf6k3gQ5ZU7E4uFVhZA7xoyD8sPX6rhdGL8JmLKJSGZQM5ccWpfpDJ5RWJp0bIJdnAJQ8gsYMRAI2OBxx2m2c76lNiUnB750dMe2H3pFzFQVkWQLkmGVY37cgmRNHyXboDMQU2nlbNH017dmklJCk4jVU8aA9Gpo8oHw","{{"assistant_caller":"comet_above_composer","conversation_guide_session_id":"{uuid.uuid4()}","conversation_guide_shown":null}}"],"feedback_source":"DEDICATED_COMMENTING_SURFACE","idempotence_token":"client:{uuid.uuid4()}","session_id":"{uuid.uuid4()}"}},"inviteShortLinkKey":null,"renderLocation":null,"scale":1,"useDefaultActor":false,"focusCommentID":null}}',
                'server_timestamps': 'true',
                'doc_id': '24323081780615819'
            }
            cmt_response = self.session.post('https://www.facebook.com/api/graphql/', headers=self.headers, data=data)
            if cmt_response.status_code != 200:
                return {'status': 'error', 'trangthai': 'thatbai', 'error': f'HTTP {cmt_response.status_code}'}
            cmt_json = cmt_response.json()
            response_str = str(cmt_json)
            if ('"feedback_submitted":true' in response_str or 
                'create_comment' in response_str or
                'comment_create' in response_str or
                'success' in response_str.lower() or
                'error' not in response_str):
                self.commented_posts.add(id)
                return {'status': 'success', 'trangthai': 'thanhcong'}
            else:
                return {'status': 'error', 'trangthai': 'thatbai', 'response': cmt_json}
        except:
            return {'status': 'error', 'trangthai': 'thatbai'}

    def tim_nhom(self, keyword):
        try:
            data = {
                'av': self.id,
                'fb_dtsg': self.fb_dtsg,
                'jazoest': self.jazoest,
                'fb_api_caller_class': 'RelayModern',
                'fb_api_req_friendly_name': 'SearchCometResultsInitialResultsQuery',
                'variables': '{"allow_streaming":false,"args":{"callsite":"COMET_GLOBAL_SEARCH","config":{"exact_match":false,"high_confidence_config":null,"intercept_config":null,"sts_disambiguation":null,"watch_config":null},"context":{"bsid":"435c49d4-a957-431e-834f-d1da37a5f10b","tsid":"0.37005625332226133"},"experience":{"client_defined_experiences":["ADS_PARALLEL_FETCH"],"encoded_server_defined_params":null,"fbid":null,"type":"GROUPS_TAB"},"filters":[],"text":"'+keyword+'"},"count":5,"cursor":"AboQDCkcpXHJTbFDxObZS3n0GamptQsxZrcXlcMFwGKIy8t_OUZV16uazBcCgVOMdao8EgVEpXIG4MarCu1ndTCT45yz6IlSEOoYZsWeqF88dZnyorpLHnwlfVTjfYgLOTH6ehf3WNbEtWS0QH3J4A4edpfakj35aqL9swaRPEe1KSYtaF_h7wjzfta_lLSzyM3JvI6JxKyZmMZJ_DAnhJw3MvQE5zgckZpVwJLHeYmG38bV6CQOTaa2hI8PY1xq5segTD2TAZZ-GJASsyGbZ8iJnjhT1MrtF5v5t_l4X4k1XXHs8woxmR1hmLVRhQGcXcwIms5_kCPaVPGE_ZBqvDGtoSq1vzx5qDIx49eXD-frk0ESlo_Nvj7ix7sXrHDZRpmA2ljWLZjmOXChNzGltKw7KekWeE0BrynOmH7k-L9pu85PJ5MVHm3uR-fFZWx8ytKb5DDwo1vN-pylOwsXs9MYR394Hcv8P4s9k90a4wqcsMHBNQmrcFO4Ab6nXcveCvFVWrF1hAEI0n9F69ye-QIy048hbmveTYV13UOLB5yrVWmAAYDuDlSS64-fHXNziJue641DOHnCxSOdPkKI6tCGm01UQgDJynSG56qtcF9HL8snD_5gZ9sDvqD8VCl-23LbiwRe2WjKrjUPaJmkk1fVLzXPrR8DURyrqHB5WBkE-Tn1idUEZaFMdKn2SSpdGB-9TIGrSWveurlC3483IkPkLveq2s0pr68FPPLMMO7Bk9art2BvG9JwszZjnQ8KjnDCmnUX1a71iCwM_iLnbuENJvWZtEO4Rjqu4XwqRtMWhc9RPZvKOaJY9L2e4DLvZbbARN0o-dS78Epa77LB-Th84FXyTs7KrZ_X57DwMjrYxh9CPyG-dMaxJtC8E-e2tFCYf9jRGgY1QrWky9rSz7oHHVnyDzNGqn-UOyHO8DSGve2mmvuQ6CubtYmcHTIL1SzU-_xhfHVpmzJiZ5lY_fwoncc-VC0uNkdoeVUmdl4OtxbTBr7VY2t5A-arm5Vy3_Dmj2hkGrUTAHFi7Zq4hehYaS04WBuYCKxiuO6Bjq7tWFVa2wnYNrTbEqTUVkc0ie5Bd7O-6Hz_PZa3Z_YWPxuobu2QpGQ_hwMBrFFNpZfPXWYPPO_ggdxV5qnRUbml5wQMyzD7w2p-NQr0jfqHPymCUjFpWj5PZUfwY4CPL-K5Ll7cTFjr6q1epx-0Xcvd5PKnt3hzfiY9yF1AygVKPM7g9KyLk9QNjV5Svjxj0tzsmxis6crBFT1PbeaHaxEkS41OnLHia80Q33yHUpfL7LoZ8QhSAYeObJR8wvmaBYZFQj5qIaYm1agsOl2Z_ukhRcDilQwX_gbPJnuJTcxDEoioLBxt5wdno4j8U7fusivPNVgKIN0Cy3znZwQOPwjDz6ZxnuhYMd9RrmG_un8eV1W6ypT1EVNRRUZlMdb3cMiFyx4CA59xaDhqpPMh_rOLoIV7RTDMjC7IdFHtAP2z4FX6Xv1TYDwipiacO-NGff2nEniPEjYIfhNKFvQQN-MRwaAVXI_VeoIfQ-B8kF2HN3fPGtTkppbuGhFAzx5trYkllKyVZZfGh23fFlAy1UyNStJ4hi61ivshFOOfgHVQpdUNV_nqE1MVPmBPIM2jwB6DpCFamSpX8Wn1LQkgdzlJRMmng-C8sAxwHeIgy5JA_CN-p2KCBCTwV_2D07lGbIVwtgZNqFWnNZa0HlX-bWGJDUGH4r_2Ns_G0VVE-VxBVcIGFC6d1iX98HS_6_ykwSc3Z2KB4nnWNlUa4gyWOlev2yg","feedLocation":"SEARCH","feedbackSource":23,"fetch_filters":true,"focusCommentID":null,"locale":null,"privacySelectorRenderLocation":"COMET_STREAM","renderLocation":"search_results_page","scale":1,"stream_initial_count":0,"useDefaultActor":false,"__relay_internal__pv__GHLShouldChangeAdIdFieldNamerelayprovider":true,"__relay_internal__pv__GHLShouldChangeSponsoredDataFieldNamerelayprovider":true,"__relay_internal__pv__IsWorkUserrelayprovider":false,"__relay_internal__pv__FBReels_deprecate_short_form_video_context_gkrelayprovider":true,"__relay_internal__pv__FeedDeepDiveTopicPillThreadViewEnabledrelayprovider":false,"__relay_internal__pv__CometImmersivePhotoCanUserDisable3DMotionrelayprovider":false,"__relay_internal__pv__WorkCometIsEmployeeGKProviderrelayprovider":false,"__relay_internal__pv__IsMergQAPollsrelayprovider":false,"__relay_internal__pv__FBReelsMediaFooter_comet_enable_reels_ads_gkrelayprovider":true,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false,"__relay_internal__pv__CometUFIShareActionMigrationrelayprovider":true,"__relay_internal__pv__CometUFI_dedicated_comment_routable_dialog_gkrelayprovider":false,"__relay_internal__pv__StoriesArmadilloReplyEnabledrelayprovider":true,"__relay_internal__pv__FBReelsIFUTileContent_reelsIFUPlayOnHoverrelayprovider":true}',
                'server_timestamps': 'true',
                'doc_id': '24016506881293628'
            }
            response = self.session.post('https://www.facebook.com/api/graphql/', headers=self.headers, data=data).json()
            thongtin = response['data']["serpResponse"]["results"]['edges'][0]['rendering_strategy']['view_model']['profile']
            name = thongtin.get('name')
            uid = thongtin.get('id')
            return {'status': 'success', 'id': uid, 'name': name}
        except:
            return {'status': 'error', 'trangthai': 'thatbai'}

    def tham_gia_nhom(self, group_id):
        try:
            data = {
                'av': self.id,
                'fb_dtsg': self.fb_dtsg,
                'jazoest': self.jazoest,
                'fb_api_caller_class': 'RelayModern',
                'fb_api_req_friendly_name': 'GroupCometJoinForumMutation',
                'variables': '{"feedType":"DISCUSSION","groupID":"'+group_id+'","imageMediaType":"image/x-auto","input":{"action_source":"GROUP_MALL","attribution_id_v2":"CometGroupDiscussionRoot.react,comet.group,via_cold_start,1673041528761,114928,2361831622,","group_id":"'+group_id+'","group_share_tracking_params":{"app_id":"2220391788200892","exp_id":"null","is_from_share":false},"actor_id":"'+self.id+'","client_mutation_id":"1"},"inviteShortLinkKey":null,"isChainingRecommendationUnit":false,"isEntityMenu":true,"scale":2,"source":"GROUP_MALL","renderLocation":"group_mall","__relay_internal__pv__GroupsCometEntityMenuEmbeddedrelayprovider":true,"__relay_internal__pv__GlobalPanelEnabledrelayprovider":false}',
                'server_timestamps': 'true',
                'doc_id': '5853134681430324',
                'fb_api_analytics_tags': '["qpl_active_flow_ids=431626709"]'
            }
            response = self.session.post('https://www.facebook.com/api/graphql/', headers=self.headers, data=data)
            if group_id in response.text:
                return {'status': 'success', 'trangthai': 'thanhcong'}
            else:
                return {'status': 'error', 'trangthai': 'thatbai'}
        except:
            return {'status': 'error', 'trangthai': 'thatbai'}

def nhap_danh_sach_cookie():
    banner()
    filename = "cookies.txt"
       
    if os.path.exists(filename):
        use_old = Prompt.ask(f"[bold yellow]Đã tìm thấy {filename}, bạn có muốn sử dụng danh sách này không? (y/n)[/]", default="y")
        if use_old.lower() == 'y':
            with open(filename, "r", encoding="utf-8") as f:
                cookie_list = [line.strip() for line in f.readlines() if line.strip()]
            console.print(f'[bold green]Đã tải {len(cookie_list)} cookie từ {filename}[/]')
            return cookie_list

    # Nếu không dùng file cũ hoặc file chưa tồn tại thì nhập mới
    cookie_list = []
    stt = 1
    while True:
        ck = Prompt.ask(f"[bold yellow]Nhập cookie thứ {stt} (Ấn 'enter' để dừng nhập)[/]")
        if ck.lower() in ['', 'enter']:
            break
        if 'c_user=' in ck:
            cookie_list.append(ck)
            stt += 1
    
    # Lưu vào file sau khi nhập xong
    if cookie_list:
        with open(filename, "w", encoding="utf-8") as f:
            for c in cookie_list:
                f.write(c + "\n")
        console.print(f'[bold green]Đã lưu {len(cookie_list)} cookie vào {filename}[/]')
    else:
        console.print('[bold red]Không có cookie nào được lưu![/]')
        
    return cookie_list

def show_menu():
    console.print("\n[bold cyan]=== MENU NHIỆM VỤ ===[/]")
    console.print("[1] Kết bạn ngẫu nhiên")
    console.print("[2] Thả cảm xúc bài viết")
    console.print("[3] Tham gia nhóm")
    console.print("[4] Bình luận bài viết")
    console.print("[5] Chạy tự động (tất cả nhiệm vụ)")
    console.print("[0] Thoát")
    return Prompt.ask("[bold yellow]Chọn nhiệm vụ[/]")

def main():
    banner()
    cookies = nhap_danh_sach_cookie()
    if not cookies:
        console.print('[bold red]Không có cookie nào được nhập![/]')
        return

    # Kiểm tra cookie
    cookies_hop_le = []
    thong_tin_tai_khoan = []
    console.print("\n[bold yellow]KIỂM TRA COOKIE[/]")
    for i, cookie in enumerate(cookies, 1):
        check = kiem_tra_cookie(cookie)
        if check['status'] == 'success':
            console.print(f"[bold green][{i}] ✅ Live - {check['name']} (ID: {check['user_id']})[/]")
            cookies_hop_le.append(cookie)
            thong_tin_tai_khoan.append({'name': check['name'], 'id': check['user_id']})
        else:
            console.print(f"[bold red][{i}] ❌ Die - {check['msg']}[/]")

    if not cookies_hop_le:
        console.print('[bold red]Không có cookie nào live, thoát chương trình![/]')
        return

    # Nhập cấu hình chung
    delay = int(Prompt.ask("[bold white]Nhập delay chung (giây)[/]", default="180"))
    so_nhiem_vu = int(Prompt.ask("[bold white]Nhập số nhiệm vụ muốn thực hiện[/]", default="9999"))
    max_per_account = int(Prompt.ask("[bold white]Giới hạn nhiệm vụ mỗi tài khoản (anti-ban)[/]", default="9999"))

    # Sinh nội dung bình luận tự động
    console.print("\n[bold yellow]SINH NỘI DUNG BÌNH LUẬN TỰ ĐỘNG[/]")
    danh_sach_binh_luan = [generate_random_comment() for _ in range(50)]  # Sinh 20 bình luận ngẫu nhiên
    console.print("[bold green]Đã sinh 50 nội dung bình luận tự động![/]")
    for i, cmt in enumerate(danh_sach_binh_luan, 1):
        console.print(f"[white]{i}. {cmt}[/]")

#nhóm
    tu_khoa_nhom = [
    'công nghệ', 'kinh doanh', 'giáo dục', 'y tế', 'thể thao', 'giải trí',
    'du lịch', 'ẩm thực', 'thời trang', 'xe cộ', 'bất động sản', 'tài chính',
    'marketing', 'thiết kế', 'lập trình', 'nhiếp ảnh', 'âm nhạc', 'phim ảnh',
    'sách vở', 'học tập', 'làm đẹp', 'sức khỏe', 'gia đình', 'tình yêu',

    'trí tuệ nhân tạo', 'blockchain', 'tiền điện tử', 'startup', 'quản lý',
    'đầu tư', 'chứng khoán', 'ngân hàng', 'bảo hiểm', 'khởi nghiệp',
    'freelancer', 'việc làm', 'tuyển dụng', 'kỹ năng mềm', 'giao tiếp',
    'lãnh đạo', 'tư duy', 'sáng tạo', 'đổi mới', 'chiến lược',

    'game', 'esport', 'streamer', 'youtube', 'tiktok',
    'mạng xã hội', 'influencer', 'content creator', 'review', 'vlog',

    'đồ ăn nhanh', 'món Việt', 'món Hàn', 'món Nhật', 'món Âu',
    'nấu ăn', 'công thức', 'đồ uống', 'cafe', 'trà sữa',

    'gym', 'fitness', 'yoga', 'thiền', 'chạy bộ',
    'bóng đá', 'bóng rổ', 'cầu lông', 'bơi lội', 'võ thuật',

    'makeup', 'skincare', 'spa', 'thẩm mỹ', 'nail',
    'tóc đẹp', 'mỹ phẩm', 'chăm sóc da', 'chăm sóc tóc',

    'du lịch bụi', 'resort', 'khách sạn', 'homestay', 'phượt',
    'review du lịch', 'ẩm thực đường phố', 'địa điểm đẹp',

    'ô tô', 'xe máy', 'xe điện', 'độ xe', 'review xe',

    'thiết bị', 'điện thoại', 'laptop', 'tablet', 'smartwatch',
    'phần mềm', 'ứng dụng', 'bảo mật', 'hack', 'tool',

    'python', 'javascript', 'java', 'web', 'app',
    'backend', 'frontend', 'fullstack', 'api', 'database',

    'photoshop', 'illustrator', 'figma', 'ui ux', '3d',
    'animation', 'video editor',

    'ca sĩ', 'idol', 'concert', 'nhạc trẻ', 'rap',
    'kpop', 'vpop', 'indie',

    'phim hành động', 'phim tình cảm', 'phim kinh dị',
    'phim hoạt hình', 'series', 'netflix',

    'truyện tranh', 'tiểu thuyết', 'self-help',
    'sách kinh doanh', 'sách kỹ năng',

    'học online', 'ôn thi', 'ielts', 'toeic',
    'du học', 'học bổng',

    'tình bạn', 'hẹn hò', 'crush', 'tâm lý',
    'cuộc sống', 'trải nghiệm',

    'nuôi dạy con', 'mẹ và bé', 'hôn nhân',
    'gia đình trẻ',

    'giảm cân', 'tăng cân', 'ăn kiêng', 'healthy',
    'vitamin', 'dinh dưỡng',

    'thiền định', 'tâm linh', 'phật giáo',
    'chiêm tinh', 'tarot',

    'meme', 'hài hước', 'trend', 'viral',

    'thời tiết', 'môi trường', 'biến đổi khí hậu',
    'năng lượng', 'điện mặt trời',

    'nông nghiệp', 'trồng trọt', 'chăn nuôi',
    'công nghệ cao',

    'logistics', 'xuất nhập khẩu', 'vận chuyển',
    'thương mại điện tử', 'dropshipping',

    'shop online', 'bán hàng', 'chốt đơn',
    'quảng cáo', 'facebook ads', 'google ads',

    'hacker', 'an ninh mạng', 'dark web',

    'robot', 'iot', 'smart home',

    'đồ chơi', 'lego', 'sưu tầm',

    'pet', 'chó', 'mèo', 'chim cảnh',

    'cosplay', 'anime', 'manga',

    'lifestyle', 'minimalism', 'decor',
    'nhà đẹp', 'setup phòng',

    'tài chính cá nhân', 'tiết kiệm', 'chi tiêu',
    'đầu tư dài hạn',

    'review sản phẩm', 'unbox',
    'so sánh', 'đánh giá',

    'câu chuyện thành công', 'động lực',
    'phát triển bản thân',

    'công việc văn phòng', 'remote work',
    'digital nomad',

    'startup công nghệ', 'saas',
    'fintech', 'edtech', 'healthtech'
]

    # Chọn cảm xúc
    ds_cam_xuc = {
        "1": "LIKE",
        "2": "LOVE",
        "3": "CARE",
        "4": "HAHA",
        "5": "WOW",
        "6": "SAD",
        "7": "ANGRY"
    }
    console.print("\n[bold yellow]CHỌN CẢM XÚC[/]")
    console.print('[white][1] Like 👍[/]')
    console.print('[white][2] Love ❤️[/]')
    console.print('[white][3] Care 💤[/]')
    console.print('[white][4] Haha 🎃[/]')
    console.print('[white][5] WOW 😧[/]')
    console.print('[white][6] Sad 🥹[/]')
    console.print('[white][7] Angry 😡[/]')
    console.print('[green]Có thể chọn nhiều cảm xúc (VD: 1345...)[/]')
    chon = Prompt.ask('[bold white]Nhập số để chọn cảm xúc[/]')
    cam_xuc_chon = [ds_cam_xuc[c] for c in chon if c in ds_cam_xuc]
    if not cam_xuc_chon:
        console.print('[bold yellow]Không có cảm xúc nào được chọn, sử dụng mặc định LIKE[/]')
        cam_xuc_chon = ['LIKE']

    # Tạo tên Việt
    vietnamese_names = generate_vietnamese_names()

    # Menu nhiệm vụ
    while True:
        choice = show_menu()
        if choice == '0':
            break

        stt = 0
        loi_lien_tuc = 0
        cookie_index = 0
        actions_per_account = {i: 0 for i in range(len(cookies_hop_le))}

        while stt < so_nhiem_vu:
            try:
                if actions_per_account[cookie_index] >= max_per_account:
                    console.print(f'[bold yellow]Tài khoản {thong_tin_tai_khoan[cookie_index]["name"]} đạt giới hạn, chuyển sang tài khoản khác[/]')
                    cookie_index = (cookie_index + 1) % len(cookies_hop_le)
                    continue

                cookie = cookies_hop_le[cookie_index]
                tai_khoan = thong_tin_tai_khoan[cookie_index]
                console.print(f'[bold cyan]Đang sử dụng tài khoản: {tai_khoan["name"]} (ID: {tai_khoan["id"]})[/]')

                fb = Facebook(cookie)
                info = fb.info()
                if info in ['cookieout', '956', '282', 'spam']:
                    console.print(f'[bold red]Tài khoản {tai_khoan["name"]} gặp lỗi: {info}[/]')
                    cookies_hop_le.pop(cookie_index)
                    thong_tin_tai_khoan.pop(cookie_index)
                    del actions_per_account[cookie_index]
                    if not cookies_hop_le:
                        console.print('[bold red]Hết tài khoản hợp lệ, dừng chương trình![/]')
                        break
                    cookie_index = cookie_index % len(cookies_hop_le)
                    continue

                if choice == '5':
                    tac_vu = random.choice(['ket_ban', 'tha_cam_xuc', 'tham_gia_nhom', 'binh_luan'])
                else:
                    tac_vu = { '1': 'ket_ban', '2': 'tha_cam_xuc', '3': 'tham_gia_nhom', '4': 'binh_luan' }.get(choice)

                if tac_vu == 'ket_ban':
                    ten = random.choice(vietnamese_names)
                    tim_ban = fb.tim_ban(ten)
                    if tim_ban.get('trangthai') == 'thatbai':
                        console.print(f'[bold red][LOI] Không tìm thấy bạn với tên {ten}[/]')
                        loi_lien_tuc += 1
                    else:
                        ket_ban = fb.ket_ban(tim_ban['id'])
                        if ket_ban.get('trangthai') == 'thanhcong':
                            stt += 1
                            actions_per_account[cookie_index] += 1
                            thoi_gian = datetime.now().strftime('%H:%M:%S')
                            console.print(f'[bold green]| {stt} | {thoi_gian} | Thêm bạn | {tim_ban["id"]} | {tim_ban["name"]}[/]')
                            loi_lien_tuc = 0
                        else:
                            console.print(f'[bold red][LOI] Không thể kết bạn với {tim_ban["name"]}[/]')
                            loi_lien_tuc += 1

                elif tac_vu == 'tha_cam_xuc':
                    bai_viet = fb.lay_id_bai_viet()
                    if bai_viet.get('trangthai') == 'thatbai':
                        console.print(f'[bold red][LOI] Không tìm thấy bài viết[/]')
                        loi_lien_tuc += 1
                    else:
                        cam_xuc = random.choice(cam_xuc_chon)
                        tha = fb.tha_cam_xuc(bai_viet['idpost'], cam_xuc)
                        if tha.get('trangthai') == 'thanhcong':
                            stt += 1
                            actions_per_account[cookie_index] += 1
                            thoi_gian = datetime.now().strftime('%H:%M:%S')
                            console.print(f'[bold green]| {stt} | {thoi_gian} | Thả cảm xúc {cam_xuc} | {bai_viet["idpost"]}[/]')
                            loi_lien_tuc = 0
                        else:
                            console.print(f'[bold red][LOI] Không thể thả cảm xúc cho bài viết {bai_viet["idpost"]}[/]')
                            loi_lien_tuc += 1

                elif tac_vu == 'tham_gia_nhom':
                    tu_khoa = random.choice(tu_khoa_nhom)
                    nhom = fb.tim_nhom(tu_khoa)
                    if nhom.get('trangthai') == 'thatbai':
                        console.print(f'[bold red][LOI] Không tìm thấy nhóm với từ khóa {tu_khoa}[/]')
                        loi_lien_tuc += 1
                    else:
                        tham_gia = fb.tham_gia_nhom(nhom['id'])
                        if tham_gia.get('trangthai') == 'thanhcong':
                            stt += 1
                            actions_per_account[cookie_index] += 1
                            thoi_gian = datetime.now().strftime('%H:%M:%S')
                            console.print(f'[bold green]| {stt} | {thoi_gian} | Tham gia nhóm | {nhom["id"]} | {nhom["name"]}[/]')
                            loi_lien_tuc = 0
                        else:
                            console.print(f'[bold red][LOI] Không thể tham gia nhóm {nhom["name"]}[/]')
                            loi_lien_tuc += 1

                elif tac_vu == 'binh_luan':
                    bai_viet = fb.lay_id_bai_viet()
                    if bai_viet.get('trangthai') == 'thatbai':
                        console.print(f'[bold red][LOI] Không tìm thấy bài viết[/]')
                        loi_lien_tuc += 1
                    else:
                        noi_dung = random.choice(danh_sach_binh_luan)
                        binh_luan = fb.binh_luan(bai_viet['idpost'], noi_dung)
                        if binh_luan.get('trangthai') == 'thanhcong':
                            stt += 1
                            actions_per_account[cookie_index] += 1
                            thoi_gian = datetime.now().strftime('%H:%M:%S')
                            console.print(f'[bold green]| {stt} | {thoi_gian} | Bình luận | {bai_viet["idpost"]} | {noi_dung}[/]')
                            loi_lien_tuc = 0
                        else:
                            console.print(f'[bold red][LOI] Không thể bình luận cho bài viết {bai_viet["idpost"]}[/]')
                            loi_lien_tuc += 1

                if loi_lien_tuc >= 50:
                    console.print('[bold red]Quá nhiều lỗi liên tục, dừng chương trình![/]')
                    break

                cookie_index = (cookie_index + 1) % len(cookies_hop_le)

                if stt < so_nhiem_vu:
                    doi_giay(delay, random_delay=True)  # Anti-ban: delay ngẫu nhiên

            except Exception as e:
                console.print(f'[bold red]Lỗi không xác định: {str(e)}[/]')
                loi_lien_tuc += 1
                if loi_lien_tuc >= 10:
                    console.print('[bold red]Quá nhiều lỗi liên tục, dừng chương trình![/]')
                    break
                doi_giay(delay, random_delay=True)

        console.print("\n[bold cyan]HOÀN THÀNH![/]")
        console.print(f"[bold white]Đã thực hiện: {stt}/{so_nhiem_vu} nhiệm vụ[/]")
        console.print(f"[bold white]Số lần lỗi: {loi_lien_tuc}[/]")
        console.print("=" * 60)
        Prompt.ask("[bold yellow]Nhấn Enter để tiếp tục...[/]")

if __name__ == "__main__":
    main()
