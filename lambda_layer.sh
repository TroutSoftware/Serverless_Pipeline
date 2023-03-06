pipenv requirements > requirements.txt
python -m pip install -r requirements.txt -t python/

zip -r layer.zip python
aws lambda publish-layer-version --layer-name serverless_pipelines \
    --zip-file fileb://layer.zip --compatible-runtimes python3.9 --region us-east-1