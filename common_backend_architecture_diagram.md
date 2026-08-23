                         Client
                    (Web / Mobile)
                           |
                           |
                           ▼
                  ┌────────────────┐
                  │ API Gateway    │
                  └───────┬────────┘
                          |
                          ▼

              ┌───────────────────────┐
              │   Controller Layer    │
              │                       │
              │ REST API / GraphQL    │
              └──────────┬────────────┘
                         |
                         ▼

              ┌───────────────────────┐
              │    Service Layer      │
              │                       │
              │ Business Logic        │
              │ Workflow              │
              └───────┬───────────────┘
                      |
          ┌───────────┼───────────┐
          |           |           |
          ▼           ▼           ▼

   Repository     External     Message
      Layer       Service      Queue
          |          |            |
          |          |            |
          ▼          ▼            ▼

     Database   ┌──────────┐   Kafka/
                │ Payment  │   RabbitMQ
                │ Provider │
                │ Email API│
                │ LLM API  │
                └──────────┘