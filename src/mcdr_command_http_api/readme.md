# MCDR Command HTTP API

> 提供 HTTP 调用 MCDR 命令的接口

## 依赖

| 插件 | 版本 |
| - | - |
| [fastapi_mcdr](https://github.com/AnzhiZhang/MCDReforgedPlugins/tree/master/src/fastapi_mcdr) | \>=2.0.0 |

## 配置

配置文件路径：`config/mcdr_command_http_api/config.json`

| 配置项 | 默认值 | 说明 |
| - | - | - |
| `token` | 随机生成 | 接口鉴权 Token，首次加载时自动生成 |

## 接口

所有接口均挂载在 `/mcdr_command_http_api` 路径下。

### 鉴权

请求时需在 HTTP Header 中携带 Bearer Token：

```http
Authorization: Bearer <token>
```

### POST /mcdr_command_http_api/execute

在 MCDR 命令系统中执行一条命令。

#### 请求体

```json
{
  "command": "!!MCDR status"
}
```

| 字段 | 类型 | 说明 |
| - | - | - |
| `command` | `string` | 要执行的 MCDR 命令 |

#### 响应

```json
{
  "status": "ok",
  "command": "!!MCDR status"
}
```

#### 错误码

| 状态码 | 说明 |
| - | - |
| `401` | Token 无效 |

## 在线调试

启动 MCDR 后访问 `http://<服务器IP>:8080/mcdr_command_http_api/docs` 可使用 Swagger UI 在线测试接口。
