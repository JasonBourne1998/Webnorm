from gptchecker import GPTChecker

class_name = "OrderTicketsInfo"

class_definition = """
OrderTicketsInfo {
    private String accountId;
    private String contactsId;

    private String tripId;

    private int seatType;

    private String loginToken;

    private String date;

    private String from;

    private String to;
    private int assurance;

    private int foodType = 0;

    private String stationName;

    private String storeName;

    private String foodName;

    private double foodPrice;


    private String handleDate;

    private String consigneeName;

    private String consigneePhone;

    private double consigneeWeight;

    private boolean isWithin;

    public String getFrom() {
        return StringUtils.String2Lower(this.from);
    }

    public String getTo() {
        return StringUtils.String2Lower(this.to);
    }

}
"""

logs = [
    "2024-05-14 20:22:07.036 INFO   1 --- [http-nio-14568-exec-3] p.s.LoggingAspect: Entering in Method: preserve, Class: preserve.service.PreserveServiceImpl, Arguments: [OrderTicketsInfo(accountId=50d545f6-5735-4857-95b9-e09baf562ddc, contactsId=50b55cf9-6b3a-4909-9e33-be43d81f1a20, tripId=G1234, seatType=2, loginToken=null, date=2024-05-14, from=zhenjiang, to=shanghai, assurance=0, foodType=1, stationName=, storeName=, foodName=Bone Soup, foodPrice=2.5, handleDate=2024-05-14, consigneeName=kpmcSwIy, consigneePhone=25, consigneeWeight=43.0, isWithin=false)",
    "2024-05-02 17:46:24.613 INFO   1 --- [http-nio-14568-exec-4] p.s.LoggingAspect: Entering in Method: preserve, Class: preserve.service.PreserveServiceImpl, Arguments: [OrderTicketsInfo(accountId=50d545f6-5735-4857-95b9-e09baf562ddc, contactsId=50b55cf9-6b3a-4909-9e33-be43d81f1a20, tripId=G1237, seatType=3, loginToken=null, date=2024-05-02, from=suzhou, to=shanghai, assurance=0, foodType=1, stationName=, storeName=, foodName=Rice, foodPrice=1.2, handleDate=2024-05-02, consigneeName=TuygJcjd, consigneePhone=651794038, consigneeWeight=56.0, isWithin=false)",
    "2024-05-14 17:25:14.854 INFO   1 --- [http-nio-14568-exec-9] p.s.LoggingAspect: Entering in Method: preserve, Class: preserve.service.PreserveServiceImpl, Arguments: [OrderTicketsInfo(accountId=50d545f6-5735-4857-95b9-e09baf562ddc, contactsId=50b55cf9-6b3a-4909-9e33-be43d81f1a20, tripId=G1236, seatType=3, loginToken=null, date=2024-05-15, from=suzhou, to=shanghai, assurance=0, foodType=1, stationName=, storeName=, foodName=Bone Soup, foodPrice=2.5, handleDate=null, consigneeName=null, consigneePhone=null, consigneeWeight=0.0, isWithin=false),"
]

checker = GPTChecker(
    api_key="sk-proj-enNNZd2GZEkaDuRa3rPfT3BlbkFJph7uEdwchQlAXWY5gm2G",
    model="gpt-4o",
    max_tokens=2048,
    top_p=0.9,
    temperature=0.0
)

result = checker.check_commonsense_constraint(
    class_name=class_name,
    class_definition=class_definition,
    logs=logs
)