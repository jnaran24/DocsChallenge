# DocsChallenge
Challenge MELI Docs en Drive Públicos

comandos para docker:
docker build --tag meli-challenge .
docker run meli-challenge

comando para docker interactivo:
docker run -t -i meli-challenge


dockerhub:
docker login -u ee106as45d68514f1
docker tag local-image:tagname new-repo:tagname
# docker tag meli-challenge:latest meli-challenge:versionx
docker push ee106as45d68514f1/meli-challenge:tagname
# docker push ee106as45d68514f1/meli-challenge
