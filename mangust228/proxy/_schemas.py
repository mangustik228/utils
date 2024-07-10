from pydantic import BaseModel


class ProxySchema(BaseModel):
    id: int
    server: str
    port: int
    username: str
    password: str
    
    def __str__(self):
        return f"proxy-{self.id}"
    
    @property
    def req_conn(self):
        return {"http": f"http://{self.username}:{self.password}@{self.server}:{self.port}"}
    
    @property 
    def httpx_conn(self):
        return f"http://{self.username}:{self.password}@{self.server}:{self.port}"
    
    @property
    def pw_conn(self):
        return {
            "server": f"http://{self.server}:{self.port}",
            "username": self.username,
            "password": self.password
        }
        