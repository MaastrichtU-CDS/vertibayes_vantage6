IMAGE=harbor.carrier-mu.src.surf-hosted.nl/carrier/vertibayes:1.0-stable

docker build --build-arg SSH_PRIVATE_KEY="$(cat ~/.ssh/id_rsa)" \
  --build-arg SSH-PUBLIC-KEY="$(cat ~/.ssh/id_rsa.pub)" \
  -t vertibayes  .

docker tag vertibayes $IMAGE

docker push $IMAGE