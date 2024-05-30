from gptchecker import GPTChecker

logs = """
2024-05-01 16:14:35.272 INFO   1 --- [http-nio-12340-exec-5] a.s.LoggingAspect: Entering in Method: getToken, Class: auth.service.impl.TokenServiceImpl, Arguments: [BasicAuthDto(username=admin, password=222222, verificationCode=1234),  Return: Response(status=1, msg=login success, data=TokenDto(userId=c4f1da0b-b6c6-412c-944c-d1b4ddb153cf, username=admin, token=eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiIsInJvbGVzIjpbIlJPTEVfQURNSU4iXSwiaWQiOiJjNGYxZGEwYi1iNmM2LTQxMmMtOTQ0Yy1kMWI0ZGRiMTUzY2YiLCJpYXQiOjE3MTQ1NTEyNzUsImV4cCI6MTcxNDU1NDg3NX0.L8kWfREHcaqOXK-rdW9nF7feTTCIi3bf41EwVlaKQyM)) 和2024-05-01 16:14:36.658 INFO   1 --- [http-nio-12342-exec-7] u.s.LoggingAspect: Entering in Method: getAllUsers, Class: user.service.impl.UserServiceImpl, Arguments: [[accept:"application/json, text/javascript, */*; q=0.01", x-requested-with:"XMLHttpRequest", authorization:"Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiIsInJvbGVzIjpbIlJPTEVfQURNSU4iXSwiaWQiOiJjNGYxZGEwYi1iNmM2LTQxMmMtOTQ0Yy1kMWI0ZGRiMTUzY2YiLCJpYXQiOjE3MTQ1NTEyNzUsImV4cCI6MTcxNDU1NDg3NX0.L8kWfREHcaqOXK-rdW9nF7feTTCIi3bf41EwVlaKQyM", user-agent:"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/120.0.6099.62 Safari/537.36", content-type:"application/json", referer:"http://192.168.49.2:32677/admin.html", accept-encoding:"gzip, deflate", cookie:"JSESSIONID=206482D23B98E97B280D8A7D34337EFF; YsbCaptcha=E26E292DC2774650ABC2C8D49D3276A7", forwarded:"proto=http;host="ts-gateway-service:18888";for="10.244.0.203:46280"", content-length:"0", x-forwarded-proto:"http", x-forwarded-port:"18888", x-forwarded-host:"ts-gateway-service:18888", host:"10.244.0.209:12342"]],  Return: Response(status=1, msg=Success, data=[User(userId=4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f, userName=fdse_microservice, password=111111, gender=1, documentType=1, documentNum=2135488099312X, email=trainticket_notify@163.com), User(userId=c4f1da0b-b6c6-412c-944c-d1b4ddb153cf, userName=admin, password=222222, gender=1, documentType=1, documentNum=2135488074882X, email=admin@163.com), User(userId=50d545f6-5735-4857-95b9-e09baf562ddc, userName=liaoyifan, password=liaoyifan1998, gender=0, documentType=1, documentNum=3333333, email=3069696872@qq.com), User(userId=631c5093-a6bd-4c62-ad77-d2239c3b9991, userName=miniship, password=miniship, gender=1, documentType=1, documentNum=2222, email=lyf1998118@gmail.com)])

2024-05-02 16:09:30.761 INFO   1 --- [http-nio-12031-exec-5] o.s.LoggingAspect: Entering in Method: queryOrdersForRefresh, Class: order.service.OrderServiceImpl, Arguments: [OrderInfo(loginId=50d545f6-5735-4857-95b9-e09baf562ddc, travelDateStart=null, travelDateEnd=null, boughtDateStart=null, boughtDateEnd=null, state=0, enableTravelDateQuery=false, enableBoughtDateQuery=false, enableStateQuery=false), 50d545f6-5735-4857-95b9-e09baf562ddc, [content-length:"223", accept:"application/json, text/javascript, */*; q=0.01", x-requested-with:"XMLHttpRequest", authorization:"Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJsaWFveWlmYW4iLCJyb2xlcyI6WyJST0xFX1VTRVIiXSwiaWQiOiI1MGQ1NDVmNi01NzM1LTQ4NTctOTViOS1lMDliYWY1NjJkZGMiLCJpYXQiOjE3MTQ2MzczNTYsImV4cCI6MTcxNDY0MDk1Nn0.fi2VDpkWx8BXuVXDmFf03Ok_Wrq7XtROywQHXmq1Xt8", user-agent:"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/120.0.6099.62 Safari/537.36", content-type:"application/json", origin:"http://192.168.49.2:32677", referer:"http://192.168.49.2:32677/client_order_list.html", accept-encoding:"gzip, deflate", cookie:"JSESSIONID=54636A62237FABE091C8C7643C4D8E2A; YsbCaptcha=99BE4F62DBB24EF1B3B1EE7462BA0504", forwarded:"proto=http;host="ts-gateway-service:18888";for="10.244.0.255:57874"", host:"10.244.1.0:12031", x-forwarded-proto:"http", x-forwarded-port:"18888", x-forwarded-host:"ts-gateway-service:18888"]], Return: Response(status=1, msg=Query Orders For Refresh Success, data=[Order(id=ea51cdaa-87d7-44a3-a281-8f9a3c89972e, boughtDate=2024-05-02 15:57:14, travelDate=2024-05-02, travelTime=2013-05-04 09:00:00, accountId=50d545f6-5735-4857-95b9-e09baf562ddc, contactsName=Jason, documentType=2, contactsDocumentNumber=EH9202323, trainNumber=G1234, coachNumber=5, seatClass=2, seatNumber=1665818175, from=nanjing, to=wuxi, status=4, price=150.0)])

2024-05-02 16:09:30.762 INFO   1 --- [http-nio-12032-exec-4] o.s.LoggingAspect: Entering in Method: queryOrdersForRefresh, Class: other.service.OrderOtherServiceImpl, Arguments: [QueryInfo(loginId=50d545f6-5735-4857-95b9-e09baf562ddc, travelDateStart=null, travelDateEnd=null, boughtDateStart=null, boughtDateEnd=null, state=0, enableTravelDateQuery=false, enableBoughtDateQuery=false, enableStateQuery=false), 50d545f6-5735-4857-95b9-e09baf562ddc, [content-length:"223", accept:"application/json, text/javascript, */*; q=0.01", x-requested-with:"XMLHttpRequest", authorization:"Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJsaWFveWlmYW4iLCJyb2xlcyI6WyJST0xFX1VTRVIiXSwiaWQiOiI1MGQ1NDVmNi01NzM1LTQ4NTctOTViOS1lMDliYWY1NjJkZGMiLCJpYXQiOjE3MTQ2MzczNTYsImV4cCI6MTcxNDY0MDk1Nn0.fi2VDpkWx8BXuVXDmFf03Ok_Wrq7XtROywQHXmq1Xt8", user-agent:"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/120.0.6099.62 Safari/537.36", content-type:"application/json", origin:"http://192.168.49.2:32677", referer:"http://192.168.49.2:32677/client_order_list.html", accept-encoding:"gzip, deflate", cookie:"JSESSIONID=54636A62237FABE091C8C7643C4D8E2A; YsbCaptcha=99BE4F62DBB24EF1B3B1EE7462BA0504", forwarded:"proto=http;host="ts-gateway-service:18888";for="10.244.0.255:57884"", host:"10.244.0.251:12032", x-forwarded-proto:"http", x-forwarded-port:"18888", x-forwarded-host:"ts-gateway-service:18888"]], Result: [Order(id=582eb81a-7431-4538-82b7-8fdfd923857b, boughtDate=2024-05-01 16:22:00, travelDate=2024-05-01, travelTime=2013-05-04 15:41:52, accountId=50d545f6-5735-4857-95b9-e09baf562ddc, contactsName=Jason, documentType=2, contactsDocumentNumber=EH9202323, trainNumber=Z1235, coachNumber=5, seatClass=3, seatNumber=1166717090, from=xuzhou, to=jinan, status=4, price=70.0)]
"""

checker = GPTChecker(
    api_key="sk-proj-DOiuAFHjceJz1shq3tn9T3BlbkFJyLl3N4v7d4slNHXF1EMV",
    model="gpt-4o",
    max_tokens=2048,
    top_p=0.9,
    temperature=0.0
)

result = checker.check_data_relationship(logs)

print(result)