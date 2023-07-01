import base64
import hashlib

password = base64.urlsafe_b64encode(hashlib.md5('mypassword'.encode()).hexdigest().encode("utf-8"))
