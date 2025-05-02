import environ
env = environ.Env()
environ.Env.read_env()  # Explicitly read the .env file

print(env('SECRET_KEY'))  # Print SECRET_KEY from .env to confirm it's loaded
