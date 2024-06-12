import json
from dataflow_and_trigger import *

log_file_path = "/home/yifannus2023/TamperLogPrompt/Train_data_modify.txt"
log_lines = read_log_file(log_file_path)
with open("/home/yifannus2023/TamperLogPrompt/openAPI.json","r") as fp:
    API_data = json.load(fp)
res = {}
for API_name, API_path in API_data.items():
    if API_name not in list(res.keys()):
        res[API_name] = []
    for line in log_lines:
        service,function = API_name.split(" ")
        if service in line and function in line:
            res[API_name].append(line)
# print(res)
with open("/home/yifannus2023/TamperLogPrompt/log_target.json","w") as fp:
    json.dump(res,fp)
    

1 reBook ( index , type , number ) {
2 // handle incoming info
3 var that = this ;
4 var rebookInfo = new Object() ;
5 rebookInfo.orderId = that.selectedOrderId ;
6 rebookInfo.oldTripId = that.oldTripId ;
7 rebookInfo.tripId = type + number;
8 rebookInfo.seatType = that.Seats[index];
9 sendAjaxRequest("/api/v1/rebookservice/rebook",
                   rebookInfo,function(res) {
10  if (res.data['differenceMoney'] == 0) {
11      updateOrder (rebookInfo);
12 } else {
13  // Pay difference
14 sendAjaxRequest("/api/v1/rebookservice/paydifference",
                   res.data['differenceMoney'],function(result) {
15      updateOrder(rebookInfo)});}
16  });
17 }

reBook ( index , type , number ) {
// handle incoming info
var that = this ;
var rebookInfo = new Object() ;
rebookInfo.orderId = that.selectedOrderId ;
rebookInfo.oldTripId = that.oldTripId ;
rebookInfo.tripId = type + number;
rebookInfo.seatType = that.Seats[index];
sendAjaxRequest("/api/v1/rebookservice/rebook",
                   rebookInfo,function(res) {
if (res.data['differenceMoney'] == 0) {
    updateOrder (rebookInfo);
} else {
    // Pay difference
    sendAjaxRequest("/api/v1/rebookservice/paydifference",
                   res.data['differenceMoney'],function(result) {
    updateOrder(rebookInfo)});}
  });
}
