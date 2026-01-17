import bcrypt
h = '$2b$12$tHmT4ApsgLf.6hraC3ZcfuSzmQdqfcAJzTitNiGAGo2gLZCC8Bae.'
print('Check admin123:', bcrypt.checkpw('admin123'.encode(), h.encode()))
