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
| Database | PostgreSQL |
| Cache | Redis |
| Real-Time | Socket.IO |
| Queue | RabbitMQ / Kafka |
| Authentication | JWT |
| Deployment | Docker + Kubernetes |

---

# Conclusion

This notification platform provides:

- Secure APIs
- Real-time communication
- Reliable notification delivery
- Scalable architecture
- Efficient performance

It is suitable for large-scale campus environments with future scalability support.

---

# Stage 2

# Database Selection

## Recommended Database

### PostgreSQL

PostgreSQL is recommended for this notification system because:

- It provides strong reliability and consistency.
- Supports structured relational data.
- Handles large-scale queries efficiently.
- Supports indexing and optimization.
- Provides ACID compliance.
- Works well with authentication and notification relationships.
- Easy integration with Node.js and FastAPI.

Redis can additionally be used for:

- Caching
- Real-time notification queues
- Session management

---

# Why PostgreSQL?

| Feature | Benefit |
|------|-------------|
| ACID Transactions | Reliable data storage |
| Indexing | Faster searches |
| Scalability | Supports large datasets |
| JSON Support | Flexible notification metadata |
| Security | Role-based permissions |
| Performance | Efficient querying |

---

# Database Schema

## Students Table

```sql
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Notifications Table

```sql
CREATE TABLE notifications (
    id UUID PRIMARY KEY,
    student_id INTEGER REFERENCES students(id),
    type VARCHAR(50) NOT NULL,
    message TEXT NOT NULL,
    priority INTEGER DEFAULT 1,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Admin Table

```sql
CREATE TABLE admins (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(150) UNIQUE,
    password_hash TEXT NOT NULL
);
```

---

# Database Relationships

```text
Students
   |
   | 1 : Many
   v
Notifications
```

One student can have multiple notifications.

---

# Indexing Strategy

```sql
CREATE INDEX idx_student_notifications
ON notifications(student_id);

CREATE INDEX idx_notification_read
ON notifications(is_read);

CREATE INDEX idx_notification_created
ON notifications(created_at DESC);
```

Benefits:

- Faster unread notification lookup
- Faster sorting by time
- Faster filtering by student

---

# Problems as Data Volume Increases

## 1. Slow Queries

Problem:
- Notification tables may contain millions of rows.

Solution:
- Use indexing
- Use pagination
- Optimize SQL queries

---

## 2. High Database Load

Problem:
- Many students requesting notifications simultaneously.

Solution:
- Use Redis caching
- Add read replicas
- Use load balancers

---

## 3. Real-Time Notification Delays

Problem:
- WebSocket traffic increases.

Solution:
- Use Redis Pub/Sub
- Use Kafka or RabbitMQ
- Horizontal scaling

---

## 4. Storage Growth

Problem:
- Notifications continuously increase.

Solution:
- Archive old notifications
- Partition tables
- Use cloud storage backups

---

## 5. API Performance Issues

Problem:
- APIs become slower during peak usage.

Solution:
- API rate limiting
- Caching
- Async processing
- CDN support

---

# Scalability Solutions

## Horizontal Scaling

Add multiple backend servers.

```text
Users
   |
Load Balancer
   |
+---------+---------+
|         |         |
Server1  Server2  Server3
```

---

## Database Partitioning

Partition notifications based on:

- Student ID
- Year
- Notification Type

Example:

```sql
CREATE TABLE notifications_2026 PARTITION OF notifications
FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');
```

---

# SQL Queries Based on APIs

## 1. Login Query

```sql
SELECT id, name, email
FROM students
WHERE email = 'student@college.edu';
```

---

## 2. Fetch Notifications

```sql
SELECT *
FROM notifications
WHERE student_id = 1042
ORDER BY created_at DESC
LIMIT 10 OFFSET 0;
```

---

## 3. Fetch Unread Notifications

```sql
SELECT *
FROM notifications
WHERE student_id = 1042
AND is_read = FALSE
ORDER BY created_at DESC;
```

---

## 4. Mark Notification as Read

```sql
UPDATE notifications
SET is_read = TRUE,
    updated_at = CURRENT_TIMESTAMP
WHERE id = 'uuid';
```

---

## 5. Mark All Notifications as Read

```sql
UPDATE notifications
SET is_read = TRUE,
    updated_at = CURRENT_TIMESTAMP
WHERE student_id = 1042;
```

---

## 6. Delete Notification

```sql
DELETE FROM notifications
WHERE id = 'uuid';
```

---

## 7. Insert Notification

```sql
INSERT INTO notifications (
    id,
    student_id,
    type,
    message,
    priority
)
VALUES (
    gen_random_uuid(),
    1042,
    'Placement',
    'Amazon hiring for SDE roles',
    10
);
```

---

# NoSQL Alternative

## MongoDB

MongoDB can also be used for:

- Flexible schemas
- High scalability
- Faster horizontal scaling
- Large notification datasets

Example Document:

```json
{
  "_id": "uuid",
  "studentId": 1042,
  "type": "Placement",
  "message": "Amazon hiring",
  "isRead": false,
  "priority": 10,
  "createdAt": "2026-04-22T10:00:00Z"
}
```

---

# Final Recommendation

Recommended Setup:

- PostgreSQL for primary relational storage
- Redis for caching and real-time queues
- Kafka/RabbitMQ for event streaming
- Socket.IO for real-time delivery

This setup provides:

- High reliability
- Better scalability
- Faster performance
- Real-time communication
- Efficient notification management

---

# Stage 3

# Query Optimization and Performance Analysis

## Existing Query

```sql
SELECT * FROM notifications
WHERE studentID = 1042 AND isRead = false
ORDER BY createdAt DESC;
```

---

# Is the Query Accurate?

The query logic is mostly correct because it:

- Fetches notifications for a specific student
- Filters unread notifications
- Sorts notifications by newest first

However, there are some issues:

| Problem | Explanation |
|------|-------------|
| Incorrect column naming | `studentID`, `isRead`, and `createdAt` do not match snake_case naming used in schema |
| SELECT * usage | Fetches unnecessary columns |
| No pagination | Returns too many rows |
| No indexing mentioned | Causes slow execution |

---

# Corrected Query

```sql
SELECT id, type, message, priority, created_at
FROM notifications
WHERE student_id = 1042
AND is_read = FALSE
ORDER BY created_at DESC;
```

---

# Why is the Query Slow?

The database currently contains:

- 50,000 students
- 5,000,000 notifications

The query becomes slow because:

## 1. Full Table Scan

Without proper indexing, the database scans millions of rows.

Time Complexity:

```text
O(n)
```

where `n` is the total number of notifications.

---

## 2. Sorting Cost

The query sorts unread notifications using:

```sql
ORDER BY created_at DESC
```

Sorting large datasets is expensive.

Approximate Cost:

```text
O(n log n)
```

---

## 3. SELECT * Problem

Using:

```sql
SELECT *
```

fetches every column even when unnecessary.

This increases:

- Disk I/O
- Memory usage
- Network transfer time

---

## 4. No Pagination

If a student has thousands of unread notifications, all rows are returned.

This slows:

- API response
- Frontend rendering
- Database memory usage

---

# Optimized Solution

## Step 1: Create Composite Index

```sql
CREATE INDEX idx_notifications_student_read_created
ON notifications(student_id, is_read, created_at DESC);
```

---

# Why Composite Index?

The query filters using:

- `student_id`
- `is_read`

and sorts using:

- `created_at DESC`

A composite index helps PostgreSQL/MySQL quickly locate matching rows.

---

# Optimized Query

```sql
SELECT id, type, message, priority, created_at
FROM notifications
WHERE student_id = 1042
AND is_read = FALSE
ORDER BY created_at DESC
LIMIT 20;
```

---

# Likely Computational Cost After Optimization

With indexing:

Search Cost:

```text
O(log n)
```

Fetching Results:

```text
O(k)
```

where `k` is the number of returned rows.

Overall query performance becomes significantly faster.

---

# Should We Add Indexes on Every Column?

## Suggestion from Another Developer

> “Add indexes on every column to be safe.”

This is NOT a good approach.

---

# Why Adding Indexes on Every Column is Bad

## 1. Increased Storage Usage

Indexes consume additional disk space.

With millions of notifications, excessive indexes increase storage cost.

---

## 2. Slower INSERT and UPDATE Operations

Whenever data changes:

- Every index must also be updated.
- Write operations become slower.

Example:

```sql
INSERT INTO notifications (...)
```

will take longer if too many indexes exist.

---

## 3. Poor Query Planner Decisions

Too many indexes may confuse the database query optimizer.

This can sometimes reduce performance instead of improving it.

---

## 4. Unused Indexes Waste Resources

Indexes should only be created for:

- Frequently filtered columns
- Frequently sorted columns
- JOIN operations

---

# Best Practice for Indexing

Create indexes only on:

| Column | Reason |
|------|-------------|
| student_id | Frequent filtering |
| is_read | Frequent filtering |
| created_at | Sorting |
| notification_type | Filtering by type |

---

# Query to Find Students Who Got Placement Notifications in Last 7 Days

## SQL Query

```sql
SELECT DISTINCT student_id
FROM notifications
WHERE notification_type = 'Placement'
AND created_at >= NOW() - INTERVAL '7 days';
```

---

# Explanation

| Clause | Purpose |
|------|-------------|
| DISTINCT | Avoid duplicate students |
| notification_type = 'Placement' | Filter placement notifications |
| INTERVAL '7 days' | Fetch recent notifications |

---

# Optimized Index for This Query

```sql
CREATE INDEX idx_notification_type_created
ON notifications(notification_type, created_at DESC);
```

This improves:

- Placement notification filtering
- Date-based searching

---

# Additional Performance Improvements

## 1. Pagination

```sql
LIMIT 20 OFFSET 0
```

Reduces large responses.

---

## 2. Cursor-Based Pagination

Better for massive datasets.

```sql
SELECT id, type, message, created_at
FROM notifications
WHERE student_id = 1042
AND created_at < '2026-05-01 10:00:00'
ORDER BY created_at DESC
LIMIT 20;
```

---

## 3. Redis Caching

Unread notifications can be cached.

Benefits:

- Faster API responses
- Reduced database load

---

## 4. Table Partitioning

Partition notifications by:

- Year
- Student range
- Notification type

---

# Final Recommendation

For large-scale notification systems:

- Use composite indexes instead of indexing every column
- Avoid SELECT * queries
- Use pagination
- Cache frequently accessed notifications
- Partition very large tables
- Archive old data periodically

These optimizations ensure:

- Faster unread notification retrieval
- Reduced database load
- Better scalability
- Improved overall API performance

