# 显示服务接口文档

## 概述
该服务用于显示文本、Markdown 和图片内容，支持自动分页和手动翻页。

## 基础 URL
```
http://<服务器地址>:5000
```

## 接口

### 1. 更新显示内容

- **URL**: `/display`
- **方法**: `POST`
- **请求头**:
  - `Content-Type: application/json`
- **请求体**:
```json
{
  "content": "要显示的内容",
  "type": "text|markdown|image"
}
```
- **参数说明**:
  - `content`: 要显示的内容，可以是文本、Markdown 或图片的 base64 编码。
  - `type`: 内容类型，支持 `text`（纯文本）、`markdown`（Markdown 格式）、`image`（图片）。

- **响应**:
```json
{
  "status": "success"
}
```
- **错误响应**:
```json
{
  "error": "错误信息"
}
```

### 2. 显示下一页

- **URL**: `/page/next`
- **方法**: `POST`
- **请求头**:
  - `Content-Type: application/json`
- **响应**:
```json
{
  "status": "success"
}
```

### 3. 显示上一页

- **URL**: `/page/prev`
- **方法**: `POST`
- **请求头**:
  - `Content-Type: application/json`
- **响应**:
```json
{
  "status": "success"
}
```

## 自动翻页
- 服务会自动翻页，每页停留 5 秒。可以通过手动翻页接口来控制翻页。

## 注意事项
- 确保服务正在运行，并且可以通过指定的 URL 访问。
- 图片内容需要以 base64 编码格式传递。

## 示例

### 更新显示内容示例
```bash
curl -X POST http://localhost:5000/display \
  -H "Content-Type: application/json" \
  -d '{"content": "这是一段测试文本", "type": "text"}'
```

### 显示下一页示例
```bash
curl -X POST http://localhost:5000/page/next
```

### 显示上一页示例
```bash
curl -X POST http://localhost:5000/page/prev
```
