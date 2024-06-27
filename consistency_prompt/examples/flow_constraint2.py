import sys 
sys.path.append("../")
from gptchecker import GPTChecker
import os
from dotenv import load_dotenv

# 加载 .env 文件
env_path = '../.env'
load_dotenv(dotenv_path=env_path)
api_key = os.getenv('API_KEY')


logs1 = [
    "2024-05-14 15:52:12.394 INFO   1 --- [http-nio-18886-exec-7] r.s.LoggingAspect: Entering in Method: rebook, Class: rebook.service.RebookServiceImpl, Arguments: [rebookInfo=null, tripAllDetail=TripAllDetail(status=false, message=null, tripResponse=TripResponse(tripId=G1234, trainTypeName=GaoTieOne, startStation=nanjing, terminalStation=suzhou, startTime=2013-05-04 09:00:00, endTime=2013-05-04 09:48:00, economyClass=1073741819, confortClass=1073741819, priceForEconomyClass=76.0, priceForConfortClass=200.0), trip=Trip(id=83e91a65-4549-4614-bf2f-5cbabc8dfa0c, tripId=G1234, trainTypeName=GaoTieOne, routeId=92708982-77af-4318-be25-57ccb0ff69ad, startStationName=shanghai, stationsName=suzhou, terminalStationName=taiyuan, startTime=2013-05-04 09:00:00, endTime=2013-05-04 15:51:52)), ticketPrice=200.0, orderMoneyDifference=60.0))",
    "2024-05-14 16:07:53.805 INFO   1 --- [http-nio-18886-exec-10] r.s.LoggingAspect: Entering in Method: rebook, Class: rebook.service.RebookServiceImpl, Arguments: [rebookInfo=null, tripAllDetail=TripAllDetail(status=false, message=null, tripResponse=TripResponse(tripId=D1345, trainTypeName=DongCheOne, startStation=shanghai, terminalStation=suzhou, startTime=2013-05-04 07:00:00, endTime=2013-05-04 07:16:00, economyClass=1073741821, confortClass=1073741821, priceForEconomyClass=22.5, priceForConfortClass=50.0), trip=Trip(id=67f8ced9-80db-4bd2-aaeb-6a40206fe261, tripId=D1345, trainTypeName=DongCheOne, routeId=f3d4d4ef-693b-4456-8eed-59c0d717dd08, startStationName=shanghai, stationsName=suzhou, terminalStationName=taiyuan, startTime=2013-05-04 07:00:00, endTime=2013-05-04 19:59:52)), ticketPrice=50.0, orderMoneyDifference=27.5))",
    "2024-05-14 17:16:23.061 INFO   1 --- [http-nio-18886-exec-3] r.s.LoggingAspect: Entering in Method: rebook, Class: rebook.service.RebookServiceImpl, Arguments: [rebookInfo=null, tripAllDetail=TripAllDetail(status=false, message=null, tripResponse=TripResponse(tripId=G1234, trainTypeName=GaoTieOne, startStation=zhenjiang, terminalStation=shanghai, startTime=2013-05-04 09:24:00, endTime=2013-05-04 10:00:00, economyClass=1073741818, confortClass=1073741818, priceForEconomyClass=57.0, priceForConfortClass=150.0), trip=Trip(id=83e91a65-4549-4614-bf2f-5cbabc8dfa0c, tripId=G1234, trainTypeName=GaoTieOne, routeId=92708982-77af-4318-be25-57ccb0ff69ad, startStationName=shanghai, stationsName=suzhou, terminalStationName=taiyuan, startTime=2013-05-04 09:00:00, endTime=2013-05-04 15:51:52)), ticketPrice=150.0, orderMoneyDifference=93.0))",
    "2024-05-14 17:27:49.390 INFO   1 --- [http-nio-18886-exec-10] r.s.LoggingAspect: Entering in Method: rebook, Class: rebook.service.RebookServiceImpl, Arguments: [rebookInfo=null, tripAllDetail=TripAllDetail(status=false, message=null, tripResponse=TripResponse(tripId=D1345, trainTypeName=DongCheOne, startStation=shanghai, terminalStation=suzhou, startTime=2013-05-04 07:00:00, endTime=2013-05-04 07:16:00, economyClass=1073741808, confortClass=1073741808, priceForEconomyClass=22.5, priceForConfortClass=50.0), trip=Trip(id=67f8ced9-80db-4bd2-aaeb-6a40206fe261, tripId=D1345, trainTypeName=DongCheOne, routeId=f3d4d4ef-693b-4456-8eed-59c0d717dd08, startStationName=shanghai, stationsName=suzhou, terminalStationName=taiyuan, startTime=2013-05-04 07:00:00, endTime=2013-05-04 19:59:52)), ticketPrice=50.0, orderMoneyDifference=27.5))"
]

logs2 = [
    "2024-05-14 16:43:09.011 INFO   1 --- [http-nio-18886-exec-8] r.s.LoggingAspect: Entering in Method: rebook, Class: rebook.service.RebookServiceImpl, Arguments: [rebookInfo=null, tripAllDetail=TripAllDetail(status=false, message=null, tripResponse=TripResponse(tripId=D1345, trainTypeName=DongCheOne, startStation=shanghai, terminalStation=suzhou, startTime=2013-05-04 07:00:00, endTime=2013-05-04 07:16:00, economyClass=1073741813, confortClass=1073741813, priceForEconomyClass=22.5, priceForConfortClass=50.0), trip=Trip(id=67f8ced9-80db-4bd2-aaeb-6a40206fe261, tripId=D1345, trainTypeName=DongCheOne, routeId=f3d4d4ef-693b-4456-8eed-59c0d717dd08, startStationName=shanghai, stationsName=suzhou, terminalStationName=taiyuan, startTime=2013-05-04 07:00:00, endTime=2013-05-04 19:59:52)), ticketPrice=22.5, orderMoneyDifference=0.0))",
    "2024-05-14 16:59:38.345 INFO   1 --- [http-nio-18886-exec-10] r.s.LoggingAspect: Entering in Method: rebook, Class: rebook.service.RebookServiceImpl, Arguments: [rebookInfo=null, tripAllDetail=TripAllDetail(status=false, message=null, tripResponse=TripResponse(tripId=G1236, trainTypeName=GaoTieOne, startStation=nanjing, terminalStation=shanghai, startTime=2013-05-04 14:00:00, endTime=2013-05-04 15:00:00, economyClass=1073741823, confortClass=1073741823, priceForEconomyClass=175.0, priceForConfortClass=250.0), trip=Trip(id=d5b5d7ae-9b33-43a9-b2c9-096af063bd09, tripId=G1236, trainTypeName=GaoTieOne, routeId=a3f256c1-0e43-4f7d-9c21-121bf258101f, startStationName=shanghai, stationsName=suzhou, terminalStationName=taiyuan, startTime=2013-05-04 14:00:00, endTime=2013-05-04 20:51:52)), ticketPrice=250.0, orderMoneyDifference=0.0))",
    "2024-05-14 17:00:59.620 INFO   1 --- [http-nio-18886-exec-9] r.s.LoggingAspect: Entering in Method: rebook, Class: rebook.service.RebookServiceImpl, Arguments: [rebookInfo=null, tripAllDetail=TripAllDetail(status=false, message=null, tripResponse=TripResponse(tripId=G1237, trainTypeName=GaoTieTwo, startStation=suzhou, terminalStation=shanghai, startTime=2013-05-04 08:00:00, endTime=2013-05-04 08:15:00, economyClass=1073741823, confortClass=1073741823, priceForEconomyClass=30.0, priceForConfortClass=50.0), trip=Trip(id=297ab826-66a6-410f-bfd5-93c94cea3601, tripId=G1237, trainTypeName=GaoTieTwo, routeId=084837bb-53c8-4438-87c8-0321a4d09917, startStationName=shanghai, stationsName=suzhou, terminalStationName=taiyuan, startTime=2013-05-04 08:00:00, endTime=2013-05-04 17:21:52)), ticketPrice=30.0, orderMoneyDifference=0.0))",
    "2024-05-14 17:11:51.684 INFO   1 --- [http-nio-18886-exec-3] r.s.LoggingAspect: Entering in Method: rebook, Class: rebook.service.RebookServiceImpl, Arguments: [rebookInfo=null, tripAllDetail=TripAllDetail(status=false, message=null, tripResponse=TripResponse(tripId=G1237, trainTypeName=GaoTieTwo, startStation=suzhou, terminalStation=shanghai, startTime=2013-05-04 08:00:00, endTime=2013-05-04 08:15:00, economyClass=1073741822, confortClass=1073741822, priceForEconomyClass=30.0, priceForConfortClass=50.0), trip=Trip(id=297ab826-66a6-410f-bfd5-93c94cea3601, tripId=G1237, trainTypeName=GaoTieTwo, routeId=084837bb-53c8-4438-87c8-0321a4d09917, startStationName=shanghai, stationsName=suzhou, terminalStationName=taiyuan, startTime=2013-05-04 08:00:00, endTime=2013-05-04 17:21:52)), ticketPrice=30.0, orderMoneyDifference=0.0))",
    "2024-05-14 17:24:38.207 INFO   1 --- [http-nio-18886-exec-6] r.s.LoggingAspect: Entering in Method: rebook, Class: rebook.service.RebookServiceImpl, Arguments: [rebookInfo=null, tripAllDetail=TripAllDetail(status=false, message=null, tripResponse=TripResponse(tripId=G1234, trainTypeName=GaoTieOne, startStation=nanjing, terminalStation=suzhou, startTime=2013-05-04 09:00:00, endTime=2013-05-04 09:48:00, economyClass=1073741818, confortClass=1073741818, priceForEconomyClass=76.0, priceForConfortClass=200.0), trip=Trip(id=83e91a65-4549-4614-bf2f-5cbabc8dfa0c, tripId=G1234, trainTypeName=GaoTieOne, routeId=92708982-77af-4318-be25-57ccb0ff69ad, startStationName=shanghai, stationsName=suzhou, terminalStationName=taiyuan, startTime=2013-05-04 09:00:00, endTime=2013-05-04 15:51:52)), ticketPrice=76.0, orderMoneyDifference=0.0))"
]

parent_url= "/api/v1/rebookService/rebook"

child_url1 = "/api/v1/rebookService/payDifference"

child_url2 = "/api/v1/rebookService/updateOrder"

checker = GPTChecker(
    api_key=api_key,
    model="gpt-4o",
    max_tokens=2048,
    top_p=0.9,
    temperature=0.0,
    turns=10
)

result = checker.check_flow_constraint(
    parent_url,
    child_url1,
    child_url2,
    logs1,
    logs2
)
# print(result[1])