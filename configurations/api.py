import threading

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from domain.entities.neural_network import NeuralNetwork
from entrypoint.dto.request import MustJump

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou defina os domínios permitidos separados por vírgula
    allow_methods=["*"],  # ou especifique os métodos HTTP permitidos
    allow_headers=["*"],  # ou defina os cabeçalhos permitidos separados por vírgula
)


@app.post("/jump")
def request(payload: MustJump):
    genome, genomeOutput = ([-0.4688943022501513, 0.11790717471133116, 0.28745275493402356, 0.8925000711936057], [0.35648677])

    nn = NeuralNetwork(
        4,
        8,
        1,
        genome,
        genomeOutput
    )

    output = nn.forward([payload.distance, payload.velocity, payload.height, payload.posix])[0]

    return {"output": output}


def start_api():
    uvicorn_thread = threading.Thread(target=uvicorn.run, args=(app,), kwargs={"host": "0.0.0.0", "port": 8000})
    uvicorn_thread.start()
