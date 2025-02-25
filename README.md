# **Vault Service Microservice**
## **Overview**
This microservice I will be implementing for Derek will provide a secure way to store, retrieve, and delete passwords using FastAPI and an SQLite database. Passwords will be stored using a hashed format using bcrypt.

## **Communication Contract**
*This constract will not change, ensuring a stable for all clients using this service*  
### **Base URL:**
`http://localhost:8000`   
### **Requesting Data from Microservice:**
To request a stored credential you have to send a GET request to:  
`GET/retrieve/{site}`   
**Example Request**  
```python
import request

site = "instagram.com"
respond = request.get(f"http://localhost:8000/retrieve/{site}'

if respond.status_code == 200:
  print(response.json())
else:
  print("Error:", response.json()) python
```
**Example Response (Success):**
```python
{
    "site": "instagram.com",
    "username": "user1234",
    "password": "****(hidden)"
}
```
**Example Response (Failed - Not Found)**
```python
{
    "detail": "Entry not found"
}
```
### **Storing Data in Microservice:**
To store a credential you have to send a POST request to:  
`POST/store/ `   
**Example Request**  
```python
import request

payload = {
    "site": "instagram.com",
    "username": "user1234",
    "password": "password"
}

response = request.post("http://localhost:8000/store/", json=payload)
print(response.json())
```
**Example Response:**
```python
{
    "message": "Password stored successfully"
}
```

### **Deleting Data from the Microservice:**
To delete a stored credential you have to send a DELETE request to:  
`DELETE/delete/{site} `   
**Example Request**  
```python
import request

site = "instagram.com"
response = request.delete(f"http://localhost:8000/delete/{site}")
print(response.json())
```
**Example Response:**
```python
{
    "message": "Password deleted successfully"
}
```








