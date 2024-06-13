import networkx as nx

G = nx.DiGraph()

G.add_node('POST /api/v1/travel2service/trips/left', description='Search Other Tickets')
G.add_node('POST /api/v1/travelservice/trips/left', description='Search Tickets')
G.add_node('GET /api/v1/verifycode/generate', description='GET verifycode')
G.add_node('POST /api/v1/users/login', description='Login')
G.add_node('POST /api/v1/orderOtherService/orderOther/refresh', description='Check Order')
G.add_node('POST /api/v1/orderservice/order/refresh', description='Check Other Order')
G.add_node('POST /api/v1/travelplanservice/travelPlan/cheapest', description='Search Cheapest Tickets')
G.add_node('POST /api/v1/travelplanservice/travelPlan/quickest', description='Search Quickest Tickets')
G.add_node('POST /api/v1/travelplanservice/travelPlan/minStation', description='Search MinStation Tickets')
G.add_node('GET /api/v1/assuranceservice/assurances/types', description='GET Assurances')
G.add_node('GET /api/v1/contactservice/contacts/account/', description='GET Contacts')
G.add_node('GET /api/v1/foodservice/foods', description='GET Foods')
G.add_node('POST /api/v1/preserveservice/preserve', description='Preserve Tickets')
G.add_node('POST /api/v1/preserveotherservice/preserveOther', description='Preserve Other Tickets')
G.add_node('POST /api/v1/rebookservice/rebook', description='Rebook')
G.add_node('GET /api/v1/cancelservice/cancel/', description='Cancel Ticket')
G.add_node('GET /api/v1/cancelservice/cancel/refound/', description='Get Refound')
G.add_node('PUT /api/v1/consignservice/consigns', description='Consign')
G.add_node('GET /api/v1/executeservice/execute/collected', description='Consign')
G.add_node('POST /api/v1/rebookservice/updateorder', description='Update Order')
G.add_node('POST /api/v1/inside_pay_service/inside_payment', description='Pay Ticket')
G.add_node('POST /api/v1/rebookservice/rebook/difference', description='Pay Difference')
G.add_node('GET /api/v1/userservice/users', description='GET Admin User')

G.add_edge('POST /api/v1/travel2service/trips/left', 'API2', database = "", condition='Condition1', dataflow='DataFlow1')
G.add_edge('API2', 'API3', condition='Condition2', dataflow='DataFlow2')
G.add_edge('API1', 'API3', condition='Condition3', dataflow='DataFlow3')

print("Nodes of the graph:", G.nodes(data=True))
print("Edges of the graph:", G.edges(data=True))

def find_related_apis(api_name, graph):
    if api_name not in graph:
        print(f"API {api_name} not found in the graph.")
        return

    related_apis = list(graph.successors(api_name))
    related_info = []
    for related_api in related_apis:
        edge_data = graph.get_edge_data(api_name, related_api)
        related_info.append((related_api, edge_data))
    
    return related_info

def analyze_logs(logs, graph):
    for log in logs:
        api_name = log['api']
        timestamp = log['timestamp']
        print(f"\nTimestamp: {timestamp}, API: {api_name}")
        related_apis = find_related_apis(api_name, graph)
        if related_apis:
            print(f"Related APIs to {api_name}:")
            for related_api, info in related_apis:
                print(f"  {related_api}: {info}")
        else:
            print(f"No related APIs found for {api_name}.")

if __name__ == "__main__":
    analyze_logs(logs, G)
     
#DataFlow $20-13.68
['travel2.service.TravelServiceImpl.queryByBatch > preserveOther.service.PreserveOtherServiceImpl.preserve', 'order.service.OrderServiceImpl.queryOrdersForRefresh > cancel.service.CancelServiceImpl.calculateRefund', 'inside_payment.service.InsidePaymentServiceImpl.pay > other.service.OrderOtherServiceImpl.queryOrdersForRefresh', 'verifycode.service.impl.VerifyCodeServiceImpl.getImageCode > auth.service.impl.TokenServiceImpl.getToken', 'auth.service.impl.TokenServiceImpl.getToken > contacts.service.ContactsServiceImpl.findContactsByAccountId', 'auth.service.impl.TokenServiceImpl.getToken > foodsearch.service.FoodServiceImpl.getAllFood', 'auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > user.service.impl.UserServiceImpl.getAllUsers', 'order.service.OrderServiceImpl.queryOrdersForRefresh > inside_payment.service.InsidePaymentServiceImpl.pay', 'auth.service.impl.TokenServiceImpl.getToken > other.service.OrderOtherServiceImpl.queryOrdersForRefresh', 'other.service.OrderOtherServiceImpl.queryOrdersForRefresh > consign.service.ConsignServiceImpl.updateConsignRecord', 'contacts.service.ContactsServiceImpl.findContactsByAccountId > preserveOther.service.PreserveOtherServiceImpl.preserve', 'auth.service.impl.TokenServiceImpl.getToken > travel2.service.TravelServiceImpl.queryByBatch', 'travel.service.TravelServiceImpl.queryByBatch > preserveOther.service.PreserveOtherServiceImpl.preserve', 'other.service.OrderOtherServiceImpl.queryOrdersForRefresh > cancel.service.CancelServiceImpl.calculateRefund', 'order.service.OrderServiceImpl.queryOrdersForRefresh > consign.service.ConsignServiceImpl.queryByOrderId', 'auth.service.impl.TokenServiceImpl.getToken > consign.service.ConsignServiceImpl.queryByAccountId', 'auth.service.impl.TokenServiceImpl.getToken > travel.service.TravelServiceImpl.queryByBatch', 'auth.service.impl.TokenServiceImpl.getToken > execute.service.ExecuteServiceImpl.ticketExecute', 'auth.service.impl.TokenServiceImpl.getToken > assurance.service.AssuranceServiceImpl.getAllAssuranceTypes', 'auth.service.impl.TokenServiceImpl.getToken > preserveOther.service.PreserveOtherServiceImpl.preserve', 'auth.service.impl.TokenServiceImpl.getToken > execute.service.ExecuteServiceImpl.ticketCollect', 'auth.service.impl.TokenServiceImpl.getToken > rebook.service.RebookServiceImpl.rebook', 'other.service.OrderOtherServiceImpl.queryOrdersForRefresh > consign.service.ConsignServiceImpl.queryByOrderId', 'order.service.OrderServiceImpl.queryOrdersForRefresh > consign.service.ConsignServiceImpl.updateConsignRecord', 'inside_payment.service.InsidePaymentServiceImpl.pay > order.service.OrderServiceImpl.queryOrdersForRefresh', 'other.service.OrderOtherServiceImpl.queryOrdersForRefresh > inside_payment.service.InsidePaymentServiceImpl.pay','contacts.service.ContactsServiceImpl.findContactsByAccountId > preserve.service.PreserveServiceImpl.preserve', 'foodsearch.service.FoodServiceImpl.getAllFood > preserve.service.PreserveServiceImpl.preserve','travel2.service.TravelServiceImpl.queryByBatch > preserve.service.PreserveServiceImpl.preserve','auth.service.impl.TokenServiceImpl.getToken > preserve.service.PreserveServiceImpl.preserve','travel.service.TravelServiceImpl.queryByBatch > preserve.service.PreserveServiceImpl.preserve']

#DataFlow:
#login_seeds: [] 52s
# cancel_seeds: ['verifycode.service.impl.VerifyCodeServiceImpl.getImageCode > auth.service.impl.TokenServiceImpl.getToken', 'auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > other.service.OrderOtherServiceImpl.queryOrdersForRefresh', 'order.service.OrderServiceImpl.queryOrdersForRefresh > cancel.service.CancelServiceImpl.calculateRefund', 'other.service.OrderOtherServiceImpl.queryOrdersForRefresh > cancel.service.CancelServiceImpl.calculateRefund'] 9.6909s
#['auth.service.impl.TokenServiceImpl.getToken > other.service.OrderOtherServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh'] 19.0419 seconds
# Change ['auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > other.service.OrderOtherServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > travel.service.TravelServiceImpl.queryByBatch', 'auth.service.impl.TokenServiceImpl.getToken > travel2.service.TravelServiceImpl.queryByBatch', 'auth.service.impl.TokenServiceImpl.getToken > rebook.service.RebookServiceImpl.rebook'] 20.95
#getConsign['auth.service.impl.TokenServiceImpl.getToken > consign.service.ConsignServiceImpl.queryByAccountId'] 11.62
#getCollect['verifycode.service.impl.VerifyCodeServiceImpl.getImageCode > auth.service.impl.TokenServiceImpl.getToken', 'auth.service.impl.TokenServiceImpl.getToken > other.service.OrderOtherServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh'] 13.8993
#Enter['auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > other.service.OrderOtherServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > execute.service.ExecuteServiceImpl.ticketExecute', 'auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > other.service.OrderOtherServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > execute.service.ExecuteServiceImpl.ticketExecute'] 15.6334
#getEnter['verifycode.service.impl.VerifyCodeServiceImpl.getImageCode > auth.service.impl.TokenServiceImpl.getToken', 'auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > other.service.OrderOtherServiceImpl.queryOrdersForRefresh'] 17.6727
#Payseeds ['auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > other.service.OrderOtherServiceImpl.queryOrdersForRefresh', 'order.service.OrderServiceImpl.queryOrdersForRefresh > inside_payment.service.InsidePaymentServiceImpl.pay', 'other.service.OrderOtherServiceImpl.queryOrdersForRefresh > inside_payment.service.InsidePaymentServiceImpl.pay', 'inside_payment.service.InsidePaymentServiceImpl.pay > order.service.OrderServiceImpl.queryOrdersForRefresh', 'inside_payment.service.InsidePaymentServiceImpl.pay > other.service.OrderOtherServiceImpl.queryOrdersForRefresh'] 29.5432s
# Consign ['auth.service.impl.TokenServiceImpl.getToken > other.service.OrderOtherServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh', 'other.service.OrderOtherServiceImpl.queryOrdersForRefresh > consign.service.ConsignServiceImpl.queryByOrderId', 'order.service.OrderServiceImpl.queryOrdersForRefresh > consign.service.ConsignServiceImpl.queryByOrderId'] 12.95 ['verifycode.service.impl.VerifyCodeServiceImpl.getImageCode > auth.service.impl.TokenServiceImpl.getToken', 'auth.service.impl.TokenServiceImpl.getToken > other.service.OrderOtherServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh'] 16.577 ['auth.service.impl.TokenServiceImpl.getToken > other.service.OrderOtherServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh', 'order.service.OrderServiceImpl.queryOrdersForRefresh > consign.service.ConsignServiceImpl.queryByOrderId', 'order.service.OrderServiceImpl.queryOrdersForRefresh > consign.service.ConsignServiceImpl.updateConsignRecord', 'other.service.OrderOtherServiceImpl.queryOrdersForRefresh > consign.service.ConsignServiceImpl.queryByOrderId', 'other.service.OrderOtherServiceImpl.queryOrdersForRefresh > consign.service.ConsignServiceImpl.updateConsignRecord'] 22.2460
# Preserve ['verifycode.service.impl.VerifyCodeServiceImpl.getImageCode > auth.service.impl.TokenServiceImpl.getToken', 'auth.service.impl.TokenServiceImpl.getToken > assurance.service.AssuranceServiceImpl.getAllAssuranceTypes', 'auth.service.impl.TokenServiceImpl.getToken > contacts.service.ContactsServiceImpl.findContactsByAccountId', 'auth.service.impl.TokenServiceImpl.getToken > foodsearch.service.FoodServiceImpl.getAllFood', 'auth.service.impl.TokenServiceImpl.getToken > preserveOther.service.PreserveOtherServiceImpl.preserve', 'contacts.service.ContactsServiceImpl.findContactsByAccountId > preserveOther.service.PreserveOtherServiceImpl.preserve', 'travel.service.TravelServiceImpl.queryByBatch > preserveOther.service.PreserveOtherServiceImpl.preserve', 'travel2.service.TravelServiceImpl.queryByBatch > preserveOther.service.PreserveOtherServiceImpl.preserve'] ['auth.service.impl.TokenServiceImpl.getToken > assurance.service.AssuranceServiceImpl.getAllAssuranceTypes', 'auth.service.impl.TokenServiceImpl.getToken > contacts.service.ContactsServiceImpl.findContactsByAccountId', 'auth.service.impl.TokenServiceImpl.getToken > foodsearch.service.FoodServiceImpl.getAllFood', 'auth.service.impl.TokenServiceImpl.getToken > preserve.service.PreserveServiceImpl.preserve', 'travel2.service.TravelServiceImpl.queryByBatch > preserve.service.PreserveServiceImpl.preserve', 'travel.service.TravelServiceImpl.queryByBatch > preserve.service.PreserveServiceImpl.preserve', 'contacts.service.ContactsServiceImpl.findContactsByAccountId > preserve.service.PreserveServiceImpl.preserve', 'foodsearch.service.FoodServiceImpl.getAllFood > preserve.service.PreserveServiceImpl.preserve', 'auth.service.impl.TokenServiceImpl.getToken > assurance.service.AssuranceServiceImpl.getAllAssuranceTypes', 'auth.service.impl.TokenServiceImpl.getToken > contacts.service.ContactsServiceImpl.findContactsByAccountId', 'auth.service.impl.TokenServiceImpl.getToken > foodsearch.service.FoodServiceImpl.getAllFood', 'auth.service.impl.TokenServiceImpl.getToken > preserve.service.PreserveServiceImpl.preserve', 'travel2.service.TravelServiceImpl.queryByBatch > preserve.service.PreserveServiceImpl.preserve', 'travel.service.TravelServiceImpl.queryByBatch > preserve.service.PreserveServiceImpl.preserve', 'contacts.service.ContactsServiceImpl.findContactsByAccountId > preserve.service.PreserveServiceImpl.preserve', 'foodsearch.service.FoodServiceImpl.getAllFood > preserve.service.PreserveServiceImpl.preserve']25s
#Login ['verifycode.service.impl.VerifyCodeServiceImpl.getImageCode > auth.service.impl.TokenServiceImpl.getToken', 'auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > other.service.OrderOtherServiceImpl.queryOrdersForRefresh']  ['verifycode.service.impl.VerifyCodeServiceImpl.getImageCode > auth.service.impl.TokenServiceImpl.getToken', 'auth.service.impl.TokenServiceImpl.getToken > user.service.impl.UserServiceImpl.getAllUsers'] 10.7168
#Collect ['auth.service.impl.TokenServiceImpl.getToken > other.service.OrderOtherServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > execute.service.ExecuteServiceImpl.ticketCollect', 'auth.service.impl.TokenServiceImpl.getToken > other.service.OrderOtherServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > execute.service.ExecuteServiceImpl.ticketCollect'] 28.3366
#Adsearch [] 6.99,29.64,11.0810