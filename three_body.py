from cryptography.fernet import Fernet
from decorator import encrypt_decorator

user_key = Fernet.generate_key()

@encrypt_decorator(input_key=user_key)
def say_hello_to_three_body(msg):
    print(f"Please do not answer !!!")
    print(f"The encrypted message is {msg}")

if __name__ == "__main__":
    say_hello_to_three_body("世界属于三体")