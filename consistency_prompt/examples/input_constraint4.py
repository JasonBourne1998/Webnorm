import sys 
sys.path.append("../")
from gptchecker import GPTChecker
import os
from dotenv import load_dotenv

# 加载 .env 文件
env_path = '../.env'
load_dotenv(dotenv_path=env_path)
api_key = os.getenv('API_KEY')

if __name__ == "__main__":
    class_name1 = "Order"

    class_name2 = "CancelInfo"

    class_definition1 = """

    /**
    * @author fdse
    */
    @Data
    @Table(name = "orders_other")
    @Entity
    @GenericGenerator(name = "jpa-uuid", strategy = "org.hibernate.id.UUIDGenerator")
    @ToString
    @JsonIgnoreProperties(ignoreUnknown = true)
    public class Order {
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

        private String price;

        public Order(){
            boughtDate = StringUtils.Date2String(new Date(System.currentTimeMillis()));
            travelDate = StringUtils.Date2String(new Date(123456789));
            trainNumber = "G1235";
            coachNumber = 5;
            seatClass = SeatClass.FIRSTCLASS.getCode();
            seatNumber = "1";
            from = "shanghai";
            to = "taiyuan";
            status = OrderStatus.PAID.getCode();
            price = "0.0";
        }

        @Override
        public boolean equals(Object obj) {
            if (this == obj) {
                return true;
            }
            if (obj == null) {
                return false;
            }
            if (getClass() != obj.getClass()) {
                return false;
            }
            Order other = (Order) obj;
            return getBoughtDate().equals(other.getBoughtDate())
                    && getBoughtDate().equals(other.getTravelDate())
                    && getTravelTime().equals(other.getTravelTime())
                    && accountId .equals( other.getAccountId() )
                    && contactsName.equals(other.getContactsName())
                    && contactsDocumentNumber.equals(other.getContactsDocumentNumber())
                    && documentType == other.getDocumentType()
                    && trainNumber.equals(other.getTrainNumber())
                    && coachNumber == other.getCoachNumber()
                    && seatClass == other.getSeatClass()
                    && seatNumber .equals(other.getSeatNumber())
                    && from.equals(other.getFrom())
                    && to.equals(other.getTo())
                    && status == other.getStatus()
                    && price.equals(other.price);
        }

        @Override
        public int hashCode() {
            int result = 17;
            result = 31 * result + (id == null ? 0 : id.hashCode());
            return result;
        }

    }
    """

    class_definition2 = """

    /**
    * @author fdse
    */
    @Data
    @Entity
    @GenericGenerator(name = "jpa-uuid", strategy = "org.hibernate.id.UUIDGenerator")
    public class CancelInfo {
        @Id
        @NotNull
        @Column(length = 36)
        @GeneratedValue(generator = "jpa-uuid")
        private String OrderId;

        @NotNull
        @Valid
        @Column(length = 36)
        private String Id;

    }
    """

    logs = [
        "2024-05-01 18:31:10.293 INFO   1 --- [http-nio-12031-exec-2] o.s.LoggingAspect: Entering in Method: queryOrdersForRefresh, Class: order.service.OrderServiceImpl, Arguments: [OrderInfo(loginId=50d545f6-5735-4857-95b9-e09baf562ddc, travelDateStart=null, travelDateEnd=null, boughtDateStart=null, boughtDateEnd=null, state=0, enableTravelDateQuery=false, enableBoughtDateQuery=false, enableStateQuery=false), 50d545f6-5735-4857-95b9-e09baf562ddc,  authorization:Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJsaWFveWlmYW4iLCJyb2xlcyI6WyJST0xFX1VTRVIiXSwiaWQiOiI1MGQ1NDVmNi01NzM1LTQ4NTctOTViOS1lMDliYWY1NjJkZGMiLCJpYXQiOjE3MTQ1NTk0NTQsImV4cCI6MTcxNDU2MzA1NH0.zeYFLwPudVdxG3SvVNRUi01oLk3s0yDag0RGmhoDUK8,  Return: Response(status=1, msg=Query Orders For Refresh Success, data=[Order(id=3fc21c15-72a6-4dd5-808e-1a9a42db5f60, boughtDate=2024-05-01 16:16:15, travelDate=2024-05-01, travelTime=2013-05-04 07:00:00, accountId=50d545f6-5735-4857-95b9-e09baf562ddc, contactsName=Jason, documentType=2, contactsDocumentNumber=EH9202323, trainNumber=D1345, coachNumber=5, seatClass=2, seatNumber=1623500807, from=shanghai, to=suzhou, status=6, price=50.0), Order(id=5ee8873c-f99e-4d97-b603-1b87873e3d34, boughtDate=2024-05-01 16:17:54, travelDate=2024-05-01, travelTime=2013-05-04 09:00:00, accountId=50d545f6-5735-4857-95b9-e09baf562ddc, contactsName=Jason, documentType=2, contactsDocumentNumber=EH9202323, trainNumber=G1234, coachNumber=5, seatClass=2, seatNumber=539659046, from=nanjing, to=suzhou, status=4, price=200.0), Order(id=6e7c6eca-0e07-43d6-b599-794ba2dac8ff, boughtDate=2024-05-01 16:36:51, travelDate=2024-05-01, travelTime=2013-05-04 09:24:00, accountId=50d545f6-5735-4857-95b9-e09baf562ddc, contactsName=Jason, documentType=2, contactsDocumentNumber=EH9202323, trainNumber=G1234, coachNumber=5, seatClass=2, seatNumber=712051873, from=zhenjiang, to=suzhou, status=4, price=100.0)])",
        "2024-05-24 15:33:16.500 INFO   1 --- [http-nio-18885-exec-5] c.s.LoggingAspect: Entering in Method: cancelOrder, Class: cancel.service.CancelServiceImpl, Arguments: [CancelInfo(OrderId= 6e7c6eca-0e07-43d6-b599-794ba2dac8ff, Id=50d545f6-5735-4857-95b9-e09baf562ddc), authorization:Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJsaWFveWlmYW4iLCJyb2xlcyI6WyJST0xFX1VTRVIiXSwiaWQiOiI1MGQ1NDVmNi01NzM1LTQ4NTctOTViOS1lMDliYWY1NjJkZGMiLCJpYXQiOjE3MTQ1NTk0NTQsImV4cCI6MTcxNDU2MzA1NH0.zeYFLwPudVdxG3SvVNRUi01oLk3s0yDag0RGmhoDUK8], Return: Response(status=1, msg=Success., data=test not null)]",
        "2024-06-07 22:29:14.577 INFO   1 --- [http-nio-12031-exec-7] o.s.LoggingAspect: Entering in Method: queryOrdersForRefresh, Class: order.service.OrderServiceImpl, Arguments: [OrderInfo(loginId=c4f1da0b-b6c6-412c-944c-d324ddb153ca, travelDateStart=null, travelDateEnd=null, boughtDateStart=null, boughtDateEnd=null, state=0, enableTravelDateQuery=false, enableBoughtDateQuery=false, enableStateQuery=false), c4f1da0b-b6c6-412c-944c-d324ddb153ca, authorization:Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJsaWFveWlmYW4iLCJyb2xlcyI6WyJST0xFX1VTRVIiXSwiaWQiOiJjNGYxZGEwYi1iNmM2LTQxMmMtOTQ0Yy1kMzI0ZGRiMTUzY2EiLCJpYXQiOjE3MTc3NzA1NTMsImV4cCI6MTcxNzc3NDE1M30.DtzrMeHTJ-OmivpTM12BEgiCFWSdtYaX8CmKgJfnQGg, Return: Response(status=1, msg=Query Orders For Refresh Success, data=[Order(id=66523b66-5c0c-44a0-93ad-219ee076b81f, boughtDate=2024-06-03 14:49:23, travelDate=2024-06-05, travelTime=2013-05-04 07:00:00, accountId=c4f1da0b-b6c6-412c-944c-d324ddb153ca, contactsName=Jason, documentType=2, contactsDocumentNumber=TREJK232, trainNumber=D1345, coachNumber=5, seatClass=2, seatNumber=1500845267, from=shanghai, to=suzhou, status=4, price=50.0), Order(id=857f73a5-2929-4d81-87e6-8e8810c07629, boughtDate=2024-06-05 22:23:02, travelDate=2024-06-07, travelTime=2013-05-04 07:00:00, accountId=c4f1da0b-b6c6-412c-944c-d324ddb153ca, contactsName=Jason, documentType=2, contactsDocumentNumber=TREJK232, trainNumber=D1345, coachNumber=5, seatClass=3, seatNumber=1153012708, from=shanghai, to=suzhou, status=4, price=22.5), Order(id=0c3e8a2c-cedd-40ef-87ee-06eb78dc005e, boughtDate=2024-06-05 22:29:01, travelDate=2024-06-06, travelTime=2013-05-04 09:48:00, accountId=c4f1da0b-b6c6-412c-944c-d324ddb153ca, contactsName=Jason, documentType=2, contactsDocumentNumber=TREJK232, trainNumber=G1234, coachNumber=5, seatClass=2, seatNumber=1843966145, from=suzhou, to=shanghai, status=4, price=50.0), Order(id=a5b20b88-41f2-4704-a2d0-bc4f28ecdef1, boughtDate=2024-06-05 22:48:58, travelDate=2024-06-07, travelTime=2013-05-04 09:48:00, accountId=c4f1da0b-b6c6-412c-944c-d324ddb153ca, contactsName=Jason, documentType=2, contactsDocumentNumber=TREJK232, trainNumber=G1234, coachNumber=5, seatClass=2, seatNumber=916558411, from=suzhou, to=shanghai, status=4, price=50.0), Order(id=80dcb992-6f48-4179-a04b-170d1f5953e0, boughtDate=2024-06-05 23:06:45, travelDate=2024-06-07, travelTime=2013-05-04 07:00:00, accountId=c4f1da0b-b6c6-412c-944c-d324ddb153ca, contactsName=Jason, documentType=2, contactsDocumentNumber=TREJK232, trainNumber=D1345, coachNumber=5, seatClass=3, seatNumber=407625143, from=shanghai, to=suzhou, status=4, price=22.5), Order(id=8fd0129c-0355-4540-a179-c034f0697d96, boughtDate=2024-06-05 23:18:58, travelDate=2024-06-07, travelTime=2013-05-04 09:48:00, accountId=c4f1da0b-b6c6-412c-944c-d324ddb153ca, contactsName=Joseph, documentType=3, contactsDocumentNumber=GFEN321, trainNumber=G1234, coachNumber=5, seatClass=2, seatNumber=2049991284, from=suzhou, to=shanghai, status=4, price=50.0), Order(id=5215fec2-118d-4064-8756-634c037de4eb, boughtDate=2024-06-05 23:31:47, travelDate=2024-06-07, travelTime=2013-05-04 09:00:00, accountId=c4f1da0b-b6c6-412c-944c-d324ddb153ca, contactsName=Joseph, documentType=3, contactsDocumentNumber=GFEN321, trainNumber=G1234, coachNumber=5, seatClass=2, seatNumber=174505174, from=nanjing, to=suzhou, status=6, price=200.0), Order(id=7020d310-e78c-4f00-827b-8c0418634a1d, boughtDate=2024-06-05 23:44:07, travelDate=2024-06-07, travelTime=2013-05-04 09:00:00, accountId=c4f1da0b-b6c6-412c-944c-d324ddb153ca, contactsName=Jason, documentType=2, contactsDocumentNumber=TREJK232, trainNumber=G1234, coachNumber=5, seatClass=3, seatNumber=1207089136, from=nanjing, to=wuxi, status=4, price=57.0), Order(id=2755d7ef-a92b-440c-80f5-477c0c7a581e, boughtDate=2024-06-05 23:56:27, travelDate=2024-06-07, travelTime=2013-05-04 14:48:00, accountId=c4f1da0b-b6c6-412c-944c-d324ddb153ca, contactsName=Jason, documentType=2, contactsDocumentNumber=TREJK232, trainNumber=G1236, coachNumber=5, seatClass=2, seatNumber=249521574, from=suzhou, to=shanghai, status=4, price=50.0), Order(id=dab80a0e-aff6-4e84-a9c3-db048927563e, boughtDate=2024-06-06 00:01:25, travelDate=2024-06-07, travelTime=2013-05-04 09:00:00, accountId=c4f1da0b-b6c6-412c-944c-d324ddb153ca, contactsName=Joseph, documentType=3, contactsDocumentNumber=GFEN321, trainNumber=G1234, coachNumber=5, seatClass=3, seatNumber=1305047450, from=nanjing, to=zhenjiang, status=4, price=38.0), Order(id=463c2a47-f3bb-4f49-9718-0f4d46a77f70, boughtDate=2024-06-06 00:41:16, travelDate=2024-06-07, travelTime=2013-05-04 09:00:00, accountId=c4f1da0b-b6c6-412c-944c-d324ddb153ca, contactsName=Joseph, documentType=3, contactsDocumentNumber=GFEN321, trainNumber=G1234, coachNumber=5, seatClass=2, seatNumber=2110052400, from=nanjing, to=wuxi, status=6, price=150.0), Order(id=8192a411-cf1c-411d-84ca-7c320340a262, boughtDate=2024-06-06 00:53:30, travelDate=2024-06-07, travelTime=2013-05-04 09:00:00, accountId=c4f1da0b-b6c6-412c-944c-d324ddb153ca, contactsName=Joseph, documentType=3, contactsDocumentNumber=GFEN321, trainNumber=G1234, coachNumber=5, seatClass=2, seatNumber=663790064, from=nanjing, to=wuxi, status=4, price=150.0), Order(id=ddec4ad2-d6d2-4e79-b4f9-cf0e25c81e47, boughtDate=2024-06-06 01:26:41, travelDate=2024-06-07, travelTime=2013-05-04 09:00:00, accountId=c4f1da0b-b6c6-412c-944c-d324ddb153ca, contactsName=Joseph, documentType=3, contactsDocumentNumber=GFEN321, trainNumber=G1234, coachNumber=5, seatClass=3, seatNumber=592758066, from=nanjing, to=suzhou, status=4, price=76.0), Order(id=dc5a10ec-1f95-4df0-9904-e13d66c09728, boughtDate=2024-06-06 01:43:14, travelDate=2024-06-08, travelTime=2013-05-04 09:24:00, accountId=c4f1da0b-b6c6-412c-944c-d324ddb153ca, contactsName=Jason, documentType=2, contactsDocumentNumber=TREJK232, trainNumber=G1234, coachNumber=5, seatClass=2, seatNumber=1671043821, from=zhenjiang, to=wuxi, status=6, price=50.0), Order(id=030bf157-2937-497a-99a5-b62a1c10f3bb, boughtDate=2024-06-06 02:51:00, travelDate=2024-06-08, travelTime=2013-05-04 09:48:00, accountId=c4f1da0b-b6c6-412c-944c-d324ddb153ca, contactsName=Jason, documentType=2, contactsDocumentNumber=TREJK232, trainNumber=G1234, coachNumber=5, seatClass=3, seatNumber=1671043821, from=suzhou, to=shanghai, status=4, price=19.0), Order(id=ea607388-1219-4c24-875d-b639c7a4b33e, boughtDate=2024-06-06 02:56:34, travelDate=2024-06-07, travelTime=2013-05-04 09:00:00, accountId=c4f1da0b-b6c6-412c-944c-d324ddb153ca, contactsName=Jason, documentType=2, contactsDocumentNumber=TREJK232, trainNumber=G1234, coachNumber=5, seatClass=3, seatNumber=1006008806, from=nanjing, to=wuxi, status=4, price=57.0), Order(id=5eb5e444-4a8e-4fad-8a0d-dfe28cc536c7, boughtDate=2024-06-06 03:04:19, travelDate=2024-06-08, travelTime=2013-05-04 09:24:00, accountId=c4f1da0b-b6c6-412c-944c-d324ddb153ca, contactsName=Joseph, documentType=3, contactsDocumentNumber=GFEN321, trainNumber=G1234, coachNumber=5, seatClass=3, seatNumber=832587659, from=zhenjiang, to=shanghai, status=4, price=57.0), Order(id=52e09a31-e66b-46e6-9164-a467786b4e96, boughtDate=2024-06-06 03:17:05, travelDate=2024-06-08, travelTime=2013-05-04 07:00:00, accountId=c4f1da0b-b6c6-412c-944c-d324ddb153ca, contactsName=Joseph, documentType=3, contactsDocumentNumber=GFEN321, trainNumber=D1345, coachNumber=5, seatClass=2, seatNumber=1604258223, from=shanghai, to=suzhou, status=4, price=50.0), Order(id=7f964298-e5df-4a99-bbfd-b355e17f2b3e, boughtDate=2024-06-06 03:31:52, travelDate=2024-06-08, travelTime=2013-05-04 14:00:00, accountId=c4f1da0b-b6c6-412c-944c-d324ddb153ca, contactsName=Jason, documentType=2, contactsDocumentNumber=TREJK232, trainNumber=G1236, coachNumber=5, seatClass=3, seatNumber=1554468791, from=nanjing, to=suzhou, status=6, price=140.0),  Order(id=0f6126ee-4ce8-496f-b512-75a0ead24d8a, boughtDate=2024-06-07 22:25:15, travelDate=2024-06-08, travelTime=2013-05-04 07:00:00, accountId=c4f1da0b-b6c6-412c-944c-d324ddb153ca, contactsName=Joseph, documentType=3, contactsDocumentNumber=GFEN321, trainNumber=D1345, coachNumber=5, seatClass=2, seatNumber=185648802, from=shanghai, to=suzhou, status=1, price=50.0)])",
        "2024-06-07 22:29:17.494 INFO   1 --- [http-nio-18885-exec-5] c.s.LoggingAspect: Entering in Method: cancelOrder, Class: cancel.service.CancelServiceImpl, Arguments: [CancelInfo(OrderId=0f6126ee-4ce8-496f-b512-75a0ead24d8a, Id=c4f1da0b-b6c6-412c-944c-d324ddb153ca), authorization: Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJsaWFveWlmYW4iLCJyb2xlcyI6WyJST0xFX1VTRVIiXSwiaWQiOiJjNGYxZGEwYi1iNmM2LTQxMmMtOTQ0Yy1kMzI0ZGRiMTUzY2EiLCJpYXQiOjE3MTc3NzA1NTMsImV4cCI6MTcxNzc3NDE1M30.DtzrMeHTJ-OmivpTM12BEgiCFWSdtYaX8CmKgJfnQGg, Return: Response(status=1, msg=Success., data=test not null)]"
    ]

    checker = GPTChecker(
        api_key=api_key,
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
    # print(result)