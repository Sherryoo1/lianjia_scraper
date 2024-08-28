import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# 请求头信息，用于伪装请求
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

# 存储数据的列表
data = []

# 爬取的页数范围
for page in range(1, 40):
    url = f"https://nj.lianjia.com/ershoufang/pg{page}/"
    print(f"正在爬取第 {page} 页的数据...")
    
    # 发送请求
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"获取网页内容失败，状态码: {response.status_code}")
        continue
    
    # 解析网页内容
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 找到每个房源的容器
    listings = soup.find_all('div', class_='info clear')

    for listing in listings:
        basic_info = listing.find('div', class_='address').text.strip()
        price_info = listing.find('div', class_='priceInfo').text.strip()
        attributes = listing.find('div', class_='houseInfo').text.strip()
        transaction_info = listing.find('div', class_='dealCycle').text.strip() if listing.find('div', class_='dealCycle') else "无"
        
        # 解析基本信息
        community_name = basic_info.split('\n')[0] if basic_info else "无"
        district = basic_info.split('\n')[1] if len(basic_info.split('\n')) > 1 else "无"
        
        # 解析房屋属性
        house_info = attributes.split('|') if attributes else ["无"] * 11
        house_type = house_info[0] if len(house_info) > 0 else "无"
        floor = house_info[1] if len(house_info) > 1 else "无"
        area = house_info[2] if len(house_info) > 2 else "无"
        layout = house_info[3] if len(house_info) > 3 else "无"
        inner_area = house_info[4] if len(house_info) > 4 else "无"
        building_type = house_info[5] if len(house_info) > 5 else "无"
        orientation = house_info[6] if len(house_info) > 6 else "无"
        building_structure = house_info[7] if len(house_info) > 7 else "无"
        decoration = house_info[8] if len(house_info) > 8 else "无"
        ladder_ratio = house_info[9] if len(house_info) > 9 else "无"
        elevator = house_info[10] if len(house_info) > 10 else "无"
        floor_height = house_info[11] if len(house_info) > 11 else "无"
        
        # 解析交易属性
        listing_time = transaction_info if transaction_info else "无"
        
        # 添加到数据列表
        data.append({
            "小区名称": community_name,
            "所在区域": district,
            "房屋总价": price_info,
            "房屋单价": price_info,
            "房屋户型": house_type,
            "所在楼层": floor,
            "建筑面积": area,
            "户型结构": layout,
            "套内面积": inner_area,
            "建筑类型": building_type,
            "房屋朝向": orientation,
            "建筑结构": building_structure,
            "装修情况": decoration,
            "梯户比例": ladder_ratio,
            "配备电梯": elevator,
            "楼层高度": floor_height,
            "挂牌时间": listing_time,
            "交易权属": "无",
            "上次交易": "无",
            "房屋用途": "无",
            "房屋年限": "无",
            "产权所属": "无",
            "抵押信息": "无",
            "房本备件": "无"
        })

    # 防止请求过于频繁
    time.sleep(5)

# 保存到 CSV 文件
df = pd.DataFrame(data)
df.to_csv('lianjia_real_estate.csv', index=False, encoding='utf-8-sig')

print("数据已成功爬取并保存到'lianjia_real_estate.csv'")
