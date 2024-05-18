from gptchecker import GPTChecker

class_name = "Order"

class_definition = """
package other.entity;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import edu.fudan.common.entity.OrderStatus;
import edu.fudan.common.entity.SeatClass;
import edu.fudan.common.util.StringUtils;
import lombok.Data;
import lombok.ToString;
import org.hibernate.annotations.GenericGenerator;

import javax.persistence.*;
import java.util.Date;

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

logs = [
    "2024-05-01 16:22:22.003 INFO   1 --- [http-nio-12031-exec-9] o.s.LoggingAspect: Entering in Method: queryOrdersForRefresh, Class: order.service.OrderServiceImpl, Arguments: [OrderInfo(loginId=50d545f6-5735-4857-95b9-e09baf562ddc, travelDateStart=null, travelDateEnd=null, boughtDateStart=null, boughtDateEnd=null, state=0, enableTravelDateQuery=false, enableBoughtDateQuery=false, enableStateQuery=false), 50d545f6-5735-4857-95b9-e09baf562ddc], Return: Response(status=1, msg=Query Orders For Refresh Success, data=[Order(id=3fc21c15-72a6-4dd5-808e-1a9a42db5f60, boughtDate=2024-05-01 16:16:15, travelDate=2024-05-01, travelTime=2013-05-04 07:00:00, accountId=50d545f6-5735-4857-95b9-e09baf562ddc, contactsName=Jason, documentType=2, contactsDocumentNumber=EH9202323, trainNumber=D1345, coachNumber=5, seatClass=2, seatNumber=1623500807, from=shanghai, to=suzhou, status=1, price=50.0), Order(id=5ee8873c-f99e-4d97-b603-1b87873e3d34, boughtDate=2024-05-01 16:17:54, travelDate=2024-05-01, travelTime=2013-05-04 09:00:00, accountId=50d545f6-5735-4857-95b9-e09baf562ddc, contactsName=Jason, documentType=2, contactsDocumentNumber=EH9202323, trainNumber=G1234, coachNumber=5, seatClass=2, seatNumber=539659046, from=nanjing, to=suzhou, status=1, price=200.0)])",
    "2024-05-01 16:22:20.995 INFO   1 --- [http-nio-19001-exec-1] c.t.s.LoggingAspect: Entering in Method: pay, Class: com.trainticket.service.PaymentServiceImpl, Arguments: [Payment(id=null, orderId=582eb81a-7431-4538-82b7-8fdfd923857b, userId=null, price=70.0)], Return: Response(status=1, msg=Pay Success, data=null)",
    "2024-05-01 16:31:57.959 INFO   1 --- [http-nio-12032-exec-4] o.s.LoggingAspect: Entering in Method: queryOrdersForRefresh, Class: other.service.OrderOtherServiceImpl, Arguments: [QueryInfo(loginId=4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f, travelDateStart=null, travelDateEnd=null, boughtDateStart=null, boughtDateEnd=null, state=0, enableTravelDateQuery=false, enableBoughtDateQuery=false, enableStateQuery=false), 4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f],  Return: Response(status=1, msg=Success, data=[Order(id=9e3c03c0-81eb-49b9-b2c2-c99ee43c9b47, boughtDate=2024-04-30 19:59:38, travelDate=2022-10-01 00:00:00, travelTime=2022-10-01 00:00:00, accountId=4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f, contactsName=Test, documentType=1, contactsDocumentNumber=Test, trainNumber=K1235, coachNumber=5, seatClass=2, seatNumber=6A, from=shanghai, to=taiyuan, status=6, price=100), Order(id=42bf5718-61e0-4e1d-b3f6-e1e2e1bf284c, boughtDate=2024-05-01 14:19:14, travelDate=2022-10-01 00:00:00, travelTime=2022-10-01 00:00:00, accountId=4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f, contactsName=Test, documentType=1, contactsDocumentNumber=Test, trainNumber=K1235, coachNumber=5, seatClass=2, seatNumber=6A, from=shanghai, to=taiyuan, status=2, price=100), Order(id=0bead1a6-229c-408a-a23d-fdafd2cabde3, boughtDate=2024-05-01 15:43:29, travelDate=2022-10-01 00:00:00, travelTime=2022-10-01 00:00:00, accountId=4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f, contactsName=Test, documentType=1, contactsDocumentNumber=Test, trainNumber=K1235, coachNumber=5, seatClass=2, seatNumber=6A, from=shanghai, to=taiyuan, status=4, price=100), Order(id=d102988d-5f9a-40e2-b589-bf569b8f61b9, boughtDate=2024-05-01 16:17:25, travelDate=2024-05-01, travelTime=2013-05-04 09:51:52, accountId=4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f, contactsName=Contacts_One, documentType=1, contactsDocumentNumber=DocumentNumber_One, trainNumber=Z1234, coachNumber=5, seatClass=2, seatNumber=489979409, from=shanghai, to=shijiazhuang, status=4, price=1000.0), Order(id=7311fd87-420e-4a47-a32b-405568b024c7, boughtDate=2024-05-01 16:19:36, travelDate=2024-05-01, travelTime=2013-05-04 09:51:52, accountId=4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f, contactsName=Contacts_One, documentType=1, contactsDocumentNumber=DocumentNumber_One, trainNumber=Z1234, coachNumber=5, seatClass=3, seatNumber=1640613243, from=shanghai, to=taiyuan, status=4, price=454.99999999999994), Order(id=37a14b99-be92-4da8-a495-1c15bab560a1, boughtDate=2024-05-01 16:19:38, travelDate=2024-05-01, travelTime=2013-05-04 09:51:52, accountId=4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f, contactsName=Contacts_One, documentType=1, contactsDocumentNumber=DocumentNumber_One, trainNumber=Z1234, coachNumber=5, seatClass=3, seatNumber=754483711, from=shanghai, to=taiyuan, status=4, price=454.99999999999994), Order(id=c86d5f19-357f-49fe-9d6f-e5445e8ea890, boughtDate=2024-05-01 16:19:40, travelDate=2024-05-01, travelTime=2013-05-04 09:51:52, accountId=4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f, contactsName=Contacts_Two, documentType=1, contactsDocumentNumber=DocumentNumber_Two, trainNumber=Z1234, coachNumber=5, seatClass=3, seatNumber=1418652845, from=shanghai, to=taiyuan, status=4, price=454.99999999999994), Order(id=a352fe69-885c-47ca-898d-9bbfa136be89, boughtDate=2024-05-01 16:28:21, travelDate=2024-05-01, travelTime=2013-05-04 12:46:52, accountId=4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f, contactsName=Contacts_Two, documentType=1, contactsDocumentNumber=DocumentNumber_Two, trainNumber=Z1234, coachNumber=5, seatClass=2, seatNumber=618144604, from=nanjing, to=taiyuan, status=0, price=950.0), Order(id=21a39b63-5a7d-46c8-97d9-ba21d99a9646, boughtDate=2024-05-01 16:31:07, travelDate=2024-05-01, travelTime=2013-05-04 09:51:52, accountId=4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f, contactsName=Contacts_Two, documentType=1, contactsDocumentNumber=DocumentNumber_Two, trainNumber=Z1234, coachNumber=5, seatClass=2, seatNumber=1491381789, from=shanghai, to=shijiazhuang, status=0, price=1000.0)])",
    "2024-05-01 16:31:58.416 INFO   1 --- [http-nio-19001-exec-1] c.t.s.LoggingAspect: Entering in Method: pay, Class: com.trainticket.service.PaymentServiceImpl, Arguments: [Payment(id=null, orderId=a352fe69-885c-47ca-898d-9bbfa136be89, userId=null, price=950.0)], Return: Response(status=1, msg=Pay Success, data=null)",
    "2024-05-01 16:38:21.357 INFO   1 --- [http-nio-12032-exec-2] o.s.LoggingAspect: Entering in Method: queryOrdersForRefresh, Class: other.service.OrderOtherServiceImpl, Arguments: [QueryInfo(loginId=50d545f6-5735-4857-95b9-e09baf562ddc, travelDateStart=null, travelDateEnd=null, boughtDateStart=null, boughtDateEnd=null, state=0, enableTravelDateQuery=false, enableBoughtDateQuery=false, enableStateQuery=false), 50d545f6-5735-4857-95b9-e09baf562ddc],  Return: Response(status=1, msg=Success, data=[Order(id=582eb81a-7431-4538-82b7-8fdfd923857b, boughtDate=2024-05-01 16:22:00, travelDate=2024-05-01, travelTime=2013-05-04 15:41:52, accountId=50d545f6-5735-4857-95b9-e09baf562ddc, contactsName=Jason, documentType=2, contactsDocumentNumber=EH9202323, trainNumber=Z1235, coachNumber=5, seatClass=3, seatNumber=1166717090, from=xuzhou, to=jinan, status=1, price=70.0)])",
    "2024-05-01 16:38:21.629 INFO   1 --- [http-nio-19001-exec-1] c.t.s.LoggingAspect: Entering in Method: pay, Class: com.trainticket.service.PaymentServiceImpl, Arguments: [Payment(id=null, orderId=6e7c6eca-0e07-43d6-b599-794ba2dac8ff, userId=null, price=100.0)], Return: Response(status=1, msg=Pay Success, data=null)",
    "2024-05-01 19:05:55.406 INFO   1 --- [http-nio-12032-exec-3] o.s.LoggingAspect: Entering in Method: queryOrdersForRefresh, Class: other.service.OrderOtherServiceImpl, Arguments: [QueryInfo(loginId=4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f, travelDateStart=null, travelDateEnd=null, boughtDateStart=null, boughtDateEnd=null, state=0, enableTravelDateQuery=false, enableBoughtDateQuery=false, enableStateQuery=false), 4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f], Return: Response(status=1, msg=Success, data=[Order(id=9e3c03c0-81eb-49b9-b2c2-c99ee43c9b47, boughtDate=2024-04-30 19:59:38, travelDate=2022-10-01 00:00:00, travelTime=2022-10-01 00:00:00, accountId=4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f, contactsName=Test, documentType=1, contactsDocumentNumber=Test, trainNumber=K1235, coachNumber=5, seatClass=2, seatNumber=6A, from=shanghai, to=taiyuan, status=6, price=100), Order(id=42bf5718-61e0-4e1d-b3f6-e1e2e1bf284c, boughtDate=2024-05-01 14:19:14, travelDate=2022-10-01 00:00:00, travelTime=2022-10-01 00:00:00, accountId=4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f, contactsName=Test, documentType=1, contactsDocumentNumber=Test, trainNumber=K1235, coachNumber=5, seatClass=2, seatNumber=6A, from=shanghai, to=taiyuan, status=6, price=100), Order(id=0bead1a6-229c-408a-a23d-fdafd2cabde3, boughtDate=2024-05-01 15:43:29, travelDate=2022-10-01 00:00:00, travelTime=2022-10-01 00:00:00, accountId=4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f, contactsName=Test, documentType=1, contactsDocumentNumber=Test, trainNumber=K1235, coachNumber=5, seatClass=2, seatNumber=6A, from=shanghai, to=taiyuan, status=4, price=100), Order(id=d102988d-5f9a-40e2-b589-bf569b8f61b9, boughtDate=2024-05-01 16:17:25, travelDate=2024-05-01, travelTime=2013-05-04 09:51:52, accountId=4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f, contactsName=Contacts_One, documentType=1, contactsDocumentNumber=DocumentNumber_One, trainNumber=Z1234, coachNumber=5, seatClass=2, seatNumber=489979409, from=shanghai, to=shijiazhuang, status=4, price=1000.0), Order(id=7311fd87-420e-4a47-a32b-405568b024c7, boughtDate=2024-05-01 16:19:36, travelDate=2024-05-01, travelTime=2013-05-04 09:51:52, accountId=4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f, contactsName=Contacts_One, documentType=1, contactsDocumentNumber=DocumentNumber_One, trainNumber=Z1234, coachNumber=5, seatClass=3, seatNumber=1640613243, from=shanghai, to=taiyuan, status=4, price=454.99999999999994), Order(id=37a14b99-be92-4da8-a495-1c15bab560a1, boughtDate=2024-05-01 16:19:38, travelDate=2024-05-01, travelTime=2013-05-04 09:51:52, accountId=4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f, contactsName=Contacts_One, documentType=1, contactsDocumentNumber=DocumentNumber_One, trainNumber=Z1234, coachNumber=5, seatClass=3, seatNumber=754483711, from=shanghai, to=taiyuan, status=4, price=454.99999999999994), Order(id=c86d5f19-357f-49fe-9d6f-e5445e8ea890, boughtDate=2024-05-01 16:19:40, travelDate=2024-05-01, travelTime=2013-05-04 09:51:52, accountId=4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f, contactsName=Contacts_Two, documentType=1, contactsDocumentNumber=DocumentNumber_Two, trainNumber=Z1234, coachNumber=5, seatClass=3, seatNumber=1418652845, from=shanghai, to=taiyuan, status=4, price=454.99999999999994), Order(id=a352fe69-885c-47ca-898d-9bbfa136be89, boughtDate=2024-05-01 16:28:21, travelDate=2024-05-01, travelTime=2013-05-04 12:46:52, accountId=4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f, contactsName=Contacts_Two, documentType=1, contactsDocumentNumber=DocumentNumber_Two, trainNumber=Z1234, coachNumber=5, seatClass=2, seatNumber=618144604, from=nanjing, to=taiyuan, status=4, price=950.0), Order(id=21a39b63-5a7d-46c8-97d9-ba21d99a9646, boughtDate=2024-05-01 16:31:07, travelDate=2024-05-01, travelTime=2013-05-04 09:51:52, accountId=4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f, contactsName=Contacts_Two, documentType=1, contactsDocumentNumber=DocumentNumber_Two, trainNumber=Z1234, coachNumber=5, seatClass=2, seatNumber=1491381789, from=shanghai, to=shijiazhuang, status=4, price=1000.0), Order(id=8e414ded-bebd-4683-a061-173b63bae4ec, boughtDate=2024-05-01 17:02:46, travelDate=2022-10-01 00:00:00, travelTime=2022-10-01 00:00:00, accountId=4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f, contactsName=Test, documentType=1, contactsDocumentNumber=Test, trainNumber=K1235, coachNumber=5, seatClass=2, seatNumber=6A, from=shanghai, to=taiyuan, status=1, price=100)])",
    "2024-05-01 19:05:55.701 INFO   1 --- [http-nio-19001-exec-1] c.t.s.LoggingAspect: Entering in Method: pay, Class: com.trainticket.service.PaymentServiceImpl, Arguments: [Payment(id=null, orderId=4b42712c-0317-4eaa-b23c-d5fc410430cf, userId=null, price=19.0)], Return: Response(status=1, msg=Pay Success, data=null)",
    "2024-05-14 17:33:30.356 INFO   1 --- [http-nio-12032-exec-7] o.s.LoggingAspect: Entering in Method: queryOrdersForRefresh, Class: other.service.OrderOtherServiceImpl, Arguments: [QueryInfo(loginId=4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f, travelDateStart=null, travelDateEnd=null, boughtDateStart=null, boughtDateEnd=null, state=0, enableTravelDateQuery=false, enableBoughtDateQuery=false, enableStateQuery=false), 4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f], Return: Response(status=1, msg=Success, data=[Order(id=9e3c03c0-81eb-49b9-b2c2-c99ee43c9b47, boughtDate=2024-04-30 19:59:38, travelDate=2022-10-01 00:00:00, travelTime=2022-10-01 00:00:00, accountId=4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f, contactsName=Test, documentType=1, contactsDocumentNumber=Test, trainNumber=K1235, coachNumber=5, seatClass=2, seatNumber=6A, from=shanghai, to=taiyuan, status=6, price=100), Order(id=42bf5718-61e0-4e1d-b3f6-e1e2e1bf284c, boughtDate=2024-05-01 14:19:14, travelDate=2022-10-01 00:00:00, travelTime=2022-10-01 00:00:00, accountId=4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f, contactsName=Test, documentType=1, contactsDocumentNumber=Test, trainNumber=K1235, coachNumber=5, seatClass=2, seatNumber=6A, from=shanghai, to=taiyuan, status=6, price=100), Order(id=0bead1a6-229c-408a-a23d-fdafd2cabde3, boughtDate=2024-05-01 15:43:29, travelDate=2022-10-01 00:00:00, travelTime=2022-10-01 00:00:00, accountId=4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f, contactsName=Test, documentType=1, contactsDocumentNumber=Test, trainNumber=K1235, coachNumber=5, seatClass=2, seatNumber=6A, from=shanghai, to=taiyuan, status=4, price=100), Order(id=d102988d-5f9a-40e2-b589-bf569b8f61b9, boughtDate=2024-05-01 16:17:25, travelDate=2024-05-01, travelTime=2013-05-04 09:51:52, accountId=4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f, contactsName=Contacts_One, documentType=1, contactsDocumentNumber=DocumentNumber_One, trainNumber=Z1234, coachNumber=5, seatClass=2, seatNumber=489979409, from=shanghai, to=shijiazhuang, status=4, price=1000.0), Order(id=7311fd87-420e-4a47-a32b-405568b024c7, boughtDate=2024-05-01 16:19:36, travelDate=2024-05-01, travelTime=2013-05-04 09:51:52, accountId=4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f, contactsName=Contacts_One, documentType=1, contactsDocumentNumber=DocumentNumber_One, trainNumber=Z1234, coachNumber=5, seatClass=3, seatNumber=1640613243, from=shanghai, to=taiyuan, status=4, price=454.99999999999994), Order(id=37a14b99-be92-4da8-a495-1c15bab560a1, boughtDate=2024-05-01 16:19:38, travelDate=2024-05-01, travelTime=2013-05-04 09:51:52, accountId=4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f, contactsName=Contacts_One, documentType=1, contactsDocumentNumber=DocumentNumber_One, trainNumber=Z1234, coachNumber=5, seatClass=3, seatNumber=754483711, from=shanghai, to=taiyuan, status=4, price=454.99999999999994), Order(id=c86d5f19-357f-49fe-9d6f-e5445e8ea890, boughtDate=2024-05-01 16:19:40, travelDate=2024-05-01, travelTime=2013-05-04 09:51:52, accountId=4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f, contactsName=Contacts_Two, documentType=1, contactsDocumentNumber=DocumentNumber_Two, trainNumber=Z1234, coachNumber=5, seatClass=3, seatNumber=1418652845, from=shanghai, to=taiyuan, status=4, price=454.99999999999994), Order(id=a352fe69-885c-47ca-898d-9bbfa136be89, boughtDate=2024-05-01 16:28:21, travelDate=2024-05-01, travelTime=2013-05-04 12:46:52, accountId=4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f, contactsName=Contacts_Two, documentType=1, contactsDocumentNumber=DocumentNumber_Two, trainNumber=Z1234, coachNumber=5, seatClass=2, seatNumber=618144604, from=nanjing, to=taiyuan, status=4, price=950.0), Order(id=21a39b63-5a7d-46c8-97d9-ba21d99a9646, boughtDate=2024-05-01 16:31:07, travelDate=2024-05-01, travelTime=2013-05-04 09:51:52, accountId=4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f, contactsName=Contacts_Two, documentType=1, contactsDocumentNumber=DocumentNumber_Two, trainNumber=Z1234, coachNumber=5, seatClass=2, seatNumber=1491381789, from=shanghai, to=shijiazhuang, status=4, price=1000.0), Order(id=8e414ded-bebd-4683-a061-173b63bae4ec, boughtDate=2024-05-01 17:02:46, travelDate=2022-10-01 00:00:00, travelTime=2022-10-01 00:00:00, accountId=4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f, contactsName=Test, documentType=1, contactsDocumentNumber=Test, trainNumber=K1235, coachNumber=5, seatClass=2, seatNumber=6A, from=shanghai, to=taiyuan, status=4, price=100), Order(id=1c1b4a81-e14f-4c15-88d5-66b1b357f4a9, boughtDate=2024-05-05 21:28:33, travelDate=2022-10-01 00:00:00, travelTime=2022-10-01 00:00:00, accountId=4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f, contactsName=Test, documentType=1, contactsDocumentNumber=Test, trainNumber=K1235, coachNumber=5, seatClass=2, seatNumber=6A, from=shanghai, to=taiyuan, status=4, price=100)])",
    "2024-05-14 17:33:31.002 INFO   1 --- [http-nio-18673-exec-5] i.s.LoggingAspect: Entering in Method: pay, Class: inside_payment.service.InsidePaymentServiceImpl, Arguments: [PaymentInfo(userId=null, orderId=3c75d5bb-19e7-4c02-9c65-6785fe64564f, tripId=G1234, price=57.0)], Return: Response(status=1, msg=Payment Success Pay Success, data=null)"
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