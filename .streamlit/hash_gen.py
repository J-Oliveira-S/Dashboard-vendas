# ⚠️ Mude 'SENHA_UNICA_ITECA' para a senha real que o time usará ⚠️
senhas_para_criptografar = ['guarana'] 

hashed_passwords = stauth.Hasher(senhas_para_criptografar).generate()

print(hashed_passwords)