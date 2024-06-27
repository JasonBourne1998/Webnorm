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
        "2024-05-01 18:31:10.293 INFO   1 --- [http-nio-12031-exec-2] o.s.LoggingAspect: Entering in Method: queryOrdersForRefresh, Class: order.service.OrderServiceImpl, Arguments: [OrderInfo(loginId=50d545f6-5735-4857-95b9-e09baf562ddc, travelDateStart=null, travelDateEnd=null, boughtDateStart=null, boughtDateEnd=null, state=0, enableTravelDateQuery=false, enableBoughtDateQuery=false, enableStateQuery=false), 50d545f6-5735-4857-95b9-e09baf562ddc,  authorization:\"Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJsaWFveWlmYW4iLCJyb2xlcyI6WyJST0xFX1VTRVIiXSwiaWQiOiI1MGQ1NDVmNi01NzM1LTQ4NTctOTViOS1lMDliYWY1NjJkZGMiLCJpYXQiOjE3MTQ1NTk0NTQsImV4cCI6MTcxNDU2MzA1NH0.zeYFLwPudVdxG3SvVNRUi01oLk3s0yDag0RGmhoDUK8\",  Return: Response(status=1, msg=Query Orders For Refresh Success, data=[Order(id=3fc21c15-72a6-4dd5-808e-1a9a42db5f60, boughtDate=2024-05-01 16:16:15, travelDate=2024-05-01, travelTime=2013-05-04 07:00:00, accountId=50d545f6-5735-4857-95b9-e09baf562ddc, contactsName=Jason, documentType=2, contactsDocumentNumber=EH9202323, trainNumber=D1345, coachNumber=5, seatClass=2, seatNumber=1623500807, from=shanghai, to=suzhou, status=6, price=50.0), Order(id=5ee8873c-f99e-4d97-b603-1b87873e3d34, boughtDate=2024-05-01 16:17:54, travelDate=2024-05-01, travelTime=2013-05-04 09:00:00, accountId=50d545f6-5735-4857-95b9-e09baf562ddc, contactsName=Jason, documentType=2, contactsDocumentNumber=EH9202323, trainNumber=G1234, coachNumber=5, seatClass=2, seatNumber=539659046, from=nanjing, to=suzhou, status=4, price=200.0), Order(id=6e7c6eca-0e07-43d6-b599-794ba2dac8ff, boughtDate=2024-05-01 16:36:51, travelDate=2024-05-01, travelTime=2013-05-04 09:24:00, accountId=50d545f6-5735-4857-95b9-e09baf562ddc, contactsName=Jason, documentType=2, contactsDocumentNumber=EH9202323, trainNumber=G1234, coachNumber=5, seatClass=2, seatNumber=712051873, from=zhenjiang, to=suzhou, status=4, price=100.0)])",
        "2024-05-24 15:33:16.500 INFO   1 --- [http-nio-18885-exec-5] c.s.LoggingAspect: Entering in Method: cancelOrder, Class: cancel.service.CancelServiceImpl, Arguments: [CancelInfo(OrderId= 6e7c6eca-0e07-43d6-b599-794ba2dac8ff, Id=50d545f6-5735-4857-95b9-e09baf562ddc), authorization:\"Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJsaWFveWlmYW4iLCJyb2xlcyI6WyJST0xFX1VTRVIiXSwiaWQiOiI1MGQ1NDVmNi01NzM1LTQ4NTctOTViOS1lMDliYWY1NjJkZGMiLCJpYXQiOjE3MTQ1NTk0NTQsImV4cCI6MTcxNDU2MzA1NH0.zeYFLwPudVdxG3SvVNRUi01oLk3s0yDag0RGmhoDUK8\"], Return: Response(status=1, msg=Success., data=test not null)]"
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