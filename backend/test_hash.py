import bcrypt
senha = '123456'
hash_armazenado = '.Ctarz3OAts3iJwrO5MLytJAv9MjVQA1U7jZBFF0zhEpFEXi'
match = bcrypt.checkpw(senha.encode('utf-8'), hash_armazenado.encode('utf-8'))
print('A senha bate com o hash?', match)
