import sys 
sys.path.append("../")
from gptchecker import GPTChecker
import os
from dotenv import load_dotenv

# 加载 .env 文件
env_path = '../.env'
load_dotenv(dotenv_path=env_path)
api_key = os.getenv('API_KEY')


logs1 = [
    'Entering in Method: checkIfCost, Class: com.nicefish.rbac.service.impl.UserServiceImpl, Arguments: [2], Request Headers: {cookie: JSESSIONID=151ad2f3-d215-4059-a68b-43f3488113b2 , Return: [cost],Entering in Method: checkIfAdmin, Class: com.nicefish.rbac.service.impl.UserServiceImpl, Arguments: [2], Request Headers: {cookie: JSESSIONID=151ad2f3-d215-4059-a68b-aff7988113b2 , Return: [preuium]',
    'Entering in Method: checkIfCost, Class: com.nicefish.rbac.service.impl.UserServiceImpl, Arguments: [10], Request Headers: {cookie: JSESSIONID=151ad2f3-d215-4059-a68b-43f3488113b2 , Return: [free],Entering in Method: checkIfAdmin, Class: com.nicefish.rbac.service.impl.UserServiceImpl, Arguments: [19], Request Headers: {cookie: JSESSIONID=151ad2f3-d215-4059-a68b-23fsfasfa32c , Return: [preuium]',
    'Entering in Method: checkIfCost, Class: com.nicefish.rbac.service.impl.UserServiceImpl, Arguments: [153], Request Headers: {cookie: JSESSIONID=151ad2f3-d215-4059-a68b-43f3488113b2 , Return: [free],Entering in Method: checkIfAdmin, Class: com.nicefish.rbac.service.impl.UserServiceImpl, Arguments: [13], Request Headers: {cookie: JSESSIONID=fahfjsaf-d215-4059-a68b-23fsfasfa32c , Return: [common]',
    'Entering in Method: checkIfCost, Class: com.nicefish.rbac.service.impl.UserServiceImpl, Arguments: [144], Request Headers: {cookie: JSESSIONID=151ad2f3-d215-4059-a68b-43f3488113b2 , Return: [free],Entering in Method: checkIfAdmin, Class: com.nicefish.rbac.service.impl.UserServiceImpl, Arguments: [12], Request Headers: {cookie: JSESSIONID=fsfagdgd-d215-4059-a68b-23fsfasfa32c , Return: [common]',
]

logs2 = [
    'Entering in Method: checkIfCost, Class: com.nicefish.rbac.service.impl.UserServiceImpl, Arguments: [14], Request Headers: {cookie: JSESSIONID=151ad2f3-d215-4059-a68b-43f3488113b2 , Return: [cost], Entering in Method: checkIfAdmin, Class: com.nicefish.rbac.service.impl.UserServiceImpl, Arguments: [14], Request Headers: {cookie: JSESSIONID=151ad2f3-d215-4059-a68b-43f3488113b2 , Return: [common]',
    'Entering in Method: checkIfCost, Class: com.nicefish.rbac.service.impl.UserServiceImpl, Arguments: [12], Request Headers: {cookie: JSESSIONID=151ad2f3-d215-4059-a68b-43f3488113b2 , Return: [cost],Entering in Method: checkIfAdmin, Class: com.nicefish.rbac.service.impl.UserServiceImpl, Arguments: [15], Request Headers: {cookie: JSESSIONID=151ad2f3-d215-4059-a68b-dfsafsf323sf , Return: [common]',
    'Entering in Method: checkIfCost, Class: com.nicefish.rbac.service.impl.UserServiceImpl, Arguments: [11], Request Headers: {cookie: JSESSIONID=151ad2f3-d215-4059-a68b-43f3488113b2 , Return: [cost],Entering in Method: checkIfAdmin, Class: com.nicefish.rbac.service.impl.UserServiceImpl, Arguments: [132], Request Headers: {cookie: JSESSIONID=151ad2f3-d215-4059-a68b-dfsafsf323sf , Return: [common]',
    'Entering in Method: checkIfCost, Class: com.nicefish.rbac.service.impl.UserServiceImpl, Arguments: [1], Request Headers: {cookie: JSESSIONID=151ad2f3-d215-4059-a68b-43f3488113b2 , Return: [cost], Entering in Method: checkIfAdmin, Class: com.nicefish.rbac.service.impl.UserServiceImpl, Arguments: [18], Request Headers: {cookie: JSESSIONID=gdsgsggd-d215-4059-a68b-dfsafsf323sf , Return: [common]',
]

parent_url= "/auth/user/checkifpreuium"

child_url1 = "/cms/file/download/<itemId>"

child_url2 = "/cms/post/post-list/<page>/<rows>"

checker = GPTChecker(
    api_key="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",
    model="gpt-4o",
    max_tokens=2048,
    top_p=0.9,
    temperature=0.0
)

result = checker.check_flow_constraint(
    parent_url,
    child_url1,
    child_url2,
    logs1,
    logs2
)