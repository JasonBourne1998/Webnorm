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
    trace = 'POST</api/v1/rebookservice/rebook POST</api/v1/rebookservice/rebook/difference POST</api/v1/rebookservice/updateorder'

    codes = """
    reBook(index, type, number) {
            var $modal = $('#doc-modal-2');
            $modal.modal('close');
            var tripId = type + number;
            this.newTripId = tripId;
            var that = this;
            $('#my-prompt1').modal({
                relatedTarget: this,
                onConfirm: function (e) {
                    var rebookInfo = new Object();
                    rebookInfo.orderId = that.selectedOrderId;
                    rebookInfo.oldTripId = that.oldTripId;
                    rebookInfo.tripId = that.newTripId;
                    rebookInfo.seatType = that.selectedSeats[index];
                    rebookInfo.date = that.dateOfToday;
                    var data = JSON.stringify(rebookInfo);
                    $.ajax({
                        type: "post",
                        url: "/api/v1/rebookservice/rebook ",
                        contentType: "application/json",
                        headers: {"Authorization": "Bearer " + sessionStorage.getItem("client_token")},
                        dataType: "json",
                        data: data,
                        xhrFields: {
                            withCredentials: true
                        },
                        success: function (result) {
                            if (result.data["orderMoneyDifference"]  == null || parseFloat(result.data['orderMoneyDifference']) == 0) {
                                var orderUpdateDto = {
                                    order: result.data["order"],
                                    tripAllDetail: result.data["tripAllDetail"],
                                    ticketPrice: result.data["ticketPrice"], 
                                    orderMoneyDifference: result.data["orderMoneyDifference"]
                                };
                                orderUpdateDto["rebookInfo"] = rebookInfo;
                                var jsonData = JSON.stringify(orderUpdateDto);
                                console.log(jsonData)
                                $.ajax({
                                    type: "POST",
                                    url: "/api/v1/rebookservice/updateorder", 
                                    contentType: "application/json",
                                    headers: {
                                        "Authorization": "Bearer " + sessionStorage.getItem("client_token") 
                                    },
                                    data: jsonData,
                                    success: function(response) {
                                        if (response.status === 1) {
                                            alert("Order updated successfully!");
                                            window.location.reload(); 
                                        } else {
                                            alert("Failed to update order: " + response.msg);
                                        }
                                    },
                                    error: function(xhr, status, error) {
                                        alert("An error occurred: " + error);
                                    }
                                });
                                window.location.reload();
                            } else if (result.data['orderMoneyDifference'] != null & parseFloat(result.data['orderMoneyDifference']) > 0) {
                                // pay difference money
                                that.differenceMoney = result.data["orderMoneyDifference"];
                                console.log(that.differenceMoney);
                                $('#my-prompt2').modal({
                                    relatedTarget: this,
                                    onConfirm: function (e) {
                                        var rebookPayInfoData = new Object();
                                        rebookPayInfoData.orderId = that.selectedOrderId;
                                        rebookPayInfoData.tripId = that.oldTripId;
                                        rebookPayInfoData.userId = sessionStorage.getItem("client_id");
                                        rebookPayInfoData.money = that.differenceMoney;
                                        var rebookPayInfoData = JSON.stringify(rebookPayInfoData);
                                        console.log(rebookPayInfoData);
                                        $.ajax({
                                            type: "post",
                                            url: "/api/v1/rebookservice/rebook/difference",
                                            contentType: "application/json",
                                            headers: {"Authorization": "Bearer " + sessionStorage.getItem("client_token")},
                                            dataType: "json",
                                            data: rebookPayInfoData,
                                            xhrFields: {
                                                withCredentials: true
                                            },
                                            success: function (res) {
                                                if (res["status"] == 1) {
                                                    var orderUpdateDto = {
                                                        order: result.data["order"],
                                                        tripAllDetail: result.data["tripAllDetail"],
                                                        ticketPrice: result.data["ticketPrice"], 
                                                        orderMoneyDifference: result.data["orderMoneyDifference"]
                                                    };
                                                    orderUpdateDto["rebookInfo"] = rebookInfo;
                                                    // 将对象转换为JSON字符串
                                                    var jsonData = JSON.stringify(orderUpdateDto);
                                                    console.log(jsonData)
                                                    // 发送AJAX请求到后端
                                                    $.ajax({
                                                        type: "POST",
                                                        url: "/api/v1/rebookservice/updateorder", 
                                                        contentType: "application/json",
                                                        headers: {
                                                            "Authorization": "Bearer " + sessionStorage.getItem("client_token") 
                                                        },
                                                        data: jsonData,
                                                        success: function(response) {
                                                            if (response.status === 1) {
                                                                alert("Order updated successfully!");
                                                                // window.location.reload(); 
                                                            } else {
                                                                alert("Failed to update order: " + response.msg);
                                                            }
                                                        },
                                                        error: function(xhr, status, error) {
                                                            alert("An error occurred: " + error);
                                                        }
                                                    });
                                                    // window.location.reload();
                                                }
                                                else{
                                                    alert("Order updated failed!");
                                                }
                                                // window.location.reload();
                                            },
                                            error: function (e) {
                                                alert("unKnow payDifference error!")
                                            }
                                        });
                                    },
                                    onCancel: function (e) {
                                        // alert('you hava canceled!');
                                    }
                                });
                            } else {
                                alert(result["msg"]);
                            }
                        },
                        error: function (e) {

                            var message = e.responseJSON.message;
                            console.log(message);
                            if (message.indexOf("Token") != -1) {
                                alert("Token is expired! please login first!");
                            } else {
                                alert("unKnow rebook error！")
                            }
                        }
                    });
                },
                onCancel: function (e) {
                    // alert('you hava canceled!');
                }
            });
        }
    """

    checker = GPTChecker(
        api_key=api_key,
        model="gpt-4o",
        max_tokens=2048,
        top_p=0.9,
        temperature=0.0
    )

    result = checker.check_trigger_relationship(trace,codes)

    # print(result)