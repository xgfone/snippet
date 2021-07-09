# HTTP API 接口调用规范

## 请求与应答参数字段名格式
所有参数（包括请求和应答）的字段名均为 `首字母大写的驼峰式(CamelCase)`。

**说明：**
- 字段名为英文单词。
- 仅首字母大写，其它均为小写，包括缩略词，如：**Ip**、**Id**、**PublicIp**、**InstanceId**。
- 如果参数值是多个实体，字段名则应使用英文单词的复数形式，如：Instances、Ips。

## 请求
### 请求方法
同时支持 GET 和 POST 两种方法，其不同之处在于请求参数的位置：
- GET：请求参数放在 Query 中。
- POST：请求参数放在 Body 中，并使用请求头 `Content-Type` 说明 Body 数据的格式，建议使用 JSON 格式。

### 请求参数

#### Query 参数
对于一个嵌套型的参数，如果通过 Query 参数进行传递，则要将其平铺成 Query 参数，比如：
```json
{
    "User": {
        "Name": "Aaron",
        "Email": "aaron@example.com"
    }
}
```
作为 Query 参数，要将其转换为 `User.Name=Aaron & User.Email=aaron@example.com`。

如果 Query 参数的值是个数组，可以直接先将其转换为 JSON 字符串，然后再作为 Query 参数的值，如 `Ids=["UUID1", "UUID2", "UUID3"]`。如果服务器接收到此 Query 参数，可以直接用 JSON 解码器进行解码。除了使用 JSON 字符串外，也可以使用以英文逗号分隔字符串，如 `UUID1,UUID2,UUID3`。

**注意：** 对于 Query 参数值，在发送请求前，要先对其进行转义，比如：`Ids=["UUID1", "UUID2", "UUID3"]` 要被转义为 `Ids=%5B%22UUID1%22%2C+%22UUID2%22%2C+%22UUID3%22%5D`。

#### 参数属性
如果一个参数值有属性，则以 **英文冒号** 分隔参数值及其属性，且 **参数值在前、属性在后**，如 `OrderBy=CreatedTime:Desc` 或 `{"OrderBy": "CreatedTime:Desc"}`，其表示以 `CreatedTime` 字段进行降序排序。

**注：** 这种情况只适用类型为 `string` 的参数。

如果是个数组，则可以表示为 `{"OrderBys": ["CreatedTime:Desc", "Name:Asc"]}`。

### 请求指令
请求指令可以通过 URL Path 来区分，也可以使用 Action 参数来表示。
- 如果使用 Path，可以使用 Router 来完成。
- 如果使用 Action 参数，则既可放在 **Query**（参数名为 `Action`）中，也可作为 **公共参数** 放在 **请求头**（请求头名为 `X-Action`）中。

**注：**
- 对于请求指令的值遵循参数字段名的规范，并使用 `VerbNoun` 格式，如 `CreateUser`、`GetUser`、`DeleteUser`。
- 如果指令操作的资源是多个，则请求指令格式应为 `VerbNouns`，如 `GetUsers`、`DeleteUsers`。

### 公共参数
**所有的公共参数均放在请求头中**，对于非 Web 标准的请求头名，则以 `X-` 作为其前缀，如 `X-User-Id`。

### API Version
API Version 可以放在 **URL Path** 中（如 `/v1`），也可以作为 **公共参数** 放在 **请求头** 中（请求头名为 `X-Version` 或 `X-Api-Version`）。

### 认证信息
**认证信息被视为公共参数，因此，则放在请求头中。** 为了兼容 Web 标准，则将认证信息放在请求头 `Authorization` 中，参数值格式为 `AuthMethod AuthInfoValue`。其中，`AutMethod`表示认证方法（如 `Basic`、`Token`、`OAuth2`、`HMAC-SHA256` 等），`AuthInfoValue` 表示完成认证所需要的信息。

对于类似 API 网关的代理，认证通过后，当转发给后端服务时，则可将解析出来的认证信息（如：登录者ID、登录者名字、登录者的角色类型等）放在请求头中（请求头名分别为 `X-Operator-Id`、`X-Operator-Name`、`X-Operator-Role-Type`等），然后再转发给后端服务；这样，后端服务在接收到请求时，则可以直接从请求头中取出相关的用户信息。

## 应答
### 状态码
无论应答是成功还是失败，状态码均返回 200。

### 应答Body
**请求的应答结果放在 Body 中**，应答头 `Content-Type` 说明 Body 数据的格式，建议使用 JSON 格式。

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
Data      | object | 当处理成功时，返回给请求者的具体应答结果，它可以是任何值，不过建议以 JSON 表示。**如果请求处理失败或没有答应结果，则可被忽略或为 `null`**。
Error     | object | **如果存在，则表示请求处理失败**，其中的参数字段信息则表示失败的原因，参见下表。

字段名   |  类型  |  说明
--------|--------|---------
Code    | string | **表示错误码，也即是错误的类型**，如 `InvalidParameter`、`AuthFailure`，根据错误类型，可以快速区分不同的错误。它也可以支持子类型，与主类型以英文点进行分隔，如 `AuthFailure.TokenFailure`、`AuthFailure.InvalidCookie`。
Message | string | **表示具体的错误信息，可以在浏览器中显示给用户**。该字段可以缺失或为空；如果缺失或为空，则可根据 `Code` 字段的错误类型来显示预定义的通用错误信息。注：如果无法识别子类型，则可按主类型表示的错误信息显示。

#### 应答成功样例
##### 没有应答数据
```json
{
    "RequestId": "9162ED80-4DD4-4ACC-B7CD-6DE858B01994"
}
```

##### 含有应答数据
```json
{
    "RequestId": "9162ED80-4DD4-4ACC-B7CD-6DE858B01994",
    "Data": {
        "Name": "Aaron",
        "Age": 18
    }
}
```

#### 应答失败样例
##### 只有错误主类型
```json
{
    "RequestId": "9162ED80-4DD4-4ACC-B7CD-6DE858B01994",
    "Error": {
        "Code": "InvalidParameter"
    }
}
```

##### 只有错误主类型及子类型
```json
{
    "RequestId": "9162ED80-4DD4-4ACC-B7CD-6DE858B01994",
    "Error": {
        "Code": "AuthFailure.InvalidCookie"
    }
}
```

##### 包含错误类型和错误消息
```json
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
