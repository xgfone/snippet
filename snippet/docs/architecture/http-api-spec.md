## HTTP API 接口调用规范

### 说明
所有参数（包括请求和应答）的字段名均为 `首字母大写的驼峰式(CamelCase)`。

说明：
- 字段名为英文单词。
- 仅首字母大写，其它均为小写，包括缩略词，如：**Ip**、**Id**、**PublicIp**、**InstanceId**。

### Method
同时支持 GET 和 POST 两种方法，其不同之处在于请求参数的位置：
- GET：请求参数放置在 Query 中。
- POST：请求参数放置在 Body 中，并使用请求头 `Content-Type` 说明 Body 数据的格式，建议使用 JSON 格式。

### 请求参数
#### 请求指令
请求指令可以通过 URL Path 来区分，也可以使用 Action 参数来表示。如果使用 Path，可以使用 Router 来完成；如果使用 Action 参数，则既可放在 Query（参数名为 `Action`）中，也可作为公共参数放在请求头（请求头名为 `X-Action`）中。

注：对于请求指令的值遵循参数字段名的规范，并使用 `VerbNoun` 格式，如 `CreateUser`、`GetUser`、`DeleteUser`。

#### 公共参数
所有的公共参数均放置在请求头中，对于非 Web 标准的请求头名，则以 `X-` 作为其前缀。

#### API Version
API Version 可以放置在 URL Path 中（如 `/v1`），也可以作为为公共参数放置在请求头中（请求头名为 `X-Version` 或 `X-Api-Version`）。

#### 认证信息
认证信息被视为公共参数，因此，则放在请求头中。为了兼容 Web 标准，则将认证信息放在请求头 `Authorization` 中，参数值格式为 `AuthMethod AuthInfoValue`。其中，`AutMethod`表示认证方法（如 `Basic`、`Token`、`OAuth2`、`HMAC-SHA256` 等），`AuthInfoValue` 表示完成认证所需要的信息。

对于类似 API 网关的代理，认证通过后，当转发给后端服务时，则可将解析出来的认证信息（如：用户ID、用户名、角色类型等）放在请求头中（请求头名分别为 `X-User-Id`、`X-User-Name`、`X-User-Role-Type`等），然后再转发给后端服务；这样，后端服务在接收到请求时，则可以直接从请求头中取出相关的用户信息。

### 应答
#### 状态码
无论应答是成功还是失败，状态码均返回 200。

### 应答Body
请求的应答结果放置在 Body 中，应答头 `Content-Type` 说明 Body 数据的格式，建议使用 JSON 格式。

```json
{
    "RequestId": "string",
    "Data": object,
    "Error": {
        "Code": "string",
        "Message": "string"
    }
}
```

字段名     |  类型  | 说明
----------|---------|---------
RequestId | string | 服务器返回给请求者的唯一请求ID（可以使用 `UUID`），当前发生错误时，请求者可以提供该ID以便快速排查具体的错误原因。对于长时间操作，可以先返回应答，并进行异步处理；而请求者则可以根据此ID查询处理结果。
Data      | object | 当处理成功时，返回给请求者的具体应答结果，它可以是任何值，不过建议以 JSON 表示。如果请求处理失败或没有答应结果，则可被忽略或为 `null`。
Error     | object | 如果存在，则表示请求处理失败，其中的参数字段信息则表示失败的原因，参见下表。

字段名   |  类型  |  说明
--------|--------|---------
Code    | string | 表示错误码，也即是错误的类型，如 `InvalidParameter`、`AuthFailure`。它可以支持子类型，与主类型以英文点进行分隔，如 `AuthFailure.TokenFailure`、`AuthFailure.InvalidCookie`。
Message | string | 表示具体的错误信息，可以在浏览器中显示给用户。该字段可以缺失或为空；如果缺失或为空，则可根据 `Code` 字段的错误类型来显示预定义的通用错误信息。注：如果无法识别子类型，则可按主类型表示的错误信息显示。

#### 应答成功样例
```json
// Example 1
{
    "RequestId": "9162ED80-4DD4-4ACC-B7CD-6DE858B01994"
}

// Example 2
{
    "RequestId": "9162ED80-4DD4-4ACC-B7CD-6DE858B01994",
    "Data": {
        "Name": "Aaron",
        "Age": 18
    }
}
```

#### 应答失败样例
```json
// Example 1
{
    "RequestId": "9162ED80-4DD4-4ACC-B7CD-6DE858B01994",
    "Error": {
        "Code": "InvalidParameter"
    }
}

// Example 2
{
    "RequestId": "9162ED80-4DD4-4ACC-B7CD-6DE858B01994",
    "Error": {
        "Code": "AuthFailure.InvalidCookie"
    }
}

// Example 3
{
    "RequestId": "9162ED80-4DD4-4ACC-B7CD-6DE858B01994",
    "Error": {
        "Code": "AuthFailure.InvalidCookie",
        "Message": "Cookie named 'sessionid' is invalid"
    }
}
```

## Example

```bash
# Example 1
$ curl -XGET http://127.0.0.1/api/v1/GetUser?UserName=Aaron

### Response
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 140

{
    "RequestId": "9ED0C269-660F-444A-91D8-BAC673C2D108",
    "Data": {
        "UserName": "Aaron",
        "Age": 18,
        ...
    }
}


# Example 2
$ curl -XPOST http://127.0.0.1/api/v1/GetUser -H 'Content-Type: application/json' -d '{"UserName": "Aaron"}'

### Response
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 140

{
    "RequestId": "9ED0C269-660F-444A-91D8-BAC673C2D108",
    "Data": {
        "UserName": "Aaron",
        "Age": 18,
        ...
    }
}


# Example 3
$ curl -XGET http://api.example.com/v1?Action=GetUser&UserName=Aaron

### Response
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 140

{
    "RequestId": "9ED0C269-660F-444A-91D8-BAC673C2D108",
    "Data": {
        "UserName": "Aaron",
        "Age": 18,
        ...
    }
}


# Example 4
$ curl -XPOST http://api.example.com -H 'X-Version: v1' -H 'X-Action: GetUser' -H 'Content-Type: application/json' -d '{"UserName": "Aaron"}'

### Response
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 140

{
    "RequestId": "9ED0C269-660F-444A-91D8-BAC673C2D108",
    "Data": {
        "UserName": "Aaron",
        "Age": 18,
        ...
    }
}
```
