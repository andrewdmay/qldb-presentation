# QLDB Presentation Demo

Simple demo of QLDB Ledger being used for Event Sourcing.
Consists of an API Lambda Function tied to an HTTP API Gateway that talks to a QLDB Ledger and either inserts
or updates the Ledger depending on whether the provided event has a new "id" attribute.

If the event is new, the received event is sent to an SNS Topic.

The Lambda function is writen in Python 3.8 and uses Poetry for dependency management.

The Lambda function is deployed using AWS SAM and the Serverless Transform automatically generates a HTTP API Gateway.

## Templates

* ledger.yaml - creates the Ledger, SNS Topic, and SQS Queue subscribed to the Topic
* template.yaml - SAM Template for Lambda Function and API Gateway

## Creating the QLDB Table

The Ledger is created via CloudFormation, but the `ApiEvent` table is not.
It can be created in the QLDB Console with these PartiQL commands:

```sql
CREATE TABLE ApiEvent

CREATE INDEX ON ApiEvent (id)
```
