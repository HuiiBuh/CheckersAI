cp -r ../src src
cp ../requirements.txt .

docker-compose build

rm -r src
rm requirements.txt