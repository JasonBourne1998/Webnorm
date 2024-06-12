from gptchecker import GPTChecker

if __name__ == "__main__":
    class_name1 = "OrderUpdateDto"

    class_name2 = "PaymentInfo"

    class_definition1 = """
    public class OrderUpdateDto {

    @Id
    @Column(length = 36)
    @GeneratedValue(generator = "jpa-uuid")
    private String id;

    private String boughtDate;


    private String travelDate;


    private String travelTime;

    /**
     * Which Account Bought it
     */
    @Column(length = 36)
    private String accountId;

    /**
     * Tickets bought for whom....
     */
    private String contactsName;

    private int documentType;

    private String contactsDocumentNumber;

    private String trainNumber;

    private int coachNumber;

    private int seatClass;

    private String seatNumber;

    @Column(name = "from_station")
    private String from;

    @Column(name = "to_station")
    private String to;

    private int status;

    private String orderMoneyDifference;
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
        "2024-06-03 19:11:51.115 INFO 1 --- [http-nio-18886-exec-10] r.s.LoggingAspect: Entering in Method: rebook, Class: rebook.service.RebookServiceImpl, Arguments: [RebookInfo(loginId=, orderId=91150e66-7bd7-4dcf-83fb-afe7db6b8cc2, oldTripId=D1345, tripId=D1345, seatType=2, date=2024-06-03), authorization:Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJVc2VyX3Rlc3QiLCJyb2xlcyI6WyJST0xFX1VTRVIiXSwiaWQiOiI4NTVhMjNhMC02MzMxLTRmODctOGMyYi1hN2U2NDFkYWI0OGUiLCJpYXQiOjE3MTc0MTMwOTksImV4cCI6MTcxNzQxNjY5OX0._bC9RR6QZPKzsNDas3HA-Css3k2CNrc-epSZxURL6GI, Return: Response(status=2, msg=Success, OrderUpdateDto(id=91150e66-7bd7-4dcf-83fb-afe7db6b8cc2, boughtDate=2024-06-03 19:11:03, travelDate=2024-06-05, travelTime=2013-05-04 07:00:00, accountId=855a23a0-6331-4f87-8c2b-a7e641dab48e, contactsName=User_test, documentType=2, contactsDocumentNumber=EH080424, trainNumber=D1345, coachNumber=5, seatClass=3, seatNumber=1934982482, from=shanghai, to=suzhou, status=1, orderMoneyDifference=27.5)",
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
    
    # Event1: "2024-06-03 19:11:51.115 INFO 1 --- [http-nio-18886-exec-10] r.s.LoggingAspect: Entering in Method: rebook, Return: Rebookinfo('id': '91150e66-7bd7-4dcf-83fb-afe7db6b8cc2','tripId': 'D1345', 'seatType': 2, 'date': '2024-06-03, orderMoneyDifference=27.5)"
    # class_definition1 = """public class RebookInfo {
    # private String Id;
    # private String tripId;
    # private int seatType;
    # private String date;
    # private String orderMoneyDifference;
    # }
    # """
    # Event2: "2024-06-03 15:55:13.475 INFO   1 --- [http-nio-18673-exec-4] i.s.LoggingAspect: Entering in Method: payDifference, Arguments: [PaymentInfo(userId=855a23a0-6331-4f87-8c2b-a7e641dab48e, orderId=91150e66-7bd7-4dcf-83fb-afe7db6b8cc2, tripId=D1345, price=27.5)
    
    # class_definition2 = """
    # public class PaydifferenceDto {
    # private String orderId;
    # private String tripId;
    # private String userId;
    # private String money;
    # }
    # """
