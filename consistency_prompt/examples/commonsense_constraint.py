import sys 
sys.path.append("../")
from gptchecker import GPTChecker
import os
from dotenv import load_dotenv

# 加载 .env 文件
env_path = '../.env'
load_dotenv(dotenv_path=env_path)
api_key = os.getenv('API_KEY')

class_name = "Contacts"

class_definition = """
public class Contacts {

    @Id
//    private UUID id;
    @GeneratedValue(generator = "jpa-uuid")
    @Column(length = 36)
    private String id;
    @Column(name = "account_id")
    private String accountId;

    private String name;
    @Column(name = "document_type")
    private int documentType;
    @Column(name = "document_number")
    private String documentNumber;
    @Column(name = "phone_number")
    private String phoneNumber;

    public Contacts() {
        //Default Constructor
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
        Contacts other = (Contacts) obj;
        return name.equals(other.getName())
                && accountId .equals( other.getAccountId() )
                && documentNumber.equals(other.getDocumentNumber())
                && phoneNumber.equals(other.getPhoneNumber())
                && documentType == other.getDocumentType();
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
    "2024-06-04 13:59:53.864 INFO   1 --- [http-nio-12347-exec-8] c.s.LoggingAspect: Entering in Method: create, Class: contacts.service.ContactsServiceImpl, Arguments: [Contacts(id=null, accountId=c4f1da0b-b6c6-412c-944c-d324ddb153ca, name=Joseph, documentType=3, documentNumber=GFEN321, phoneNumber=132424352)",
    "2024-06-04 14:23:48.720 INFO   1 --- [http-nio-12347-exec-3] c.s.LoggingAspect: Entering in Method: create, Class: contacts.service.ContactsServiceImpl, Arguments: [Contacts(id=null, accountId=855a23a0-6331-4f87-8c2b-a7e641dab48e, name=Mason, documentType=2, documentNumber=EH2984321, phoneNumber=1123425345)"
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