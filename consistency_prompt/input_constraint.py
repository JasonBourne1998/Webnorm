from gptchecker import GPTChecker

if __name__ == "__main__":
    class_name1 = "Order"

    class_name2 = "Payment"

    class_definition1 = """
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

    class_definition2 = """
    package com.trainticket.entity;

    import lombok.Data;
    import org.hibernate.annotations.GenericGenerator;

    import javax.persistence.Column;
    import javax.persistence.Entity;
    import javax.persistence.GeneratedValue;
    import javax.persistence.Id;
    import javax.validation.Valid;
    import javax.validation.constraints.NotNull;
    import java.util.UUID;

    /**
    * @author fdse
    */
    @Data
    @Entity
    @GenericGenerator(name = "jpa-uuid", strategy = "org.hibernate.id.UUIDGenerator")
    public class Payment {
        @Id
        @NotNull
        @Column(length = 36)
        @GeneratedValue(generator = "jpa-uuid")
        private String id;

        @NotNull
        @Valid
        @Column(length = 36)
        private String orderId;

        @NotNull
        @Valid
        @Column(length = 36)
        private String userId;

        @NotNull
        @Valid
        @Column(name = "payment_price")
        private String price;

        public Payment(){
            this.id = UUID.randomUUID().toString();
            this.orderId = "";
            this.userId = "";
            this.price = "";
        }

    }
    """

    logs = [
        "2024-05-01 16:31:57.959 INFO   1 --- [http-nio-12032-exec-4] o.s.LoggingAspect: Entering in Method: queryOrdersForRefresh, Class: other.service.OrderOtherServiceImpl, Arguments: [QueryInfo(loginId=4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f, travelDateStart=null, travelDateEnd=null, boughtDateStart=null, boughtDateEnd=null, state=0, enableTravelDateQuery=false, enableBoughtDateQuery=false, enableStateQuery=false), 4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f],  Return: Response(status=1, msg=Success, data=[Order(id=9e3c03c0-81eb-49b9-b2c2-c99ee43c9b47, boughtDate=2024-04-30 19:59:38, travelDate=2022-10-01 00:00:00, travelTime=2022-10-01 00:00:00, accountId=4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f, contactsName=Test, documentType=1, contactsDocumentNumber=Test, trainNumber=K1235, coachNumber=5, seatClass=2, seatNumber=6A, from=shanghai, to=taiyuan, status=6, price=100), Order(id=42bf5718-61e0-4e1d-b3f6-e1e2e1bf284c, boughtDate=2024-05-01 14:19:14, travelDate=2022-10-01 00:00:00, travelTime=2022-10-01 00:00:00, accountId=4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f, contactsName=Test, documentType=1, contactsDocumentNumber=Test, trainNumber=K1235, coachNumber=5, seatClass=2, seatNumber=6A, from=shanghai, to=taiyuan, status=2, price=100), Order(id=0bead1a6-229c-408a-a23d-fdafd2cabde3, boughtDate=2024-05-01 15:43:29, travelDate=2022-10-01 00:00:00, travelTime=2022-10-01 00:00:00, accountId=4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f, contactsName=Test, documentType=1, contactsDocumentNumber=Test, trainNumber=K1235, coachNumber=5, seatClass=2, seatNumber=6A, from=shanghai, to=taiyuan, status=4, price=100), Order(id=d102988d-5f9a-40e2-b589-bf569b8f61b9, boughtDate=2024-05-01 16:17:25, travelDate=2024-05-01, travelTime=2013-05-04 09:51:52, accountId=4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f, contactsName=Contacts_One, documentType=1, contactsDocumentNumber=DocumentNumber_One, trainNumber=Z1234, coachNumber=5, seatClass=2, seatNumber=489979409, from=shanghai, to=shijiazhuang, status=4, price=1000.0), Order(id=7311fd87-420e-4a47-a32b-405568b024c7, boughtDate=2024-05-01 16:19:36, travelDate=2024-05-01, travelTime=2013-05-04 09:51:52, accountId=4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f, contactsName=Contacts_One, documentType=1, contactsDocumentNumber=DocumentNumber_One, trainNumber=Z1234, coachNumber=5, seatClass=3, seatNumber=1640613243, from=shanghai, to=taiyuan, status=4, price=454.99999999999994), Order(id=37a14b99-be92-4da8-a495-1c15bab560a1, boughtDate=2024-05-01 16:19:38, travelDate=2024-05-01, travelTime=2013-05-04 09:51:52, accountId=4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f, contactsName=Contacts_One, documentType=1, contactsDocumentNumber=DocumentNumber_One, trainNumber=Z1234, coachNumber=5, seatClass=3, seatNumber=754483711, from=shanghai, to=taiyuan, status=4, price=454.99999999999994), Order(id=c86d5f19-357f-49fe-9d6f-e5445e8ea890, boughtDate=2024-05-01 16:19:40, travelDate=2024-05-01, travelTime=2013-05-04 09:51:52, accountId=4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f, contactsName=Contacts_Two, documentType=1, contactsDocumentNumber=DocumentNumber_Two, trainNumber=Z1234, coachNumber=5, seatClass=3, seatNumber=1418652845, from=shanghai, to=taiyuan, status=4, price=454.99999999999994), Order(id=a352fe69-885c-47ca-898d-9bbfa136be89, boughtDate=2024-05-01 16:28:21, travelDate=2024-05-01, travelTime=2013-05-04 12:46:52, accountId=4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f, contactsName=Contacts_Two, documentType=1, contactsDocumentNumber=DocumentNumber_Two, trainNumber=Z1234, coachNumber=5, seatClass=2, seatNumber=618144604, from=nanjing, to=taiyuan, status=0, price=950.0), Order(id=21a39b63-5a7d-46c8-97d9-ba21d99a9646, boughtDate=2024-05-01 16:31:07, travelDate=2024-05-01, travelTime=2013-05-04 09:51:52, accountId=4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f, contactsName=Contacts_Two, documentType=1, contactsDocumentNumber=DocumentNumber_Two, trainNumber=Z1234, coachNumber=5, seatClass=2, seatNumber=1491381789, from=shanghai, to=shijiazhuang, status=0, price=1000.0)])",
        "2024-05-01 16:31:58.416 INFO   1 --- [http-nio-19001-exec-1] c.t.s.LoggingAspect: Entering in Method: pay, Class: com.trainticket.service.PaymentServiceImpl, Arguments: [Payment(id=null, orderId=a352fe69-885c-47ca-898d-9bbfa136be89, userId=null, price=950.0)], Return: Response(status=1, msg=Pay Success, data=null)"
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
    code_string = result[1]
    exec(code_string)

    # 现在可以使用 is_related 函数
    instance_A = {'id': 123, 'price': 99.99}
    instance_B = {'orderId': 123, 'price': 99.99}

    print(is_related(instance_A, instance_B)) 