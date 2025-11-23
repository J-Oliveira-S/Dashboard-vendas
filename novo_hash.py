import bcrypt
password = 'guarana'.encode('utf-8')
# Gera o hash para a senha 'guarana'
hashed = bcrypt.hashpw(password, bcrypt.gensalt())
print(hashed.decode())