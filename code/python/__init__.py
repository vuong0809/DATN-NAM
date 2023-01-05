import argparse
import json
import uvicorn

parser = argparse.ArgumentParser()
parser.add_argument('--host', default='0.0.0.0')
parser.add_argument('--port', type=int, default=8000)
parser.add_argument('--dev', default=False)

args = parser.parse_args()
if __name__ == '__main__':
    import main as main
    # if args.dev is False:
    uvicorn.run(main.app,
                host=args.host,
                port=args.port,
                ssl_keyfile="./helpers/ssl/localhost+2-key.pem",
                ssl_certfile="./helpers/ssl/localhost+2.pem"
                )
    # uvicorn.run(main.app, host=args.host, port=args.port, reload=True)
