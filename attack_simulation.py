from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import time
import subprocess

# 配置 Selenium WebDriver
driver = webdriver.Chrome()

# 打开目标网页
driver.get('http://example.31303')  # 替换为你的目标URL

# 找到需要点击的按钮
button = driver.find_element(By.ID, 'button-id')  # 替换为你的按钮的ID

# 记录点击前的时间
start_time = datetime.now()
print(f"开始时间: {start_time}")

# 模拟手动点击
input("按回车键开始点击...")
button.click()

# 记录点击后的时间
end_time = datetime.now()
print(f"结束时间: {end_time}")

# 关闭浏览器
driver.quit()

# 将时间格式化为 kubectl 使用的时间格式
start_time_str = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
end_time_str = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')

# 使用 kubectl 获取日志
namespace = 'default'  # 替换为你的命名空间
pod_name = 'your-pod-name'  # 替换为你的 Pod 名称

kubectl_command = [
    'kubectl', 'logs', pod_name, '--namespace', namespace,
    '--since-time', start_time_str, '--until-time', end_time_str
]
