import secrets
from uuid import uuid4
secret = secrets.token_hex(32)
print(secret)

print(str(uuid4()))
print(60*24*30)
""""	
	
Response body
Download
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxNywidHlwZSI6ImFjY2VzcyIsImV4cCI6MTc4MzA1OTUxOSwiaWF0IjoxNzgzMDU5NDU5LCJqdGkiOiI4MWM2MTZiYy03NjFjLTRmMDMtYTdiZC1jYjk4ZjJlNDI3YjcifQ.2cofbNnQOh4fzyrL0oCxdirRVSXg5oZRVn51t6EJ5KM",
  "refresh_token": "JIUzI1NiIs9.eyJ1c2VyX2lkIjoxNywidHlwZSI6InJlZnJlc2giLCJleHAiOjE3ODU2NTE0NTksImlhdCI6MTc4MzA1OTQ1OSwianRpIjoiMjJmM2U0NjYtNDY0OS00NTM1LTkzZDMtYTc0NzFiZWQyY2YzIn0.2D34KAeAwUvp40GO46VbIzAa-TLrJEGSydOQpUcHucs",
  "token_type": "bearer"
}
}"""