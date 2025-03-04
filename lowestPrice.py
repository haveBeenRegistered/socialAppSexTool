__all__ = ["get_amazon_search_results", "extract_data_from_divs"]
import requests
from bs4 import BeautifulSoup
import urllib.parse
import json
import sys


def extract_data_from_divs(divs,
                           s_image_src_list=None,
                           a_href_list=None,
                           h2_aria_list=None,
                           price_list=None,
                           coupon_value_list=None,
                           shipping_cost_list=None,
                           sponsor_list=None):
    """
    从传入的 divs 列表中提取数据，并追加到对应的列表中：
      - s_image_src_list: 查找类名为 "s-image" 的元素的 src 属性；
      - a_href_list: 查找类名包含 "s-line-clamp" 的 a 标签的 href 属性；
      - h2_aria_list: 查找所有 h2 标签的 aria-label 属性；
      - price_list: 查找类名为 "a-price-whole" 的 span 标签，解析为整数，不成功设为 -1；
      - coupon_value_list: 查找指定 class 的 span 标签，提取文本中 "%" 前的数字，不成功设为 0；
      - shipping_cost_list: 遍历所有带有 aria-label 的 span 标签，若包含 "配送料 ￥" 则提取其后的数字，否则为 0；
      - sponsor_list: 如果存在包含 "スポンサー情報を表示、または広告フィードバックを残す" 的 aria-label，则值为 1，否则为 0。
    如果参数为 None，则内部初始化为空列表。
    返回一个字典，包含各个列表提取到的数据。
    """
    if s_image_src_list is None:
        s_image_src_list = []
    if a_href_list is None:
        a_href_list = []
    if h2_aria_list is None:
        h2_aria_list = []
    if price_list is None:
        price_list = []
    if coupon_value_list is None:
        coupon_value_list = []
    if shipping_cost_list is None:
        shipping_cost_list = []
    if sponsor_list is None:
        sponsor_list = []
    for div in divs:
        # 提取图片 src 属性
        img = div.find(class_="s-image")
        if img and img.get("src"):
            s_image_src_list.append(img.get("src"))

        # 提取 a 标签的 href（类名包含 "s-line-clamp"）
        a_tag = div.find("a", class_=lambda cls: cls and "s-line-clamp" in cls)
        if a_tag and a_tag.get("href"):
            a_href_list.append(a_tag.get("href"))

        # 提取所有 h2 标签中的 aria-label 属性
        h2_tags = div.find_all("h2")
        for h2 in h2_tags:
            aria = h2.get("aria-label")
            if aria:
                h2_aria_list.append(aria)

        # 提取价格，查找类名为 "a-price-whole" 的 span 标签
        span_price = div.find("span", class_="a-price-whole")
        if span_price:
            try:
                price = int(span_price.get_text().replace(",", "").strip())
            except ValueError:
                price = -1
        else:
            price = -1
        price_list.append(price)

        # 提取优惠券信息
        span_coupon = div.find(
            "span", class_="a-size-base s-highlighted-text-padding s-coupon-highlight-color aok-inline-block")
        if span_coupon:
            text = span_coupon.get_text().strip()  # 例如 "10% off"
            if "%" in text:
                num_str = text.split("%")[0]
                try:
                    coupon_val = int(num_str.replace(",", "").strip())
                except ValueError:
                    coupon_val = 0
            else:
                coupon_val = 0
        else:
            coupon_val = 0
        coupon_value_list.append(coupon_val)

        # 提取配送料
        shipping_cost = 0
        for span in div.find_all("span", attrs={"aria-label": True}):
            aria_value = span["aria-label"]
            if "配送料 ￥" in aria_value:
                try:
                    num_str = aria_value.split("配送料 ￥", 1)[1].split()[0]
                    shipping_cost = int(num_str.replace(",", "").strip())
                except Exception:
                    shipping_cost = 0
        shipping_cost_list.append(shipping_cost)

        # 判断 sponsor 信息
        sponsor_flag = 0
        for span in div.find_all("span", attrs={"aria-label": True}):
            if "スポンサー情報を表示、または広告フィードバックを残す" in span["aria-label"]:
                sponsor_flag = 1
                break
        sponsor_list.append(sponsor_flag)
    return {
        "s_image_src_list": s_image_src_list,
        "a_href_list": a_href_list,
        "h2_aria_list": h2_aria_list,
        "price_list": price_list,
        "coupon_value_list": coupon_value_list,
        "shipping_cost_list": shipping_cost_list,
        "sponsor_list": sponsor_list
    }


def get_amazon_search_results():
    # 如果传入参数，则使用该参数作为搜索关键词，否则使用默认值
    if len(sys.argv) > 1:
        keyWord = sys.argv[1]
    else:
        keyWord = "蕁麻疹"
    # 如果传入参数有两个，则 sponsorFilter 设置为第二个参数，否则为 False
    sponsorFilter = sys.argv[2] if len(sys.argv) > 2 else False
    encoded_keyword = urllib.parse.quote(keyWord)
    url = f"https://www.amazon.co.jp/s?k={encoded_keyword}&s=price-asc-rank"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "Accept-Language": "zh-JP,zh;q=0.9,ja-JP;q=0.8,ja;q=0.7,zh-CN;q=0.6"
    }
    print(url)
    response = requests.get(url, headers=headers)
    # 打印响应结果
    print(response.status_code)
    # 判断请求是否成功
    if response.status_code != 200:
        print(f"请求失败，状态码：{response.status_code}")
        return None
        # 解析页面
    soup = BeautifulSoup(response.text, "html.parser")

    # 查找所有类名为 s-pagination-container 的 div 元素
    pagination_divs = soup.find_all("div", class_="s-pagination-container")
    a_list_items = []

    if not pagination_divs:
        # 默认值为 "1"
        new_value = "1\n"
    else:
        # 遍历每个 pagination_div，收集内部所有类为 a-list-item 的元素
        for div in pagination_divs:
            items = div.find_all(class_="a-list-item")
            a_list_items.extend(items)
        # 更新 pagination.txt 第一行为 items 长度减 1
        new_value = f"{len(a_list_items) - 1}\n"

    # 更新 pagination.txt 文件的第一行值
    with open("C:/Users/81804/Desktop/python/pagination.txt", "r+", encoding="utf-8") as pf:
        lines = pf.readlines()
        if lines:
            lines[0] = new_value
        else:
            lines = [new_value]
        pf.seek(0)
        pf.writelines(lines)
        pf.truncate()

    if len(a_list_items) > 2:
        # 排除第一个和最后一个元素，取中间元素
        middle_items = a_list_items[1:-1]
        urls = []
        for item in middle_items:
            a_tag = item.find("a")
            if a_tag and a_tag.get("href"):
                full_url = "https://www.amazon.co.jp" + a_tag.get("href")
                urls.append(full_url)

        # 以写模式打开文件，清空第一行之后的内容，
        # 注意 new_value 已经包含换行符
        with open("C:/Users/81804/Desktop/python/pagination.txt", "w", encoding="utf-8") as pf:
            pf.write(new_value)
            for url in urls:
                pf.write(url + "\n")
        print(f"找到 {len(a_list_items)} 个 a-list-item 元素")
    else:
        # 如果 a_list_items 的长度小于等于 2，则清空文件中第一行之后的内容
        with open("C:/Users/81804/Desktop/python/pagination.txt", "r+", encoding="utf-8") as pf:
            lines = pf.readlines()
            if lines:
                pf.seek(0)
                pf.write(lines[0])
                pf.truncate()
        print("a_list_items are less than or equal to 2")

    # 查找所有类名包含 "a-section a-spacing-base" 的 div，然后筛选出其内部包含 "s-product-image-container" 的元素
    divs = soup.find_all("div", class_="a-section a-spacing-base")
    matched_divs = [div for div in divs if div.find(
        class_="s-product-image-container")]
    # 进一步筛选出内部存在 data-cy="reviews-block" 的 div
    rematched_divs = [div for div in matched_divs if div.find(
        attrs={"data-cy": "reviews-block"})]

    print(f"原始匹配数量：{len(matched_divs)}")
    print(f"含有 data-cy='reviews-block' 的数量：{len(rematched_divs)}")
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
    # 如果 a_list_items > 2，同时分页文件中存在第二行以后内容，则对分页 URL 做如下处理
    if len(a_list_items) > 2:
        with open("C:/Users/81804/Desktop/python/pagination.txt", "r", encoding="utf-8") as pf:
            lines = pf.readlines()
        if len(lines) > 1:
            extra_urls = [line.strip() for line in lines[1:] if line.strip()]
            for idx, extra_url in enumerate(extra_urls, start=1):
                print(f"Processing URL ：{extra_url}")
                extra_response = requests.get(extra_url, headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
                    "Accept-Language": "zh-JP,zh;q=0.9,ja-JP;q=0.8,ja;q=0.7,zh-CN;q=0.6"
                })
                if extra_response.status_code != 200:
                    print(
                        f"error code：{extra_url}, 状态码：{extra_response.status_code}")
                    continue
                extra_soup = BeautifulSoup(extra_response.text, "html.parser")

                # 查找所有类名为 "a-section a-spacing-base" 的 div
                extra_divs = extra_soup.find_all(
                    "div", class_="a-section a-spacing-base")
                # 筛选出内部包含 "s-product-image-container" 的 div
                extra_matched_divs = [div for div in extra_divs if div.find(
                    class_="s-product-image-container")]
                # 进一步筛选出内部存在 data-cy="reviews-block" 的 div
                # extra_matched_divs = [div for div in extra_matched_divs if div.find(attrs={"data-cy": "reviews-block"})]

                # 为 extra_matched_divs 中的每个 a 标签，其 href 添加后缀（遍历的 index）
                for div in extra_matched_divs:
                    a_tag = div.find(
                        "a", class_=lambda cls: cls and "s-line-clamp" in cls)
                    if a_tag and a_tag.get("href"):
                        a_tag["href"] = a_tag["href"].rstrip() + f"-{idx}"

                # 调用数据提取函数获取 extra_data
                extra_data = extract_data_from_divs(extra_matched_divs)
                # 合并 extra_data 中的各个列表到主变量中
                s_image_src_list.extend(extra_data["s_image_src_list"])
                a_href_list.extend(extra_data["a_href_list"])
                h2_aria_list.extend(extra_data["h2_aria_list"])
                price_list.extend(extra_data["price_list"])
                coupon_value_list.extend(extra_data["coupon_value_list"])
                shipping_cost_list.extend(extra_data["shipping_cost_list"])
                sponsor_list.extend(extra_data["sponsor_list"])

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
    with open("C:/Users/81804/Desktop/python/priceResult.txt", "w", encoding="utf-8") as f:
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
    return soup
    # 查找所有class为s-line-clamp-2的 a 标签，并将索引和href存入字典


if __name__ == "__main__":
    get_amazon_search_results()
