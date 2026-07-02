from cryptography.fernet import Fernet

# 生成固定的key
FIXED_KEY = b'kLIReP6Mmbm0S3HWjdAISc3Zk9H9G2OqzNAUYKcc3uY='
cipher = Fernet(FIXED_KEY)

class DecryptMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):

        if request.method == 'POST':
            params = request.POST
        elif request.method == 'GET':
            params = request.GET

        # 解密
        decrypted_params = self.decrypt_params(dict(params))

        # 复制对象 因为不能直接改request
        params = params.copy()

        for k,v in decrypted_params.items():
            params[k] = v   # v是列表

        if request.method == 'POST':
            request.POST = params
        elif request.method == 'GET':
            request.GET = params
        
        return self.get_response(request)
    

    def decrypt_params(self, params):
        decrypted = {}
        for key, value in params.items():
            try:
                decrypted[key] = cipher.decrypt(value[0].encode()).decode()
            except Exception:
                decrypted[key] = value[0]
        return decrypted
    

def encrypt_params():
    username_encrypted = cipher.encrypt('Cara'.encode()).decode()
    password_encrypted = cipher.encrypt('Cara8888'.encode()).decode()

    print(f"加密后的 username: {username_encrypted}")
    print(f"加密后的 password: {password_encrypted}")


if __name__ == "__main__":
    encrypt_params()