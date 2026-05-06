# Campus Notification System Design

## Objective

Design a simple and scalable notification system for students to receive updates about:

- Placements
- Results
- Events

The system supports:

- Real-time notifications
- Notification history
- Read/Unread status
- Priority notifications
- REST APIs

---

# System Architecture

```text
Client Apps
   |
   v
API Gateway
   |
   v
Notification Service
   |
   +----------------------+
   |                      |
   v                      v
Database              WebSocket Server
   |                      |
   v                      v
Notification Store    Real-time Push
```

---

# Main Features

1. Student Login
2. View Notifications
3. Mark Notifications as Read
4. Real-Time Updates
5. Filter Notifications
6. Pagination Support
7. Priority Notifications
8. Admin Broadcast Notifications

---

# API Details

## Base URL

```text
/api/v1
```

## Authentication

```http
Authorization: Bearer <JWT_TOKEN>
```

## Content Type

```http
Content-Type: application/json
```

---

# 1. Login API

## Endpoint

```http
POST /api/v1/auth/login
```

## Request

```json
{
  "email": "student@college.edu",
  "password": "password123"
}
```

## Response

```json
{
  "success": true,
  "token": "jwt_token_here",
  "student": {
    "id": 1042,
    "name": "Rudrabhishek",
    "email": "student@college.edu"
  }
}
```

## Status Codes

| Code | Description |
|------|-------------|
| 200 | Login Successful |
| 401 | Invalid Credentials |
| 500 | Server Error |

---

# 2. Fetch Notifications

## Endpoint

```http
GET /api/v1/notifications
```

## Query Parameters

| Parameter | Type | Description |
|----------|------|-------------|
| page | integer | Page number |
| limit | integer | Notifications per page |
| unreadOnly | boolean | Fetch only unread notifications |
| type | string | Placement / Event / Result |

## Example Request

```http
GET /api/v1/notifications?page=1&limit=10&unreadOnly=true
```

## Response

```json
{
  "success": true,
  "page": 1,
  "limit": 10,
  "total": 125,
  "notifications": [
    {
      "id": "uuid",
      "type": "Placement",
      "message": "CSX Corporation hiring",
      "isRead": false,
      "priority": 10,
      "createdAt": "2026-04-22T10:00:00Z"
    }
  ]
}
```

---

# 3. Mark Notification as Read

## Endpoint

```http
PATCH /api/v1/notifications/{notificationId}/read
```

## Example Request

```http
PATCH /api/v1/notifications/123/read
```

## Response

```json
{
  "success": true,
  "message": "Notification marked as read"
}
```

---

# 4. Mark All Notifications as Read

## Endpoint

```http
PATCH /api/v1/notifications/read-all
```

## Response

```json
{
  "success": true,
  "message": "All notifications marked as read"
}
```

---

# 5. Delete Notification

## Endpoint

```http
DELETE /api/v1/notifications/{notificationId}
```

## Response

```json
{
  "success": true,
  "message": "Notification deleted"
}
```

---

# 6. Admin Broadcast Notification

## Endpoint

```http
POST /api/v1/admin/notifications/broadcast
```

## Headers

```http
Authorization: Bearer <ADMIN_JWT_TOKEN>
```

## Request

```json
{
  "type": "Placement",
  "message": "Microsoft hiring for SDE roles",
  "targetAudience": "all_students"
}
```

## Response

```json
{
  "success": true,
  "message": "Notification broadcast initiated"
}
```

---

# Notification Schema

```json
{
  "id": "UUID",
  "studentId": 1042,
  "type": "Placement",
  "message": "Google Hiring",
  "isRead": false,
  "priority": 10,
  "createdAt": "2026-04-22T10:00:00Z",
  "updatedAt": "2026-04-22T10:05:00Z"
}
```

---

# Real-Time Notification

## Recommended Technology

- WebSockets
- Socket.IO

### Advantages

- Fast communication
- Real-time updates
- Low latency
- Better than polling

---

# WebSocket Endpoint

```text
ws://domain.com/socket.io
```

---

# WebSocket Events

## Connection Event

```json
{
  "event": "connect",
  "studentId": 1042
}
```

## New Notification Event

```json
{
  "event": "new_notification",
  "data": {
    "id": "uuid",
    "type": "Placement",
    "message": "Amazon hiring",
    "createdAt": "2026-04-22T10:00:00Z"
  }
}
```

## Read Event

```json
{
  "event": "notification_read",
  "notificationId": "uuid"
}
```

---

# Security Features

1. JWT Authentication
2. HTTPS
3. Role-Based Access Control
4. Rate Limiting
5. Input Validation
6. SQL Injection Prevention
7. WebSocket Authentication

---

# Error Response Format

```json
{
  "success": false,
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Invalid notification ID"
  }
}
```

---

# Pagination

## Offset Pagination

```http
GET /api/v1/notifications?page=1&limit=20
```

## Cursor Pagination

```http
GET /api/v1/notifications?cursor=abc123&limit=20
```

---

# Scalability Features

1. Stateless APIs
2. Load Balancers
3. Redis Caching
4. Database Indexing
5. Asynchronous Processing
6. Horizontal Scaling
7. Message Queues

---

# Suggested Tech Stack

| Layer | Technology |
|------|-------------|
| Backend | Node.js / FastAPI |
| Data