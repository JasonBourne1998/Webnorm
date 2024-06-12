from gptchecker import GPTChecker

checker = GPTChecker(
    api_key="sk-proj-enNNZd2GZEkaDuRa3rPfT3BlbkFJph7uEdwchQlAXWY5gm2G",
    model="gpt-4o",
    max_tokens=2048,
    top_p=0.9,
    temperature=0.0
)

class_name = "PriceConfig"

class_definition = """
public class PriceConfig {
    private UUID id;
    private String trainType;
    private String routeId;
    private double basicPriceRate;
    private double firstClassPriceRate;
}
"""

logs1 = [
    "2024-05-01 16:14:31.760 INFO   1 --- [http-nio-16579-exec-5] p.s.LoggingAspect: Execution of repository method: findByRouteIdAndTrainType, Execution Time: 4 milliseconds, Result: PriceConfig(id=6d20b8cb-039c-474c-ae25-b6177ea41152, trainType=GaoTieOne, routeId=92708982-77af-4318-be25-57ccb0ff69ad, basicPriceRate=0.38, firstClassPriceRate=1.0)"
]

logs2 = [
    '"2024-06-03 15:55:13.475 INFO 1 --- [http-nio-18673-exec-4] p.s.LoggingAspect: Execution of repository method: findByRouteIdsAndTrainTypes, Execution Time: 2 milliseconds, Result: [PriceConfig(id=d5c4523a-827c-468c-95be-e9024a40572e, trainType=DongCheOne, routeId=f3d4d4ef-693b-4456-8eed-59c0d717dd08, basicPriceRate=0.45, firstClassPriceRate=1.0), PriceConfig(id=6d20b8cb-039c-474c-ae25-b6177ea41152, trainType=GaoTieOne, routeId=92708982-77af-4318-be25-57ccb0ff69ad, basicPriceRate=0.38, firstClassPriceRate=1.0)]'
]

checker.check_database_constraint(
    class_name,
    class_definition,
    logs1,
    logs2
)