import requests

HOST_ADDRESS = "http://localhost"
HOST_PORT = "5000"

casos_teste = [
    {"api_endpoint": "/api/cashback",
     "teste_requests": [{"entrada":"""{
                                "sold_at": "2026-01-02 00:00:00",
                                "customer": {
                                   "document": "00000000000",
                                   "name": "JOSE DA SILVA",
                                },
                                "total": "100.00",
                                "products": [
                                   {
                                      "type": "A",
                                      "value": "10.00",
                                      "qty": 1,
                                   },
                                   {
                                      "type": "B",
                                      "value": "10.00",
                                      "qty": 9,
                                   }
                                ],
                            }""",
                         "saida": """{
                                      "createdAt": "2021-07-26T22:50:55.740Z",
                                      "message": "Cashback criado com sucesso!",
                                      "id": "NaN",
                                      "document": "33535353535",
                                      "cashback": "10"
                                    }"""},
                        ]

     }

]

def main ():
    for caso in casos_teste:
        for teste in caso["teste_requests"]:
            retorno = requests.post("%s:%s%s"%(HOST_ADDRESS,HOST_PORT,caso["api_endpoint"]), json=teste["entrada"])
            if retorno == teste["saida"] :
                continue
            else:
                raise Exception("fail during teste %s of endpoint %s: unexpected return %s"%(teste["entrada"],caso["api_endpoint"],retorno))


main()

