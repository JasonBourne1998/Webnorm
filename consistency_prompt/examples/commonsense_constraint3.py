import sys 
sys.path.append("../")
from gptchecker import GPTChecker
import os
from dotenv import load_dotenv

# 加载 .env 文件
env_path = '../.env'
load_dotenv(dotenv_path=env_path)
api_key = os.getenv('API_KEY')

class_name = "Consign"

class_definition = """
@Data
@AllArgsConstructor
@NoArgsConstructor
@GenericGenerator(name="jpa-uuid",strategy ="uuid")
public class Consign {
    @Id
    @GeneratedValue(generator = "jpa-uuid")
    @Column(length = 36)
    private String id;        
    private String orderId;   
    private String accountId; 

    private String handleDate;
    private String targetDate;
    private String from;
    private String to;
    private String consignee;
    private String phone;
    private double weight;
    private boolean isWithin;


}
"""

logs = [
    "2024-05-02 11:14:15.961 INFO   1 --- [http-nio-16111-exec-9] c.s.LoggingAspect: Entering in Method: updateConsignRecord, Class: consign.service.ConsignServiceImpl, Arguments: [Consign(id=06caff0b-4ad9-47c3-8c3b-3fb3d0e7e9c0, orderId=87064d70-224d-42c8-b234-346e89752b67, accountId=50d545f6-5735-4857-95b9-e09baf562ddc, handleDate=2024-05-02, targetDate=2024-05-02 11:04:11, from=zhenjiang, to=shanghai, consignee=Yifan, phone=22222, weight=123.0, isWithin=false), Return: Response(status=1, msg=Update consign success, data=ConsignRecord(id=06caff0b-4ad9-47c3-8c3b-3fb3d0e7e9c0, orderId=87064d70-224d-42c8-b234-346e89752b67, accountId=50d545f6-5735-4857-95b9-e09baf562ddc, handleDate=2024-05-02, targetDate=2024-05-02 11:04:11, from=zhenjiang, to=shanghai, consignee=Yifan, phone=22222, weight=123.0, price=496.0))",
    "2024-05-02 13:27:35.906 INFO   1 --- [http-nio-16111-exec-5] c.s.LoggingAspect: Entering in Method: updateConsignRecord, Class: consign.service.ConsignServiceImpl, Arguments: [Consign(id=, orderId=dd022f0a-6ed3-48d4-a29c-f8465f286348, accountId=50d545f6-5735-4857-95b9-e09baf562ddc, handleDate=2024-05-02, targetDate=2024-05-02 13:26:16, from=nanjing, to=shanghai, consignee=Yifan, phone=22222, weight=123.0, isWithin=false), Return: Response(status=1, msg=You have consigned successfully! The price is 496.0, data=ConsignRecord(id=5e35fff2-e270-4185-ae60-bae5b74061f5, orderId=dd022f0a-6ed3-48d4-a29c-f8465f286348, accountId=50d545f6-5735-4857-95b9-e09baf562ddc, handleDate=2024-05-02, targetDate=2024-05-02 13:26:16, from=nanjing, to=shanghai, consignee=Yifan, phone=22222, weight=123.0, price=496.0))",
    "2024-05-02 14:15:27.447 INFO   1 --- [http-nio-16111-exec-7] c.s.LoggingAspect: Entering in Method: updateConsignRecord, Class: consign.service.ConsignServiceImpl, Arguments: [Consign(id=, orderId=1d2f3103-a5b4-459a-8057-0c698bce2921, accountId=50d545f6-5735-4857-95b9-e09baf562ddc, handleDate=2024-05-02, targetDate=2024-05-02 14:14:35, from=shanghai, to=suzhou, consignee=Yifan, phone=22222, weight=123.0, isWithin=false),Return: Response(status=1, msg=You have consigned successfully! The price is 496.0, data=ConsignRecord(id=4b6242d0-19ae-4b2c-8d7c-90e266741dc0, orderId=1d2f3103-a5b4-459a-8057-0c698bce2921, accountId=50d545f6-5735-4857-95b9-e09baf562ddc, handleDate=2024-05-02, targetDate=2024-05-02 14:14:35, from=shanghai, to=suzhou, consignee=Yifan, phone=22222, weight=123.0, price=496.0))"
]



checker = GPTChecker(
    api_key=api_key,
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