from gptchecker import GPTChecker

if __name__ == "__main__":
    class_name1 = "RebookInfo"

    class_name2 = "PaymentInfo"

    class_definition1 = """
    RebookInfo {

    @Valid
    @NotNull
    private String loginId;

    @Valid
    @NotNull
    private String orderId;

    @Valid
    @NotNull
    private String oldTripId;

    @Valid
    @NotNull
    private String tripId;

    @Valid
    @NotNull
    private int seatType;

    @Valid
    @NotNull
    private String date;

    public RebookInfo(){
        //Default Constructor
        this.loginId = "";
        this.orderId = "";
        this.oldTripId = "";
        this.tripId = "";
        this.seatType = 0;
        this.date = StringUtils.Date2String(new Date());
    }

}
    """

    class_definition2 = """
    public class PaydifferenceDto {
    private String orderId;
    private String tripId;
    private String userId;
    private String money;
}
    """

    logs = [
        "2024-06-03 19:11:51.115 INFO   1 --- [http-nio-18886-exec-10] r.s.LoggingAspect: Entering in Method: rebook, Class: rebook.service.RebookServiceImpl, Arguments: [RebookInfo(loginId=, orderId=91150e66-7bd7-4dcf-83fb-afe7db6b8cc2, oldTripId=D1345, tripId=D1345, seatType=2, date=2024-06-03),  authorization:Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJVc2VyX3Rlc3QiLCJyb2xlcyI6WyJST0xFX1VTRVIiXSwiaWQiOiI4NTVhMjNhMC02MzMxLTRmODctOGMyYi1hN2U2NDFkYWI0OGUiLCJpYXQiOjE3MTc0MTMwOTksImV4cCI6MTcxNzQxNjY5OX0._bC9RR6QZPKzsNDas3HA-Css3k2CNrc-epSZxURL6GI, Return: Response(status=2, msg=Success, data=OrderUpdateDto(order=Order(id=91150e66-7bd7-4dcf-83fb-afe7db6b8cc2, boughtDate=2024-06-03 19:11:03, travelDate=2024-06-05, travelTime=2013-05-04 07:00:00, accountId=855a23a0-6331-4f87-8c2b-a7e641dab48e, contactsName=User_test, documentType=2, contactsDocumentNumber=EH080424, trainNumber=D1345, coachNumber=5, seatClass=3, seatNumber=1934982482, from=shanghai, to=suzhou, status=1, price=22.5, differenceMoney=0.0), rebookInfo=null, tripAllDetail=TripAllDetail(status=false, message=null, tripResponse=TripResponse(tripId=D1345, trainTypeName=DongCheOne, startStation=shanghai, terminalStation=suzhou, startTime=2013-05-04 07:00:00, endTime=2013-05-04 07:16:00, economyClass=1073741820, confortClass=1073741820, priceForEconomyClass=22.5, priceForConfortClass=50.0), trip=Trip(id=e07590f6-b759-4358-bac4-6e33b1f62306, tripId=D1345, trainTypeName=DongCheOne, routeId=f3d4d4ef-693b-4456-8eed-59c0d717dd08, startStationName=shanghai, stationsName=suzhou, terminalStationName=taiyuan, startTime=2013-05-04 07:00:00, endTime=2013-05-04 19:59:52)), ticketPrice=50.0, orderMoneyDifference=27.5))",
        "2024-06-03 15:55:13.475 INFO   1 --- [http-nio-18673-exec-4] i.s.LoggingAspect: Entering in Method: Entering in Method: payDifference, Class: inside_payment.service.InsidePaymentServiceImpl, Arguments: [PaymentInfo(userId=855a23a0-6331-4f87-8c2b-a7e641dab48e, orderId=91150e66-7bd7-4dcf-83fb-afe7db6b8cc2, tripId=D1345, price=27.5), authorization: Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmZHNlX21pY3Jvc2VydmljZSIsInJvbGVzIjpbIlJPTEVfVVNFUiJdLCJpZCI6IjRkMmE0NmM3LTcxY2ItNGNmMS1iNWJiLWI2ODQwNmQ5ZGE2ZiIsImlhdCI6MTcxNzQwMTI5NSwiZXhwIjoxNzE3NDA0ODk1fQ.VPT6VQ2WUgUyTz9qJ5XhlPr1S2bMBpFGvohSEswPKQA ,Return: Response(status=1, msg=Pay Difference Success, data=null)"
    ]

    checker = GPTChecker(
        api_key="sk-proj-enNNZd2GZEkaDuRa3rPfT3BlbkFJph7uEdwchQlAXWY5gm2G",
        model="gpt-4o",
        max_tokens=2048,
        top_p=0.9,
        temperature=0.0
    )

    result = checker.check_input_constraint(
        class_name1=class_name1,
        class_name2=class_name2,
        class_definition1=class_definition1,
        class_definition2=class_definition2,
        logs=logs
    )
    print(result)
    # code_string = result[1]
    # exec(code_string)

    # # 现在可以使用 is_related 函数
    # instance_A = {'id': 123, 'price': 99.99}
    # instance_B = {'orderId': 123, 'price': 99.99}

    # print(is_related(instance_A, instance_B)) 