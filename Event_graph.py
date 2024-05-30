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
