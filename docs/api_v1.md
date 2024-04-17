# API V1

## Base URL

`/api/v1`

## Endpoints

### Create Entity

- **URL:** `/api/v1/entities`
- **Methods:** `POST`, `PUT`
- **Description:** This endpoint facilitates the creation of an entity.

#### Request:

For `POST` method:

- `msisdn`: Mobile phone number (Required)

For `PUT` method:

- `msisdn`: Mobile phone number (Required)
- `code`: Verification code (Required)
- `password`: Password (Required)
- `username`: Username (Required)

#### Response:

- `POST`:
  - **Status Code:** `201`
  - **Body:** `{}`
- `PUT`:
  - **Status Code:** `200`
  - **Body:** `{"eid": <entity_id>}`

#### Error Responses:

- `400 Bad Request`: Indicates that required parameters are missing or invalid.
- `401 Unauthorized`: Indicates that the verification code is incorrect.
- `409 Conflict`: Indicates that the entity MSISDN or username already exists.
- `405 Method Not Allowed`: Indicates that an unsupported HTTP method is used.
- `500 Internal Server Error`: Indicates an unexpected error occurrence.
