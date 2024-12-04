# Teste de integração

```mermaid
graph LR
        Input1["TestCase 1"]
        Input2["TestCase 2"]
        Input3["TestCase 3"]



        Hidden1_1["Class A"]
        Hidden1_2["Class B"]
        Hidden1_3["Class C"]


        Hidden2_1["Class D"]
        Hidden2_2["Class E"]
        Hidden2_3["Class F"]
        Hidden2_4["Class G"]

        Output1["Pass"]
        Output2["Fail"]

    Input1 --> Hidden1_1
    Input1 --> Hidden1_2
    Input1 --> Hidden1_3

    Input2 --> Hidden1_1
    Input2 --> Hidden1_2
    Input2 --> Hidden1_3

    Input3 --> Hidden1_1
    Input3 --> Hidden1_2
    Input3 --> Hidden1_3

    Hidden1_1 --> Hidden2_1
    Hidden1_1 --> Hidden2_2
    Hidden1_1 --> Hidden2_3
    Hidden1_1 --> Hidden2_4

    Hidden1_2 --> Hidden2_1
    Hidden1_2 --> Hidden2_2
    Hidden1_2 --> Hidden2_3
    Hidden1_2 --> Hidden2_4

    Hidden1_3 --> Hidden2_1
    Hidden1_3 --> Hidden2_2
    Hidden1_3 --> Hidden2_3
    Hidden1_3 --> Hidden2_4

    Hidden2_1 --> Output1
    Hidden2_1 --> Output2

    Hidden2_2 --> Output1
    Hidden2_2 --> Output2

    Hidden2_3 --> Output1
    Hidden2_3 --> Output2

    Hidden2_4 --> Output1
    Hidden2_4 --> Output2
    style Output1 fill:#7FFF7F,stroke:#32CD32,stroke-width:2px,color:black
    style Output2 fill:#FF7F7F,stroke:#FF4500,stroke-width:2px,color:black
    style Input1 fill:#454545,stroke:#454545,stroke-width:2px,color:white
    style Input2 fill:#454545,stroke:#454545,stroke-width:2px,color:white
    style Input3 fill:#454545,stroke:#454545,stroke-width:2px,color:white
```

> [Para que serve?](/pages/p1.md)

> [Quando usar testes de integração e usar ou não 'mocks'?](/pages/p2.md)

> [Ferramentas](/pages/p3.md)

> [Implementação em um projeto real](/pages/p5.md)
