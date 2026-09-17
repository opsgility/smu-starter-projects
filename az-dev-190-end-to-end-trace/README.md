# az-dev-190-end-to-end-trace

Intake API (`Program.cs`) + Function (`OrdersFunction.cs`) that together trace an order through HTTP → Service Bus → Function → Cosmos → downstream HTTP. Deploy the intake as an App Service and the function to the pre-provisioned Function App. One traceparent covers every hop; the Application Insights end-to-end trace view will show all five stages under a single TraceId.
