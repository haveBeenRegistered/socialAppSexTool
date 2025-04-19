import requests
from bs4 import BeautifulSoup
from lowestPrice import extract_data_from_divs
import json
import sys
from playwright.sync_api import sync_playwright
# 全局变量定义
updated_url = None

# 新增：无头浏览器抓取
def fetch_with_playwright(url, headers=None):
    print("[fetch] start →", url)
    
    # 构建更真实的请求头
    real_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-JP,zh;q=0.9,ja-JP;q=0.8,ja;q=0.7,zh-CN;q=0.6",
        "sec-ch-ua": "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-ch-ua-platform-version": "\"19.0.0\""
    }
    
    # 如果传入了headers，使用其中的User-Agent（如果有）
    if headers and "User-Agent" in headers:
        ua = headers["User-Agent"]
        real_headers["User-Agent"] = ua
    
    print("[fetch] Using User-Agent →", real_headers["User-Agent"])
    
    with sync_playwright() as p:
        print("[fetch] launching browser…")
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        print("[fetch] browser launched")
        
        # 创建更真实的浏览器上下文
        context = browser.new_context(
            viewport={"width": 1366, "height": 768},
            locale="ja-JP",
            timezone_id="Asia/Tokyo",
            user_agent=real_headers["User-Agent"]
        )
        
        page = context.new_page()
        print("[fetch] new page created")
        
        # 设置更多请求头以模拟真实浏览器
        page.set_extra_http_headers(real_headers)
        print("[fetch] headers set")
        
        # 增加一个随机延迟
        import random
        delay = random.uniform(1, 3)
        print(f"[fetch] adding random delay: {delay:.2f}s")
        page.wait_for_timeout(delay * 1000)  # 毫秒为单位
        
        print("[fetch] navigating to →", url)
        # 使用domcontentloaded而不是networkidle，加快加载速度
        response = page.goto(url, timeout=60000, wait_until="domcontentloaded")
        status = response.status if response else None
        print(f"[fetch] HTTP status → {status}")
        
        
        # 增加一个随机滚动行为，模拟真实用户
        print("[fetch] scrolling page to simulate user behavior")
        page.evaluate("""() => {
            window.scrollTo(0, Math.floor(Math.random() * 300));
        }""")
        page.wait_for_timeout(1000)
            
        html = page.content()
        print(f"[fetch] got html ({len(html)} bytes)")
        
        # 调试信息 - 打印HTML摘要
        print("[fetch] HTML preview (first 300 chars):")
        print(html[:300])
        print("...")
        
        browser.close()
        print("[fetch] browser closed")
    return status, html

def update_pagination_third_line(file_path="/app/python/pagination.txt"):
    """
    读取 pagination.txt 文件，若第三行不为空，则将该行作为 URL 发送请求，
    从返回的页面中查找所有 s-pagination-container 中的 a-list-item 元素，
    如果最后一个 item 内存在 a 标签，则更新第三行为亚马逊链接拼接 a 标签 href 后的 URL，
    否则打印 "false"。
    """
    # 读取文件
    with open(file_path, "r", encoding="utf-8") as pf:
        lines = pf.readlines()

    # 判断文件是否至少有三行且第三行不为空
    if len(lines) < 3 or not lines[2].strip():
        print("false")
        return

    url = lines[2].strip()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "Accept-Language": "zh-JP,zh;q=0.9,ja-JP;q=0.8,ja;q=0.7,zh-CN;q=0.6"
    }
    status, html = fetch_with_playwright(url, headers)
    if status != 200:
        print(f"Request failed with status code: {status}")
        return

    soup = BeautifulSoup(html, "html.parser")
    print("Successfully retrieved soup")

    # 查找所有类名为 s-pagination-container 的 div 元素
    pagination_divs = soup.find_all("div", class_="s-pagination-container")
    a_list_items = []
    # 遍历每个 pagination_div，收集内部所有类为 a-list-item 的元素
    for div in pagination_divs:
        items = div.find_all(class_="a-list-item")
        a_list_items.extend(items)
    # 检查是否找到了有效的 item，并判断最后一个 item 是否包含 a 标签
    if a_list_items:
        last_item = a_list_items[-1]
        if not last_item.find("a"):
            print("false")
            return False
        else:
            # 构造新的第三行内容：亚马逊链接拼接 last_item a 标签的 href
            new_third_line = "https://www.amazon.co.jp" + \
                last_item.find("a")["href"] + "\n"
            # 更新全局 url（并存入 url_list 列表）
            global updated_url
            updated_url = new_third_line.strip()
            # 读取原文件内容，并更新第三行
            with open(file_path, "r+", encoding="utf-8") as pf:
                file_lines = pf.readlines()
                if len(file_lines) >= 3:
                    file_lines[2] = new_third_line
                else:
                    while len(file_lines) < 2:
                        file_lines.append("\n")
                    file_lines.append(new_third_line)
                pf.seek(0)
                pf.writelines(file_lines)
                pf.truncate()
            print("third line updated")
            return True
    else:
        print("false")
        return False

# 调用示例
if __name__ == "__main__":
    result = update_pagination_third_line()
    print(result)
    # 如果传入参数，则使用该参数作为搜索关键词，否则使用默认值
    if len(sys.argv) > 1:
        sponsorFilter = sys.argv[1]
    else:
        sponsorFilter = False
    if result:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
            "Accept-Language": "zh-JP,zh;q=0.9,ja-JP;q=0.8,ja;q=0.7,zh-CN;q=0.6"
        }
        status, html = fetch_with_playwright(updated_url, headers)
        if status == 200:
            new_soup = BeautifulSoup(html, "html.parser")
            # 查找所有类名包含 "a-section a-spacing-base" 的 div，然后筛选出其内部包含 "s-product-image-container" 的元素
            divs = new_soup.find_all("div", class_="a-section a-spacing-base")
            matched_divs = [div for div in divs if div.find(
                class_="s-product-image-container")]
            # 进一步筛选出内部存在 data-cy="reviews-block" 的 div
            rematched_divs = [div for div in matched_divs if div.find(
                attrs={"data-cy": "reviews-block"})]
            # 调用 extract_data_from_divs 将结果保存在 data 字典中
            data = extract_data_from_divs(matched_divs)
            # 后续操作直接使用 data 中的各个列表：
            s_image_src_list = data["s_image_src_list"]
            a_href_list = data["a_href_list"]
            h2_aria_list = data["h2_aria_list"]
            price_list = data["price_list"]
            coupon_value_list = data["coupon_value_list"]
            shipping_cost_list = data["shipping_cost_list"]
            sponsor_list = data["sponsor_list"]
            
            # 按照 s_image_src_list 的长度创建一个字典，
            # 每个字典项（即 product 对象）的属性来自各对应列表的相同索引值
            product_dict = {
                i: {
                    "image": s_image_src_list[i],
                    "href": "https://www.amazon.co.jp" + a_href_list[i] if i < len(a_href_list) else None,
                    "aria": h2_aria_list[i] if i < len(h2_aria_list) else None,
                    "price": (price_list[i] * (1 - 0.01 * coupon_value_list[i]) + shipping_cost_list[i])
                    if i < len(price_list) and i < len(coupon_value_list) and i < len(shipping_cost_list)
                    else None,
                    "shipping_cost": shipping_cost_list[i] if i < len(shipping_cost_list) else 0,
                    "coupon": coupon_value_list[i] if i < len(coupon_value_list) else 0,
                    "sponsor": sponsor_list[i] if i < len(sponsor_list) else 0
                }
                for i in range(len(s_image_src_list))
            }

            # 根据 sponsorFilter 进行过滤
            if sponsorFilter:
                # 如果 sponsorFilter 为 True，则过滤掉 sponsor 值为 1 的商品
                filtered_products = {
                    i: prod for i, prod in product_dict.items()
                    if prod["price"] > 1 and prod["sponsor"] != 1
                }
            else:
                filtered_products = {
                    i: prod for i, prod in product_dict.items()
                    if prod["price"] > 1
                }
            print(f"have been filtered：{len(filtered_products)}")
        
            # 然后依据 price 的值从小到大重新排序
            sorted_product_dict = {
                k: v for k, v in sorted(filtered_products.items(), key=lambda item: item[1]["price"])
            }
            # 假设 sorted_product_dict 已经生成
            products = list(sorted_product_dict.values())
            # 假设 sorted_product_dict 已经生成
            with open("/app/python/priceResult.txt", "w", encoding="utf-8") as f:
                f.write("[\n")
                for i, product in enumerate(products):
                    # 将每个产品对象转换为 JSON 字符串
                    product_json = json.dumps(product, ensure_ascii=False)
                    # 如果不是最后一个对象，则在对象大括号后添加逗号
                    if i < len(products) - 1:
                        f.write(product_json + ",\n")
                    else:
                        f.write(product_json)
                    f.flush()  # 确保输出不被缓存
                f.write("\n]")
            print("success")
            sys.stdout.flush()
        else:
            print(f"Request failed with status code: {status}")
