import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    DATABASE_URL = os.getenv(
        "DATABASE_URL", "sqlite+aiosqlite:///./test.db")  # ✅ Use aiosqlite
    SECRET_KEY = '2aa5d8dd5958d14637e5bb7c908ea279284f0f5dbec3eeb0caa8c3caa6b217b9f2cc7e5f76f6ff9562d1aa753f313968fbf6d1e3817274dae29588656dad8919088a5b12ac6652534b739289be47873b65ff360f1fa49453de50728da2456933301bf391c578775427976cac49b6c4a22c16c3c2fbae73ade9ae64a36a91410a8dd15fdeab26226a67ce55962411805018dd69c89f4a1d7e00792453899cdf7cc74ac80ea3b24f677fca793343d52b82c66819149b8507d4c34f31fc15ccfce0726ef3b6c80faab0b0e7cf3d3e06c7b18143d256885153520d9d105ac8b4d40aeba12cac60885fcbb32051f6f37319f6e4dcca2cf5e7dc2a95b878aeddb997e3'
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30


settings = Settings()
