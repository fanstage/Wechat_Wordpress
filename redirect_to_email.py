import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import urllib.request
from bs4 import BeautifulSoup
from wcferry.client import Wcf, __version__
from wcferry.wxmsg import WxMsg


def send_email(sender_email, auth_code, receiver_email, subject, content):
    # 设置邮件内容
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = formataddr(("发件人昵称", sender_email))  # 设置发件人昵称和邮箱
    msg['To'] = formataddr(("收件人昵称", receiver_email))  # 设置收件人昵称和邮箱，可选
    msg['Subject'] = subject

    try:
        # 使用SSL加密，连接QQ邮箱的SMTP服务器，端口是465
        smtp_server = 'smtp.qq.com'
        port = 465
        server = smtplib.SMTP_SSL(smtp_server, port)
        # 登录QQ邮箱，使用授权码而不是你的QQ密码
        server.login(sender_email, auth_code)
        # 发送邮件
        server.sendmail(sender_email, receiver_email, msg.as_string())
        # 关闭连接
        server.quit()
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print(f"邮件发送失败: {e}")

def fetch_weixin_article(url):
    # 使用urllib请求网页内容
    with urllib.request.urlopen(url) as response:
        html = response.read()

        # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html, 'html.parser')

    # 尝试提取文章标题
    title_div = soup.find('h1', class_='rich_media_title')
    if title_div:
        title = title_div.get_text(strip=True)
    else:
        title = None

    # 微信公众号文章的内容通常包含在特定的div中，但结构可能有所不同
    # 这里我们尝试通过一些常见的class或id来提取内容，但可能需要根据实际页面调整
    content_div = soup.find('div', class_='rich_media_content')
    if content_div:
        content = content_div.get_text(strip=True)
    else:
        content = None

    return content